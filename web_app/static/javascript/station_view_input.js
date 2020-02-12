let el = document.getElementById('stack');
new Sortable(el, {
    animation: 150,
    onEnd: function (evt) {
        let itemEl = evt.item;  // dragged HTMLElement
        let target = evt.originalEvent.target;
        if (el !== target && el.contains(target))
            array_move(stack_f, evt.oldIndex, evt.newIndex);
    },
    removeOnSpill: true,
    onSpill: function (/**Event*/evt) {
        if (stack_f.length > 1) {
            stack_f.splice(evt.oldIndex, 1);
        } else {
            stack_f = [];
        }
        console.log(evt.oldIndex, stack_f);
    },
});


function array_move(arr, old_index, new_index) {
    if (new_index >= arr.length) {
        let k = new_index - arr.length + 1;
        while (k--) {
            arr.push(undefined);
        }
    }
    arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
    return arr; // for testing
};


document.getElementById("add_sector").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.innerHTML = "Sector";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_sector');
    if (element.length > 0) {
    } else {
        let s_a = document.getElementById("start_angle_val").value;
        let e_a = document.getElementById("end_angle_val").value;
        let d_s = document.getElementById("sec_dist_val").value;
        let t_h = document.getElementById("sec_threshold_val").value;
        let url = "/sector/" + iid +
            "/" + s_a + "/" + e_a +
            "/" + d_s + "/" + t_h;
        if (url.includes("//"))
            return;
        stack.appendChild(z);
        stack_f.push(function () {
            u_sector(data, s_a, e_a, d_s, t_h);
        });
    }

};
document.getElementById("add_cluster").onclick = function () {
    let z = document.createElement('li'); // is a node
    z.innerHTML = "<p id='stack_cluster'>Cluster</p>";
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_cluster');
    if (!element.length > 0) {
        stack.appendChild(z)
        let url = "/cluster/" + iid;
        $.get(url, function (data, status) {
            // processCentroids(data);
            document.getElementById("test_out").innerHTML = data;
        });
        stack_f.push(function () {
            u_cluster();
        });

    }
};

document.getElementById("add_filter").onclick = function () {
    let z = document.createElement('li'); // is a node
    let type = document.getElementById("filter_option");
    let type_f = type.options[type.selectedIndex].value;
    z.innerHTML = "Filter by " + type_f;
    let stack = document.getElementById("stack");
    let element = $('#stack #stack_filter');
    stack.appendChild(z);
    stack_f.push(function () {
        u_filter(type_f);
    });
};

document.getElementById("calculate").onclick = function () {
    calculate()
};


function Delete(currentEl) {
    currentEl.parentNode.parentNode.removeChild(currentEl.parentNode);
}