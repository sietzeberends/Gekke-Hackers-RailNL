width_map = 1000
height_map = 1200

// Determine the size of the map
widthMap = 1000
heightMap = 1200

// when scripts loaded, implement functions that require d3 and tooltip
window.onload = function(d){


  // create tooltip for stations
var tipStations = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
      return "<span>" + "Station: " + d.station + "</span>";
    })

// create tooltip for connections
var tipConnections = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10,0])
  .html(function(d){
      return "<span>" + "Connection: " + d.station1 + " -> " + d.station2 + "</span>";
  })


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

map.call(tipStations);
map.call(tipConnections);

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

=======
    .range([heightMap - 90, 175])

// store the location of each station in this dict
var locations_stations = {}

// create button to select solution
var button = d3.select("body").append("div")
    .attr("class", "menu")

button
  .append("button")
    .attr("type", "button")
    .attr("class", "btn btn-primary dropdown-toggle")
    .attr("data-toggle", "dropdown")
    .text("Pick a solution!")
    .append("span")
    .attr("class", "caret")


// queue the csv's for each solution
var q = d3.queue()
  .defer(d3.json, "StationsNationaal.json")
  .defer(d3.json, "Greedy_4.json")
  .defer(d3.json, "HillclimberNoordZuid.json")
  .defer(d3.json, "HillclimberNationaal.json")
  .defer(d3.json, "HillclimberNationaalNoUtrecht.json")
  .await(makemap);

// function that draws the lines for a solution
  function createSolution (data){

  var counter = 0

  // store colours for each trajectory
  var colours = ["placeholder","red","#ff8000","#ffff00","#40ff00",
  				 "#00ffff", "#0000ff", "#bf00ff", "#ff00ff", "#black",
  				 "#fffff0", "#008B8B", "#A52A2A", "#006400", "#BDB76B"]

  // save the Coordinates for each connection
  var connectionCoordinates = []

  // draw the lines for each connection
  var lines = map.selectAll("connection")
  .data(data)
    .enter().append("line")
    .transition()
    .delay(function(d,i){ return i * 200})
    .attr('class', 'connection')
    .attr('x1', function(d){if (d.nextTrajectory=="False")
                            {
                              return scale_x(locations_stations[d.station1][1]);
                            }
                          })
    .attr('x2', function(d){ if (d.nextTrajectory=="False")
                            {
                              return scale_x(locations_stations[d.station2.trim()][1]);
                            }
                          })
    .attr('y1', function(d){ if (d.nextTrajectory=="False")
                            {
                              return scale_y(locations_stations[d.station1.trim()][0]);
                            }
                          })
    .attr('y2', function(d){ if (d.nextTrajectory=="False")
                            {
                              return scale_y(locations_stations[d.station2.trim()][0]);
                            }
                          })
  .attr("stroke-width", 2)
  .attr("stroke", function(d){ if (d.nextTrajectory=="True")
                               {
                                 counter = counter + 1
                               }
                              return colours[counter]
                             })
  }

// function that makes map
function makemap(error, stations, Greedy, HillclimberNoordZuid, HillclimberNationaal, HillclimberNoUtrecht){
  if (error) throw error;

// save locations of stations to list
stations.forEach(function(d){
	locations_stations[String(d.station)] = [d.latitude, d.longitude, d.critical]
})

// change domain
scale_x
.domain(d3.extent(stations,function(d){return d.longitude;})).nice();

scale_y
.domain(d3.extent(stations,function(d){return d.latitude;})).nice();

// create circles
var circles = map.selectAll("dot")
    .data(stations)
    .enter().append("circle")
    .attr({
      "class":"dot",
      "cx": function(d){ return scale_x(d.longitude)} ,
      "cy": function(d){ return scale_y(d.latitude)},
      "r": 5,
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
    .on("mouseover", function(d){
              tipStations.show(d);
          })
    .on("mouseout", function(d){
              tipStations.hide(d);
          })


// strings with names of each solution
var solutions = ["Greedy", "Hillclimber - NoordZuid",
                 "Hillclimber - Nationaal",
                 "Hillcimber - Nationaal - No Utrecht"]

// create dropdown menu when button is pressed
var menu = button.append("ul")
    .attr("class", "dropdown-menu")
    .attr("role", "menu")

// create dropdown menu for button
  menu.selectAll("li")
      .data(solutions)
      .enter().append("li")
          .append("a")
          .attr("class", "m")
          .attr("href", "#")
          .text(function(d){ return d})
          .attr("value", function(d){ return d})
          .on("click", function(d){
            d3.selectAll(".connection").remove()
            var solution = this.getAttribute("value")

            if (solution == "Hillclimber - NoordZuid"){
              createSolution(HillclimberNoordZuid)
            }
            else if (solution == "Greedy"){
              createSolution(Greedy)
            }
            else if (solution == "Hillclimber - Nationaal"){
              createSolution(HillclimberNationaal)
            }
            else if (solution == "Hillcimber - Nationaal - No Utrecht"){
              createSolution(HillclimberNoUtrecht)
            }
          })

// show tooltip if mouse over connection
d3.selectAll(".connection")
  .on("mouseover", function(d){
              tipConnections.show(d);
          })
  .on("mouseout", function(d){
              tipConnections.hide(d);
          })

  }
}
