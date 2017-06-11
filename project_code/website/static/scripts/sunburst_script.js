var width = 1000,
    height = 1000,
    radius = Math.min(width, height) / 2,
    color = d3.scale.category20c();

var x = d3.scale.linear()
    .range([0, 2 * Math.PI]);

var y = d3.scale.linear()
    .range([0, radius]);

var zoom = d3.behavior.zoom()
    .scaleExtent([1, 10])
    .on("zoom", zoomed);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
	.append("g")
    .attr("transform", "translate(" + width/2 + "," + height * .52 + ")")
	.call(zoom);

function zoomed() {
  svg.attr("transform", "translate(" + width/2 + "," + height * .52 + ")scale(" + d3.event.scale + ")");
}



var partition = d3.layout.partition()
    .sort(null)
    //.size([2 * Math.PI, radius * radius])
    .value(function(d) { return d.size; });

var arc = d3.svg.arc()
    .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
    .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
    .innerRadius(function(d) { return Math.max(0, y(d.y)); })
    .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

//var stack = d3.layout.stack()
	//.values(function(d) { return d.values; })

// Keep track of selected node
var node;
var currAngle = 0;


d3.json("/static/data/flare.json", function(error, root) {
  if (error) throw error;

  node = root;

  var gc = svg.datum(root).selectAll("g")
			.data(partition.nodes)
			.enter().append("g");


  var path = gc.append("path")
      //.attr("display", function(d) { return d.depth ? null : "none"; }) // hide inner ring
      .attr("d", arc)
      .style("stroke", "#fff")
      .style("fill", function(d) { return color((d.children ? d : d.parent).name); })
      .style("fill-rule", "evenodd")
	  .on("click", click)
      .each(stash);

  var text = gc.append("text")
		.style("font-size", function(d) { return d.depth ? Math.min(d.dx * 900 * 900/Math.pow((d.depth-node.depth+1), .1),24/Math.pow((d.depth-node.depth+1), .6)) + "px" : (24 + "px") })
		.attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
		.attr("x", function(d) { return y(d.y); })
		.attr("dx", "6") // margin
		.attr("dy", ".35em") // vertical-align
		.on("click", click)
		.text(function(d) { return d.name; });

  d3.selectAll("input").on("change", function change() {
    var value = this.value === "count"
        ? function() { return 1; }
        : function(d) { return d.size; };

    path
        .data(partition.value(value).nodes)
      .transition()
        .duration(1500)
        .attrTween("d", arcTweenData);


	text
		.data(partition.value(value).nodes)
	  .transition()
        .duration(1500)
		.attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
  });

	function click(d){
	if(node == d)
		return;
	else
		node = d;
	text.transition()
		.duration(500)
		.attr("opacity", 0);

	path.transition()
		.duration(1000)
		.attrTween("d", arcTweenZoom(d))
		.each("end", function(e, i){
			if(e.x >= d.x && e.x < (d.x +d.dx)){
				var tx = d3.select(this.parentNode).select("text");
				tx.transition()
					.duration(450)
		.style("font-size", function(d) { return d.depth ? Math.min(d.dx * 900 * 900/Math.pow((d.depth-node.depth+1), .1),24/Math.pow((d.depth-node.depth+1), .6)) + "px" : (24 + "px") })
					.attr("x", function(d) { return y(d.y); })
					.attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
				tx.transition()
					.duration(50)
		.style("font-size", function(d) { return d.depth ? Math.min(d.dx * 900 * 900/Math.pow((d.depth-node.depth+1), .1),24/Math.pow((d.depth-node.depth+1), .6)) + "px" : (24 + "px") })
					.attr("x", function(d) { return y(d.y); })
					.attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
					.attr("opacity", 1);
			}
		});
	//THIS CODE IS ADDED BY ME, CONDITION CAN BE REMOVED IF EVERY CLICK SHOULD RESULT IN AN ACTION
	if (d.depth == 3){
			fillTable(d)
		}
	}
});

function update_table(d){
	//window.parent.document.getElementById('target');
}

d3.select(self.frameElement).style("height", height + "px");

// Stash the old values for transition.
function stash(d) {
  d.x0 = d.x;
  d.dx0 = d.dx;
}

// When switching data: interpolate the arcs in data space.
function arcTweenData(a, i) {
  var oi = d3.interpolate({x: a.x0, dx: a.dx0}, a);
  function tween(t) {
    var b = oi(t);
    a.x0 = b.x;
    a.dx0 = b.dx;
    return arc(b);
  }
  if (i == 0) {
   // If we are on the first arc, adjust the x domain to match the root node
   // at the current zoom level. (We only need to do this once.)
    var xd = d3.interpolate(x.domain(), [node.x, node.x + node.dx]);
    return function(t) {
      x.domain(xd(t));
      return tween(t);
    };
  } else {
    return tween;
  }
}

// When zooming: interpolate the scales.
function arcTweenZoom(d) {
  var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
      yd = d3.interpolate(y.domain(), [d.y, 1]),
      yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
  return function(d, i) {
    return i
        ? function(t) { return arc(d); }
        : function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
  };
}

function computeTextRotation(d) {
  //var a = x(d.x + d.dx/2) * 180 / Math.PI - 180;
  if(!(d.depth-node.depth)) return (x(d.x + d.dx / 2) * 180) / Math.PI - 180;
  return (x(d.x + d.dx / 2) * 180) / Math.PI - 90;
  //return a;
}


//added javascript to allow table update_table (by RICK BEELOO)

function fillTable(d) {
	var head = ["name", "summary", "pubmed","orthologs"];
	//NEED TO ADD SOME SCRIPTING TO RETRIEVE THE DATA FROM THE DATBASE AND PUT THE DATA IN THE DATA ARRAY
	var data = [d.name,"Dit is een hele mooie samenvatting van het gen","124354,126623","henkjeHetGen"];
	var need_textbox = ["summary", "pubmed","orthologs"]
	var length = head.length;
	for (var i = 0; i < length; i++){
		if (need_textbox.includes(head[i])) { //NEED TO LOOK IN need_textbox array!
			parent.document.getElementById(head[i]).innerHTML = "<textarea class=\"output\" rows=\"4\" cols=\"20\">" + data[i] + "</textarea>";
		}
		else {
			if (head[i] == "name") {
				var gene_link = "https://www.ncbi.nlm.nih.gov/gene/?term=" + data[i] + "+AND+PLANTS%5BORGN%5D";
				var hyperlink = "<a href=" + gene_link + ">" + data[i] + "</a>";
				parent.document.getElementById(head[i]).innerHTML = hyperlink;
			}
			else {
				parent.document.getElementById(head[i]).innerHTML = data[i];
			}

		}

	}
}