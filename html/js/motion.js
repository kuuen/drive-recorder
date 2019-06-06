
var motionStopUrl = '' 

function init() {

//  var json = JSON.stringify({'text': 'test'});
  
  $.ajax({
    type: 'POST',
    url: 'cgi-bin/motion-page-init.py',
    contentType: 'application/json',
//    data: json,
    success: function(data) {
      console.log(data);
      console.log(data.screenurl);

      $("#frameScreen").attr("src", data.screenurl);

      motionStopUrl = data.motionurl + '/0/action/quit'

    }
  });
  
  return false;
}

