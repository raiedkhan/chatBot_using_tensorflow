import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
from flask import Flask, request, jsonify, render_template, redirect, url_for,flash
from forms import RegistrationForm,LoginForm

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words,labels,training,output=pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle","wb") as f:
        pickle.dump((words,labels,training,output),f)

tensorflow.reset_default_graph()

net=tflearn.input_data(shape=[None,len(training[0])])
net=tflearn.fully_connected(net,8)
net=tflearn.fully_connected(net,8)
net=tflearn.fully_connected(net,len(output[0]),activation="softmax")
net=tflearn.regression(net)
model=tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training,output,n_epoch=1000,batch_size=8,show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]
    s_words=nltk.word_tokenize(s)
    s_words=[stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w==se:
                bag[i]=1
    return numpy.array(bag)

app = Flask(__name__)
app.config['SECRET_KEY']='bcf89ccf37493530152e15de30778064'

@app.route('/')
def home():
    user_input="Type Something first..."
    bot_response="Welcome to Pretzel Chat Bot,Ask me something..."
    return render_template('index.html',user_input=user_input,bot_response=bot_response)
    

@app.route('/chat',methods=['POST'])
def chat():
    if request.method == 'POST':
        input=request.form['user_input']
        result=model.predict([bag_of_words(input,words)])[0]
        result_index=numpy.argmax(result)
        tag=labels[result_index]
        if result[result_index]>0.7:
            for tg in data['intents']:
                if tg['tag']==tag:
                    responses=tg['responses']
            bot_response=random.choice(responses)
        else:
            bot_response="I didn't get that ,Please try again"
        if input=='quit':
            return redirect(url_for('home'))
    return render_template('index.html',user_input=input,bot_response=bot_response)
        
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',title='Login',form=form)

if __name__ == "__main__":
    app.run(debug=True)