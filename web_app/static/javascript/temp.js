function exportJson(el) {
    var obj = {
        a: 123,
        b: "4 5 6"
    };
    var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));

    el.setAttribute("href", "data:" + data);
    el.setAttribute("download", "data.json");
}

var lineFunction = d3.line()
    .x(function (d) {
        return projection_([d[1], d[0]])[0];
    })
    .y(function (d) {
        return projection_([d[1], d[0]])[1];
    }).curve(d3.curveCatmullRom.alpha(0.5));


function renderLines() {
    $.getJSON(traj, function (json) {
        for (let l = 0; l < 8; l++) {
            p_ = [];
            lats = json[l][0];
            longs = json[l][1];
            for (let i = 0; i < lats.length; i++) {
                p_.push([lats[i], longs[i]]);
            }
            p.push(p_);
        }
    });
    console.log(path_p);
    for (let i = 0; i < 80000; i += 50) {
        g.append("path")
            .attr("d", lineFunction(path_p[i]))
            .attr("stroke", "red")
            .attr("stroke-width", 0.2)
            .attr("fill", "none");
    }
}
