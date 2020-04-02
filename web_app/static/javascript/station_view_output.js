function create_graph(x_values, datasets) {

    var ctx = document.getElementById('OutputCanvas');

    options = {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: datasets[1]["x_label"],
            },
          }],
          yAxes: [{
            position: "left",
            scaleLabel: {
              display: true,
              labelString: datasets[1]["y_label"],
            },
          }],
        },
      };

    var chart_out = new Chart(ctx, {
      type: 'line',
      data: {
        labels: x_values,
        datasets: datasets[0]
      },
      options: options
    });


    return chart_out;

}


// example use, make dataset outside function and pass in
// then options is made inside with labels from dataset[1]


times = [0,1,2,3,4,5,6,7,8,9];

datasets = [[{
          data: [9,8,6,5,7,8,9,4,3,2],
          label: "Traj 1",
          borderColor: "#3e95cd",
          fill: false
        }, {
          data: [2,4,6,8,7,5,3,1,8,9],
          label: "Traj 2",
          borderColor: "#8e5ea2",
          fill: false
        }, {
          data: [3,4,6,7,5,3,2,1,1,1],
          label: "Traj 3",
          borderColor: "#3cba9f",
          fill: false
        }, {
          data: [4,2,1,1,2,3,7,1,5,7],
          label: "Traj 4",
          borderColor: "#e8c3b9",
          fill: false
        }, {
          data: [6,3,2,2,7,12,13,8,5,2],
          label: "Traj 5",
          borderColor: "#c45850",
          fill: false
        }],
        {
          x_label: "Time",
          y_label: "Height"
        }
        ];


create_graph(times, datasets);


