min_width = '400px'

// look at https://gist.github.com/femto113/1784503 to find out how to transpose data arrays so that we can parse a csv with multiple countries' data

d3.text('/static/data/credit_gap.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.year, +d.credit_gap];
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
			name : 'Credit Gap',
			data : data,
			tooltip: {
				valueDecimals: 2
			}
		}]
	});

});

d3.text('/static/data/property_gap.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.year, +d.property_gap];
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

d3.text('/static/data/market_gap.csv', function(unparsedData) {
	var data = d3.csv.parse(unparsedData, function(d) {
		return [+d.year, +d.market_gap];
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
