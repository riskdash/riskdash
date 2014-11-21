f3_data = [];

$(document).ready(function() {
	d3.text('/static/data/noise_liquidity.csv', function(unparsedData) {
		var data = d3.csv.parse(unparsedData, function(d) {
		var pattern = /(\d{4})(\d{2})(\d{2})/;
		f3_data.push([new Date(d.date.replace(pattern,'$1-$2-$3')), +d.noise]);
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
				data : f3_data,
				tooltip: {
					valueDecimals: 4
				}
			}]
		});
	});
});

