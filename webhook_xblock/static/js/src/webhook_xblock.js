/* Javascript for WebhookXblock. */
function WebhookXblock(runtime, element) {
    var frequency = document.getElementById('webhook_xblock_frequency').value;
    var button_text = document.getElementById('webhook_xblock_button_text').value;
    var studio_mode = document.getElementById('webhook_xblock_studio_mode').value;
    var handlerUrl = runtime.handlerUrl(element, 'send_payload');

    function notifyStudent(result) {
        alert('The information has been sent');
    }

    function checkFrequency() {
        if (frequency == 'sent-by-student'){
            var div = document.getElementById('webhook-xblock-center-button');
            var button = document.createElement('button');
            button.type = 'button';
            button.innerHTML = button_text;
            button.className = 'btn-styled';

            if (studio_mode == 'True'){
                button.disabled = true;
                button.title = 'The payload cannot be sent when running from Studio mode';
            }
            
            button.onclick = function() {
                $.ajax({
                    type: "POST",
                    url: handlerUrl,
                    data: JSON.stringify({'send_payload': 'True'}),
                    success: notifyStudent
                });
            };


            div.appendChild(button);
        }
        else{
            $(function ($) {
                $.ajax({
                    type: "POST",
                    url: handlerUrl,
                    data: JSON.stringify({checkpoint: true}),
                    success: function(result) {
                        runtime.notify('save', {state: 'end'});
                    }
                });
            });
        }
    }

    window.onload = checkFrequency();

}

