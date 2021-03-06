
/* TODO: create choosing data source dialogs */
var jsonTrackerData;
function getTrackerData() {
    $.ajax({
        method: 'GET',
        url: '/get_tracker_chg_info/' + $("select#measure").val(),
        dataType: 'json',
        contentType: "application/json",
        success: function (resp) {
            jsonTrackerData = resp;
            // Load the Visualization API and the corechart package.
            google.charts.load('current', {'packages': ['corechart']});
            // Set a callback to run when the Google Visualization API is loaded.
            google.charts.setOnLoadCallback(drawTrackerChgChart);
        }
    });
}
function drawTrackerChgChart() {
    // Create the data table.
    // var data = new google.visualization.DataTable();
    // data.addColumn('string', 'Abc');
    // data.addColumn('number', 'Temp2');
    // data.addRows(jsonData);
    var data = google.visualization.arrayToDataTable(jsonTrackerData);

    // Set chart options
    var options = {'title':'Tracker Charge Info',
                   'width':1000,
                   'height':400};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('tracker_chart_div'));
    chart.draw(data, options);
}
$(document).ready(function () {

  $("select#measure").change(function() {
      getData();
      getTrackerData();
  });

  var jsonData;
  function getData(update) {
      var url;
      // TODO: decide how to define if it is a NEW measure !!
      // Decided ! Reset checkbox !!!
      var isNewMeasure = 0; // 0 - is default
      if ($("#is_new_measure_check").is(':checked')) {
        isNewMeasure = 1;
      } else {
        isNewMeasure = 0;
      }
      if (update) {
        url = '/update_measures/' + $("select#measure").val() + '/' + isNewMeasure;
      } else {
        url = '/get_measures/' + $("select#measure").val();
      }
      $.ajax({
        method: 'GET',
        url: url,
        dataType: 'json',
        contentType:"application/json",
        success: function(resp) {
          jsonData = resp;
          // Load the Visualization API and the corechart package.
          google.charts.load('current', {'packages':['corechart']});
          // Set a callback to run when the Google Visualization API is loaded.
          google.charts.setOnLoadCallback(drawChart);
          // reset checkbox here, because new measure ID needed only one time for updating measures, not every!!
          $("#is_new_measure_check").attr('checked', false);
          // $("#is_new_measure_check").prop('checked', false);
        }
      });
  }
  getData();

  // Callback that creates and populates a data table,
  // instantiates the pie chart, passes in the data and
  // draws it.
  function drawChart() {
    // Create the data table.
    // var data = new google.visualization.DataTable();
    // data.addColumn('string', 'Abc');
    // data.addColumn('number', 'Temp2');
    // data.addRows(jsonData);
    var data = google.visualization.arrayToDataTable(jsonData);

    // Set chart options
    var options = {'title':'Moto Data Visualizer',
                   'width':1200,
                   'height':700};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('main_chart_div'));
    chart.draw(data, options);
  }
  var t = setInterval(function() {
    console.log("Updating graphs...");
    getData(true);
  }, 12000);
});