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
        // Scale up percantage input to units of distance in projection
        let d_s = document.getElementById("sec_dist_val").value * 2.5;
        let t_h = document.getElementById("sec_threshold_val").value;

        //Check inputs are of right type
        if( (s_a >= 0 && s_a <= 360)
            && (e_a >= 0 && e_a <= 360)
            && (d_s > 0 && d_s <= 0)
            && (t_h > 0 && t_h%1 === 0)){
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
        } else{
            let alert_msg = "";
            if(s_a <= 0){
                alert_msg = alert_msg.concat("Please enter a positive value for the start angle.\n")
            }
            if(e_a <= 0){
                alert_msg = alert_msg.concat("Please enter a positive value for the end angle.\n")
            }
            if(d_s <= 0){
                alert_msg = alert_msg.concat("Please enter a positive value for the distance.\n")
            }
            if(!(t_h > 0 && t_h%1 === 0)){
                alert_msg = alert_msg.concat("Please enter a positive integer for the threshold.\n")
            }
            if(alert_msg === ""){
                alert_msg = alert_msg.concat("Unexpected input.");
        }
        alert(alert_msg);
        }
    }
};


// CLUSTERING KMEANS

document.getElementById("add_cluster_kmeans").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "zstack_cluster");


    //  Assign variable for cluster number (user input)
    let c_nu = document.getElementById("number_of_cluster").value;

    //  Check input is of correct type
    if (c_nu > 0 && c_nu%1 === 0) {
        z.innerHTML = "K-means Cluster (" + c_nu + ")";
        let stack = document.getElementById("stack");
        let element = $('#stack #zstack_cluster');

        if (!element.length > 0) {
            stack.appendChild(z);

            stack_f.push([function () {
                return u_cluster2_kmeans(c_nu);
            }, 100]);
            stack_f.sort(sortFunction)
        }
    //  Alert user to incorrect type
    } else {
        alert("Please enter a positive integer for the cluster number.");
    }
}


// CLUSTERING DBSCAN

document.getElementById("add_cluster").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "zstack_cluster");

    // REDUNDANT LINE IF WE'RE USING DBSCAN
    // let c_nu = document.getElementById("number_of_cluster").value;

    //  Assign variables for eps (max distance between 2 points to be considered in same cluster)
    //  and min cluster size (user input)
    let min_samp = document.getElementById("minimum_samples_for_cluster").value;
    let eps_val = document.getElementById("eps_value").value;

    //Check inputs are of correct type
    if(min_samp > 0 && min_samp%1 === 0 && eps_val > 0) {
        z.innerHTML = "DBScan Cluster (" + min_samp + ", " + eps_val + ")";
        let stack = document.getElementById("stack");
        let element = $('#stack #zstack_cluster');

        if (!element.length > 0) {
            stack.appendChild(z);

            stack_f.push([function () {
                return u_cluster2_dbscan(min_samp, eps_val);
            }, 100]);
            stack_f.sort(sortFunction)
        }
    } else {
        let alert_msg = "";
        if (min_samp <= 0 || min_samp%1 !== 0) {
            alert_msg = alert_msg.concat("Please enter a positive integer for Minimum Samples for Cluster\n");
        }
        if (eps_val <= 0) {
            alert_msg = alert_msg.concat("Please enter a positive value for the EPS Value.\n");
        }
        if(alert_msg === ""){
            alert_msg = alert_msg.concat("Unexpected input.");
        }
        alert(alert_msg);
    }
};

// document.getElementById("add_cluster_kmeans").onclick = function () {
//     let z = document.createElement('li'); // is a node
//     z.setAttribute("id", "zstack_cluster_2");
//
//     let c_nu = document.getElementById("number_of_cluster").value;
//
//     // let min_samp = document.getElementById("minimum_samples_for_cluster").value;
//     // let eps_val = document.getElementById("eps_value").value;
//
//     z.innerHTML = "Cluster (" + c_nu + ")";
//     let stack = document.getElementById("stack");
//     let element = $('#stack #zstack_cluster');
//
//     if (!element.length > 0) {
//         stack.appendChild(z)
// ;
//         stack_f.push([function () {
//             return u_cluster2_dbscan(c_nu);
//         }, 100]);
//         stack_f.sort(sortFunction)
//     }
// };


document.getElementById("add_filter").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.setAttribute("id", "stack_filter");

    let type = document.getElementById("filter_option");
    let type_f = type.options[type.selectedIndex].value;
    let max = document.getElementById("filter_max_val").value;
    let min = document.getElementById("filter_min_val").value;
    let thresh = document.getElementById("filter_thresh_val").value;

    //INPUT CHECKING FOR FILTERING WILL DEPEND ON TYPE - ONE TO LOOK AT LATER

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
    localStorage.clear();
    calculate()
};


function Delete(currentEl) {
    currentEl.parentNode.parentNode.removeChild(currentEl.parentNode);
}

let download_button = document.getElementById('export_data_button').onclick = function () {
    zip_files();
    console.log("TEEEEE");
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