var path = require("path");

var optionsPython = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, 'Engine/'),
    pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
    args: []
};

$(document).ready(function(){
    const { PythonShell } = require("python-shell");

    let sectionCode = $('#code-interpreter')
    let uploadFile = sectionCode.find('#file-input-code-interpreter')
    let codeArea = sectionCode.find("#code-area")
    let btnInterpreter = sectionCode.find("#btn-code-interpreter");

    let pathCode = "";
    uploadFile.change(function(e){
        let fileIn = e.target.files[0];
        $(this).parent().find("p#title-code-interpreter").html("Archivo Cargado: '"+fileIn.name+"'")
        pathCode = fileIn.path;
        if(fileIn){
            var fr = new FileReader(); 
            fr.onload = function(e) { 
                codeArea.val(e.target.result);
            }; 
            fr.readAsText(fileIn);
        }
    });
    //Boton Interpretar
    let resultCode = sectionCode.find("#result-code")
    btnInterpreter.click(function(e){
        e.preventDefault();
        console.log(pathCode)
        optionsPython.args = ["Interpreter", pathCode];

        let resultPython = new PythonShell('main.py', optionsPython);
        let finalAns = ""
        resultPython.on('message', function (ans) {
            //Insertar JSON en Arreglo
            auxAns = "<p>"+ans+"</p>";
            resultCode.append(auxAns)
        });
        
    })
});