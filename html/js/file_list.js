
function init() {

//  $('#content').append("<a href='drive/'>一覧(メニュー削除予定)</a><br/>");
//  $('#content').append("<a href='drive/'>はやてちゃん</a><br/>");
//  $('#content').append("<a href='drive/'>かわいい</a><br/>");

  
  $.ajax({
    type: 'POST',
    url: 'cgi-bin/file_list.py',
    contentType: 'application/json',
//    timeout: 10000000
//    data: json,

  }).then(
    // 1つめは通信成功時のコールバック
    function (data) {
      console.log(data);
      console.log(data.screenurl);

      for(var i in data.list) {
        if (data.list[i].link != 'non link') {
          $('#content').append("<a href='" + data.list[i].link + "'>" + data.list[i].name + "</a>&nbsp;&nbsp;" + data.list[i].storage_location +"<br />")
//          $('#content').append("<video src='" + data.list[i].link + "'></video><br/>")

        } else {
          $('#content').append(data.list[i].name + "<br />")
        }
      }


      $("#frameScreen").attr("src", data.screenurl);
      $('#wait_msg').html('')

    },
    // 2つめは通信失敗時のコールバック
    function (XMLHttpRequest, textStatus, errorThrown) {
      alert("読み込み失敗");
      $('#wait_msg').html('読み込み失敗:' + textStatus)
  });



  return false;
}

/*
$('#btn-camera-top').click(function(){

  var json = JSON.stringify({'move': '1'});

  $.ajax({
    type: 'POST',
    url: 'cgi-bin/motion-camera-move.py',
    contentType: 'application/json',
    data: json

  }).then(
    // 1つめは通信成功時のコールバック
    function (data) {
      $("#results").append(data);
    },
    // 2つめは通信失敗時のコールバック
    function () {
      alert("読み込み失敗");
  });

})

$('#btn-camera-bottom').click(function(){
  var json = JSON.stringify({'move': '2'});

  $.ajax({
    type: 'POST',
    url: 'cgi-bin/motion-camera-move.py',
    contentType: 'application/json',
    data: json
  }).then(
    // 1つめは通信成功時のコールバック
    function (data) {
      $("#results").append(data);
    },
    // 2つめは通信失敗時のコールバック
    function () {
      alert("読み込み失敗");
  });
})

$('#btn-camera-left').click(function(){
  var json = JSON.stringify({'move': '3'});

  $.ajax({
    type: 'POST',
    url: 'cgi-bin/motion-camera-move.py',
    contentType: 'application/json',
    data: json,
    success: function(data) {
      console.log(data);
      console.log(data.result);

      $("#frameScreen").attr("src", data.screenurl);

    }
  });
})

$('#btn-camera-right').click(function(){
  var json = JSON.stringify({'move': '4'});

  $.ajax({
    type: 'POST',
    url: 'cgi-bin/motion-camera-move.py',
    contentType: 'application/json',
    data: json,
    success: function(data) {
      console.log(data);
      console.log(data.result);

      $("#frameScreen").attr("src", data.screenurl);

    }
  });
})
*/

