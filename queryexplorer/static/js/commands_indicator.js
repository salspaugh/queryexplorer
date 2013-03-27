
var DISPLAY_ROWS = 1000; 
var RECT_HEIGHT = 5;
var RECT_WIDTH = 5;
var SVG_WIDTH = 600; // fix this later - don't hard code it

var rects = null;
var topQueryIdx = 0;
var bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;
var labels = [];

var colormap = {};
var colors = ["#66CC66", "#336699"];
var currentColorIdx = 0;

d3.select("button")
    .on("click", function() {
        addLabels();
    });

$("body").height(58500);
$("window").scrollTop(0);

var tooltip = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0); // not visible by default

var svg = d3.select("#content")
            .append("svg");

var svgOffset = svg[0][0].getBoundingClientRect().top;

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

// function definitions

function addLabels() {
    var text = $("input").val();            
    var selected = getSelectedRects();
    updateLabels(selected, text);
}

function getSelectedRects() {
    if (rects) {
        var selected = rects.filter(function(d, i) {
            selected = d3.select(this).attr("selected");
            multiSelected = d3.select(this).attr("multi-selected");
            return (selected == "true" || multiSelected == "true");
        });
        return selected;
    }
}

function updateLabels(selectedRects, text) {
    selectedRects.attr("label", text);
    selectedRects.datum(function(d, i) {
        d.label = text;
        labelData = d;
        labelData.hash = d.ridx + d.label + '_background';
        labels = labels.filter(function(elem, idx, arr) {
            return elem.ridx != d.ridx;    
        });
        labels.push(labelData);
        bg = svg.selectAll(".background")
            .data(labels, function(d) { return d.hash; })
        bg.enter()
            .append("rect")
            .call(setBackgroundAttributes);
        bg.exit().remove();
        d.label = text;
        return d;
    });
    $(".square").remove();
    renderVisualization(topQueryIdx, bottomQueryIdx);
}

function setBackgroundAttributes(items) {
    items.attr("class", "background")
        .attr("height", function() {
            return (RECT_HEIGHT - 1) + "px";
        })
        .attr("width", function() { 
            return SVG_WIDTH + "px";
        })
        .attr("x", function(d) {
            return parseInt(d.cidx) * RECT_WIDTH;
         })
        .attr("y", function(d) {
            console.log(d.label);
            return parseInt(d.ridx) * RECT_HEIGHT;
        })
        .attr("fill", function(d) {
            return getColor(d.label);
        })
        .attr("fill-opacity", .1);
}

function getColor(label) {
    //console.log(colormap);
    if (label in colormap) {
        //console.log(colormap[label]);
        //console.log('here');
        return colormap[label];
    }
    else {
        colormap[label] = colors[currentColorIdx];
        currentColorIdx += 1;
    }
    return colormap[label];
}

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

        //console.log("Done loading.");
        //console.log(json);
        
        // Get the correct data to display.
        var toRender = json.filter(isInRange);

        // Add the wanted elements.
        rects = svg.selectAll(".square")
            .data(toRender, function(d) { return d.hash; });

        rects.enter()
            .append("rect")
            .attr("class", "square")
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
        unSelectRow(datum);
    } else { 
        clearMultiSelection();
        clearSelection();
        selectRow(datum);
    }
}

function toggleMultiSelection(datum, elem){
    multiSelected = elem.attr("multi-selected");
    if (multiSelected == "true") {
        unMultiSelectRow(datum);
    } else {
        clearSelection();
        multiSelectRow(datum);
    }
}

function unSelectRow(datum) {
    rects.attr("fill", function(d) {
        currentColor = d3.select(this)
                        .attr("fill");
            if (d.ridx == datum.ridx) {
                return "black";
            }
            return currentColor;
        })
        .attr("selected", function(d) {
            currentVal = d3.select(this)
                            .attr("selected");
            if (d.ridx == datum.ridx) {
                return false;
            }
            return currentVal;
        });
}

function selectRow(datum) {
    rects.attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            if (d.ridx == datum.ridx) {
                return "#666699";
            }
            return currentColor;
        })
        .attr("selected", function(d) {
            currentVal = d3.select(this)
                            .attr("selected");
            if (d.ridx == datum.ridx) {
               return true;
            }
            return currentVal;
        });
}

function unMultiSelectRow(datum) {
    rects.attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            if (d.ridx == datum.ridx) {
                return "black";
            }
            return currentColor;
        })
        .attr("multi-selected", function(d) {
            currentVal = d3.select(this)
                            .attr("multi-selected");
            if (d.ridx == datum.ridx) {
               return false;
            }
            return currentVal;
        });
}

function multiSelectRow(datum) {
    rects.attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            if (d.ridx == datum.ridx) {
                return "#CC6633";
            }
            return currentColor;
        })
        .attr("multi-selected", function(d) {
            currentVal = d3.select(this)
                            .attr("multi-selected");
            if (d.ridx == datum.ridx) {
               return true;
            }
            return currentVal;
        });
}

function clearSelection(){
    svg.selectAll(".square")
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
    svg.selectAll(".square")
        .attr("selected", false);
}

function clearMultiSelection(){
    svg.selectAll(".square")
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
    svg.selectAll(".square")
        .attr("multi-selected", false);
}
