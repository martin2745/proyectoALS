function crearformoculto(name, action) {

    if ($("#" + name).length == 0) {

        var formu = document.createElement('form');
        document.body.appendChild(formu);
        formu.name = name;
        formu.action = action;
        formu.method = "POST";
        formu.id = name;
        formu.style.display = "none";
    }
}

function insertacampo(form, name, value) {

    formulario = form;
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    input.className = name;
    formulario.appendChild(input);
}

function abrirFormRegistro(){
    document.getElementById("dvLogin").style.display = "none";
    document.getElementById("dvSingUp").style.display = "block";
    document.getElementById("enlaceSingUp").style.display = "none";
    document.getElementById("enlaceLogin").style.display = "block";

}
function abrirFormLogin(){
    document.getElementById("dvLogin").style.display = "block";
    document.getElementById("dvSingUp").style.display = "none";
    document.getElementById("enlaceLogin").style.display = "none";
    document.getElementById("enlaceSingUp").style.display = "block";
}

function abrirFormCreaLibro() {
    document.getElementById("dvCreaLibro").style.display = "block";
    $("#edIsbn").attr("disabled", false);
    document.getElementById("dvCreaLibroForm").setAttribute('action', '/guarda_libro');
}

function cerrarFormCreaLibro() {
    document.getElementById("dvCreaLibro").style.display = "none";
    rellenarFormulario("","","","")

}

function rellenarFormulario(titulo, autor, isbn, url, argumento) {

    $("#edTitulo").val(titulo);
    $("#edAutor").val(autor);
    $("#edIsbn").val(isbn);
    $("#edArgumento").val(argumento);
    $("#edUrl").val(url);

}

function editarLibro(titulo, autor, isbn, argumento, url, oid) {
    $("#edIsbn").attr("disabled", true);
    document.getElementById("dvCreaLibroForm").setAttribute('action', '/edita_libro');
    rellenarFormulario(titulo, autor, isbn, url, argumento);
    insertacampo(document.dvCreaLibroForm, "edOid", oid);
    document.getElementById("dvCreaLibro").style.display = "block";
}

function eliminarLibro(valor) {
    crearformoculto('formularioEliminarLibro', '/elimina_libro');
    insertacampo(document.formularioEliminarLibro, "edOid", valor);
    document.formularioEliminarLibro.submit();
}

function abrirFormCreaResenha() {
    document.getElementById("dvCreaResenha").style.display = "block";
}

function abrirFormCreaResenhaVistaLibro(titulo) {
    document.getElementById("dvCreaResenha").style.display = "block";
    document.getElementById("edTituloResenha").value = titulo;
    document.getElementById("edTituloResenhaOculto").value = titulo;

}

function cerrarFormCreaResenha() {
    document.getElementById("dvCreaResenha").style.display = "none";
    rellenarFormularioResenha("","","")
}


function rellenarFormularioResenha(titulo, url, opinion) {

    $("#edTitulo").val(titulo);
    $("#edUrl").val(url);
    $("#edOpinion").val(opinion);

}