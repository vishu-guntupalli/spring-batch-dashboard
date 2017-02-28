/**
 * Created by guntupv on 2/25/17.
 */
var svg = d3.select("#barg").select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().rangeRound([height, 0]);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<b><span style='color:greenyellow'>" + d.jobName + "</span></b>";
  });

svg.call(tip);

d3.json("/dashboard/job-success-failure", function(error, data) {
  if (error) throw error;

  x.domain(data.map(function(d) { return d.jobName; }));
  y.domain([0, d3.max(data, function(d) { return d.totalCount; })]);

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickValues([]));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Frequency");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.jobName); })
      .attr("y", function(d) { return y(d.totalCount); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.totalCount); })
      .on('mouseover', function(d){
        tip.show(d);
        removePie(d)
        renderPie(d);
      })
      .on('mouseout', function(d){
          tip.hide

      });
});