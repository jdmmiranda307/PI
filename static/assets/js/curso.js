var current_disciplinas = []
$(document).ready(function() {
    curso_id = $("#data-div").data("id")

    $.ajax({
        url: 'http://localhost:8000/disciplinas/get-disciplinas',
        cache: false,
        success: function(response) {
            $("#disciplinasSelect").empty()
            response.disciplinas.forEach(function (disciplina){
                option = "<option value="+ disciplina.id +">"+ disciplina.nome +"</option>"
                $("#disciplinasSelect").append(option)
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
            getCurso()
        }
    });

    $("#editContent").click(function(){
        editableProps($(this))
    })

    

    $("#excluir").click(function(){
        $.ajax({
            url: 'http://localhost:8000/cursos/delete-curso/' + curso_id,
            cache: false,
            success: function(response) {
                window.location = "/cursos/"
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
        if (curso_id){
            formData.append('id', curso_id)
        }
        $(".input-form").each(function () {
            name = $(this).prop("name")
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
            url: 'http://localhost:8000/cursos/',
            data: formData,
            processData: false,
            contentType: false,
            type: "POST",
            complete: function(response) {
                if(response.status == 204 || response.status == 200)
                    window.location = "/cursos/"
                else
                    window.alert("Erro ao salvar!");
            }
        });
    })

    if(!$("#data-div").data("id")){
        editableProps($("#editContent"))
        $("#excluir").hide()
        $("#cancel").click(function(){
            window.location = '/cursos'
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

var getCurso = function (){
    curso_id = $("#data-div").data("id")
    $.ajax({
        url: 'http://localhost:8000/cursos/get-curso/' + curso_id,
        cache: false,
        success: function(response) {
            response.cursos.forEach(function (curso){
                $("#inputNome").val(curso.nome)
                current_disciplinas =  curso.disciplinas_id
                curso.disciplinas_id.forEach(function (disciplina_id){
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