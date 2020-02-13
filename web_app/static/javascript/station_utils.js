let stack_f = [];

function u_sector(data, start_ang, end_ang, dist, thresh) {
    console.log("sector");
    console.log("data", start_ang, end_ang, dist, thresh);
    let out = sector_trajecotory(data, start_ang, end_ang, dist, thresh);
    console.log(out);
    console.log(out.filter(x => x == 1).length);
    return out;
}

function u_filter(data, type, min, max, thresh) {
    console.log("filter " + type);
    let out = filter(data, type, min, max, thresh);
    console.log(out);
    console.log(out.filter(x => x == 1).length);
    return out;
}

function u_cluster(data, num_clust) {
    console.log("cluster");
    // $.post("/cluster/req/", data);
    // $.ajax({
    //     type: 'POST',
    //     url: "/cluster/req",
    //     dataType: "json",
    //     data: {mask: [1, 1, 0]},
    //     success: function (data) {
    //         alert("huraa");
    //     }
    // });
    $.ajax({
        url: '/cluster/req/'+iid,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            alert(data);
        },
        data: JSON.stringify([JSON.stringify(data),"ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json"])
    });

}

function calculate() {
    console.log(stack_f);
    let return_stack = [];
    for (let i = 0; i < stack_f.length; i++) {
        let r = stack_f[i]();
        return_stack.push(r);
    }
    console.log(return_stack);

    let comb = combine_mask(return_stack);
    let f = applyMask(comb, data);

    // renderLines(f);
    u_cluster(comb, 8);
}

function combine_mask(masks) {
    let combined = [];
    for (let i = 0; i < masks[0].length; i++) {
        let o = 0;
        for (let m = 0; m < masks.length; m++) {
            o += masks[m][i];
        }
        if (o == masks.length) {
            combined.push(1);
        } else {
            combined.push(0);
        }
    }
    return combined;
}

function applyMask(mask, d) {
    let lat = d["lat"];
    let lon = d["lon"];
    let time = d["time"];
    let height = d["height"];
    let pressure = d["pressure"];

    let n_lat = [];
    let n_lon = [];
    let n_time = [];
    let n_height = [];
    let n_pressure = [];
    for (let i = 0; i < mask.length; i++) {
        if (mask[i] == 1) {
            n_lat.push(lat[i]);
            n_lon.push(lon[i]);
            n_time.push(time[i]);
            n_height.push(height[i]);
            n_pressure.push(pressure[i]);
        }
    }
    let json = {
        "lat": n_lat,
        "lon": n_lon,
        "time": n_time,
        "height": n_height,
        "pressure": n_pressure
    };

    return JSON.stringify(json);
}
