
var DISPLAY_ROWS = 1000; 
var RECT_HEIGHT = 5;
var RECT_WIDTH = 5;

var topQueryIdx = 0;
var bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;

$("body").height(58500);
$("window").scrollTop(0);

var tooltip = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0); // not visible by default

//d3.select("#content")
//    .append("p")
//    .text("Each column is a command. Each row is a query. The square at row i and column j will be black if query i used command j.");

var svg = d3.select("#content")
            .append("svg");

var svgOffset = svg[0][0].getBoundingClientRect().top;

var rects = null;

renderVisualization(topQueryIdx, bottomQueryIdx);

$(document).ready(function() {   
    $(window).scroll(function() {
        rectdata = rects[0];
        topQueryIdx = Math.max(0, ($(window).scrollTop() - svgOffset)/RECT_HEIGHT);
        bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;
        console.log("New window location:", $(window).scrollTop());
        console.log("New query range:", topQueryIdx, bottomQueryIdx);
        console.log("Rects before:", rectdata[0], rectdata[rectdata.length - 1]);
        renderVisualization(topQueryIdx, bottomQueryIdx);
        console.log("Rects after:", rectdata[0], rectdata[rectdata.length - 1]);
    });
});

function isInRange(element, index, array) {
    return element.ridx >= topQueryIdx && element.ridx <= bottomQueryIdx;
}

function range(start, end)
{
    var a = [];
    for (var i = start; i <= end; i++)
        a.push(i);
    return a;
}

function renderVisualization(topIdx, botIdx) {
    
    d3.json('/commands_indicator_coordinates', function(error, json) {

        console.log("Done loading.");
        console.log(json);
        
        // Get the correct data to display.
        var toRender = json.filter(isInRange);

        // Add the wanted elements.
        rects = svg.selectAll("rect")
            .data(toRender, function(d) { return d.hash; });

        rects.enter()
            .append("rect")
            .attr("height", function() {
                return (RECT_HEIGHT - 1) + "px";
            })
            .attr("width", function() { 
                return (RECT_WIDTH - 1) + "px";
            })
            .attr("x", function(d) {
                return parseInt(d.cidx) * RECT_WIDTH;
             })
            .attr("y", function(d) {
                return parseInt(d.ridx) * RECT_HEIGHT;
            })
            .on("mouseover", function(d) {      
                tooltip.transition()        
                    .duration(100)      
                    .style("opacity", .8);      
                tooltip.html(d.ridx + ": " + d.cmd)  
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");    
            })     
            .on("mouseout", function(d) {       
                tooltip.transition()        
                    .duration(100)      
                    .style("opacity", 0);   
            })
            .on("click", function(d) {
                if (d3.event.shiftKey) {
                    toggleMultiSelection(d, d3.select(this));
                } else {        
                    toggleSelection(d, d3.select(this));
                }
            }); 

        // Remove unwanted elements.
        rects.exit().remove()
    });
}

function toggleSelection(datum, elem) {
    selected = elem.attr("selected");
    if (selected == "true") {
        elem.attr("fill", "black")
            .attr("selected", false);
    } else { 
        clearMultiSelection();
        elem.attr("fill", "#666699")
            .attr("selected", true);
    }
}

function toggleMultiSelection(datum, elem){
    multiSelected = elem.attr("multi-selected");
    if (multiSelected == "true") {
        //d3.selectAll("rects")
        //    .attr("fill", function(d) {
        //        currentColor = d3.select(this)
        //                        .attr("fill");
        //        if (d.ridx == datum.ridx) {
        //            return "black";
        //        }
        //        return currentColor;
        //    })
        //    .attr("multi-selected", function(d) {
        //        currentVal = d3.select(this)
        //                        .attr("multi-selected");
        //        if (d.ridx == datum.ridx) {
        //           return false;
        //        }
        //        return currentVal;
        //    });
        elem.attr("fill", "black")
            .attr("multi-selected", false);
    } else {
        clearSelection();
        //d3.selectAll("rects")
        //    .attr("fill", function(d) {
        //        currentColor = d3.select(this)
        //                        .attr("fill");
        //        if (d.ridx == datum.ridx) {
        //            return "#CC6633";
        //        }
        //        return currentColor;
        //    })
        //    .attr("multi-selected", function(d) {
        //        currentVal = d3.select(this)
        //                        .attr("multi-selected");
        //        if (d.ridx == datum.ridx) {
        //           return true;
        //        }
        //        return currentVal;
        //    });
        elem.attr("fill", "#CC6633")
            .attr("multi-selected", true);
    }
}

function clearSelection(){
    svg.selectAll("rect")
        .attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            selected = d3.select(this)
                .attr("selected");
            multiSelected = d3.select(this)
                            .attr("multi-selected");
            if (selected == "true") {
                return "black";
            }
            return currentColor;
        });
    svg.selectAll("rect")
        .attr("selected", false);
}

function clearMultiSelection(){
    svg.selectAll("rect")
        .attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            multiSelected = d3.select(this)
                            .attr("multi-selected");
            if (multiSelected == "true") {
                return "black";
            }
            return currentColor;
        });
    svg.selectAll("rect")
        .attr("multi-selected", false);
}
