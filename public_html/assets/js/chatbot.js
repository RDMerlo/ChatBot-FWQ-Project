$(function () {

    function message_bot_form(msg){
        let now = new Date();
        let year = now.getFullYear();
        let datetime = now.getHours() + ":" + (now.getMinutes()<10?'0':'') + now.getMinutes();
        return  '<div class="row">' +
                '   <div class="media media-chat">' +
                '       <img class="avatar" ' +
                '            src="https://img.icons8.com/office/40/null/chatbot.png" ' +
                '            alt="...">' +
                '       <div class="media-body answer-bot">' +
                '           <div class="answer-bubble">' + msg + '</div>' +
                '           <p class="meta"><time datetime="' + year + '">' + datetime + '</time></p>' +
                '       </div>' +
                '   </div>' +
                '</div>';
    }

    function message_user_form(msg){
        let now = new Date();
        let year = now.getFullYear();
        let datetime = now.getHours() + ":" + (now.getMinutes()<10?'0':'') + now.getMinutes();
        return '<div class="row">' +
                    '<div class="media media-chat media-chat-reverse">' +
                        '<div class="media-body">' +
                            '<div class="answer-bubble">' + msg + '</div>' +
                            '<p class="meta"><time datetime="' + year + '">' + datetime + '</time></p>' +
                        '</div>' +
                    '</div>' +
               '</div>';
    }

    function message_form(msg){
        return '<div class="row chat-message">' +
                    '<div class="media media-load-answer">' +
                        '<div class="media-body answer-bot">' +
                            '<p>' + msg + '</p>' +
                        '</div>' +
                    '</div>' +
                '</div>';
    }

    function chatbot(){

        $('.chat-message').detach();
        let quest = $('#quest_text').val();
        $('#quest_text').val("");

        let module_dataset = $('#module_dataset').val();

        // alert(module_dataset);

        if (quest !== "" && module_dataset !== "") {
            $('#quest_text').attr('disabled', 'disabled');
            $('#send_question_click').attr('disabled', 'disabled');

            $('.chat-dialog').append(message_user_form(quest));
            $('.chat-dialog').append(message_form("Пожалуйста, подождите..."));

            $.ajax({
                url: "/cgi-bin/chatbot.py",
                type: "get",
                datatype: "json",
                data: {'quest_text': quest, 'module_dataset': module_dataset},
                error: function (jqXHR, exception) {
                    var msg = '';
                    if (jqXHR.status === 0) {
                        msg = 'Not connect.\n Verify Network.';
                    } else if (jqXHR.status == 404) {
                        msg = 'Requested page not found. [404]';
                    } else if (jqXHR.status == 500) {
                        msg = 'Internal Server Error [500].';
                    } else if (exception === 'parsererror') {
                        msg = 'Requested JSON parse failed.';
                    } else if (exception === 'timeout') {
                        msg = 'Time out error.';
                    } else if (exception === 'abort') {
                        msg = 'Ajax request aborted.';
                    } else {
                        msg = 'Uncaught Error.\n' + jqXHR.responseText;
                    }
                    console.log(msg);

                    $('.chat-message').detach();
                    $('.chat-dialog').append(message_form("Извините, произошла ошибка."));

                    setTimeout(function() {
                            $('#quest_text').removeAttr('disabled');
                            $('#send_question_click').removeAttr('disabled');
                        }, 3000);
                },
                success: function (response) {
                    console.log(response)
                    $('.chat-message').detach();
                    if (response.success) {

                        $('.chat-dialog').append(message_bot_form(response.message));

                        setTimeout(function() {
                            $('#quest_text').removeAttr('disabled');
                            $('#send_question_click').removeAttr('disabled');
                        }, 3000);
                    } else {
                        if (response.message !== ""){
                            $('.chat-dialog').append(message_bot_form(response.message));
                        } else {
                            $('.chat-dialog').append(message_form("Не удалось получить ответ."));
                        }

                        setTimeout(function() {
                            $('#quest_text').removeAttr('disabled');
                            $('#send_question_click').removeAttr('disabled');
                        }, 1000);
                    }
                },
            });

            $('#chat-content').animate(
            {
                    scrollTop: $('#chat-content').get(0).scrollHeight+300
                 }, 1000);
        }
    }

    $(document).on("keypress", "#quest_text", function(e){
        if (e.key === "Enter" || e.keyCode === 13) {
             chatbot();
             var lenValue = $('#quest_text').val().length;
             var maxLenValue = $('#quest_text').attr('maxlength');
             $('.number-characters-entered').text(lenValue + '/' + maxLenValue);
        }
    });

    $('#send_question_click').click(function () {
        chatbot();
        var lenValue = $('#quest_text').val().length;
        var maxLenValue = $('#quest_text').attr('maxlength');
        $('.number-characters-entered').text(lenValue + '/' + maxLenValue);
    });

    $('#quest_text').on('input', function () {
        var lenValue = $('#quest_text').val().length;
        var maxLenValue = $('#quest_text').attr('maxlength');
        $('.number-characters-entered').text(lenValue + '/' + maxLenValue);
    });
});

