$(document).ready(function() {
    curso_id = $("#data-div").data("id")
    getDisciplina()
    $("#editContent").click(function(){
        editableProps($(this))
    })

    $("#excluir").click(function(){
        $.ajax({
            url: 'http://localhost:8000/disciplinas/delete-disciplina/' + disciplina_id,
            cache: false,
            success: function(response) {
                window.location = "/disciplinas/"
            },
            error: function(response) {
                alert("Ocorreu algum erro")
            }
        });
    })

    $("#save").click(function(){
        var formData = new FormData();
        if (disciplina_id){
            formData.append('id', disciplina_id)
        }
        $(".input-form").each(function () {
            formData.append($(this).prop("name"), $(this).val())
        })
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: 'http://localhost:8000/disciplinas/',
            data: formData,
            processData: false,
            contentType: false,
            type: "POST",
            complete: function(response) {
                if(response.status == 204 || response.status == 200)
                    window.location = "/disciplinas/"
                else
                    window.alert("Erro ao salvar!");
            }
        });
    })

    if(!$("#data-div").data("id")){
        editableProps($("#editContent"))
        $("#excluir").hide()
        $("#cancel").click(function(){
            window.location = '/disciplinas'
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

var getDisciplina = function (){
    disciplina_id = $("#data-div").data("id")
    $.ajax({
        url: 'http://localhost:8000/disciplinas/get-disciplina/' + disciplina_id,
        cache: false,
        success: function(response) {
            response.disciplinas.forEach(function (disciplina){
                $("#inputNome").val(disciplina.nome)
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