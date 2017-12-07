
width_map = 1000
height_map = 1200

// when scripts loaded, implement functions that require d3 and tooltip
window.onload = function(d){

 // create svg for scatterplot

var map = d3.select("body").append("svg")
    .attr({"width": width_map,
           "height": height_map})
    .append("g");

var img = map.append("svg:image")
    .attr("xlink:href", "Blank_map_of_the_Netherlands.svg")
    .attr("width", width_map)
    .attr("height", height_map)
    .attr("x", 0)
    .attr("y", 0);


// create scale for X axis
var scale_x = d3.scale.linear()
    .range([110, width_map - 90])

// create scale for Y axis
var scale_y = d3.scale.linear()
    .range([height_map - 90, 175])


locations_stations = {}
    

d3.json("StationsNationaaltest.json", function(data){


// save locations of stations to list
data.forEach(function(d){

	locations_stations[String(d.station)] = [d.latitude, d.longitude, d.critical]
})


// change domain
scale_x
.domain(d3.extent(data,function(d){return d.longitude;})).nice();

scale_y
.domain(d3.extent(data,function(d){return d.latitude;})).nice();

// create circles 
var circles = map.selectAll("dot")
    .data(data)
    .enter().append("circle")
    .attr({
      "class":"dot", 
      "cx": function(d){ return scale_x(d.longitude)} ,
      "cy": function(d){ return scale_y(d.latitude)},
      "r": 3.5,
      "fill": function(d){if (d.critical == "Kritiek")
  						  {
  						  	return "red"
  						  }
  						  else
  						  {
  						    return "black"
  						  }
  						}
    	})


	})


d3.json("ConnectiesNationaaltest.json", function(data){


var lines = map.selectAll("connection")
	.data(data)
    .enter().append("line")
    .attr('class', 'connection')
    .attr('x1', function(d){return scale_x(locations_stations[d.station1][1]); })
    .attr('x2', function(d){return scale_x(locations_stations[d.station2][1]); })
    .attr('y1', function(d){return scale_y(locations_stations[d.station1][0]); })
    .attr('y2', function(d){return scale_y(locations_stations[d.station2][0]); })
    .attr("stroke-width", 2)
	.attr("stroke", function(d){ if (d.critical == "TRUE")
								 {
								 	return "red"
								 }
								 else
								 {
								 	return "black"
								 }
				});

})

}