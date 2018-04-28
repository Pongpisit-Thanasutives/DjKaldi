var recognition;

initRecognizer();

function initRecognizer(){
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 5;
    recognition.onresult = function(event) {
        handleResult(event.results);
    };
    recognition.onend = function(event){
        disableListeningButton(false);
        initRecognizer();
    };
}
function startRecognition(){
    setResultPanelText("");
    recognition.start();
    disableListeningButton(true);
}
function handleResult(results){
    console.log(results);
    setResultPanelText(event.results[0][0].transcript);
}