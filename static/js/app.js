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
      clearGraph();
      if(response.data !="error"){
        // create a new graph using method from graph.js
        createGraph(response.data);
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

  $scope.uploadFiles = function(file, errFiles) {
    $scope.f = file;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
        file.upload = Upload.upload({
            url: 'uploadGraph',
            data: {file: file}
        });

        file.upload.then(function (response) {
            $timeout(function () {
                file.result = response.data;
                console.log(file.result);
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
