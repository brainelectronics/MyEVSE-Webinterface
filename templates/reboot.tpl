<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="Reboot system">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>Reboot system</title>
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

  <script>
    window.onload = function(e) {
      setTimeout(showPage, 1000);
    };
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      //document.getElementById("rcorners3").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    document.getElementById("perform_reboot_system_form").onsubmit = function(e) {
      window.onbeforeunload = null;
      return confirm("Are you sure you want to reboot?");
    };
  </script>
</body>
</html>