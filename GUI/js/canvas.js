
$(document).ready(function(){

    // var canvas = document.getElementById("goodCanvas1");
    // var ctx = canvas.getContext("2d");
    // ctx.fillText("Hello ARIA World", canvas.width/2, canvas.height/2);
    // ctx.arc(50, 100, 50, 0, Math.PI*2);
    // ctx.stroke();

    var addBasicAFDBtn = $("a.btn.add-btn#basicAFD");
    var addRangeAFDBtn = $("a.btn.add-btn#rangeAFD")

    const {PythonShell} = require("python-shell");
    var path = require("path");

    addBasicAFDBtn.click(function(e){
        e.preventDefault();
        //Lanzar Alerta
        Swal.fire({
            type: 'question',   
            title: 'Ingresa el caracter',
            input: 'text',
            inputPlaceholder: 'E.g. a, b, c, 0, 1, 2 '
        }).then((result) => {
            if (result.value) {
                if(result.value.length == 1){
                    //Caracter valido
                    var options = {
                        scriptPath:  path.join(__dirname, 'Engine/'),
                        pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
                        args: [result.value]
                    };

                    var car = new PythonShell('test.py', options);

                    car.on('message',function(message){
                        Swal.fire(message);
                    });

                }else
                    Swal.fire("Solo se permite un caracter", "Por favor revisa la entrada", "error")                
            }
        });

        
    });

    /*
    //Boton Agregar Automata
    
    
    //AFD Basico
    addBasicAFDBtn.click(function(e){
        
        
    });
    //AFD de Rango
    addRangeAFDBtn.click(function(e){
        e.preventDefault();

        Swal.fire({
            type: 'question',  
            title: 'Ingresa el rango del automata',
            text: 'Separado por un "-"',
            input: 'text',
            inputPlaceholder: 'E.g a-z, A-Z, 0-9'
        }).then((result) => {
            if (isValidRange(result.value)) {
                console.log("Result: " + result.value.length);
            }else
                Swal.fire("No ingreso un rango valido", "Por favor revisa la entrada", "error")                

        });
        
    })
    */
})

function isValidRange(string){
    if(string.length == 3){
        if(string[1] == '-'){
            if (string.charCodeAt(0) < string.charCodeAt(2))
                return true;
            else
                return false;
        }
        else
            return false;
    }else{
        return false;
    }
}