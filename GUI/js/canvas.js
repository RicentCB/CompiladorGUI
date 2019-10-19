
const LINEW = 60;
const SPACE_BSTS = 180;
let Y_INI = 0;
let Y_ADD = 120;

let arrayAFNS = [];
/* ------------- Funcion que actulza los select Box ------------- */
function updateHTMLSelectAFN(){
    var arraySelect = $('.container-select .select-options');
    for (let i = 0; i < arraySelect.length; i++) {
        $(arraySelect[i]).empty();
        let strId = $(arraySelect[i]).attr("id");
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
function pushAFN(jsonString) {
    //Insertamos el objeto JSON en arreglo del AFNS
    arrayAFNS.push(jsonString);
    //Mdificar el HTML de los selectores de AFNS
    updateHTMLSelectAFN();
    //Incrementar Y INI para el proximo automata
    Y_INI = (Y_INI + Y_ADD)
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
/*---------------------------------------------------------------
 * ---- FUNCION QUE DIBUJA UN AUTOMATA DADO UN OBJETO JSON ----
---------------------------------------------------------------*/
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
}
function drawAFN(jsonStr) {
    let actualState = jsonStr["iniSt"];
    let endState = jsonStr["endSt"];
    let transitions = jsonStr["transitions"];
    //Arreglo de Estados para insertar en el main JSON AFN
    let arrayStates= [];
    //Arreglo de Transncions para insertar en el main JSON AFN
    let arrayTrans = [];
    goX = 0
    yIni= Y_INI
    //Insertar Estado Inicial
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
            console.log("bifurcacion");
        } else {//Solo hay un estado al que se llega
            iniState = actualState
            actualState = auxArrayTrans[0][1]   //Estado al que se llega, indice cero ya que solo hay una transcion
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

}
//-----------------------------------------------------------------------
/*=======================================================================
 * ---- FUNCION QUE DIBUJA UN AUTOMATA DADO UN OBJETO JSON CON GO JS ----
 ======================================================================*/
//-----------------------------------------------------------------------
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


$(document).ready(function () {

    //Inicializar GoJS
    init();
    //Botones para crear Automatas
    var addBasicAFDBtn = $("a.btn.add-btn#basicAFD");
    var addRangeAFDBtn = $("a.btn.add-btn#rangeAFD")

    const { PythonShell } = require("python-shell");
    var path = require("path");
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
                var options = {
                    mode: 'json',
                    pythonOptions: ['-u'],
                    scriptPath: path.join(__dirname, 'Engine/'),
                    pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
                    args: ["AFN", "Basico", result.value]
                };

                let car = new PythonShell('main.py', options);
                //Creamos el automata
                car.on('message', function (jsonString) {
                    drawAFN(jsonString["AFN"])
                    pushAFN(jsonString["AFN"]);
                    if (jsonString["message"] == true){
                        Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                        LoadGoJS(); //Cargar GoJS
                    }
                    else
                        console.log(jsonString["message"])
                });

            } else
                Swal.fire("Solo se permite un caracter", "Por favor revisa la entrada", "error")
        });
    });
    //AFD de Rango
    addRangeAFDBtn.click(function (e) {
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
                    scriptPath: path.join(__dirname, 'Engine/'),
                    pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
                    args: ["AFN", "Rango", result.value]
                };

                let car = new PythonShell('main.py', options);
                //Creamos el automata
                car.on('message', function (jsonString) {
                    drawAFN(jsonString["AFN"]);
                    pushAFN(jsonString["AFN"]);
                    if (jsonString["message"] == true){
                        Swal.fire("Exito al crear automata", "Id: " + jsonString["Id"], "success");
                        LoadGoJS(); //Cargar GoJS
                    }
                    else
                        console.log(jsonString["message"])
                });
            } else
                Swal.fire("No ingreso un rango valido", "Por favor revisa la entrada", "error")

        });

    })
    /* ======================= OPERACIONES CON AFNS =======================*/
    var btnOpUnion = $('a.btn.operAFN#union');
    var btnOpConc= $('a.btn.operAFN#conc');
    var btnOpOptional= $('a.btn.operAFN#optional');
    var btnOpKlPlus = $('a.btn.operAFN#klPlus');
    var btnOpKlStar = $('a.btn.operAFN#klStar');

})

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

Math.radians = function (degrees) {
    return degrees * Math.PI / 180;
}