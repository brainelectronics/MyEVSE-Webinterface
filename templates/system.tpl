{% args req, content %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="System Info">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>System Info</title>
  <link href="bootstrap.min.css" rel="stylesheet">
  <!--
  <link href="style.css" rel="stylesheet">
  <link href="bootstrap.min.css" rel="stylesheet">
  <link href="list-groups.css" rel="stylesheet">
  -->
  <style type="text/css">
    .overlay{position:fixed;top:0;left:0;right:0;bottom:0;background-color:gray;color:#fff;opacity:1;transition:.5s;visibility:visible}
    .overlay.hidden{opacity:0;visibility:hidden}
    .loader{position:absolute;left:50%;top:50%;z-index:1;width:120px;height:120px;margin:-76px 0 0 -76px;border:16px solid #f3f3f3;border-radius:50%;border-top:16px solid #3498db;-webkit-animation:spin 2s linear infinite;animation:spin 2s linear infinite}
    @-webkit-keyframes spin{0%{-webkit-transform:rotate(0)}100%{-webkit-transform:rotate(360deg)}
    }@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
  </style>
  <style type="text/css">
    body {padding:50px 80px;}
  </style>
</head>
<body>
  <div id="overlay" class="overlay">
    <div id="loader" class="loader"></div>
  </div>

  <div style="display:none;" id="myDiv" class="animate-bottom">
    <div class="d-flex flex-column min-vh-100 justify-content-center align-items-center">
    <h4>Latest System Info</h4>
    <div>
      Data age:
      <label id="data_age_minutes">00</label>:<label id="data_age_seconds">00</label> sec
    </div>
    <div name="system_info" id="system_info">
      {{ content }}
    </div>
    <form>
      <input type="button" class="btn btn-lg btn-warning list-group-item" onclick="window.location.href = '/';" value="Go Back"/>
    </form>
    </div>
  </div>

  <script>
    var minutesLabel = document.getElementById("data_age_minutes");
    var secondsLabel = document.getElementById("data_age_seconds");
    var totalSeconds = 0;

    window.onload = function(e) {
      setTimeout(showPage, 1000);
      setInterval(setDataAgeTime, 1000);
    };
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      //document.getElementById("rcorners3").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    function setDataAgeTime() {
      ++totalSeconds;
      secondsLabel.innerHTML = pad(totalSeconds % 60);
      minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
    }
    function pad(val) {
      var valString = val + "";
      if (valString.length < 2) {
        return "0" + valString;
      } else {
        return valString;
      }
    }
  </script>
</body>
</html>