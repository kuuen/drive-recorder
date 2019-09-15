
function init() {

  $('#content').append("<a href='drive/'>一覧(メニュー削除予定)</a><br/>");
  $('#content').append("<a href='drive/'>はやてちゃん</a><br/>");
  $('#content').append("<a href='drive/'>かわいい</a><br/>");

  
  $.ajax({
    type: 'POST',
    url: 'cgi-bin/local_file_list.py',
    contentType: 'application/json',
//    data: json,

  }).then(
    // 1つめは通信成功時のコールバック
    function (data) {
      console.log(data);
      console.log(data.screenurl);

      for(var i in data.list) {
        $('#content').append(data.list[i].name + "<br />")
      }


      $("#frameScreen").attr("src", data.screenurl);

    },
    // 2つめは通信失敗時のコールバック
    function (XMLHttpRequest, textStatus, errorThrown) {
      alert("読み込み失敗");
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

