$(document).ready(function() {
    TABLE = $('#alunos').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.20/i18n/Portuguese-Brasil.json"
        }
    })
    getData()
    $("#edit").click(function () {
        window.location = "/aulas/" + $('#aulaid').data('aulaid')
    })
});

setInterval(function() {
    getData()
    getButton()
}, 1000)

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

var getData = function (){
    link = 'http://localhost:8000/aulas/get-alunos/' + $('#aulaid').data('aulaid')
    $.ajax({
        url: link,
        cache: false,
        success: function(response) {
            $('#table-body').empty()
            n = 0
            aulaAtivo = ($("#aulaid").data('aulaativo') == 'True' ? true : false)
            if (response.alunos.length > 0){
                $('.dataTables_empty').remove()
                response.alunos.forEach(function (aluno){
                    n += 1
                    if(n % 2 == 0)
                        class_odd = 'even'
                    else
                        class_odd = 'odd'
                    rw = '<tr role="row" class='+ class_odd +'>'+
                            '<td><img src="'+ aluno.foto + '" style="width:75px"/></td>'+
                            '<td>'+ aluno.nome +'</td>' +
                            '<td>'+ aluno.status +'</td>'+
                            '<td> <button '+ ( aulaAtivo ? '' : 'disabled' ) +' data-aulaaluno="'+ aluno.id +'" class="alterar">Alterar</button> <td>'+
                        '<tr>'
                    $('#table-body').append(rw)
                })
            }
            else {
                rw = '<tr><td valign="top" colspan="4" class="dataTables_empty">No data available in table</td></tr>'
                $('#table-body').append(rw)
            }
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
            if (aulaAtivo){
                $('.alterar').on('click', function(){
                    id = $(this).data('aulaaluno')
                    url = 'http://localhost:8000/aulas/change-status-aula-aluno/'+ $('#aulaid').data('aulaid') +'/'+ id
                    $.ajax({
                        url: url,
                        processData: false,
                        contentType: false,
                        type: "POST",
                        data: {},
                        headers: { "X-CSRFToken": getCookie("csrftoken") },
                        cache: false,
                        success: function(response) {
                            // $('#buttons').empty()
                            // $('#buttons').append(response.button)
                        },
                        complete: function(response) {
                            $('body').css('cursor', 'auto');
                        }
                    })
                })
            }
        }
    });
}

var getButton = function (){
    link = 'http://localhost:8000/aulas/status-aula/' + $('#aulaid').data('aulaid')
    $.ajax({
        url: link,
        cache: false,
        success: function(response) {
            $('#buttons').empty()
            $('#buttons').append(response.button)
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });
}