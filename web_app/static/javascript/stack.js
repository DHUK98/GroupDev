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

        clear() {
            this.function_array = [];
        }

        async calculate() {
            let acc = [];
            for (let i = 0; i < this.function_array.length; i++) {
                let prev = null;
                if (i >= 1) {
                    prev = this.function_array[i - 1];
                }
                await this.function_array[i].compute(prev);
                acc = process_stack.combine_output(acc,this.function_array[i].mask);
                console.log(this.function_array[i].name() + " finished");
                console.log(this.function_array[i].output);
            }
            console.log(acc.filter(x => x!=0).length);
            return this.function_array;
        }
    },


    combine_output: function (a, b) {
        let out = [];
        let b_i = 0;
        if(a.length === 0){
            return b;
        }
        for (let i = 0; i < a.length; i++) {
            if (a[i] === 0) {
                out.push(0);
                if (a.length === b.length) {
                    b_i += 1;
                }
            } else {
                out.push(b[b_i]);
                b_i += 1;
            }
        }
        return out;
    },

    sector: function (start_angle, end_angle, distance, threshold) {
        this.pos = 100;
        this.s_angle = start_angle;
        this.e_angle = end_angle;
        this.d = distance;
        this.thresh = threshold;
        this.output = null;
        this.compute = function (previous) {
            return new Promise((resolve, reject) => {
                this.output = sector_utils.sector_trajecotory(data, this.s_angle, this.e_angle, this.d, this.thresh);
                this.mask = this.output;
                resolve("Finished");
            });
        };
        this.name = function () {
            return "sectoring";
        };
        this.toString = function () {
            return "Start angle: " + this.s_angle + ", End angle: " + this.e_angle + ", Distance: " + this.d + ", Threshold: " + this.thresh;
        };
    },

    filter: function (type, min, max, threshold) {
        this.pos = 100;
        this.type = type;
        this.min = min;
        this.max = max;
        this.thresh = threshold;
        this.output = null;
        this.mask = [];
        this.compute = function (previous) {
            return new Promise((resolve, reject) => {
                this.output = sector_utils.filter(data, this.type, this.min, this.max, this.thresh);
                this.mask = this.output;
                resolve("Finished");
            });
        };
        this.name = function () {
            return "filtering";
        };
        this.toString = function () {
        };
    },

    cluster: function () {
        this.pos = 1;
        this.compute = function (previous) {
            return test_u_cluster(previous.output, 4).then(
                result => {this.output = result; this.mask = this.output["labels"];});
        };
        this.name = function () {
            return "clustering";
        };
        this.toString = function () {
        };
    },

    render: function (data) {

    }
};