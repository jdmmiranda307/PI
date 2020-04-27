$(document).ready(function() {
    var table = $('#alunos').DataTable({
        "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            }
        ]
    });

    $.ajax({
        url: 'http://localhost:8000/alunos/get-alunos',
        cache: false,
        success: function(response) {
            response.alunos.forEach(function (aluno){
                table.row.add( [aluno.id, aluno.nome, aluno.registro_academico, aluno.curso] ).draw( false )
            })
            $('#alunos').on('click', 'tbody tr', function() {
                aluno_id = table.row( this ).data()[0];
                window.location = "/alunos/" + aluno_id
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });

    $("#create").click(function () {
        window.location = "/alunos/create-aluno"
    })

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