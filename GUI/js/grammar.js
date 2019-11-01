var path = require("path");

    var optionsPython = {
        mode: 'json',
        pythonOptions: ['-u'],
        scriptPath: path.join(__dirname, 'Engine/'),
        pythonPath: '/usr/bin/python3',         //Cambiar la ruta de acuerdo al sistema
        args: []
    };

$(document).ready(function(){

    const { PythonShell } = require("python-shell");

    let JSONTable = {
        Head :["SIM1", "SIM2", "SIM3", "SIM4", "SIM5", "SIM6"],
        Body : [
            ["1","2","3", "4","5", "6"],
            ["1","2","3", "4","5", "6"],
            ["1","2","3", "4","5", "6"],
        ]
    }
    

    let btnGetFile = $("main#grammar #file-input-grammar");
    let containerTable = $("main#grammar .create-table-result#grammar-ll1");
    
    btnGetFile.change(function (e){
        let fileIn = e.target.files[0];
        if(fileIn.type != "text/plain"){
            swal.fire("Error", "Solo archivos (*.txt)", "error");
        }else{
            //NO hay error en el tipo de archivo
            console.log()
            //Llamamos al metodo de Python
            optionsPython.args = ["Grammar", "Path", fileIn.path]

            let resultPython = new PythonShell('main.py', optionsPython);
            resultPython.on('message', function (jsonString) {
                //Insertar JSON en Arreglo
                console.log(jsonString);
                if (jsonString["message"] == true){
                    Swal.fire("Gramatica Aceptada", "", "success");
                    //Creamos la tabla
                    
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
                    containerTable.html("");
                    containerTable.append(strTable);
                    
                }
                else{
                    swal.fire("Error en la gramatica", "", "error");
                    console.log(jsonString["message"])
                }
            });
        }
        
    })

})