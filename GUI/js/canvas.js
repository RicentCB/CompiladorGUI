
const LINEW = 60;
const SPACE_BSTS = 160;
let Y_INI = 0;
let Y_ADD = 120;

let arrayAFNS = [];

var mainJsonAFN = {
    "class": "go.GraphLinksModel",
    "nodeKeyProperty": "id",
    "nodeDataArray": [
        // { "id": 0, "loc": "0 0", "text": "Q0"},
        // { "id": 1, "loc": "200 0", "text": ">Q10" },
        // { "id": 2, "loc": "0 150", "text": "Q2*"},
        // { "id": 3, "loc": "200 150", "text": "Q3"},
    ],
    "linkDataArray": [
        // { "from": 0, "to": 0, "text": "up or timer", "curviness": -30 },
        // { "from": 0, "to": 3, "text": "down", "curviness": 30 },
    ]
};
var path = require("path");
var optionsPython = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, 'Engine/'),
    pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
    args: []
};

function init() {
    var $ = go.GraphObject.make;  // for conciseness in defining templates
    myDiagram =
        $(go.Diagram, "myDiagramDivAFN",  // must name or refer to the DIV HTML element
            {
                // have mouse wheel events zoom in and out instead of scroll up and down
                "toolManager.mouseWheelBehavior": go.ToolManager.WheelZoom,
                // support double-click in background creating a new node
                // "clickCreatingTool.archetypeNodeData": { text: "new node" },
                // enable undo & redo
                "undoManager.isEnabled": true
            });
    // define the Node template
    myDiagram.nodeTemplate =
        $(go.Node, "Auto",
            {desiredSize: new go.Size(70,70)},
            new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
            // define the node's outer shape, which will surround the TextBlock
            $(go.Shape, "Circle",
                {
                    parameter1: 50,  // the corner has a large radius
                    fill: $(go.Brush, "Radial", { 0: "rgb(147, 227, 243)", 1: "rgb(0, 141, 163)" }),//Botones
                    stroke: null,
                    portId: "",  // this Shape is the Node's port, not the whole Node
                    fromLinkable: true, fromLinkableSelfNode: true, fromLinkableDuplicates: true,
                    toLinkable: true, toLinkableSelfNode: true, toLinkableDuplicates: true,
                    cursor: "pointer"
                    
                }),
            $(go.TextBlock,
                {
                    font: "bold 14pt 'Anton', helvetica, bold arial, sans-serif",
                    editable: true  // editing the text automatically updates the model data
                },
                new go.Binding("text").makeTwoWay())
        );
    // replace the default Link template in the linkTemplateMap
    myDiagram.linkTemplate =
        $(go.Link,  // the whole link panel
            {
                curve: go.Link.Bezier, adjusting: go.Link.Stretch,
                reshapable: true, relinkableFrom: true, relinkableTo: true,
                toShortLength: 3
            },
            new go.Binding("points").makeTwoWay(),
            new go.Binding("curviness"),
            $(go.Shape,  // the link shape
                { strokeWidth: 1.5 }),
            $(go.Shape,  // the arrowhead
                { toArrow: "standard", stroke: null }),
            $(go.Panel, "Auto",
                $(go.Shape,  // the label background, which becomes transparent around the edges
                    {
                        fill: $(go.Brush, "Radial",
                            { 0: "rgb(255, 255, 255)", 0.8: "rgb(255, 255, 255)", 1: "rgba(255, 255, 255, 0)" }),
                        stroke: null
                    }),
                $(go.TextBlock, "transition",  // the label text
                    {
                        textAlign: "center",
                        font: "18pt 'Quicksand',helvetica, arial, sans-serif",
                        margin: 4,
                        editable: true  // enable in-place editing
                    },
                    // editing the text automatically updates the model data
                    new go.Binding("text").makeTwoWay())
            )
        );
    
}

function LoadGoJS() {
    myDiagram.model = go.Model.fromJson(mainJsonAFN);
}

/* ------------- Funcion que actulza los select Box ------------- */
function updateHTMLSelectAFN(){
    var arraySelect = $('.container-select .select-options');
    for (let i = 0; i < arraySelect.length; i++) {
        $(arraySelect[i]).empty();
        let strId = $(arraySelect[i]).attr("id");
        //Recorrer Arreglo de AFNS
        for (let j = 0; j < arrayAFNS.length; j++) {
            if (arrayAFNS[j]["visible"]){
                $(arraySelect[i]).append("<p class='element'>"
                +"<input type='radio' id='rd"+strId+(j)+"' value='"+(arrayAFNS[j]["id"]-1)+"' name='radio-group-"+strId+"' >"
                +"<label for='rd"+strId+(j)+"' >AFN "+arrayAFNS[j]["id"] +"</label>"
              +"</p>")         
            }
        }
    }
}
/* ---- FUNCION QUE GUARDA UN JSON EN LA PILA DE AUTOMATAS ---- */
function pushAFN(jsonString) {
    //Insertamos el objeto JSON en arreglo del AFNS
    arrayAFNS.push(jsonString);
}

//---------------------------------------------------------------
//Funcion que devuelve un string con el caracter de transicion
function getCarTransition(row) {
    let stringOut = "";
    (row[2] != row[3]) ?
        stringOut = "[" + row[2] + "-" + row[3] + "]" :
        stringOut = row[2]
    if (stringOut == "Epsilon")
        stringOut = "ε";
    return stringOut;
}
//Funcion que verifica su existen dos transciones que llevan a un mismo estado
function existTwoTrans(arrayTtransitions, state){
    //Trasncion = [IniState, EndState, MinSymbol, MaxSimbol]
    let arrayStates = []
    let cont = 0;
    for (let i = 0; i < arrayTtransitions.length; i++) {
        if(parseInt(arrayTtransitions[i][1]) == parseInt(state)){
            cont ++;
            arrayStates.push(arrayTtransitions[i][0]) //Insertamos el estado de origen
        }
    }
    if(cont > 1){
        return true;
    }else{
        return false;
    }
}
/*---------------------------------------------------------------
 * ---- FUNCION QUE DIBUJA UN AUTOMATA DADO UN OBJETO JSON ----
---------------------------------------------------------------*/

function drawAFN(jsonStr) {
    let actualState = jsonStr["iniSt"];
    let endState = jsonStr["endSt"];
    let transitions = jsonStr["transitions"];
    //Arreglo para saber si ya se ha dibujado el estado
    let drawStates = [];
    //Arreglo de Estados para insertar en el main JSON AFN
    let arrayStates= [];
    //Arreglo de Transncions para insertar en el main JSON AFN
    let arrayTrans = [];
    goX = 0
    yIni= Y_INI
    //Insertar Estado Inicial
    drawStates.push(jsonStr["iniSt"]);
    arrayStates.push({"id":jsonStr["iniSt"], "loc":""+0+" "+Y_INI, "text":">Q"+jsonStr["iniSt"]})
    while (actualState != endState) {
        //Buscamos las transiciones que pertenecen al estado actual
        auxArrayTrans = [];
        for (let i = 0; i < transitions.length; i++) {
            if (transitions[i][0] == actualState)
                auxArrayTrans.push(transitions[i])
        }
        //Hay una bifurcacion
        if (auxArrayTrans.length > 1) {
            let analizeSt1 = existTwoTrans(transitions, auxArrayTrans[0][1]);   //Estado al que se llega primer transicion
            let analizeSt2 = existTwoTrans(transitions, auxArrayTrans[1][1]);   //Estado al que se llega segunda transicion
            if(!analizeSt1 && !analizeSt2){
                console.log("bifurcacion tipo OR");
            }
            //Dos transiciones hacia un mismo estado
            else if(analizeSt1 || analizeSt2){   
                //Buscamos cual es el estado "lineal" y  "curvo"
                let indexSpecialState = 0;
                let indexLinealState = 0
                if (analizeSt1){
                    indexSpecialState = 0;
                    indexLinealState = 1;
                }else if(analizeSt2){   //Dos transnciones al estado 2 ()
                    indexSpecialState = 1;
                    indexLinealState = 0;
                }
                // ------ C U R V O ------
                if(drawStates.includes(auxArrayTrans[indexSpecialState][0])){//Ya se ha pasado por ahi
                    //Agregamos Transicion Especial
                    arrayTrans.push({"from": actualState, "to":auxArrayTrans[indexSpecialState][1], "text": getCarTransition(auxArrayTrans[indexSpecialState]),"curviness": 60 });
                }else{  //Nuevo Estado
                    //Agregar Transicion                    
                    arrayTrans.push({"from": actualState, "to":auxArrayTrans[indexSpecialState][1], "text": getCarTransition(auxArrayTrans[indexSpecialState]),"curviness": -100 });
                }
                // ------ L I N E A L ----- 
                //Cambiar de Estado
                iniState = actualState;
                actualState = auxArrayTrans[indexLinealState][1];
                drawStates.push(actualState);
                goX = (goX + SPACE_BSTS);
                //Agregar Estado
                if(actualState == endState) //Llegmaos al estado de aceptacion
                    arrayStates.push({"id": actualState, "loc":""+goX+" "+Y_INI, "text":"Q"+actualState+"*"})
                else                        //NO ES Aceptacion
                    arrayStates.push({"id": actualState, "loc":""+goX+" "+Y_INI, "text":"Q"+actualState})
                //Agregar Transcion
                arrayTrans.push({"from": iniState,"to":actualState, "text": getCarTransition(auxArrayTrans[indexLinealState]),"curviness": 30 })
                
            }
            
        //Solo hay un estado al que se llega desde el estado Actual
        } else {
            iniState = actualState
            actualState = auxArrayTrans[0][1]   //Estado al que se llega, indice cero ya que solo hay una transcion
            drawStates.push(actualState);
            goX = (goX + SPACE_BSTS);
            if(actualState == endState) //Llegmaos al estado de aceptacion
                arrayStates.push({"id": actualState, "loc":""+goX+" "+Y_INI, "text":"Q"+actualState+"*"})
            else
                arrayStates.push({"id": actualState, "loc":""+goX+" "+Y_INI, "text":"Q"+actualState})
            //Agregar Transicion
            arrayTrans.push({"from": iniState,"to":actualState, "text": getCarTransition(auxArrayTrans[0]),"curviness": 30 })
        }
    }
    //Modificar Main Json
    for (let i = 0; i < arrayStates.length; i++)    //Agregar Estados
        mainJsonAFN["nodeDataArray"].push(arrayStates[i]);
    for (let i = 0; i < arrayTrans.length; i++)    //Agregar Transiciones
        mainJsonAFN["linkDataArray"].push(arrayTrans[i]);
    //Incrementar Y INI para el proximo automata
    Y_INI = (Y_INI + Y_ADD)

}
/*======================================================================
 * -------------- FUNCION QUE INICIALIZA ---------- GO JS --------------
 =====================================================================*/

//Funcion que inserta cada estado y trnasicion de todos los AFNS 
// en el Main JSON
function reloadJsonString(){
    //Mdificar el HTML de los selectores de AFNS
    updateHTMLSelectAFN();
    //Inicializar Main Json
    mainJsonAFN["nodeDataArray"] = [];
    mainJsonAFN["linkDataArray"] = [];
    //Cargar Estados y transisicones de Main JSON
    for (let i = 0; i < arrayAFNS.length; i++) {
        if (arrayAFNS[i]["visible"])
            drawAFN(arrayAFNS[i]["AFN"]);
    }
    //Cargar en GoJS
    LoadGoJS();
}

$(document).ready(function () {

    //Inicializar GoJS
    init();
    //Botones para crear Automatas
    var addBasicAFDBtn = $("a.btn.add-btn#basicAFD");
    var addRangeAFDBtn = $("a.btn.add-btn#rangeAFD")

    const { PythonShell } = require("python-shell");
    
    /* ========================== CONSTRUIR AFNS ==========================*/
    //Boton de Automata Basico
    addBasicAFDBtn.click(function (e) {
        e.preventDefault();
        //Lanzar Alerta
        Swal.fire({
            type: 'question',
            title: 'Ingresa el caracter',
            input: 'text',
            inputPlaceholder: 'E.g. a, b, c, 0, 1, 2 '
        }).then((result) => {
            if (result.value.length == 1) {
                //Caracter valido
                optionsPython.args = ["AFN", "Basico", result.value]

                let car = new PythonShell('main.py', optionsPython);
                //Creamos el automata
                car.on('message', function (jsonString) {
                    //Insertar JSON en Arreglo
                    // pushAFN(jsonString["AFN"]);
                    pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});
                    
                    if (jsonString["message"] == true){
                        Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                        reloadJsonString(); //Cargar GoJS
                    }
                    else
                        console.log(jsonString["message"])
                });

            } else
                Swal.fire("Solo se permite un caracter", "Por favor revisa la entrada", "error")
        });
    });
    //Boton de Automata Rango
    addRangeAFDBtn.click(function (e) {
        e.preventDefault();

        Swal.fire({
            type: 'question',
            title: 'Ingresa el rango del automata',
            text: 'Separado por un "-"',
            input: 'text',
            inputPlaceholder: 'E.g a-z, A-Z, 0-9'
        }).then((result) => {
            if (isValidRange(result.value)) {//Rango Valido
                
                optionsPython.args = ["AFN", "Rango", result.value]
                let car = new PythonShell('main.py', optionsPython);
                //Creamos el automata
                car.on('message', function (jsonString) {
                    //Insertar en el arreglo AFN
                    pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});                    
                    if (jsonString["message"] == true){
                        Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                        reloadJsonString(); //Cargar GoJS
                    }
                    else
                        console.log(jsonString["message"])
                });
            } else
                Swal.fire("No ingreso un rango valido", "Por favor revisa la entrada", "error")

        });

    })
    /* ======================= OPERACIONES CON AFNS =======================*/
    var btnOpConc= $('a.btn.operAFN#conc');
    var btnOpUnion = $('a.btn.operAFN#union');
    var btnOpOptional= $('a.btn.operAFN#optional');
    var btnOpKlPlus = $('a.btn.operAFN#klPlus');
    var btnOpKlStar = $('a.btn.operAFN#klStar');

    //Concatenar AFN
    btnOpConc.click(function(e){
        e.preventDefault();
        //El id es el indice de la pila de AFNS serializados por Python, nos servira para hacer la operacion
        let idAFN1 = $("input[name='radio-group-1']:checked", "#1").val();  
        let idAFN2 = $("input[name='radio-group-2']:checked", "#2").val();

        if (typeof(idAFN1) == "undefined" || typeof(idAFN2) == "undefined" ){
            Swal.fire("Verfica tu seleccion","","warning");

        }else if (idAFN1 == idAFN2){//Selecciono el mismo AFN
            Swal.fire("No puedes concatenar el mismo AFN", "Elige dos diferentes", "warning");
        }else{//Operacion Concatenar
            //Llamamos a Python
            optionsPython.args = ["AFN", "Concatenar", idAFN1, idAFN2]
            let answer = new PythonShell('main.py', optionsPython);
            //Creamos el automata
            answer.on('message', function (jsonString) {
                //Sacar AFNS
                arrayAFNS[parseInt(idAFN1)]["visible"] = false
                arrayAFNS[parseInt(idAFN2)]["visible"] = false
                //InsertarAFN
                pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});
                if (jsonString["message"] == true){
                    Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                    reloadJsonString(); //Cargar GoJS
                }
                else
                    console.log(jsonString["message"])
            });
        }
        
    })
    //Opcional AFN
    btnOpOptional.click(function(e){
        e.preventDefault();
        let idAFN = $("input[name='radio-group-3']:checked", "#3").val();  

        if(typeof(idAFN) == "undefined"){
            Swal.fire("Seleccione un AFN", "", "error");
        }else{
            //Llamar a Metodo en Python
            optionsPython.args = ["AFN", "Opcional", idAFN]
            let answer = new PythonShell('main.py', optionsPython);
            //Creamos el automata
            answer.on('message', function (jsonString) {
                //Sacar AFNS
                arrayAFNS[parseInt(idAFN)]["visible"] = false
                //InsertarAFN
                pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});
                if (jsonString["message"] == true){
                    Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                    reloadJsonString(); //Cargar GoJS
                }
                else
                    console.log(jsonString["message"])
            });
        }
    })
    //Kleen Plus AFN
    btnOpKlPlus.click(function(e){
        e.preventDefault();
        let idAFN = $("input[name='radio-group-3']:checked", "#3").val();  

        if(typeof(idAFN) == "undefined"){
            Swal.fire("Seleccione un AFN", "", "error");
        }else{
            //Llamar a Metodo en Python
            optionsPython.args = ["AFN", "Plus", idAFN]
            let answer = new PythonShell('main.py', optionsPython);
            //Creamos el automata
            answer.on('message', function (jsonString) {
                //Sacar AFN
                arrayAFNS[parseInt(idAFN)]["visible"] = false
                //InsertarAFN
                pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});
                if (jsonString["message"] == true){
                    Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                    reloadJsonString(); //Cargar GoJS
                }
                else
                    console.log(jsonString["message"])
            });
        }
    })
    //Kleen Star AFN
    btnOpKlStar.click(function(e){
        e.preventDefault();
        let idAFN = $("input[name='radio-group-3']:checked", "#3").val();  

        if(typeof(idAFN) == "undefined"){
            Swal.fire("Seleccione un AFN", "", "error");
        }else{
            //Llamar a Metodo en Python
            optionsPython.args = ["AFN", "Star", idAFN]
            let answer = new PythonShell('main.py', optionsPython);
            //Creamos el automata
            answer.on('message', function (jsonString) {
                console.log(jsonString["AFN"])
                //Sacar AFN
                arrayAFNS[parseInt(idAFN)]["visible"] = false
                //InsertarAFN
                pushAFN({"AFN": jsonString["AFN"], "id": jsonString["Id"], "visible": true});
                if (jsonString["message"] == true){
                    Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                    reloadJsonString(); //Cargar GoJS
                }
                else
                    console.log(jsonString["message"])
            });
        }

    })
})

//--------------------------------------------------
// ---- F U N C I O N E S   A U X I L I A R E S ----
//--------------------------------------------------
function isValidRange(string) {
    if (string.length == 3) {
        if (string[1] == '-') {
            if (string.charCodeAt(0) < string.charCodeAt(2))
                return true;
            else
                return false;
        }
        else
            return false;
    } else {
        return false;
    }
}
