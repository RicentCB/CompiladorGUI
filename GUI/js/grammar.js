$(document).ready(function(){
    let JSONTable = {
        Head :["SIM1", "SIM2", "SIM3", "SIM4", "SIM5", "SIM6"],
        Body : [
            ["1","2","3", "4","5", "6"],
            ["1","2","3", "4","5", "6"],
            ["1","2","3", "4","5", "6"],
        ]
    }
    let containerTable = $("main#grammar .create-table-result#grammar-ll1");
    //Construir la tabla con json generado
    let strTable = "<table>";
        //Agregar Encabezado
        strTable += "<thead><tr>";
        for (let i = 0; i < JSONTable.Head.length; i++) {
            strTable += "<td>"+JSONTable.Head[i]+"</td>";
        }
        strTable += "</tr></thead>";
        //Agregar cuerpo
        strTable += "<tbody>";
        for (let i = 0; i < JSONTable.Body.length; i++) {
            strTable += "<tr>";
            for (let j = 0; j < JSONTable.Body[0].length; j++) {
                strTable += "<td>"+JSONTable.Body[i][j]+"</td>";                
            }
            strTable += "</tr>";
            
        }
        strTable += "</tbody>";
        strTable += "</table>";
    //Insertar el Nodo
    containerTable.html("");
    containerTable.append(strTable);

    let btnGetFile = $("main#grammar #file-input-grammar");
    
    btnGetFile.change(function (e){

        let fileType = e.target.files[0].type;
        if(fileType != "text/plain"){
            swal.fire("Error", "Solo archivos (*.txt)", "error");
        }else{
            //NO hay error en el tipo de archivos
        }
        
    })

})