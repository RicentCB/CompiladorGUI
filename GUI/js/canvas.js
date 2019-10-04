const R = 25;
const LINEW = 60;
const HEADLEN = 10; 
const DEC_TXT = 14;
const INI_SP = 20;
const SPACE_BSTS = 150;
const COLOR_CNVS = "#555";
let Y_INI = 50;
let Y_ADD = 70;

let arrayAFNS = [];

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
function arrowBetweenStates(context, x1, y1, x2, y2, transition){
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
    (transition.length == 1) ?
        context.fillText(transition, x1+(Math.abs(x1-x2)/2) - 8, y1+(Math.abs(y1-y2)/2) - 10) :
        context.fillText(transition, x1+(Math.abs(x1-x2)/2) - 25 , y1+(Math.abs(y1-y2)/2) - 10) 
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

function drawState(context, x, y, name){
    //Dibujar Circulo
    context.beginPath();
    context.arc(x, y, R, 0, 2 * Math.PI);
    context.stroke();
    //Titulo
    context.beginPath();
    context.fillText(name, x-DEC_TXT, y+5);
    context.fill();
}
function drawIniState(context, x, y, number){
    drawState(context, x, y, ("Q"+number))
    arrowBetweenStates(context, x-1.5*LINEW, y, x, y, "");
}
function drawEndState(context, x, y, name){
    drawState(context, x,y, name)
    //Dibujar circulo pequeño
    context.beginPath();
    context.arc(x, y, R-(R*.2), 0, 2 * Math.PI);
    context.stroke();
}
/*-----------------------------------------------------------------------
 * ---- FUNCION QUE ACTUALIZA EL HTML DE ACUERDO A LOS OBJETO JSON ----
-----------------------------------------------------------------------*/
function updateHTMLSelectAFN(){
    var arraySelect = $('.container-select .select-options');
    for (let i = 0; i < arraySelect.length; i++) {
        $(arraySelect[i]).empty();
        let strId = $(arraySelect[i]).attr("id");
        console.log(strId);
        for (let j = 0; j < arrayAFNS.length; j++) {
            $(arraySelect[i]).append("<p class='element'>"
						+"<input type='radio' id='rd"+strId+(j)+"' name='radio-group'"+strId+" >"
						+"<label for='rd"+strId+(j)+"' >AFN "+(j+1)+"</label>"
				  	+"</p>")
        }
    }
}

/*--------------------------------------------------------------
 * ---- FUNCION QUE GUARDA UN JSON EN LA PILA DE AUTOMATAS ----
--------------------------------------------------------------*/
 function pushAFN(jsonString){
    //Insertamos el objeto JSON en arreglo del AFNS
    arrayAFNS.push(jsonString);
    //Mdificar el HTML de los selectores de AFNS
    updateHTMLSelectAFN();
    //Incrementar Y INI para el proximo automata
    Y_INI = Math.floor((Y_INI + Y_ADD),2);
}

//---------------------------------------------------------------
//Funcion que devuelve un string con el caracter de transicion
function getCarTransition(row){
    let stringOut = "";
    (row[2] != row[3]) ?
        stringOut = "["+row[2]+"-"+row[3]+"]" :
        stringOut = row[2]
    return stringOut;    
}
//---------------------------------------------------------------
/*==============================================================
 * ---- FUNCION QUE DIBUJA UN AUTOMATA DADO UN OBJETO JSON ----
 =============================================================*/
function drawAFN(jsonStr, context){
    let actualState = jsonStr["iniSt"];
    let endState = jsonStr["endSt"];
    let transitions = jsonStr["transitions"];
    let states = jsonStr["transitions"];

    console.log(transitions);
    xIni = 2*LINEW;
    yIni = Y_INI;
    xEnd = 0;
    yEnd = 0
    drawIniState(context, xIni, yIni, actualState);
    
    while(actualState != endState){
        //Buscamos las transiciones que pertenecen al estado actual
        auxArrayTrans = [];
        for (let i = 0; i < transitions.length; i++) {
            if(transitions[i][0] == actualState)
                auxArrayTrans.push(transitions[i])
        }
        //Hay una bifurcacion
        if(auxArrayTrans.length > 1){   
            console.log("bifurcacion");
        }else{//Solo hay un estado al que se llega
            actualState = auxArrayTrans[0][1]   //Estado al que se llega
            xEnd = Math.floor(xIni+SPACE_BSTS,2);
            yEnd = yIni;
        }
        //Dibujar el estado de aceptacion
        if  (actualState == endState){
            drawEndState(context, xEnd, yEnd, ("Q"+actualState));
            arrowBetweenStates(context, xIni, yIni, xEnd, yEnd, getCarTransition(auxArrayTrans[0]));
        }
    }
    //Insertamos el objeto JSON y modificar el HTML
    pushAFN(jsonStr);
    return (arrayAFNS.length);
}

$(document).ready(function(){

    //Inicializar Canvas
    var canvas = document.getElementById("goodCanvas1");
    var ctx = canvas.getContext("2d");
    ctx.strokeStyle = COLOR_CNVS;
    ctx.lineWidth = 2;
    ctx.font = "20px Quicksand";
    ctx.fillStyle = COLOR_CNVS;
    //Botones para crear Automatas
    var addBasicAFDBtn = $("a.btn.add-btn#basicAFD");
    var addRangeAFDBtn = $("a.btn.add-btn#rangeAFD")

    const {PythonShell} = require("python-shell");
    var path = require("path");

    //Boton de Automata Basico
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
                    //Creamos el automata
                    car.on('message',function(jsonString){
                        answer = drawAFN(jsonString, ctx);
                        if(answer != false)
                            Swal.fire("Exito al crear automata", "Id: "+answer, "success");
                    });

                }else
                    Swal.fire("Solo se permite un caracter", "Por favor revisa la entrada", "error")                
            }
        });

        
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
                //Rango Valido
                var options = {
                    mode: 'json',
                    pythonOptions: ['-u'],
                    scriptPath:  path.join(__dirname, 'Engine/'),
                    pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
                    args: ["AFN","Rango",result.value]
                };

                let car = new PythonShell('main.py', options);
                //Creamos el automata
                car.on('message',function(jsonString){
                    answer = drawAFN(jsonString, ctx);
                    if(answer != false)
                        Swal.fire("Exito al crear automata", "Id: "+answer, "success");
                });
            }else
                Swal.fire("No ingreso un rango valido", "Por favor revisa la entrada", "error")                

        });
        
    })

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