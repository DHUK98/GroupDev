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

function u_cluster2(n) {
    return n;
}

function u_cluster(data_l, num_clust) {
    console.log("cluster");
    let out;
    $.ajax({
        url: '/cluster/req/' + iid + "/" + num_clust,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data__) {
            out = JSON.parse(data__);
            console.log(out["labels"]);
            console.log(out["centroids"]);
            let weight = [];
            for (let j = 1; j <= new Set(out["labels"]).size; j++) {
                weight[j - 1] = out["labels"].filter(x => x == j).length;
            }
            console.log("WWW", weight);
            let d = {"lat": out["centroids"][0], "lon": out["centroids"][1]};
            console.log(d);
            renderLines(d, weight);
            console.log(applyMask2(out["labels"], data));
        },
        data: JSON.stringify([JSON.stringify(data_l), "ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json"])
    });

}

function calculate() {
    console.log(stack_f);
    let return_stack = [];
    for (let i = 0; i < stack_f.length; i++) {
        if (i == stack_f.length - 1 && stack_f[i].toString().includes("cluster")) {
            let comb = combine_mask(return_stack);
            let n = stack_f[i]();
            u_cluster(comb, n);
            return;
        } else {
            let r = stack_f[i]();
            return_stack.push(r);
        }
    }

    let comb = combine_mask(return_stack);
    // let d = applyMask(data,comb);
    renderLines(d);
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

function applyMask2(mask, d) {
    console.log("data", d);
    let lat = d["lat"];
    let lon = d["lon"];
    let time = d["time"];
    let height = d["height"];
    let pressure = d["pressure"];

    let out = [];
    for (let j = 1; j <= new Set(mask).size; j++) {
        let n_lat = [];
        let n_lon = [];
        let n_time = [];
        let n_height = [];
        let n_pressure = [];
        for (let i = 0; i < mask.length; i++) {
            if (mask[i] == j) {
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

        out.push(json);

    }
    $('#json-renderer').jsonViewer(out[0], {collapsed: true, withQuotes: true, withLinks: false});

    return out;
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
