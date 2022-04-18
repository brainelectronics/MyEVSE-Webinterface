<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="Reboot system">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>Reboot system</title>
  <link href="bootstrap.min.css" rel="stylesheet">
  <script type="text/javascript" src="toast.js"></script>
  <style type="text/css">
    .overlay{position:fixed;top:0;left:0;right:0;bottom:0;background-color:gray;color:#fff;opacity:1;transition:.5s;visibility:visible}
    .overlay.hidden{opacity:0;visibility:hidden}
    .loader{position:absolute;left:50%;top:50%;z-index:1;width:120px;height:120px;margin:-76px 0 0 -76px;border:16px solid #f3f3f3;border-radius:50%;border-top:16px solid #3498db;-webkit-animation:spin 2s linear infinite;animation:spin 2s linear infinite}
    @-webkit-keyframes spin{0%{-webkit-transform:rotate(0)}100%{-webkit-transform:rotate(360deg)}
    }@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
  </style>
  <style type="text/css">
    .list-group{width:auto;max-width:460px;margin:4rem auto}
    .form-check-input:checked+.form-checked-content{opacity:.5}
    .form-check-input-placeholder{pointer-events:none;border-style:dashed}[contenteditable]:focus{outline:0}
    .list-group-checkable{display:grid;gap:.5rem;border:0}
    .list-group-checkable .list-group-item{cursor:pointer;border-radius:.5rem}
    .list-group-item-check{position:absolute;clip:rect(0,0,0,0);pointer-events:none}
    .list-group-item-check:hover+.list-group-item{background-color:var(--bs-light)}
    .list-group-item-check:checked+.list-group-item{color:#fff;background-color:var(--bs-blue)}
    .list-group-item-check:disabled+.list-group-item,.list-group-item-check[disabled]+.list-group-item{pointer-events:none;filter:none;opacity:.5}
  </style>
  <style type="text/css">
    body {padding:50px 80px;}
  </style>
</head>
<body>
  <div id="overlay" class="overlay">
    <div id="loader" class="loader"></div>
    <canvas id="circularLoader" width="200" height="200" style="position:absolute;left:50%;top:50%;z-index:1;width:120px;height:120px;margin:-76px 0 0 -76px;"></canvas>
  </div>

  <div style="display:none;" id="myDiv" class="animate-bottom">
    <div class="d-flex flex-column min-vh-100 justify-content-center align-items-center">
    <h4>Reboot system</h4>
      <form action="perform_reboot_system" method="post" id="perform_reboot_system_form">
        <div class="list-group">
          <button type="submit" id="save" value="Save" class="btn btn-lg btn-primary list-group-item active">Reboot</button>
          <form>
            <input type="button" class="btn btn-lg btn-warning list-group-item" onclick="window.location.href = '/';" value="Go Back"/>
          </form>
        </div>
      </form>
    </div>
  </div>
  <div id="alert_container" style="position: fixed;z-index: 9999;top: 20px;right: 20px;"></div>

  <script>
    window.onload = function(e) {
      setTimeout(showPage, 1000);
    };
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    document.getElementById("perform_reboot_system_form").onsubmit = function(e) {
      var res = confirm("Rebooting the system?");
      if (res) {
        var xmlhttp = new XMLHttpRequest();
        var url = '/perform_reboot_system';
        xmlhttp.open('POST', url, true);
        var data = JSON.stringify({"reboot": true});
        xmlhttp.send(data);
        createToast('alert-success', 'Success!', 'System is rebooting...', 45000);
        startProgress(1, 450);
      }
      return res;
    };
    var ctx = document.getElementById('circularLoader').getContext('2d');
    var diff,sim,val=0,start=4.72,cw=ctx.canvas.width,ch=ctx.canvas.height;
    function progressCircle(inc) {
      val += inc;
      if(val < 0){val = 0};
      if(val > 100){val = 100};
      diff = ((val / 100) * Math.PI*2*10).toFixed(2);
      ctx.clearRect(0, 0, cw, ch);
      ctx.lineWidth = 17;
      ctx.fillStyle = '#f3f3f3';
      ctx.strokeStyle = '#f3f3f3';
      ctx.textAlign = "center";
      ctx.font = "28px monospace";
      ctx.fillText(val+'%', cw*.52, ch*.5+5, cw+12);
      ctx.beginPath();
      ctx.arc(100, 100, 75, start, diff/10+start, false);
      ctx.stroke();
      if(val >= 100){
        clearTimeout(sim);
        window.location='/';
      }
    }
    function startProgress(inc, t){
      document.getElementById("overlay").style.display = "block";
      document.getElementById("myDiv").style.display = "none";
      progressCircle(inc);
      sim = setInterval(function() {progressCircle(inc)}, t);
    }
  </script>
</body>
</html>