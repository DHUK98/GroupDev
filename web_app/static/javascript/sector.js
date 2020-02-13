var netcdf4 = require("netcdf4");

function fmod(dividend, divisor) {
    var multiplier = 0;

    while (divisor * multiplier < dividend) {
        ++multiplier;
    }

    --multiplier;

    return dividend - (divisor * multiplier);
}


function is_P3_between_P1_and_P2(p1, p2, p3) {
    let p1_p2 = fmod(p2 - p1 + 360, 360);
    let p1_p3 = fmod(p3 - p1 + 360, 360);

    return (p1_p2 <= 180) != (p1_p3 > p1_p2);
}

function angle_between_points(p1_x, p1_y, p2_x, p2_y) {
    return Math.atan2(p2_y - p1_y, p2_x - p1_x) * 180 / Math.PI;
}


function sector(x, y, start_angle, end_angle, dist) {
    let point_ang = angle_between_points(0, 0, x, y);
    let a = 0 - x;
    let b = 0 - y;
    let d = Math.sqrt(a * a + b * b);
    if (d > dist) {
        return false;
    }
    if (!is_P3_between_P1_and_P2(start_angle, end_angle, point_ang)) {
        return false;
    }
    return true;
}

console.log(sector(10, 10, 0, 90, 14));

function sector_trajecotory(trajs, start_angle, end_angle, dist, thresh) {
    output = [];
    for (let i = 0; i < trajs.length; i++) {
        let outside = 0;
        let cur_traj = traj[i];
        for (let j = 0; j < cur_traj.length; j++) {
            if (outside > 5) {
                break;
            }
            if (!sector(cur_traj[j][0], cur_traj[j][1]), start_angle, end_angle, dist) {
                outside += 1;
            }
        }
        if (outside <= thresh) {
            output.push(cur_traj);
        }
    }
    return output;
}