const R = 25;
const LINEW = 50;
const DEC_TXT = 12
const INI_SP = 20
const Y_INI = 100
const COLOR_CNVS = "#555";

//Funcion que dibuja una flecha dadas coordenadas x,y de orgine y destino
function canvas_arrow(context, fromx, fromy, tox, toy) {
    var headlen = 10; // length of head in pixels
    var dx = tox - fromx;
    var dy = toy - fromy;
    var angle = Math.atan2(dy, dx);
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    context.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
    context.moveTo(tox, toy);
    context.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
}
$(document).ready(function(){

    

    var canvas = document.getElementById("goodCanvas1");
    var ctx = canvas.getContext("2d");
    
    ctx.strokeStyle = COLOR_CNVS;
    ctx.lineWidth = 2;
    ctx.font = "20px Quicksand";
    ctx.fillStyle = COLOR_CNVS;

    ctx.beginPath();
    ctx.arc((R+LINEW+INI_SP), Y_INI, R, 0, 2 * Math.PI, false);
    ctx.stroke();

    ctx.beginPath();
    ctx.fillText("q0", R+LINEW+INI_SP-DEC_TXT, Y_INI+5);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(INI_SP+(R+LINEW)+((2*R)+LINEW), Y_INI, R, 0, 2 * Math.PI, false);
    ctx.stroke();

    ctx.beginPath();
    ctx.fillText("q1", INI_SP+(R+LINEW)+((2*R)+LINEW)-DEC_TXT, Y_INI+5);
    ctx.fill();

    ctx.beginPath();
    canvas_arrow(ctx, INI_SP, Y_INI, INI_SP+LINEW, Y_INI);
    canvas_arrow(ctx, INI_SP+(2*R+LINEW), Y_INI, INI_SP+(2*R+LINEW)+1*(LINEW), Y_INI);
    ctx.stroke();

    ctx.beginPath();
    ctx.fillText("a-b", (INI_SP+LINEW+R)+(LINEW+R)/2, Y_INI-10);
    ctx.fill();


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
