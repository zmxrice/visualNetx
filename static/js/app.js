var app = angular.module("visualNetx", ['angularSpinner', 'ngFileUpload']);

app.controller("netCtrl", function($scope, $http, usSpinnerService, Upload, $timeout) {
  $('#btnSubmit').click(function(){
    //add a spinner and disable button and text input
    usSpinnerService.spin('spinner-1');
    $("#txtUserAction").prop("disabled",true);
    $("#btnSubmit").prop("disabled",true);

    // make a request to generate graph
    $http({
      method: 'POST',
      url: 'generateGraph',
      headers: {'Content-Type': 'application/json'},
      data: { 'userAction': $scope.action }
    }).then(function(response) {
      // clear the graph using method from graph.js
      clearGraph('#svgGen');
      if(response.data !="error"){
        // create a new graph using method from graph.js
        createGraph(response.data, '#svgGen');
        $('#error').text("");
        $('#divExport').css('visibility', 'visible');
      }else{
        $('#error').text(" You have an error!");
        $('#divExport').css('visibility', 'hidden');
      }

      //stop spinner and enable input and button
      usSpinnerService.stop('spinner-1');
      $("#txtUserAction").prop("disabled",false);
      $("#btnSubmit").prop("disabled",false);
    });
  });

  $('#btnExport').click(function(){
    $http({
      method: 'POST',
      url: 'exportGraph',
      headers: {'Content-Type': 'application/json'},
      data: { 'fmat': $('#selectFmat').val() }
    }).then(function(response) {
      if(response.data !="error"){
        //a neat way to open up a download window
        window.location.assign(response.data);
      }
    });
  });

  $("#btnSaveImg").click(function(){
    var doctype = '<?xml version="1.0" standalone="no"?>'
      + '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">';

    // serialize our SVG XML to a string.
    var source = (new XMLSerializer()).serializeToString(d3.select('svg').node());

    // create a file blob of our SVG.
    var blob = new Blob([ doctype + source], { type: 'image/svg+xml;charset=utf-8' });

    var url = window.URL.createObjectURL(blob);

    // Put the svg into an image tag so that the Canvas element can read it in.
    var img = d3.select('body').append('img')
     .attr('width', 960)
     .attr('height', 600)
     .node();

    img.onload = function(){
      // Now that the image has loaded, put the image into a canvas element.
      var canvas = d3.select('body').append('canvas').node();
      canvas.width = 960;
      canvas.height = 600;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      var a = document.createElement("a");
      var d = new Date();
      a.download = "export_"+d.getTime()+".png";
      a.href = canvas.toDataURL("image/png");
      a.click();
      //remove the temporily created elements
      $(a).remove();
      $(canvas).remove();
    }
    // start loading the image.
    img.src = url;
    $(img).remove();
  });

  $scope.uploadFiles = function(file, errFiles) {
    clearGraph('#svgImp');
    $scope.f = file;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
      //try upload the file to the server, also handles possible errors
      file.upload = Upload.upload({
          url: 'uploadGraph',
          data: {file: file}
      });

      file.upload.then(function (response) {
          $timeout(function () {
            if(response.data !="error"){
              // create a new graph using method from graph.js
              createGraph(response.data, '#svgImp');
            }else{
              console.log("error");
            }
          });
      }, function (response) {
          if (response.status > 0)
              $scope.errorMsg = response.status + ': ' + response.data;
      }, function (evt) {
          file.progress = Math.min(100, parseInt(100.0 *
                                   evt.loaded / evt.total));
      });
    }
  }

});
