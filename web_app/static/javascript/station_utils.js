// method to be used to sort the stack from lowest to highest [1,2,3,...,n]
function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    } else {
        return (a[0] > b[0]) ? -1 : 1;
    }
}

function convert_cluster_jsons(current_data) {
    for (let i = 0; i < current_data.length; i++) {
        console.log("sending json to netcdf");
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
