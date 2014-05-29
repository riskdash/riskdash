$(function() {

  $.getJSON('/pca/data/', function(data) {
    // Create the chart
    $('#chart').highcharts('StockChart', {
      

      rangeSelector : {
        selected : 1,
        inputEnabled: $('#chart').width() > 480
      },

      title : {
        text : 'AAPL Stock Price'
      },
      
      series : [{
        name : 'AAPL',
        date : data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });

});
