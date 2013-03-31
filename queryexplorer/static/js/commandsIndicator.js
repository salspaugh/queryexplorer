
// global variables

var DISPLAY_ROWS = 1000; 
var RECT_HEIGHT = 5;
var RECT_WIDTH = 5;
var SVG_WIDTH = 600; // fix this later - don't hard code it

var tooltip;
var svg;

var topQueryIdx = 0;
var bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;
var svgOffset;

var coordinates = null;
var squares = null;
var labels = [];
var legends = [];

var colormap = {};
var colors = ["#5254a3", "#6b6ecf", "#9c9ede", "#637939", "#8ca252", "#b5cf6b", "#cedb9c", "#8c6d31", "#bd9e39", "#e7ba52", "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#e7969c", "#7b4173", "#a55194", "#ce6dbd", "#de9ed6"]
var currentColorIdx = 0;
var curLegendY = 0;


main()

function main() {

    // add tooltip
    tooltip = d3.select("body").append("div")   
        .attr("class", "tooltip")               
        .style("opacity", 0); // not visible by default
    
    // add "Assign Label" button handler
    d3.select(".addlabel")
        .on("click", function() {
            assignLabelsClicked();
        });

    // add "Remove Label" button handler
    d3.select(".removelabel")
        .on("click", function() {
            removeLabelsClicked();
        });

    // add svg container
    svg = d3.select("#content")
            .append("svg");
    rightsidesvg = d3.select("#rightsidebar")
            .append("svg")
            .attr("width", "250px");

    // ready the height of the container
    svgOffset = svg[0][0].getBoundingClientRect().top;
    $("body").height(bottomQueryIdx + svgOffset);

    // render the main viz
    loadJSON();
}

$(document).ready(function() {   
    $(window).scroll(function() {
        //rectdata =squares[0];
        topQueryIdx = Math.max(0, ($(window).scrollTop() - svgOffset)/RECT_HEIGHT);
        bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;
        $("body").height(bottomQueryIdx+svgOffset);
        //console.log("New window location:", $(window).scrollTop());
        //console.log("New query range:", topQueryIdx, bottomQueryIdx);
        //console.log("Rects before:", rectdata[0], rectdata[rectdata.length - 1]);
        redrawSquares(topQueryIdx, bottomQueryIdx);
        //console.log("Rects after:", rectdata[0], rectdata[rectdata.length - 1]);
    });
});

function removeLabelsClicked() {
    var label = $("input").val();            
    $("input").val("");
    var selectedSquares = getSelectedSquares();
    if (label == "") {
        //label = selectedSquares[0][0].__data__.label;
        label = selectedSquares.attr("label");
    }
    removeLabels(selectedSquares, label);
}

function assignLabelsClicked() {
    var label = $("input").val();            
    $("input").val("");
    var selectedSquares = getSelectedSquares();
    updateLabels(selectedSquares, label);
}

function getSelectedSquares() {
    if (squares) {
        var selectedSquares =squares.filter(function(d) {
            selected = d3.select(this).attr("selected");
            multiSelected = d3.select(this).attr("multi-selected");
            return (selected == "true" || multiSelected == "true");
        });
        return selectedSquares;
    }
}

function removeLabels(selectedSquares, label) {
    updateSquaresElements(selectedSquares, null);
    selectedSquares.datum(function(squareData, index) {
        updateSquaresData(squareData, null);
        updateCoordinatesData(squareData, null);
        removeGlobalLabelData(label, squareData.ridx);    
        redrawBackgroundRects();
        updateQueryData(squareData);
        return squareData;
    });
    removeLegendData(label);
    redrawLegend();
    $(".square").remove();
    redrawSquares(topQueryIdx, bottomQueryIdx);
}

function updateLabels(selectedSquares, label) {
    updateSquaresElements(selectedSquares, label);
    selectedSquares.datum(function(squareData, index) {
        updateSquaresData(squareData, label);
        updateCoordinatesData(squareData, label);
        addGlobalLabelData(squareData, label);        
        redrawBackgroundRects();
        updateQueryData(squareData);
        return squareData;
    });
    addLegendData(label);
    redrawLegend();
    $(".square").remove();
    redrawSquares(topQueryIdx, bottomQueryIdx);
}

function updateSquaresElements(selectedSquares, label) {
    selectedSquares.attr("label", label);
}

function updateSquaresData(data, label) {
    data.label = label;
}

function updateCoordinatesData(squareData, label) {
    selectedCoordinates = coordinates.filter(function(elem, idx, arr) {
        return elem.hash == squareData.hash; 
    });
    for (c in selectedCoordinates) {
        c.label = label;
    }
}

function removeGlobalLabelData(label, ridx) {
    labels = labels.filter(function(elem, idx, arr) {
        return (elem.label != label || elem.ridx != ridx);
    });
}

function addGlobalLabelData(squareData, label) {
    labelData = {};
    labelData.group_id = squareData.group_id;
    labelData.ridx = squareData.ridx;
    labelData.label = squareData.label
    labelData.hash = squareData.ridx + squareData.label + '_background';
    labels = labels.filter(function(elem, idx, arr) {
        return elem.ridx != squareData.ridx;    
    });
    labels.push(labelData);
}

function removeLegendData(label) {
    stillThere = false;
    for (labelData in labels) {
        if (labelData.label == label) {
            stillThere = true;
        }
    }
    if (!stillThere) {
        legends = legends.filter(function(elem, idx, arr) {
            return elem.label != label;
        });
    }
}

function addLegendData(label) {
    legend = {}
    legend.label = label
    legend.y = curLegendY
    curLegendY += 20;
    legends = legends.filter(function(elem, idx, arr) {
        return elem.label != label;
    });
    legends.push(legend);
}

function redrawLegend() {
    legendColor = rightsidesvg.selectAll(".legend")
        .data(legends, function(d) { return d.label; })
    legendColor.enter()
        .append("rect")
        .call(setLegendColorAttributes);
    legendColor.exit().remove();
    legendText = rightsidesvg.selectAll("text")
        .data(legends, function(d) { return d.label; })
    legendText.enter()
        .append("text")
        .call(setLegendTextAttributes);
    legendText.exit().remove();
}

function redrawBackgroundRects() {
    backgroundRects = svg.selectAll(".background")
        .data(labels, function(d) { return d.hash; })
    backgroundRects.enter()
        .append("rect")
        .call(setBackgroundAttributes);
    backgroundRects.exit().remove();
}

function updateQueryData(squareData) {
    $.post("/commands_indicator_class", squareData, function(data) {
        console.log(data);
    });
}

function setLegendColorAttributes(items) {
    items.attr("class", "legend")
        .attr("width", "75px")
        .attr("height", "10px")
        .attr("fill", function(d) {
            return getColor(d.label)
        })
        .attr("y", function(d) {
            return d.y;
        });
}

function setLegendTextAttributes(items) {
    items.attr("font-size", 14)
        .attr("fill", "black")
        .attr("x", 100)
        .attr("y", function(d) {
            return d.y + 10;
        })
        .text(function(d) { return d.label });
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
            return 0;
         })
        .attr("y", function(d) {
            return parseInt(d.ridx) * RECT_HEIGHT;
        })
        .attr("fill", function(d) {
            return getColor(d.label);
        })
        .attr("fill-opacity", 1);
}

function getColor(label) {
    if (label in colormap) {
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

function range(start, end) {
    var a = [];
    for (var i = start; i <= end; i++)
        a.push(i);
    return a;
}

function loadJSON() {
    
    d3.json('/commands_indicator_coordinates', function(error, json) {
        console.log("Loaded data."); 
        coordinates = json;
        redrawSquares(topQueryIdx, bottomQueryIdx);
    });
}

function redrawSquares(topIdx, botIdx) {
    
    // Get the correct data to display.
    var toRender = coordinates.filter(isInRange);

    // Add the wanted elements.
   squares = svg.selectAll(".square")
        .data(toRender, function(d) { return d.hash; });

   squares.enter()
        .append("rect")
        .call(setSquareAttributes);

    // Remove unwanted elements.
   squares.exit().remove()
}

function setSquareAttributes(items) {
    items.attr("label", function(d) { 
            return d.label;
        })
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
   squares.attr("fill", function(d) {
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
   squares.attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            if (d.ridx == datum.ridx) {
                return "yellow";
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
   squares.attr("fill", function(d) {
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
   squares.attr("fill", function(d) {
            currentColor = d3.select(this)
                            .attr("fill");
            if (d.ridx == datum.ridx) {
                return "orange";
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
