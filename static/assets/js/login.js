$(document).ready(function() {
    $('#login-btn').on('click', function () {
        data = {
            'username': $('#input-usuario').val(),
            'password': $('#input-senha').val()
        }
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: '',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            type: "POST",
            complete: function(response) {
                if(response.status == 200)
                    window.location = "/aulas/"
                else
                    window.alert("Usuário ou senha incorretos!");
            }
        });
    });


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
(function(){
    /* 
    *
    *   This function is used to login with the enter key.
    *   When the enter key is pressed an event click is added on class .login
    * 
    */
    document.querySelector('body').addEventListener('keypress',function(e){
        if((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)){
                document.querySelector('#login-btn').click();
            }
        })
})();
