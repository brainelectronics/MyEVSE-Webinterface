{% args req, tcp_port, register_file, setup_checked, client_checked, ap_checked %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="Setup system">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>Setup system</title>
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
  </div>

  <div style="display:none;" id="myDiv" class="animate-bottom">
    <div class="d-flex flex-column min-vh-100 justify-content-center align-items-center">
    <h4>Setup system</h4>
    <div class="list-group list-group-checkable">
      <form action="save_system_config" method="post" id="save_system_config_form">
        <div class="form-group row">
          <label for="tcp_port" class="col-sm-10 col-form-label">ModBus TCP port</label>
          <div class="col-sm-10">
            <input type="number" class="form-control" id="tcp_port" name="TCP_PORT" placeholder="ModBus TCP port" value={{tcp_port}}>
          </div>
        </div>
        <div class="form-group row">
          <label for="register_file" class="col-sm-10 col-form-label">Register file</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="register_file" name="REGISTERS" placeholder="ModBus Registers file" value={{register_file}}>
          </div>
        </div>
        <fieldset class="form-group">
          <div class="row">
            <legend class="col-form-label col-sm-10 pt-0">Connection Mode</legend>
            <div class="col-sm-10">
              <div class="form-check">
                <input class="form-check-input" type="radio" name="CONNECTION_MODE" id="connection_mode_setup" value=0 {{setup_checked}}>
                <label class="form-check-label" for="connection_mode_setup">
                  Setup
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="radio" name="CONNECTION_MODE" id="connection_mode_station" value=1 {{client_checked}}>
                <label class="form-check-label" for="connection_mode_station">
                  Client
                </label>
              </div>
              <div class="form-check disabled">
                <input class="form-check-input" type="radio" name="CONNECTION_MODE" id="connection_mode_ap" value=2 {{ap_checked}}>
                <label class="form-check-label" for="connection_mode_ap">
                  AccessPoint
                </label>
              </div>
            </div>
          </div>
        </fieldset>
        <div class="list-group">
          <button type="submit" id="save" value="Save" class="btn btn-lg btn-primary list-group-item active">Submit</button>
          <form>
            <input type="button" class="btn btn-lg btn-warning list-group-item" onclick="window.location.href = '/';" value="Go Back"/>
          </form>
        </div>
      </form>
    </div>
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
    document.getElementById("save_system_config_form").onsubmit = function(e) {
      // do not redirect somewhere
      e.preventDefault();
      window.onbeforeunload = null;
      var xmlhttp = new XMLHttpRequest();
      var url = '/save_system_config';
      xmlhttp.open('POST', url, true);
      var formData = new FormData(document.getElementById("save_system_config_form"));
      xmlhttp.setRequestHeader("Content-Type", "application/json");
      var data = JSON.stringify(Object.fromEntries(formData));
      xmlhttp.send(data);
      createToast('alert-success', 'Success!', 'Configuration updated', 5000);
      return true;
    };
  </script>
</body>
</html>