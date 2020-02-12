function angle_between_points(p1_x, p1_y, p2_x, p2_y) {
    return Math.atan2(p2_y - p1_y, p2_x - p1_x) * 180 / Math.PI;
}

function angle_between(n, a, b) {
    n = (360 + (n % 360)) % 360;
    a = (3600000 + a) % 360;
    b = (3600000 + b) % 360;
    a += 90;
    b += 90;
    n += 90;
    if (a < b)
        return a <= n && n <= b;
    return a <= n || n <= b;
}
function sector(x, y, ssaa, eeaa, dist) {
    let point_ang = angle_between_points(0, 0, x, y);

    let a = 0 - x;
    let b = 0 - y;
    let d = Math.sqrt(a * a + b * b);
    // if (d > dist) {
    //     return false;
    // }
    // console.log(ssaa, eeaa, point_ang);

    return angle_between(point_ang, ssaa, eeaa);
}

function sector_trajecotory(data, start_angle, end_angle, dist, thresh) {
    let output = [];
    let lat = data["lat"];
    let lon = data["lon"];
    for (let i = 0; i < lat.length; i++) {
        let outside = 0;
        for (let j = 0; j < lat[i].length; j++) {
            if (outside > thresh) {
                break;
            }
            let start = projection_([lon[0][0], lat[0][0]]);
            let t_traj = projection_([lon[i][j], lat[i][j]]);
            t_traj[0] -= start[0];
            t_traj[1] -= start[1];

            if (!sector(t_traj[1], t_traj[0], start_angle, end_angle, dist)) {
                outside += 1;
            }
        }
        if (outside <= thresh) {
            output.push(1);
        } else {
            output.push(0);
        }
    }
    return output;
}
