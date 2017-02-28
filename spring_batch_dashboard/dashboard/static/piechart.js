/**
 * Created by guntupv on 2/26/17.
 */

var pieWidth = 250,
    pieHeight = 250,
    radius = Math.min(pieWidth, pieHeight) / 2;

var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

var pieArc = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

var labelArc = d3.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

var pie = d3.pie()
    .sort(null)
    .value(function(d) { return d.totalCount; });

var svg = d3.select("#pieg").select("svg")
    .attr("pieWidth", pieWidth)
    .attr("pieHeight", pieHeight)
    .append("g")
    .attr("transform", "translate(" + pieWidth / 2 + "," + pieHeight / 2 + ")");

var renderPie = function(data) {
    var g = svg.selectAll(".arc")
      .data(pie(data))
      .enter().append("g")
      .attr("class", "arc");


  g.append("text")
      .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .text(function(d) { return d.succeededCount; });
}
