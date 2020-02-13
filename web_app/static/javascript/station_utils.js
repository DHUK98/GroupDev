let stack_f = [];

function u_sector(data, start_ang, end_ang, dist, thresh) {
    console.log("sector");
    console.log("data", start_ang, end_ang, dist, thresh);
    let out = sector_trajecotory(data, start_ang, end_ang, dist, thresh);
    console.log(out);
    console.log(out.filter(x => x == 1).length);
    return out;
}

function u_filter(data, type, min,max, thresh) {
    console.log("filter " + type);
    let out = filter(data, type, min,max, thresh);
    console.log(out);
    console.log(out.filter(x => x == 1).length);
    return out;
}

function u_cluster() {
    console.log("cluster");

}

function calculate() {
    console.log(stack_f);
    let return_stack = [];
    for (let i = 0; i < stack_f.length; i++) {
        let r = stack_f[i]();
        return_stack.push(r);
    }
    console.log(return_stack);
    let combine = []
    for (let i = 0; i < return_stack[0].length; i++) {
        let a = 0;
        for(let c = 0; c < return_stack.length-1; c++){
             a += return_stack[c][i];
        }
        if (a == 3) {
            combine.push(1);
        } else {
            combine.push(0);
        }
    }
    console.log(combine);
    renderLines(combine);
}