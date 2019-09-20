$(document).ready(function(){
    let mainTitle = $("h1.main-title");
    let abtn = $("a.btn");

    abtn.click(function(e){
        e.preventDefault()
        mainTitle.html("COMPPP")
    })
})