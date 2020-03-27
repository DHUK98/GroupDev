// method to be used to sort the stack from lowest to highest [1,2,3,...,n]
function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    } else {
        return (a[0] > b[0]) ? -1 : 1;
    }
}



function u_cluster2_dbscan(min_samp, eps_val) {
    let params = [min_samp, eps_val];
    return params
}


function dbscan_cluster_func(data_l, params) {
    let min_samp = params[0];
    let eps_val = params[1];

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

function kmeans_cluster_func(data_l, num_clust) {
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
                let d = {"lat": out["centroids"][0], "lon": out["centroids"][1], "labels": out["labels"]};
                resolve(d);
            },
            data: JSON.stringify(JSON.stringify(data_l))
        })
    });
}

function filter(var_,min,max,thresh){

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

function downloadObjectAsJson(exportObj, exportName) {
    let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    let downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}
