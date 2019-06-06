var stopMotionUrl = '';

function init() {

//  var json = JSON.stringify({'text': 'test'});
  
  $.ajax({
    type: 'POST',
    url: 'cgi-bin/status.py',
    contentType: 'application/json',
//    data: json,
    success: function(data) {
      console.log(data);
      console.log(data.text);
      $('#result').empty();
      $('#result').val(data.msg);
      if (data.r_recorder == 1) {
         $("#btn-start-recorder").prop("disabled", true);
         $("#btn-stop-recorder").prop("disabled", false);
      } else {
         $("#btn-start-recorder").prop("disabled", false);
         $("#btn-stop-recorder").prop("disabled", true);
      }

      if (data.r_motion == 1) {
         $("#btn-start-motion").prop("disabled", true);
         $("#btn-stop-motion").prop("disabled", false);
         $("#btn-motion-screen").prop("disabled", false);
      } else {
         $("#btn-start-motion").prop("disabled", false);
         $("#btn-stop-motion").prop("disabled", true);
         $("#btn-motion-screen").prop("disabled", true);
      }

      stopMotionUrl = data.motion_stop_link

//      $("#btn-test").attr('disabled', true);
//      $("#btn-test").prop("disabled", true);

      $("#btn-stop-motion").click(function() {
         window.location.href = stopMotionUrl;
      });


    }
  });
  
  return false;
}

