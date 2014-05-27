var months = ["12/1996", "01/1997", "02/1997", "03/1997", "04/1997", "05/1997", "06/1997", "07/1997", "08/1997",
"09/1997", "10/1997", "11/1997", "12/1997", "01/1998", "02/1998", "03/1998", "04/1998", "05/1998", "06/1998",
"07/1998", "08/1998", "09/1998", "10/1998", "11/1998", "12/1998","01/1999", "02/1999", "03/1999", "04/1999",
"05/1999", "06/1999", "07/1999", "08/1999", "09/1999", "10/1999", "11/1999", "12/1999", "01/2000", "02/2000",
"03/2000", "04/2000", "05/2000", "06/2000", "07/2000", "08/2000", "09/2000", "10/2000", "11/2000", "12/2000",
"01/2001", "02/2001", "03/2001", "04/2001", "05/2001", "06/2001", "07/2001", "08/2001", "09/2001", "10/2001",
"11/2001", "12/2001", "01/2002", "02/2002", "03/2002", "04/2002", "05/2002", "06/2002", "07/2002", "08/2002",
"09/2002", "10/2002", "11/2002", "12/2002", "01/2003", "02/2003", "03/2003", "04/2003", "05/2003", "06/2003",
"07/2003", "08/2003", "09/2003", "10/2003", "11/2003", "12/2003", "01/2004", "02/2004", "03/2004", "04/2004",
"05/2004", "06/2004", "07/2004", "08/2004", "09/2004", "10/2004", "11/2004", "12/2004", "01/2005", "02/2005",
"03/2005", "04/2005", "05/2005", "06/2005", "07/2005", "08/2005", "09/2005", "10/2005", "11/2005", "12/2005",
"01/2006", "02/2006", "03/2006", "04/2006", "05/2006", "06/2006", "07/2006", "08/2006", "09/2006", "10/2006",
"11/2006", "12/2006", "01/2007", "02/2007", "03/2007", "04/2007", "05/2007", "06/2007", "07/2007", "08/2007",
"09/2007", "10/2007", "11/2007", "12/2007", "01/2008", "02/2008", "03/2008", "04/2008", "05/2008", "06/2008",
"07/2008", "08/2008", "09/2008", "10/2008", "11/2008", "12/2008", "01/2009", "02/2009", "03/2009", "04/2009",
"05/2009", "06/2009", "07/2009", "08/2009", "09/2009", "10/2009", "11/2009", "12/2009", "01/2010", "02/2010",
"03/2010", "04/2010", "05/2010", "06/2010", "07/2010", "08/2010", "09/2010", "10/2010", "11/2010", "12/2010",
"01/2011", "02/2011", "03/2011", "04/2011", "05/2011", "06/2011", "07/2011", "08/2011", "09/2011", "10/2011",
"11/2011", "12/2011", "01/2012", "02/2012", "03/2012", "04/2012", "05/2012", "06/2012", "07/2012", "08/2012",
"09/2012", "10/2012", "11/2012", "12/2012", "01/2013", "02/2013", "03/2013", "04/2013", "05/2013", "06/2013",
"07/2013", "08/2013", "09/2013", "10/2013", "11/2013", "12/2013"];

$("#slider-left")
  .each(function () {
    var input = $(this);
    $("<span>")
      .addClass("output")
      .html("01/2008")
      .insertAfter($(this));
  })
  .simpleSlider()
  .simpleSlider("setValue", months.indexOf("01/2008")/months.length);

$("#slider-right")
  .each(function () {
    var input = $(this);
    $("<span>")
      .addClass("output")
      .html("12/2013")
      .insertAfter($(this));
  })
  .simpleSlider()
  .simpleSlider("setValue", months.indexOf("12/2013")/months.length);

$('#slider-left').bind("slider:changed", function (event, data) {
  console.log(months[Math.floor(data.value*months.length)]);
    $(this)
      .nextAll(".output:first")
      .html(months[Math.floor(data.value*months.length)]);
      draw_granger('#chart-left', months[Math.floor(data.value*months.length)])
});

$('#slider-right').bind("slider:changed", function (event, data) {
    $(this)
      .nextAll(".output:first")
        .html(months[Math.floor(data.value*months.length)]);
        draw_granger('#chart-right', months[Math.floor(data.value*months.length)])
});

var draw_granger = function(selector, date) {
  $(selector).html('');
  var w = 960,
      h = 960,
      rx = w / 2,
      ry = h / 2,
      m0,
      rotate = 0;

  var radius = 960 / 2,
      splines = [];

  var cluster = d3.layout.cluster()
      .size([360, radius - 120])
      .sort(null)
      .value(function(d) { return d.size; });

  var bundle = d3.layout.bundle();

  var line = d3.svg.line.radial()
      .interpolate("bundle")
      .tension(.85)
      .radius(function(d) { return d.y; })
      .angle(function(d) { return d.x / 180 * Math.PI; });

  var div = d3.select(selector).append("svg")
     .style("top", "40px")
      .style("left", "-8%")
      .style("width", w + "px")
      .style("height", w + "px")
      .style("position", "relative")
      .style("-webkit-backface-visibility", "hidden");

  var svg = div.append("svg:svg")
      .attr("width", w)
      .attr("height", w)
    .append("svg:g")
      .attr("transform", "translate(" + rx + "," + ry + ")");

  svg.append("svg:path")
      .attr("class", "arc")
      .attr("d", d3.svg.arc().outerRadius(ry - 120).innerRadius(0).startAngle(0).endAngle(2 * Math.PI))
      .on("mousedown", mousedown);

  d3.json("/granger/data?date=" + encodeURIComponent(date), function(classes) {
    var nodes = cluster.nodes(packages.root(classes)),
        links = packages.imports(nodes),
        splines = bundle(links);

    var path = svg.selectAll("path.link")
        .data(links)
      .enter().append("svg:path")
        .attr("class", function(d) { return "link source-" + d.source.key + " target-" + d.target.key; })
        .attr("d", function(d, i) { return line(splines[i]); });

    svg.selectAll("g.node")
        .data(nodes.filter(function(n) { return !n.children; }))
      .enter().append("svg:g")
        .attr("class", "node")
        .attr("id", function(d) { return "node-" + d.key; })
        .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
      .append("svg:text")
        .attr("dx", function(d) { return d.x < 180 ? 8 : -8; })
        .attr("dy", ".31em")
        .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
        .attr("transform", function(d) { return d.x < 180 ? null : "rotate(180)"; })
        .text(function(d) { return d.key; })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);

  });

  d3.select(window)
      .on("mousemove", mousemove)
      .on("mouseup", mouseup);

  function mouse(e) {
    return [e.pageX - rx, e.pageY - ry];
  }

  function mousedown() {
    m0 = mouse(d3.event);
    d3.event.preventDefault();
  }

  function mousemove() {
    if (m0) {
      var m1 = mouse(d3.event),
          dm = Math.atan2(cross(m0, m1), dot(m0, m1)) * 180 / Math.PI;
      div.style("-webkit-transform", "translateY(" + (ry - rx) + "px)rotateZ(" + dm + "deg)translateY(" + (rx - ry) + "px)");
    }
  }

  function mouseup() {
    if (m0) {
      var m1 = mouse(d3.event),
          dm = Math.atan2(cross(m0, m1), dot(m0, m1)) * 180 / Math.PI;

      rotate += dm;
      if (rotate > 360) rotate -= 360;
      else if (rotate < 0) rotate += 360;
      m0 = null;

      div.style("-webkit-transform", null);

      svg
          .attr("transform", "translate(" + rx + "," + ry + ")rotate(" + rotate + ")")
        .selectAll("g.node text")
          .attr("dx", function(d) { return (d.x + rotate) % 360 < 180 ? 8 : -8; })
          .attr("text-anchor", function(d) { return (d.x + rotate) % 360 < 180 ? "start" : "end"; })
          .attr("transform", function(d) { return (d.x + rotate) % 360 < 180 ? null : "rotate(180)"; });
    }
  }

  function mouseover(d) {
    svg.selectAll("path.link.target-" + d.key)
        .classed("target", true)
        .each(updateNodes("source", true));

    svg.selectAll("path.link.source-" + d.key)
        .classed("source", true)
        .each(updateNodes("target", true));
  }

  function mouseout(d) {
    svg.selectAll("path.link.source-" + d.key)
        .classed("source", false)
        .each(updateNodes("target", false));

    svg.selectAll("path.link.target-" + d.key)
        .classed("target", false)
        .each(updateNodes("source", false));
  }

  function updateNodes(name, value) {
    return function(d) {
      if (value) this.parentNode.appendChild(this);
      svg.select("#node-" + d[name].key).classed(name, value);
    };
  }

  function cross(a, b) {
    return a[0] * b[1] - a[1] * b[0];
  }

  function dot(a, b) {
    return a[0] * b[0] + a[1] * b[1];
  }
}

draw_granger('#chart-left', '01/2008');
draw_granger('#chart-right', '12/2013');