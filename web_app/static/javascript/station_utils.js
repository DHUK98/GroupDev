let stack_f = [];

// method to be used to sort the stack from lowest to highest [1,2,3,...,n]
function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    } else {
        return (a[0] > b[0]) ? -1 : 1;
    }
}


function u_sector(data, start_ang, end_ang, dist, thresh) {
    console.log("sector");
    console.log("data", start_ang, end_ang, dist, thresh);
    let out = sector_utils.sector_trajecotory(data, start_ang, end_ang, dist, thresh);

    return out;
}

function u_filter(data, type, min, max, thresh) {
    console.log("filter " + type);
    let out = filter(data, type, min, max, thresh);

    return out;
}

function u_cluster2_dbscan(min_samp, eps_val) {
    let params = [min_samp, eps_val];
    return params
}


function u_cluster_dbscan(data_l, params) {
    let min_samp = params[0]
    let eps_val = params[1]

    console.log("clustering (DBScan)...");
    let out;
    $.ajax({
        url: '/cluster/req/' + iid + "/" + min_samp + "/" + eps_val,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data__) {
            console.log("Clustered sucessfully (DBScan)");
            out = JSON.parse(data__);
            console.log(out["labels"]);
            console.log(out["centroids"]);
            let colours = out["colours"];
            let weight = [];
            for (let j = 1; j <= new Set(out["labels"]).size; j++) {
                weight[j - 1] = out["labels"].filter(x => x == j).length;
            }
            console.log("WWW", weight);
            let d = {"lat": out["centroids"][0], "lon": out["centroids"][1]};
            console.log(d);
            renderLines(d, weight, colours);
            console.log(applyMask2(out["labels"], data));
            console.log("cluster Success");
            document.getElementById("calculate").value = "";
        },
        data: JSON.stringify([JSON.stringify(data_l), "ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json"])
    })
}

function u_cluster2_kmeans(n) {
    return n;
}

function test_u_cluster(data_l, num_clust) {
    console.log("clustering K-means");
    let out;
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/cluster/req/' + iid + "/" + num_clust,
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data__) {
                out = JSON.parse(data__);
                let d = {"lat": out["centroids"][0], "lon": out["centroids"][1], "labels":out["labels"]};
                resolve(d);
            },
            data: JSON.stringify([JSON.stringify(data_l), "ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json"])
        })
    });
}

function u_cluster(data_l, num_clust) {
    console.log("clustering K-means");
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
            let colours = out["colours"];
            let weight = [];
            for (let j = 1; j <= new Set(out["labels"]).size; j++) {
                weight[j - 1] = out["labels"].filter(x => x == j).length;
            }
            console.log("WWW", weight);
            let d = {"lat": out["centroids"][0], "lon": out["centroids"][1]};
            console.log(d);
            renderLines(d, weight, colours);
            console.log(applyMask2(out["labels"], data));
            console.log("cluster Success");
            document.getElementById("calculate").value = "";
        },
        data: JSON.stringify([JSON.stringify(data_l), "ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json"])
    });
}


function calculate() {
    let has_been_clustered = false;

    document.getElementById("calculate").value = "Loading";

    let render_all = document.getElementById("render_all_check").checked;
    if (render_all) {
        console.log("RENDER ALL IS CHECKED");
        render_all_lines2(data);
    }

    console.log(stack_f);
    let return_stack = [];
    for (let i = 0; i < stack_f.length; i++) {
        if (i == stack_f.length - 1 && stack_f[i][0].toString().includes("dbscan")) {
            console.log("In the DBScan Stack if clause");
            let comb = combine_mask(return_stack);

            let dbscan_vars = stack_f[i][0]();
            u_cluster_dbscan(comb, dbscan_vars);
            has_been_clustered = true;
            return;


        } else if (i == stack_f.length - 1 && stack_f[i][0].toString().includes("kmeans")) {
            console.log("In the K-Means Stack if clause");
            let comb = combine_mask(return_stack);
            let n = stack_f[i][0]();
            u_cluster(comb, n);
            has_been_clustered = true;
            return;

        } else {
            console.log(stack_f[i][0].toString());
            let r = stack_f[i][0]();
            return_stack.push(r);
        }
    }

    document.getElementById("calculate").value = "Calculate";


    let comb = combine_mask(return_stack);


    let d = applyMask(comb, data);

    console.log("Return stack is: ");
    console.log(return_stack);

    console.log("Comb is: ");
    console.log(comb);

    console.log("d is: ");
    console.log(d);

    if (!has_been_clustered) {
        render_all_lines(d)
    }
}


if (typeof console != "undefined")
    if (typeof console.log != 'undefined')
        console.olog = console.log;
    else
        console.olog = function () {
        };

console.log = function (message) {
    console.olog(message);
    $('#debugDiv').append('<p>' + message + '</p>');
};
console.error = console.debug = console.info = console.log;


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

function convert_cluster_jsons(current_data) {
    for (let i = 0; i < current_data.length; i++) {
        console.log("sending json to netcdf")
        send_json_to_netcdf(current_data[i], i);
    }

}

function send_json_to_netcdf(single_json, json_index) {
    single_json = JSON.stringify(single_json);
    $.ajax({
        url: '/convert_to_netcdf/' + json_index,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log("json_to_netcdf post success!")
        },
        data: single_json
    });
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
    convert_cluster_jsons(out);
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

function downloadObjectAsJson(exportObj, exportName) {
    let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    let downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}
