let el = document.getElementById('stack');
let options = {
    valueNames: ['id', 'type', 'info'],
    item: '<li class="stack_item"><p class="id" style="display:none;"><h3 class="type"></h3><p class="info"></p>'
};

let stackList = new List("stack_list", options);


function update_stack_html() {
    stackList.clear();
    for (let i = 0; i < proc_stack.function_array.length; i++) {
        stackList.add({
            id: proc_stack.function_array[i].id,
            type: proc_stack.function_array[i].name(),
            info: proc_stack.function_array[i].toString(),
        });
    }
    let stack_items = $('.stack_item');

    stack_items.click(function () {
        let itemId = $(this).closest('li').find('.id').text();
        stackList.remove('id', itemId);
        $(this).css('cursor', 'pointer');
        proc_stack.remove(parseInt(itemId));
    });
}

document.getElementById("add_sector").onclick = function () {
    let s_a = $('#start_angle_val').val(),
        e_a = $('#end_angle_val').val(),
        d_s = $('#sec_dist_val').val() * 1000,
        t_h = $('#sec_threshold_val').val();

    if (d_s > 0 && t_h >= 0 && t_h % 1 === 0) {
        let url = "/sector/" + iid +
            "/" + s_a + "/" + e_a +
            "/" + d_s + "/" + t_h;
        if (url.includes("//"))
            return;
        renderSector(s_a, e_a, d_s / (20000 * 1000) * 250);

        let sec_test = new process_stack.sector(s_a, e_a, d_s, t_h);
        proc_stack.add(sec_test);
        update_stack_html();
    } else {
        let alert_msg = "";
        if (d_s <= 0) {
            alert_msg = alert_msg.concat("Please enter a positive value for the distance.\n")
        }
        if (!(t_h >= 0 && t_h % 1 === 0)) {
            alert_msg = alert_msg.concat("Please enter a positive integer for the threshold.\n")
        }
        if (alert_msg === "") {
            alert_msg = alert_msg.concat("Unexpected input.");
        }
        alert(alert_msg);
    }
};
// CLUSTERING DBSCAN

document.getElementById("add_cluster").onclick = function () {
    let cluster_type = document.getElementById("cluster_option").value;
    if (cluster_type === "kmeans") {
        let c_nu = document.getElementById("input_k").value;
        let clu_test = new process_stack.k_means_cluster(c_nu);
        proc_stack.add(clu_test);
    } else if (cluster_type === "dbscan") {
        let min_samp = document.getElementById("minimum_samples_for_cluster").value;
        let eps_val = document.getElementById("eps_value").value;
        let clu_test = new process_stack.dbscan_cluster(min_samp,eps_val);
        proc_stack.add(clu_test);
    }
    update_stack_html();
};

document.getElementById("add_filter").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "stack_filter");

    let type = document.getElementById("filter_option");
    let type_f = type.options[type.selectedIndex].value;
    let max = document.getElementById("filter_max_val").value;
    let min = document.getElementById("filter_min_val").value;
    let thresh = document.getElementById("filter_thresh_val").value;


    proc_stack.add(new process_stack.filter(type_f, min, max, thresh));
    update_stack_html();
};

document.getElementById("load_data_button").onclick = function () {
    let boxes = $(".data_tickbox");
    let key_ticked = [];
    let ticked = [];
    console.log(boxes);
    boxes.each(function (index) {
        let x = $(this).prop('checked');
        let id = index;
        if (x) {
            ticked.push(parseInt(id));
        }
    });
    console.log(ticked);
    $.ajax({
        url: '/load_data/' + iid + "/",
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (d) {
            console.log("data loaded");
        },
        data: JSON.stringify([ticked])
    });
};


document.getElementById("calculate").onclick = function () {
    proc_stack.calculate();
};

function Delete(currentEl, name) {
    proc_stack.remove(name);
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

function chooseClusterType() {
    let cluster_type = document.getElementById("cluster_option").value;
    let container = document.getElementById("cluster_inputs");
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }
    container.appendChild(document.createElement("br"));
    if (cluster_type === "kmeans") {
        container.appendChild(document.createTextNode("Cluster number:"));
        let input_k = document.createElement("input");
        input_k.type = "number";
        input_k.id = "input_k";
        input_k.className = "w3-input";
        container.appendChild(input_k);
        container.appendChild(document.createElement("br"));
    } else if (cluster_type === "dbscan" || cluster_type === "dbscan_kmeans") {
        if (cluster_type === "dbscan_kmeans") {
            container.appendChild(document.createTextNode("Cluster number:"));
            let input_k = document.createElement("input");
            input_k.type = "number";
            input_k.id = "input_k";
            input_k.className = "w3-input";
            container.appendChild(input_k);
            container.appendChild(document.createElement("br"));
        }
        container.appendChild(document.createTextNode("Minimum Samples for cluster"));
        let input_minsamp = document.createElement("input");
        input_minsamp.type = "number";
        input_minsamp.id = "minimum_samples_for_cluster";
        input_minsamp.className = "w3-input";
        container.appendChild(input_minsamp);
        container.appendChild(document.createElement("br"));

        container.appendChild(document.createTextNode("EPS Value (neighbourhood point radius)"));
        let input_eps = document.createElement("input");
        input_eps.type = "number";
        input_eps.id = "eps_value";
        input_eps.className = "w3-input";
        container.appendChild(input_eps);
        container.appendChild(document.createElement("br"));
    }
    let content = document.getElementById('cluster_container');
    let val = content.scrollHeight + "px";
    content.style.maxHeight = val;
}

function updateRangeSlider(val) {
    document.getElementById('distance_label').innerHTML = "Distance: " + numberWithCommas(val) + "km";
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}