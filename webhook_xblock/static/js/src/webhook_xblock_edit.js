/* Called when rendering the studio edit page */
function WebhookXblockEditBlock(runtime, element) {
  function setDefaultValues() {
    var sendCourseGrade = $(element).find('input[name=webhook_xblock_send_course_grade]').val();
    var sendAsync = $(element).find('input[name=webhook_xblock_send_async]').val();
    var extraInfo = $(element).find('input[name=webhook_xblock_extra_info_value]').val();
    var frequency = $(element).find('input[name=webhook_xblock_frequency_value]').val();
    var componentText = $(element).find('input[name=webhook_xblock_component_text_value]').val();
  
    $(element).find('select[name=webhook_xblock_frequency]').val(frequency);
    document.getElementById('webhook_xblock_extra_info').value = (!extraInfo) ? '{}' : extraInfo;

    if (!componentText){
      document.getElementById('webhook_xblock_component_text').placeholder = "This is<br>a test paragraph<br>with line breaks."; 
    }
    else{
      document.getElementById('webhook_xblock_component_text').value = componentText;
    }
    if (sendCourseGrade == 'True'){
      $(element).find('input[name=webhook_xblock_send_course_grade]').prop('checked', true);
    }
    if (sendAsync == 'True'){
      $(element).find('input[name=webhook_xblock_send_async]').prop('checked', true);
    }
  }
  window.onload = setDefaultValues();

  $(element).find('.save-button').bind('click', function() {
    var name = $(element).find('input[name=webhook_xblock_name]').val()
    var webhook_url = $(element).find('input[name=webhook_xblock_url]').val()

    if (!name || !webhook_url){
      alert("One or more required fields are missing")
    }
    else{
      var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
      var data = {
        name: name,
        webhook_url: webhook_url,
        component_text: $(element).find('textarea[name=webhook_xblock_component_text]').val(),
        button_text: $(element).find('input[name=webhook_xblock_button_text]').val(),
        frequency: $(element).find('select[name=webhook_xblock_frequency]').val(),
        extra_info: $(element).find('textarea[name=webhook_xblock_extra_info]').val(),
        send_course_grade: $(element).find('input[name=webhook_xblock_send_course_grade]').prop('checked'),
        send_async: $(element).find('input[name=webhook_xblock_send_async]').prop('checked')
      };
      runtime.notify('save', {state: 'start'});
      $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
        runtime.notify('save', {state: 'end'});
      });
    }
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
