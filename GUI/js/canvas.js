const R = 40;
const LINEW = 150;
const HEADLEN = 10; 
const DEC_TXT = 14;
const INI_SP = 20;
const Y_INI = 100;
const COLOR_CNVS = "#555";

//Funcion que dibuja una flecha dadas coordenadas x,y de origen y destino
function canvas_arrow(context, fromx, fromy, tox, toy) {
    var dx = tox - fromx;
    var dy = toy - fromy;
    var angle = Math.atan2(dy, dx);
    //Creacion de Linea
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    //Flecha
    context.lineTo(tox - HEADLEN * Math.cos(angle - Math.PI / 6), toy - HEADLEN * Math.sin(angle - Math.PI / 6));   //Linea Inferior
    context.moveTo(tox, toy);
    context.lineTo(tox - HEADLEN * Math.cos(angle + Math.PI / 6), toy - HEADLEN * Math.sin(angle + Math.PI / 6));
}
//Funcion que dibuja una flecha entre dos estados dados los centros
function arrowBetweenStates(context, x1, y1, x2, y2, str){
    const alphaAngle = Math.atan2(Math.abs(x1-x2),Math.abs(y1-y2));
    const betaAngle = Math.atan2(Math.abs(y1-y2),Math.abs(x1-x2));

    const iniArrowX = Math.round(R*Math.sin(alphaAngle),2) + x1; 
    const iniArrowY = Math.round(R*Math.cos(alphaAngle),2) + y1; 
    const endArrowX = x2 - Math.round(R*Math.cos(betaAngle),2); 
    const endArrowY = y2 - Math.round(R*Math.sin(betaAngle),2); 
    
    //Dibujar Flecha
    context.beginPath();
    canvas_arrow(context, iniArrowX, iniArrowY, endArrowX, endArrowY);
    context.stroke();
    //String de Cadena
    context.beginPath();
    context.fillText(str, x1+(Math.abs(x1-x2)/2) , y1+(Math.abs(y1-y2)/2) - 15);
    context.fill();
}
//Funcion Pitagoras calcula un cateto dado la hipotenusa y otro cateto
function calcCat(hipo, cat){
    const PowHipo = Math.pow(hipo,2);
    const PowCat = Math.pow(cat,2);
    return Math.floor(Math.sqrt(PowHipo-PowCat),4);
}

//Funcion que dibuja un arco entre dos estados dados los centros de idhcos estados
function arcBetweenStates(context, xState1, yState1, xState2, yState2, string, up=true){
    //Calcular Espacio en X para el text
    var spaceXText = 0;
    if(string.length > 1){
        spaceXText -= DEC_TXT;
    }
    if (yState1 == yState2){
        const MiniCircleX1 = Math.floor(xState1 + (R/2),2);             //Coordenada en X del minicirculo 1
        const MiniCircleX2 = Math.floor(xState2 - (R/2), 2);            //Coordenada en X del minicirculo 1
        const BigRadius = Math.floor(MiniCircleX2 - MiniCircleX1,4)     //Radio del arco
        //Calcular coordenadas del Centro del Arco
        const DeltaValueX = ((xState2 - xState1) /2 );          
        const BigCircleX = DeltaValueX + xState1;                       //Coordenada en Equis del Circulo Arco
        const DeltaValueY = calcCat((BigRadius - R/2), DeltaValueX);   
        let BigCircleY = 0             //Cordenada en Ye del Ciruclo Arco
        let startAngle = 0             //Angulo de Inicio 
        let endAngle = 0;              //Angulo de fin
        let negCte = 0;                //Variable para sumar o restar al momento de dibujar la cabeza de flecha

        if (up){
            //Coordenada en Y y angulo de inicio y Fin
            BigCircleY = yState1 + DeltaValueY
            startAngle = 180+60 
            endAngle = 180+60+60 
            //Dibujar Flecha
            negCte = -1;      
            //Colocar Leyenda
            context.beginPath();
            context.fillText(string, BigCircleX+spaceXText, (BigCircleY-BigRadius-5));
            context.fill();

        }else{
            BigCircleY = yState1 - DeltaValueY;
            startAngle = 60
            endAngle = 60+60 
            //Dibujar Flecha
            negCte = 1;
            //Colocar Leyenda
            context.beginPath();
            context.fillText(string, BigCircleX+spaceXText, (BigCircleY+BigRadius+17));
            context.fill();
        }
        //Dibujar Cabeza de la flecha
        context.moveTo(BigCircleX+(negCte)*(Math.sin(Math.PI /6) * BigRadius), BigCircleY+(negCte)*(Math.cos(Math.PI /6) * BigRadius));   //Incio de la cabeza de flecha
        context.lineTo(BigCircleX+(negCte)*(Math.sin(Math.PI /6) * BigRadius) +(-1*negCte)*HEADLEN, BigCircleY+(negCte)*(Math.cos(Math.PI /6) * BigRadius));  //Trazo Inferior
        context.moveTo(BigCircleX+(negCte)*(Math.sin(Math.PI /6) * BigRadius), BigCircleY+(negCte)*(Math.cos(Math.PI /6) * BigRadius));   //Incio de la cabeza de flecha
        context.lineTo(BigCircleX+(negCte)*(Math.sin(Math.PI /6) * BigRadius) +(-1*negCte)*HEADLEN*Math.sin(Math.PI/6), BigCircleY+(negCte)*(Math.cos(Math.PI /6) * BigRadius)+(negCte)* (HEADLEN)*Math.cos(Math.PI/6));    //Trazo Superior
        context.stroke();  
        //Dibujar Arco
        context.beginPath();
        context.arc(BigCircleX, BigCircleY, BigRadius, Math.radians(startAngle),Math.radians(endAngle), false);
        context.stroke();
    
    }else{  
        console.log("Solo con Ye Iguales ")
    }
}


$(document).ready(function(){

    var canvas = document.getElementById("goodCanvas1");
    var ctx = canvas.getContext("2d");
    
    ctx.strokeStyle = COLOR_CNVS;
    ctx.lineWidth = 2;
    ctx.font = "20px Quicksand";
    ctx.fillStyle = COLOR_CNVS;

    ctx.beginPath();
    ctx.arc((R+LINEW+INI_SP), Y_INI, R, 0, 2 * Math.PI);
    ctx.stroke();

    ctx.beginPath();
    ctx.fillText("q0", R+LINEW+INI_SP-DEC_TXT, Y_INI+5);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(INI_SP+(R+LINEW)+((2*R)+LINEW), Y_INI, R, 0, 2 * Math.PI);
    ctx.stroke();

    ctx.beginPath();
    ctx.fillText("q1", INI_SP+(R+LINEW)+((2*R)+LINEW)-DEC_TXT, Y_INI+5);
    ctx.fill();

    ctx.beginPath();
    canvas_arrow(ctx, INI_SP, Y_INI, INI_SP+LINEW, Y_INI);
    ctx.stroke();

    
    arcBetweenStates(ctx, (R+LINEW+INI_SP), Y_INI, INI_SP+(R+LINEW)+((2*R)+LINEW), Y_INI, '\u03B5', false);
    arcBetweenStates(ctx, (R+LINEW+INI_SP), Y_INI, INI_SP+(R+LINEW)+((2*R)+LINEW), Y_INI, '\u03B5', true);

    arrowBetweenStates(ctx, (R+LINEW+INI_SP), Y_INI, INI_SP+(R+LINEW)+((2*R)+LINEW), Y_INI, '\u03B5');
    

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
                        mode: 'json',
                        pythonOptions: ['-u'],
                        scriptPath:  path.join(__dirname, 'Engine/'),
                        pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
                        args: ["AFN","Basico",result.value]
                    };

                    let car = new PythonShell('main.py', options);

                    car.on('message',function(message){
                        // Swal.fire(message);
                        console.log(message);
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

Math.radians = function(degrees) {
	return degrees * Math.PI / 180;
}