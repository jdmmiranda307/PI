var current_disciplinas = []
$(document).ready(function() {
    professor_id = $("#data-div").data("id")
    $.ajax({
        url: 'http://localhost:8000/cursos/get-cursos',
        cache: false,
        success: function(response) {
            $("#cursosSelect").empty()
            option = "<option>Selecione</option>"
            $("#cursosSelect").append(option)
            response.cursos.forEach(function (curso){
                option = "<option value="+ curso.id +">"+ curso.nome +"</option>"
                $("#cursosSelect").append(option)
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });

    $.ajax({
        url: 'http://localhost:8000/cursos/get-curso-disciplinas',
        cache: false,
        success: function(response) {
            $("#disciplinasSelect").empty()
            response.cursoDisciplinas.forEach(function (cursoDisciplina){
                option = "<option value="+ cursoDisciplina.id +">"+ cursoDisciplina.nome +"</option>"
                $("#disciplinasSelect").append(option)
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
            getProfessor()
        }
    });

    $("#editContent").click(function(){
        editableProps($(this))
    })

    

    $("#excluir").click(function(){
        $.ajax({
            url: 'http://localhost:8000/professores/delete-professor/' + professor_id,
            cache: false,
            success: function(response) {
                window.location = "/professores/"
            },
            error: function(response) {
                alert("Ocorreu algum erro")
            }
        });
    })

    $("#save").click(function(){
        var formData = new FormData();
        data = {
            'disciplinas_removidas': []
        }
        if (professor_id){
            formData.append('id', professor_id)
        }
        $(".input-form").each(function () {
            name = $(this).prop("name")
            if(name=="is_superuser")
                val = $(this).prop("checked")
            else
                val = $(this).val()
            data[name] = val
            formData.append(name, val)
        })
        disciplinas_removidas = []
        current_disciplinas.forEach(function(disciplina){
            if(!data['disciplinas'].includes(String(disciplina))){
                disciplinas_removidas.push(disciplina)
            }
        })
        formData.append('disciplinas_removidas', disciplinas_removidas)
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: 'http://localhost:8000/professores/',
            data: formData,
            processData: false,
            contentType: false,
            type: "POST",
            complete: function(response) {
                if(response.status == 204 || response.status == 200)
                    window.location = "/professores/"
                else if(response.status == 406)
                    window.alert("Email já está em uso!")
                else
                    window.alert("Erro ao salvar!");
            }
        });
    })

    if(!$("#data-div").data("id")){
        editableProps($("#editContent"))
        $("#excluir").hide()
        $("#cancel").click(function(){
            window.location = '/alunos'
        })
    }
    else{
        $("#cancel").click(function(){
            cancelFunctEdit()
        })
    }



    function getCookie(c_name){
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
});

var getProfessor = function (){
    professor_id = $("#data-div").data("id")
    $.ajax({
        url: 'http://localhost:8000/professores/get-professor/' + professor_id,
        cache: false,
        success: function(response) {
            response.professores.forEach(function (professor){
                $("#inputNome").val(professor.nome)
                $("#inputCPF").val(professor.cpf)
                $("#inputDataNascimento").val(professor.data_nascimento)
                $("#inputEmail").val(professor.email)
                $("#inputAdministrador").prop('checked', professor.administrador)
                current_disciplinas =  professor.disciplinas_id
                professor.disciplinas_id.forEach(function (disciplina_id){
                    $('#disciplinasSelect option[value=' + disciplina_id + ']').attr('selected', true);
                })
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });
}

var editableProps = function($this) {
    $this.css("display", "none")
    $(".hidden-elems").removeAttr('hidden')
    $(".input-form").removeAttr("disabled")
}

var cancelFunctEdit = function() {
    $("#editContent").css("display", "block")
    $(".hidden-elems").attr('hidden', true)
    $(".input-form").attr("disabled", true)
}