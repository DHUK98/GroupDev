let stack_f = [];

function u_sector(data, start_ang, end_ang, dist, thresh) {
    console.log("sector");
    console.log("data", start_ang, end_ang, dist, thresh);
    let out = sector_trajecotory(data, start_ang, end_ang, dist, thresh);
    console.log(out);
    console.log(out.filter(x => x==1).length);
    return out;
}

function u_filter(type) {
    console.log("filter " + type);

}

function u_cluster() {
    console.log("cluster");

}

function calculate() {
    console.log(stack_f);

    for (let i = 0; i < stack_f.length; i++) {
        stack_f[i]();
    }
}