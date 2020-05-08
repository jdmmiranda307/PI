$(document).ready(function() {
    var table = $('#aulas').DataTable({
        "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            }
        ],
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.20/i18n/Portuguese-Brasil.json"
        }
    });

    $.ajax({
        url: 'http://localhost:8000/aulas/get-aulas',
        cache: false,
        success: function(response) {
            response.aulas.forEach(function (aula){
                table.row.add( [aula.id, aula.descricao, aula.curso, aula.disciplina, aula.data, aula.ativo] ).draw( false )
            })
            $('#aulas').on('click', 'tbody tr', function() {
                aula_id = table.row( this ).data()[0];
                window.location = "/aulas/aula/" + aula_id
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });

    $("#create").click(function () {
        window.location = "/aulas/create-aula"
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