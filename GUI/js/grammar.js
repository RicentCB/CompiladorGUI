var path = require("path");

    var optionsPython = {
        mode: 'json',
        pythonOptions: ['-u'],
        scriptPath: path.join(__dirname, 'Engine/'),
        pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
        args: []
    };
const WORD_ACCEPT = "Aceptar";
$(document).ready(function(){

    //Botones de Tabs
    let tabContainer = $("main #tabs");
    let tabMenuLl1 = tabContainer.find(".nav-tab#item-ll1");
    let tabMenuLr0 = tabContainer.find(".nav-tab#item-lr0");
    let tabMenuLr1 = tabContainer.find(".nav-tab#item-lr1");

    let tabContainerLl1 = tabContainer.find(".container-tab#ll1");
    let tabContainerLr0 = tabContainer.find(".container-tab#lr0");
    let tabContainerLr1 = tabContainer.find(".container-tab#lr1");

    function activeItemNavTab(obj){
        //Clase active
        allItems = $(obj).parent().find(".nav-tab");
        for (let i = 0; i < allItems.length; i++) 
            $(allItems[i]).removeClass("active")
        $(obj).addClass("active");
        //Mostrar contenido del item selccionado
        let objId = $(obj).attr("id")
        if (objId == $(tabMenuLl1).attr("id")){
            tabContainerLl1.slideDown(500)
            tabContainerLr0.css({"display": "none"})
            tabContainerLr1.css({"display": "none"})
        }else if(objId == $(tabMenuLr0).attr("id")){
            tabContainerLl1.css({"display": "none"})
            tabContainerLr0.slideDown(500)
            tabContainerLr1.css({"display": "none"})
        }else if(objId == $(tabMenuLr1).attr("id")){
            tabContainerLl1.css({"display": "none"});
            tabContainerLr0.css({"display": "none"})
            tabContainerLr1.slideDown(500)
        }
    }

    tabMenuLl1.click(function(e){
        e.preventDefault();
        activeItemNavTab($(this))
    })
    tabMenuLr0.click(function(e){
        e.preventDefault();
        activeItemNavTab($(this))
    })
    tabMenuLr1.click(function(e){
        e.preventDefault();
        activeItemNavTab($(this))
    })
    /*===================================================
        =========== ANALIZAR CADENAS ===============
    ===================================================*/
    const { PythonShell } = require("python-shell");

    let pathLexAn = "";
    let btnGetFileLex = $("main#grammar #file-input-lexAn");
    let pathSymb = "";
    let btnGetFileSymb = $("main#grammar #file-input-symb");

    btnGetFileLex.change(function(e){
        let fileIn = e.target.files[0];
        $(this).parent().find("p#title-lexAn").html("Archivo Cargado: '"+fileIn.name+"'")
        pathLexAn = fileIn.path;
    })
    btnGetFileSymb.change(function(e){
        let fileIn = e.target.files[0];
        $(this).parent().find("p#title-symb").html("Archivo Cargado: '"+fileIn.name+"'")
        pathSymb = fileIn.path;
    })
    /* ======================================================================== */
    /* --------------------- A N A L I Z A D O R    L L 1 --------------------- */ 
    /* ======================================================================== */
    let btnGetFileGrammarLL1 = $("main#grammar #file-input-grammar-ll1");
    let containerTableLL1 = $("main#grammar .create-table-result#grammar-ll1");
    let sectionAnStringLL1 = $("#analizeStr-ll1")
    let containerAnStringLL1 = sectionAnStringLL1.find("#analizeStrLL1");
    let btnAnStringLL1 = sectionAnStringLL1.find("#btnStringAnGrammarLL1")
    let inputStringLL1 = sectionAnStringLL1.find("#inStringAnGrammarLL1");
    let tableStringLL1 = sectionAnStringLL1.find("#regsAnalizeStringLL1");

    btnGetFileGrammarLL1.change(function (e){
        let fileIn = e.target.files[0];
        containerTableLL1.html("")
        containerAnStringLL1.slideUp();
        $(this).parent().find("#title-in-grammar-ll1").html("Archivo Cargado: '"+fileIn.name+"'")
        if(fileIn.type != "text/plain"){
            swal.fire("Error", "Solo archivos (*.txt)", "error");
        }else{
            //NO hay error en el tipo de archivo
            //Llamamos al metodo de Python
            optionsPython.args = ["Grammar", "PathLL1", fileIn.path]

            let resultPython = new PythonShell('main.py', optionsPython);
            resultPython.on('message', function (jsonString) {
                //Insertar JSON en Arreglo
                if (jsonString["message"] == true){
                    Swal.fire("Gramatica Aceptada", "", "success");
                    containerAnStringLL1.slideDown();
                    tableStringLL1.html("")
                    containerAnStringLL1.find("#inStringAnGrammarLL1").val("")
                    //Construir la tabla con json generado
                    let strTable = "<table>";
                    //Agregar Encabezado
                    strTable += "<thead><tr>";
                    for (let i = 0; i < jsonString.Head.length; i++) {
                        strTable += "<td>"+jsonString.Head[i]+"</td>";
                    }
                    strTable += "</tr></thead>";
                    //Agregar cuerpo
                    strTable += "<tbody>";
                    for (let i = 0; i < jsonString.Body.length; i++) {
                        strTable += "<tr>";
                        for (let j = 0; j < jsonString.Body[0].length; j++) {
                            if (j == jsonString.Body[0].length -1 && i==jsonString.Body.length-1){
                                strTable += "<td class='td-accept'>Aceptar</td>"
                            }
                            else if(jsonString.Body[i][j] == " "){
                                strTable += "<td></td>";
                            }else{
                                strTable += "<td>"+jsonString.Body[i][j]+"</td>";                
                            }

                        }
                        strTable += "</tr>";
                        
                    }
                    strTable += "</tbody>";
                    strTable += "</table>";
                    //Insertar el Nodo
                    containerTableLL1.html("");
                    containerTableLL1.append(strTable);
                    //Seccion para analizar Cadena
                    sectionAnStringLL1.slideDown()
                    
                }
                else{
                    swal.fire("Error en la gramatica", "", "error");
                    console.log(jsonString["message"])
                }
            });
        }
        
    })
    //Escribir cadena LL1
    inputStringLL1.click(function(e){
        console.log("inputStr");
        if (pathSymb == "" || pathLexAn == ""){
            Swal.fire("Faltan Archivos", "Por favor eliga primero, el analizador lexico y la relacion simbolos terminales", "warning");
        }
    })
    //  -------------- ANALIZAR CADENA -------------------- 
    btnAnStringLL1.click(function(e){
        e.preventDefault();
        let valString = sectionAnStringLL1.find("#inStringAnGrammarLL1").val();
        console.log(valString)
        optionsPython.args = ["Grammar", "StringLL1", valString, pathLexAn, pathSymb]

        let resultPython = new PythonShell('main.py', optionsPython);
        resultPython.on('message', function (jsonString) {

            if (jsonString["message"] == true){
                Swal.fire("Cadena Aceptada", "", "success");
                //Construir la tabla con json generado
                let strTable = "<table class='title-upper'>";
                //Agregar Encabezado
                strTable += "<thead><tr>";
                    strTable += "<th>Pila</th>"
                    strTable += "<th>Cadena</th>"
                    strTable += "<th>Accion</th>"
                    
                strTable += "</tr></thead>";
                //Agregar cuerpo
                strTable += "<tbody>";
                for (let i = 0; i < jsonString.Action.length; i++) {
                    strTable += "<tr>";
                        strTable += "<td>"+jsonString.Stack[i]+"</td>"
                        strTable += "<td>"+jsonString.String[i]+"</td>"
                        strTable += "<td>"+jsonString.Action[i]+"</td>"
                    strTable += "</tr>";
                }
                strTable += "</tbody>";
                strTable += "</table>";
                //Insertar el Nodo
                tableStringLL1.html("");
                tableStringLL1.append(strTable);
                
            }
            else{
                swal.fire("Error en la gramatica", "", "error");
                console.log(jsonString["message"])
            }
        });
        
                
            
    })
    /* ======================================================================== */
    /* --------------------- A N A L I Z A D O R    L R 0 --------------------- */ 
    /* ======================================================================== */
    let sectionLRO = $(".container-tab#lr0");
    let btnGetFileGrammarLR0 = sectionLRO.find("#file-input-grammar-lr0");
    let containerTableLR0 = sectionLRO.find(".create-table-result#grammar-lr0");
   
    btnGetFileGrammarLR0.change(function(e){
        let fileIn = e.target.files[0];
        containerTableLR0.html("")
        containerAnStringLL1.slideUp();
        $(this).parent().find("#title-in-grammar-ll1").html("Archivo Cargado: '"+fileIn.name+"'")
        if(fileIn.type != "text/plain"){
            swal.fire("Error", "Solo archivos (*.txt)", "error");
        }else{
            //NO hay error en el tipo de archivo
            //Llamamos al metodo de Python
            optionsPython.args = ["Grammar", "PathLR0", fileIn.path]

            let resultPython = new PythonShell('main.py', optionsPython);
            resultPython.on('message', function (jsonString) {
                //Insertar JSON en Arreglo
                console.log(jsonString);
                if (jsonString["message"] == true){
                    Swal.fire("Gramatica LR0 Aceptada", "", "success");
                    containerAnString.slideDown();
                    //Construir la tabla con json generado
                    let strTable = "<table>";
                    //Agregar Encabezado
                    strTable += "<thead><tr>";
                    for (let i = 0; i < jsonString.Head.length; i++) {
                        strTable += "<td>"+jsonString.Head[i]+"</td>";
                    }
                    strTable += "</tr></thead>";
                    //Agregar cuerpo
                    strTable += "<tbody>";
                    for (let i = 0; i < jsonString.Body.length; i++) {
                        strTable += "<tr>";
                        for (let j = 0; j < jsonString.Body[0].length; j++) {
                            if (jsonString.Body[i][j] == WORD_ACCEPT){
                                strTable += "<td class='td-accept'>Aceptar</td>"
                            }
                            else if(jsonString.Body[i][j] == " "){
                                strTable += "<td class='td-white'></td>"
                            }else{
                                strTable += "<td>"+jsonString.Body[i][j]+"</td>";                
                            }

                        }
                        strTable += "</tr>";
                        
                    }
                    strTable += "</tbody>";
                    strTable += "</table>";
                    //Insertar el Nodo
                    containerTableLR0.html("");
                    containerTableLR0.append(strTable);
                    //Seccion para analizar Cadena
                    // sectionAnStringLR0.slideDown()
                    
                }
                else{
                    swal.fire("Error en la gramatica", "", "error");
                    console.log(jsonString["message"])
                }
                
            });
        }
    });
    //Escribir Cadena LR0
    

})