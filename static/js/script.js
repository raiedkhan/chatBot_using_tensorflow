var array=['How are you','Is anyone there?','Whats up','See you later','How old are you','How old is Raied','What should I call you','What is your name','Whats on the menu','what do you reccommend?','Could i get something to eat','At what Price you sell cookie','For how much is cookie available','What is the Price Of cookie','When are you guys open','What cookies do you sell','If cookies are available ?','What cookies are available with you ?']

array=shuffle(array);
var rand1 = getRndmFromArray(array);
Delete(rand1);
array=shuffle(array);
var rand2 = getRndmFromArray(array);
Delete(rand2);
var rand3 = getRndmFromArray(array);
Delete(rand3);
var rand4 = getRndmFromArray(array);
Delete(rand4);

function myfunction(){
    document.getElementById("ques1").innerHTML = rand1;
    document.getElementById("ques2").innerHTML = rand2;
    document.getElementById("ques3").innerHTML = rand3;
    document.getElementById("ques4").innerHTML = rand4;
}
function clicked(id){
    document.getElementById("formGroupExampleInput2").value=document.getElementById(id).innerHTML;
    document.getElementById("myform").submit();
}

function Delete(rand){
    for( var i = 0; i < array.length; i++){ 
        if ( array[i] === rand) {
          array.splice(i, 1); 
        }
    }
}

function getRndmFromArray(array){
    var rand=array[Math.floor(Math.random() * Array.length)];
    return rand;
}

function shuffle(array) {
    var i = array.length,
        j = 0,
        temp;

    while (i--) {
        j = Math.floor(Math.random() * (i+1));
        // swap randomly chosen element with current element
        temp = array[i];
        array[i] = array[j];
        array[j] = temp;

    }
    return array;
}