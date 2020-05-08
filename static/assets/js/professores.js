$(document).ready(function() {
    var table = $('#professores').DataTable({
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
        url: 'http://localhost:8000/professores/get-professores',
        cache: false,
        success: function(response) {
            response.professores.forEach(function (professor){
                table.row.add( [professor.id, professor.nome, professor.cursos, professor.email] ).draw( false )
            })
            $('#professores').on('click', 'tbody tr', function() {
                professor_id = table.row( this ).data()[0];
                window.location = "/professores/" + professor_id
            })
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });

    $("#create").click(function () {
        window.location = "/professores/create-professor"
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