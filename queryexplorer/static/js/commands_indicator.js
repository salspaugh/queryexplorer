
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

var rects = null;
var labels = [];

var colormap = {};
var colors = ["#66CC66", "#336699"];
var currentColorIdx = 0;

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

    // ready the height of the container
    svgOffset = svg[0][0].getBoundingClientRect().top;
    $("body").height(bottomQueryIdx + svgOffset);

    // render the main viz
    renderVisualization(topQueryIdx, bottomQueryIdx);

}

$(document).ready(function() {   
    $(window).scroll(function() {
        //rectdata = rects[0];
        topQueryIdx = Math.max(0, ($(window).scrollTop() - svgOffset)/RECT_HEIGHT);
        bottomQueryIdx = topQueryIdx + DISPLAY_ROWS;
        $("body").height(bottomQueryIdx+svgOffset);
        //console.log("New window location:", $(window).scrollTop());
        //console.log("New query range:", topQueryIdx, bottomQueryIdx);
        //console.log("Rects before:", rectdata[0], rectdata[rectdata.length - 1]);
        renderVisualization(topQueryIdx, bottomQueryIdx);
        //console.log("Rects after:", rectdata[0], rectdata[rectdata.length - 1]);
    });
});

function removeLabelsClicked() {
    var label = $("input").val();            
    $("input").val("");
    var selectedSquares = getSelectedSquares();
    if (label == "") {
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
    if (rects) {
        var selectedSquares = rects.filter(function(d) {
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
        removeGlobalLabelData(label);    
        redrawBackgroundRects();
        updateQueryData(squareData);
        return squareData;
    });
    $(".square").remove();
    renderVisualization(topQueryIdx, bottomQueryIdx);
}

function updateLabels(selectedSquares, label) {
    updateSquaresElements(selectedSquares, label);
    selectedSquares.datum(function(squareData, index) {
        updateSquaresData(squareData, label);
        addGlobalLabelData(squareData, label);        
        redrawBackgroundRects();
        updateQueryData(squareData);
        return squareData;
    });
    $(".square").remove();
    renderVisualization(topQueryIdx, bottomQueryIdx);
}

function updateSquaresElements(selectedSquares, label) {
    console.log(selectedSquares);
    selectedSquares.attr("label", label);
}

function updateSquaresData(data, label) {
    data.label = label;
}

function removeGlobalLabelData(label) {
    labels = labels.filter(function(elem, idx, arr) {
        return elem.label != label;
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

//function updateRemoveLabels(selectedSquares, text) {
//    selectedSquares.attr("label", null);
//    selectedSquares.datum(function(d, i) {
//        d.label = null;
//        nullData = d
//        labels = labels.filter(function(elem, idx, arr) {
//            return elem.label != text;
//        });
//        bg = svg.selectAll(".background")
//            .data(labels, function(d) { return d.hash; })
//        bg.enter()
//            .append("rect")
//            .call(setBackgroundAttributes);
//        bg.exit().remove();
//        $.post("/commands_indicator_class", nullData, function(data) {
//            console.log(data);
//        });
//        return d;
//    });
//    $(".square").remove();
//    renderVisualization(topQueryIdx, bottomQueryIdx);
//}
//
//
//function updateLabels(selectedSquares, text) {
//    selectedSquares.attr("label", text);
//    selectedSquares.datum(function(d, i) {
//        d.label = text;
//        labelData = d;
//        labelData.hash = d.ridx + d.label + '_background';
//        labels = labels.filter(function(elem, idx, arr) {
//            return elem.ridx != d.ridx;    
//        });
//        labels.push(labelData);
//        bg = svg.selectAll(".background")
//            .data(labels, function(d) { return d.hash; })
//        bg.enter()
//            .append("rect")
//            .call(setBackgroundAttributes);
//        bg.exit().remove();
//        $.post("/commands_indicator_class", labelData, function(data) {
//            console.log(data);
//        });
//        return d;
//    });
//    $(".square").remove();
//    renderVisualization(topQueryIdx, bottomQueryIdx);
//}

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
        .attr("fill-opacity", .1);
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
            .attr("label", function(d) { 
                return d.class;
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
