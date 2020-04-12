$(document).ready(function() {
    getData()
});

setInterval(function() {
    getData()
    getButton()
}, 1000)

var getData = function (){
    var table = $('#alunos').DataTable()
    link = 'http://localhost:8000/aulas/get-alunos/' + $('#aulaid').data('aulaid')
    $.ajax({
        url: link,
        cache: false,
        success: function(response) {
            $('#table-body').empty()
            n = 0
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
                        '<tr>'
                    $('#table-body').append(rw)
                })
            }
            else {
                rw = '<tr><td valign="top" colspan="3" class="dataTables_empty">No data available in table</td></tr>'
                $('#table-body').append(rw)
            }
        },
        complete: function(response) {
            $('body').css('cursor', 'auto');
        }
    });
}

var getButton = function (){
    var table = $('#alunos').DataTable()
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