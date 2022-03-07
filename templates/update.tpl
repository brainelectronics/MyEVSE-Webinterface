<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="Update system">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>Update system</title>
  <link href="bootstrap.min.css" rel="stylesheet">
  <style type="text/css">
    .overlay{position:fixed;top:0;left:0;right:0;bottom:0;background-color:gray;color:#fff;opacity:1;transition:.5s;visibility:visible}
    .overlay.hidden{opacity:0;visibility:hidden}
    .loader{position:absolute;left:50%;top:50%;z-index:1;width:120px;height:120px;margin:-76px 0 0 -76px;border:16px solid #f3f3f3;border-radius:50%;border-top:16px solid #3498db;-webkit-animation:spin 2s linear infinite;animation:spin 2s linear infinite}
    @-webkit-keyframes spin{0%{-webkit-transform:rotate(0)}100%{-webkit-transform:rotate(360deg)}
    }@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
  </style>
  <style type="text/css">
    .list-group{width:auto;max-width:460px;margin:4rem auto}
    .list-group-item-check{position:absolute;clip:rect(0,0,0,0);pointer-events:none}
    .list-group-item-check:hover+.list-group-item{background-color:var(--bs-light)}
    .list-group-item-check:checked+.list-group-item{color:#fff;background-color:var(--bs-blue)}
    .list-group-item-check:disabled+.list-group-item,.list-group-item-check[disabled]+.list-group-item{pointer-events:none;filter:none;opacity:.5}
  </style>
  <style type="text/css">
    body {padding:50px 80px;}
  </style>
  <style>
    /*modal style*/
    .cmodal {display: none;position: fixed;z-index: 1;padding-top: 100px;left: 0;top: 0;width: 100%;height: 100%;overflow: auto;background-color: rgb(0,0,0);background-color: rgba(0,0,0,0.4);}
    .cmodal-content {position: relative;background-color: #fefefe;margin: auto;padding: 0;border: 1px solid #888;width: 200px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);-webkit-animation-name: animatetop;-webkit-animation-duration: 0.4s;animation-name: animatetop;animation-duration: 0.4s}
    @-webkit-keyframes animatetop {from {top:-300px; opacity:0}to {top:0; opacity:1}}
    @keyframes animatetop {from {top:-300px; opacity:0}to {top:0; opacity:1}}
    .close {float: right;font-size: 28px;font-weight: bold;}
    .close:hover,
    .close:focus {color: blue;text-decoration: none;cursor: pointer;}
    .cmodal-header {padding: 2px 16px;}
    .cmodal-body {padding: 2px 16px;}
    .cmodal-footer {padding: 2px 16px;}
  </style>
</head>
<body>
  <div id="overlay" class="overlay">
    <div id="loader" class="loader"></div>
  </div>
  <div style="display:none;" id="myDiv" class="animate-bottom">
    <div class="d-flex flex-column min-vh-100 justify-content-center align-items-center">
    <h4>Update system</h4>
      <p id="demo"></p>
      <form action="perform_system_update" method="post" id="perform_system_update_form">
        <div class="list-group">
          <button type="submit" id="update_button" value="update" class="btn btn-lg btn-primary list-group-item active">Update</button>
          <form>
            <input type="button" id="back_button" class="btn btn-lg btn-warning list-group-item" onclick="window.location.href = '/';" value="Go Back"/>
          </form>
        </div>
      </form>
    </div>
  </div>
  <div id="updateModal" class="cmodal">
    <div class="cmodal-content">
      <div class="cmodal-header">
        <span class="close" id="modal_close_btn">&times;</span>
        <h2>System update in progress...</h2>
      </div>
      <div class="cmodal-body">
        <div id="progressbar" class="progressbar">
          <label for="file">Update progress:</label>
          <progress id="update_progressbar" value="0" max="200"> 0 </progress>
        </div>
      </div>
      <div class="cmodal-footer">
        <button type="button" id="close_button" class="btn btn-secondary" data-dismiss="modal" disabled>Close</button>
        <button type="button" id="reboot_button" class="btn btn-primary" onclick="trigger_reboot()" disabled>Reboot</button>
      </div>
    </div>
  </div>
  <script>
    var update_progress_value = 0;
    var refreshProgressbarId = 0;
    var updateModal = document.getElementById("updateModal");
    var modal_close_btn = document.getElementById("modal_close_btn");
    window.onload = function(e) {
      setTimeout(showPage, 1000);
    };
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    document.getElementById("perform_system_update_form").onsubmit = function(e) {
      // do not redirect somewhere
      e.preventDefault();
      window.onbeforeunload = null;
      var confirm_result = confirm("Are you sure you want to update the system?");
      if (confirm_result) {
        updateModal.style.display = "block";
        modal_close_btn.style.display = "none";
        document.getElementById("update_button").disabled = true;
        document.getElementById("update_button").style.display = "none";
        document.getElementById("back_button").disabled = true;
        refreshProgressbarId = setInterval(update_progressbar_value, 1000);
        start_update();
      }
      return confirm_result;
    };
    function start_update() {
      var xmlhttp = new XMLHttpRequest();
      var url = '/perform_system_update';
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var data = JSON.parse(this.responseText);
          if (data.success && refreshProgressbarId != 0) {
            clearInterval(refreshProgressbarId);
            document.getElementById("update_progressbar").value = 200;
            document.getElementById("reboot_button").disabled = false;
            document.getElementById("close_button").disabled = false;
            modal_close_btn.style.display = "block";
          }
          document.getElementById("demo").innerHTML = this.responseText;
        }
      }
      xmlhttp.open('POST', url, true);
      var data = JSON.stringify({"start_update": true});
      xmlhttp.send(data);
    };
    function update_progressbar_value() {
      update_progress_value++;
      document.getElementById("update_progressbar").value = update_progress_value;
    };
    function trigger_reboot() {
      var xmlhttp = new XMLHttpRequest();
      var url = '/perform_reboot_system';
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("demo").innerHTML = "Reboot triggered";
        }
      }
      xmlhttp.open('POST', url, true);
      var data = JSON.stringify({"reboot": true});
      xmlhttp.send(data);
      updateModal.style.display = "none";
      document.getElementById("update_button").disabled = true;
      document.getElementById("update_button").style.display = "none";
      document.getElementById("back_button").disabled = true;
    };
    // When the user clicks on <span> (x), close the modal
    modal_close_btn.onclick = function() {
      updateModal.style.display = "none";
    }
  </script>
</body>
</html>