function setResultPanelText(html){
    document.getElementById("result-panel").innerHTML = html;
}
function disableListeningButton(disabled){
    document.getElementById("start-button").disabled = disabled?"disabled":null;
}