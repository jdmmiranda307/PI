var current_disciplinas = []
$(document).ready(function() {
    aula_id = $("#data-div").data("id")

    $.ajax({
        url: 'http://localhost:8000/cursos/get-curso-disciplinas',
        cache: false,
        success: function(response) {
            $("#cursoDisciplinaSelect").empty()
            response.cursoDisciplinas.forEach(function (cursoDisciplina){
                option = "<option value="+ cursoDisciplina.id +">"+ cursoDisciplina.nome +"</option>"
                $("#cursoDisciplinaSelect").append(option)
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
            getAula()
        }
    });

    $("#editContent").click(function(){
        editableProps($(this))
    })

    

    $("#excluir").click(function(){
        $.ajax({
            url: 'http://localhost:8000/aulas/delete-aula/' + aula_id,
            cache: false,
            success: function(response) {
                window.location = "/aulas/"
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
        if (aula_id){
            formData.append('id', aula_id)
        }
        $(".input-form").each(function () {
            name = $(this).prop("name")
            val = $(this).val()
            data[name] = val
            if(name == "foto"){
                formData.append("foto", $(this)[0].files[0])
            }
            else
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
            url: 'http://localhost:8000/aulas/create-aula/',
            data: formData,
            processData: false,
            contentType: false,
            type: "POST",
            complete: function(response) {
                if(response.status == 204 || response.status == 200)
                    window.location = "/aulas/"
                else
                    window.alert("Erro ao salvar!");
            }
        });
    })

    if(!$("#data-div").data("id")){
        editableProps($("#editContent"))
        $("#excluir").hide()
        $("#cancel").click(function(){
            window.location = '/aulas'
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

var getAula = function (){
    aula_id = $("#data-div").data("id")
    $.ajax({
        url: 'http://localhost:8000/aulas/get-aula/' + aula_id,
        cache: false,
        success: function(response) {
            response.aulas.forEach(function (aula){
                $("#inputNome").val(aluno.nome)
                $("#inputRA").val(aluno.registro_academico)
                $("#inputDataNascimento").val(aluno.data_nascimento)
                $("#cursosSelect").val(aluno.curso_id)
                $("#foto").attr("src", aluno.foto);
                current_disciplinas =  aluno.disciplinas_id
                aluno.disciplinas_id.forEach(function (disciplina_id){
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
    $("#foto").hide()
    $(".hidden-elems").removeAttr('hidden')
    $(".input-form").removeAttr("disabled")
}

var cancelFunctEdit = function() {
    $("#editContent").css("display", "block")
    $("#foto").show()
    $(".hidden-elems").attr('hidden', true)
    $(".input-form").attr("disabled", true)
}