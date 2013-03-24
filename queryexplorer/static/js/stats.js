
d3.json("/stats", function(error, json) {
  
    table = d3.select("#content")
        .append("table");
   
    table.attr("class", "sans");
    
    header = table.append("tr");

    header.append("td")
        .text("Data set");
    header.append("td")
        .text("Count");
   
    $.each(json, function(idx, val) {
        row = table.append("tr");
        row.append("td")
            .text(function () {
                return val.dataset
             });
        row.append("td")
            .text(val.count);
    });
    
});

