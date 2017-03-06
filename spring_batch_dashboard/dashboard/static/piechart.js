/**
 * Created by guntupv on 2/26/17.
 */

var pieWidth = 250,
    pieHeight = 250,
    radius = Math.min(pieWidth, pieHeight) / 2;

var successColor = d3.rgb("#6fff84")
var failureColor = d3.rgb("#ff0433")

var pieArc = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

var labelArc = d3.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

var pie = d3.pie()
    .sort(null)
    .value(function(d) { return d.count; });

var svg = d3.select("#pieg").select("svg")
    .attr("pieWidth", pieWidth)
    .attr("pieHeight", pieHeight)
    .append("g")
    .attr("transform", "translate(" + pieWidth / 2 + "," + pieHeight / 2 + ")");

var textSvg = d3.select("#pieg")
                .select("#jobLabel");

var renderPie = function(data) {
    var fcount = data.failedCount == null ? 0 : data.failedCount;
    var formattedData = [{'jobName' : data.jobName, 'count': data.succeededCount, 'label': 'success'},
                         {'jobName' : data.jobName, 'count': fcount, 'label': 'failure'}]

    var g = svg.selectAll(".arc")
      .data(pie(formattedData))
      .enter().append("g")
      .attr("class", "arc");

    g.append("path")
      .attr("d", pieArc)
      .style("fill", function(d){
                                if (d.data.label=='success')
                                    return successColor
                                else
                                    return failureColor});

    g.append("text")
      .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .text(function(d) { return d.data.count; });
}

var removePie = function(data) {
    svg.selectAll(".arc").remove()
}

var renderJobName = function(jobName) {
    textSvg.text(jobName)
}
