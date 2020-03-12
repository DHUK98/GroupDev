let process_stack = {
    stack_sort: function (a, b) {
        if (a.pos === b.pos) {
            return 0;
        } else {
            return (a.pos > b.pos) ? -1 : 1;
        }
    },

    stack: class {
        constructor() {
            this.function_array = [];
        }

        add(f) {
            this.function_array.push(f);
            this.sort();
        }

        remove(f) {
            this.sort();
        }

        sort() {
            this.function_array.sort(process_stack.stack_sort);
        }

        clear(){
            this.function_array = [];
        }

        async calculate() {
            for (let i = 0; i < this.function_array.length; i++) {
                let prev = null;
                if (i >= 1) {
                    prev = this.function_array[i - 1];
                }
                await this.function_array[i].compute(prev);
                console.log("11");
            }
            console.log("compute finished");
            return this.function_array;
        }
    },

    sector: function (start_angle, end_angle, distance, threshold) {
        this.pos = 2;
        this.s_angle = start_angle;
        this.e_angle = end_angle;
        this.d = distance;
        this.thresh = threshold;
        this.output = null;
        this.compute = function (previous) {
            // return "Sectoring with " + this.toString();
            this.output = sector_utils.sector_trajecotory(data, this.s_angle, this.e_angle, this.d, this.thresh);
            return new Promise(resolve => setTimeout(resolve, Math.random() * 1000));
        };
        this.toString = function () {
            return "Start angle: " + this.s_angle + ", End angle: " + this.e_angle + ", Distance: " + this.d + ", Threshold: " + this.thresh;
        };
    },

    filter: function (type, min, max, threshold) {
        this.pos = 2;
        this.type = type;
        this.min = min;
        this.max = max;
        this.thresh = threshold;
        this.output = null;
        this.compute = function (previous) {
            this.output = sector_utils.filter(data, this.type, this.min, this.max, this.thresh);
            return new Promise(resolve => setTimeout(resolve, Math.random() * 1000));
        };
        this.toString = function () {
        };
    },

    cluster: function () {
        this.pos = 1;
        this.compute = function (previous) {
            return this.output = test_u_cluster(previous.output,4).then(data => {
                console.log(data);
            });
        };
        this.toString = function () {
        };
    },
};