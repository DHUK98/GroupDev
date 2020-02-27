let el = document.getElementById('stack');

document.getElementById("add_sector").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "stack_sector");
    z.innerHTML = "Sector";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_sector');
    if (element.length > 0) {
    } else {
        let s_a = document.getElementById("start_angle_val").value;
        let e_a = document.getElementById("end_angle_val").value;
        let d_s = document.getElementById("sec_dist_val").value * 2.5;
        let t_h = document.getElementById("sec_threshold_val").value;
        let url = "/sector/" + iid +
            "/" + s_a + "/" + e_a +
            "/" + d_s + "/" + t_h;
        if (url.includes("//"))
            return;
        renderSector(s_a, e_a, d_s);

        stack.appendChild(z);
        stack_f.push([function () {
            return u_sector(data, s_a, e_a, d_s, t_h);
        }, 1]);
        stack_f.sort(sortFunction);
    }
};

document.getElementById("add_cluster").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "zstack_cluster");
    let c_nu = document.getElementById("number_of_cluster").value;
    z.innerHTML = "Cluster (" + c_nu + ")";
    let stack = document.getElementById("stack");
    let element = $('#stack #zstack_cluster');
    if (!element.length > 0) {
        stack.appendChild(z)

        stack_f.push([function () {
            return u_cluster2(c_nu);
        }, 100]);
        stack_f.sort(sortFunction);
    }
};

document.getElementById("add_filter").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "stack_filter");

    let type = document.getElementById("filter_option");
    let type_f = type.options[type.selectedIndex].value;
    let max = document.getElementById("filter_max_val").value;
    let min = document.getElementById("filter_min_val").value;
    let thresh = document.getElementById("filter_thresh_val").value;
    z.innerHTML = "Filter by " + type_f + "<br/><br/>[min/max/thresh : " + min + "/" + max + "/" + thresh + "]";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_filter');
    stack.appendChild(z);
    stack_f.push([function () {
        return u_filter(data, type_f, min, max, thresh);
    }, 1]);
    stack_f.sort(sortFunction);
};

document.getElementById("calculate").onclick = function () {
    calculate()
};


function Delete(currentEl) {
    currentEl.parentNode.parentNode.removeChild(currentEl.parentNode);
}

let download_button = document.getElementById('export_data_button').onclick = function () {
    zip_files();
};


function zip_files() {
    console.log("zip_files javascript function");
    $.ajax({
        url: '/zip_netcdf_exports',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log("About to download");
            window.open("/static/netcdf_export/download.zip", '_self');
        },
        data: ""
    });
}