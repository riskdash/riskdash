d3.text('/static/data/credit_gap.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		
		var pattern = /(\d{4})(\d{2})(\d{2})/;
		return [new Date(d.date.replace(pattern,'$1-$2-$3')), +d.noise];

	});

	// Create the chart
	$('#container').highcharts('StockChart', {


		rangeSelector : {
			selected : 5,
			inputEnabled: $('#container').width() > 480
		},

		series : [{
			name : 'Noise',
			data : data,
			tooltip: {
				valueDecimals: 4
			}
		}]
	});
});
