var app = angular.module("visualNetx", ['angularSpinner']);

app.controller("netCtrl", function($scope, $http, usSpinnerService) {
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
      }else{
        $('#error').text("You have an error!");
      }

      //stop spinner and enable input and button
      usSpinnerService.stop('spinner-1');
      $("#txtUserAction").prop("disabled",false);
      $("#btnSubmit").prop("disabled",false);
    });
  });
});
