let el = document.getElementById('stack');
new Sortable(el, {
    animation: 150
});
document.getElementById("add_sector").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.innerHTML = "<button class='w3-button w3-white' id='stack_sector' onclick='Delete(this)' ali>x</button>" + "\tSector";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_sector');
    if (element.length > 0) {
    } else {
        let url = "/sector/" + iid +
            "/" + document.getElementById("start_angle_val").value + "/" + document.getElementById("end_angle_val").value +
            "/" + document.getElementById("sec_dist_val").value + "/" + document.getElementById("sec_threshold_val").value;
        if (url.includes("//"))
            return;
        stack.appendChild(z);

        $.get(url, function (data, status) {
            document.getElementById("test_out").innerHTML = data;
        });
    }

}
document.getElementById("add_cluster").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.innerHTML = "<button class='w3-button w3-white' id='stack_cluster' onclick='Delete(this)' ali>x</button>" + "\tCluster";
    let stack = document.getElementById("stack");
    let element = $('#stack #cluster');
    if (element.length > 0) {
    } else {
        stack.appendChild(z)
        let url = "/cluster/" + iid;
        $.get(url, function (data, status) {
            processCentroids(data);
            document.getElementById("test_out").innerHTML = data;
        });
    }
}

document.getElementById("add_height_filter").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.innerHTML = "<button class='w3-button w3-white' id='stack_heightfilter' onclick='Delete(this)' ali>x</button>" + "\tHeight Filter";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_heightfilter');
    if (element.length > 0) {
    } else {
        stack.appendChild(z)
    }
}


function Delete(currentEl) {
    currentEl.parentNode.parentNode.removeChild(currentEl.parentNode);
}

function processCentroids(json){
    console.log(json["centroids"]);
    let centroids = json["centroids"];
    let num = centroids.length;
}