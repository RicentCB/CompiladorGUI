$(document).ready(function(){
    const {PythonShell} = require("python-shell");
    var path = require("path");
    //Funcion que Incializa el arreglo de Automatas
    var options = {
        mode: 'json',
        pythonOptions: ['-u'],
        scriptPath:  path.join(__dirname, 'Engine/'),
        pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
        args: ["AFN","Inicializar"]
    };

    let ans = new PythonShell('main.py', options);
    //Creamos el automata
    ans.on('message',function(jsonString){
        console.log("Incilizado")
    });

})