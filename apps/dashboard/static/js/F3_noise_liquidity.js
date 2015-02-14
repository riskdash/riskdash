var localSeries = [];

var drawChart = function(name, data, color) {
	var newSeriesData = {
		name: name,
		data: data,
		color: color,
		tooltip: {
			valueDecimals: 4,
		},
	};

	// add data to series array
	localSeries.push(newSeriesData);

	// re-draw graph
	$('#container').highcharts('StockChart', {


		rangeSelector : {
			selected : 5,
			inputEnabled: $('#container').width() > 480
		},

		series : localSeries
	});

};


d3.text('/static/data/F3_noise_liquidity_source.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		
		var pattern = /(\d{4})(\d{2})(\d{2})/;
		return [new Date(d.date.replace(pattern,'$1-$2-$3')), +d.noise];

	});

	// Create the chart
	drawChart('Noise (source)', data, '#2f7ed8');
});

d3.text('/static/data/F3_noise_liquidity_calc.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		
		var pattern = /(\d{4})(\d{2})(\d{2})/;
		return [new Date(d.quoteDate.replace(pattern,'$1-$2-$3')), +d.noise];

	});

	// Create the chart
	drawChart('Noise (calc)', data, '#910000');
});

