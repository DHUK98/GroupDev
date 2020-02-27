// new Sortable(el, {
//     animation: 150,
//     onEnd: function (evt) {
//         let itemEl = evt.item;  // dragged HTMLElement
//         let target = evt.originalEvent.target;
//         if (el !== target && el.contains(target))
//             array_move(stack_f, evt.oldIndex, evt.newIndex);
//     },
//     removeOnSpill: true,
//     onSpill: function (evt) {
//         if (stack_f.length > 1) {
//             stack_f.splice(evt.oldIndex, 1);
//         } else {
//             stack_f = [];
//         }
//         console.log(evt.oldIndex, stack_f);
//     },
// });
//
//
// function array_move(arr, old_index, new_index) {
//     console.log("MOVE");
//     if (new_index >= arr.length) {
//         let k = new_index - arr.length + 1;
//         while (k--) {
//             arr.push(undefined);
//         }
//     }
//     arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
//     return arr; // for testing
// };
//
//
//
//
//
//
// function exportJson(el) {
//     var obj = {
//         a: 123,
//         b: "4 5 6"
//     };
//     var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));
//
//     el.setAttribute("href", "data:" + data);
//     el.setAttribute("download", "data.json");
// }
//
// var lineFunction = d3.line()
//     .x(function (d) {
//         return projection_([d[1], d[0]])[0];
//     })
//     .y(function (d) {
//         return projection_([d[1], d[0]])[1];
//     }).curve(d3.curveCatmullRom.alpha(0.5));
//
//
// function renderLines() {
//     $.getJSON(traj, function (json) {
//         for (let l = 0; l < 8; l++) {
//             p_ = [];
//             lats = json[l][0];
//             longs = json[l][1];
//             for (let i = 0; i < lats.length; i++) {
//                 p_.push([lats[i], longs[i]]);
//             }
//             p.push(p_);
//         }
//     });
//     console.log(path_p);
//     for (let i = 0; i < 80000; i += 50) {
//         g.append("path")
//             .attr("d", lineFunction(path_p[i]))
//             .attr("stroke", "red")
//             .attr("stroke-width", 0.2)
//             .attr("fill", "none");
//     }
// }
