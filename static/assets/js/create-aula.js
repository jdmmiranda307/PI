$(document).ready(function() {
    aula_id = $("#data-div").data("id")
    if(sessionStorage.getItem("is_superuser") == 'true'){
        $("#professor-col").append(
            "<label for='exampleFormControlSelect1'>Professor</label>" +
            "<select disabled name='professor_responsavel_id' class='input-form form-control' id='ProfessorSelect'>"+
            "</select>"
        )
    }

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
            getProfessores()
            getAula()
        }
    });

    $('#cursoDisciplinaSelect').on('change', function(){
        getProfessores()
    })

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
                $("#inputDescricao").val(aula.descricao)
                $("#inputData").val(aula.data_field)
                $("#cursoDisciplinaSelect").val(aula.curso_disciplina_id)
                $("#ProfessorSelect").val(aula.professor_responsavel_id)
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

var getProfessores = function() {
    $.ajax({
        url: 'http://localhost:8000/professores/get-professor-disciplina/' + $('#cursoDisciplinaSelect').val(),
        cache: false,
        success: function(response) {
            $("#ProfessorSelect").empty()
            response.professores.forEach(function (professor){
                option = "<option value="+ professor.id +">"+ professor.nome +"</option>"
                $("#ProfessorSelect").append(option)
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });
}