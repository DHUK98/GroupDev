function angle_between_points(p1_x, p1_y, p2_x, p2_y) {
    return Math.atan2(p2_y - p1_y, p2_x - p1_x) * 180 / Math.PI;
}

function angle_between(n, a, b) {
    n = (360 + (n % 360)) % 360;
    a = (3600000 + a) % 360;
    b = (3600000 + b) % 360;

    if (a < b)
        return a <= n && n <= b;
    return a <= n || n <= b;
}

function is_P3_between_P1_and_P2(p1, p2, p3)
{
  let p1_p2, p1_p3;
  p1_p2 = fmod(p2 - p1 + 360, 360);
  p1_p3 = fmod(p3 - p1 + 360, 360);

  return (p1_p2 <= 180) != (p1_p3 > p1_p2);
}

function sector(x, y, eeaa, ssaa, dist) {
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
    start_angle -= 90;
    end_angle += 90;
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



function filter(data,var_, min, max,thresh){
    d = data[var_];
    let r = [];
    for(let i = 0; i < d.length; i ++){
        let cur_traj = d[i];
        let out = 0;
        for(let k = 0; k < cur_traj.length; k++){
            if(cur_traj[k] > max || cur_traj[k] < min){
                out += 1;
            }
            if(out > thresh){
                r.push(0);
                break;
            }
        }
        if(out <= thresh){
            r.push(1);
        }
    }
    return r;
}