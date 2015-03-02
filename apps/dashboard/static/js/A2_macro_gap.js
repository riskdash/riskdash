min_width = '400px'

// look at https://gist.github.com/femto113/1784503 to find out how to transpose data arrays so that we can parse a csv with multiple countries' data

d3.text('/static/data/A2_UScreditgaps.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.time, +d.data];
	});

	// Create the chart
	$('#credit_gap').highcharts({
		title: {
			text: 'Credit/GDP Gap',
		},

		legend: {
			enabled: false, // enable it when there are more lines
		},

		series : [{
			name : 'US Credit Gap',
			data : data,
			tooltip: {
				valueDecimals: 2
			}
		}]
	});

});

d3.text('/static/data/A2_USpropertygaps.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.time, +d.data];
	});

	// Create the chart
	$('#property_gap').highcharts({
		title: {
			text: 'Real Property Price Gap',
		},

		legend: {
			enabled: false, // enable it when there are more lines
		},

		series : [{
			name : 'Property Gap',
			data : data,
			tooltip: {
				valueDecimals: 2
			}
		}]
	});
});

d3.text('/static/data/A2_USmarketgaps.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.time, +d.data];
	});

	// Create the chart
	$('#market_gap').highcharts({
		title: {
			text: 'Market (Equity) Gap',
		},

		legend: {
			enabled: false, // enable it when there are more lines
		},

		series : [{
			name : 'Market Gap',
			data : data,
			tooltip: {
				valueDecimals: 2
			}
		}]
	});
});

// set all the graphs to minimum width
d3.select('#container').selectAll('span').style('min-width',min_width).style('float','left');
