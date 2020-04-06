let process_stack = {
    stack_sort: function (a, b) {
        if (a.pos === b.pos) {
            return 0;
        } else {
            return (a.pos > b.pos) ? -1 : 1;
        }
    },

    stack: class {
        /**
         *
         */
        constructor() {
            this.function_array = [];
        }

        /**
         *
         * @param f
         */
        add(f) {
            this.function_array.push(f);
            this.sort();
            for (let i = 0; i < this.function_array.length; i++) {
                this.function_array[i].output = null;
            }
        }

        /**
         *
         * @param f
         */
        remove(id) {
            for (let i = this.function_array.length - 1; i >= 0; --i) {
                if (this.function_array[i].id === id) {
                    this.function_array.splice(i, 1);
                }
            }
            // this.function_array.splice(this.function_array.indexOf(f), 1);
            this.sort();
        }

        /**
         *
         */
        sort() {
            this.function_array.sort(process_stack.stack_sort);
        }

        /**
         *
         */
        clear() {
            this.function_array = [];
        }

        /**
         *
         * @returns {Promise<[]|*[]>}
         */
        async calculate() {
            console.log(this.function_array);
            let accumulated_mask = [];
            let num_funcs = this.function_array.length;
            for (let i = 0; i < num_funcs; i++) {
                let item = $('.stack_item').eq(i);
                console.log(this.function_array[i].name() + " started");


                console.log(item);
                item.LoadingOverlay("show");

                await this.function_array[i].compute(accumulated_mask);
                item.LoadingOverlay("hide");
                item.css("background-color", "#567D46");

                accumulated_mask = process_stack.combine_output(accumulated_mask, this.function_array[i].mask);

                console.log(this.function_array[i].name() + " finished");
                console.log(this.function_array[i].output);
            }
            if (this.function_array[num_funcs - 1].output["lat"]) {
                console.log(accumulated_mask);
                console.log(this.function_array[num_funcs - 1].output);
                render_all_lines(this.function_array[num_funcs - 1].output);
            } else {
                await process_stack.get_data(accumulated_mask).then(data => {
                    console.log("data back");
                    console.log(data);
                    render_all_lines(data);
                });
            }
            return this.function_array;
        }
    },

    /**
     *
     * @param mask
     * @returns {Promise<unknown>}
     */
    get_data: function (mask) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/getdata/' + iid,
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                success: function (d) {
                    resolve(d);
                },
                data: JSON.stringify([mask, ["lat", "lon"]])
            });
        });
    },

    /**
     *
     * @param a
     * @param b
     * @returns {[]|*}
     */
    combine_output: function (a, b) {
        let out = [];
        let b_i = 0;
        if (a.length === 0) {
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

    /**
     *
     * @param start_angle
     * @param end_angle
     * @param distance
     * @param threshold
     */
    sector: function (start_angle, end_angle, distance, threshold) {
        this.pos = 100;
        this.id = Math.floor(Math.random() * 110000);
        this.s_angle = start_angle;
        this.e_angle = end_angle;
        this.d = distance;
        this.thresh = threshold;
        this.output = null;
        this.mask = [];
        this.compute = function (acc) {
            return new Promise((resolve, reject) => {
                $.get(["/sector", iid, "2", this.s_angle, this.e_angle, this.d, this.thresh].join("/"), function (data) {
                    resolve(data);
                });
            }).then(data => {
                this.output = this.mask = data;
            });
        };
        this.name = function () {
            return "sectoring";
        };
        this.toString = function () {
            return "Start angle: " + this.s_angle + ", End angle: " + this.e_angle + ", Distance: " + this.d + ", Threshold: " + this.thresh;
        };
    },

    /**
     *
     * @param type
     * @param min
     * @param max
     * @param threshold
     */
    filter: function (type, min, max, threshold) {
        this.pos = 100;
        this.id = Math.floor(Math.random() * 110000);
        this.type = type;
        this.min = min;
        this.max = max;
        this.thresh = threshold;
        this.output = null;
        this.mask = [];
        this.compute = function (acc) {
            return new Promise((resolve, reject) => {
                $.get(["/filter", iid, "2", this.type, this.min, this.max, this.thresh].join("/"), function (data) {
                    resolve(data);
                });
            }).then(data => {
                this.output = this.mask = data;
            });
        };
        this.name = function () {
            return "filtering_by_" + this.type;
        };
        this.toString = function () {
        };
    },

    /**
     *
     * @param num_clusters
     */
    k_means_cluster: function (num_clusters) {
        this.pos = 1;
        this.id = Math.floor(Math.random() * 110000);
        this.mask = [];
        this.n = num_clusters;
        /**
         *
         * @param acc
         * @returns {Promise<T>}
         */
        this.compute = function (acc) {
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: '/cluster/req/' + iid + "/" + this.n,
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (data__) {
                        let out = JSON.parse(data__);
                        let d = {"lat": out["centroids"][0], "lon": out["centroids"][1], "labels": out["labels"]};
                        resolve(d);
                    },
                    data: JSON.stringify(acc)
                })
            }).then(
                result => {
                    this.output = result;
                    this.mask = this.output["labels"];
                });
        };

        /**
         *
         * @returns {string}
         */
        this.name = function () {
            return "Cluster (K-means)";
        };

        /**
         *
         */
        this.toString = function () {
            return "N: " + this.n;
        };
    },
    dbscan_cluster: function (min_samp, eps) {
        this.pos = 1;
        this.id = Math.floor(Math.random() * 110000);
        this.mask = [];
        this.min_samp = min_samp;
        this.eps = eps;

        /**
         *
         * @param acc
         * @returns {Promise<T>}
         */
        this.compute = function (acc) {
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: '/cluster/req/' + iid + "/" + this.min_samp + "/" + this.eps,
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (data__) {
                        console.log("Clustered sucessfully (DBScan)");
                        out = JSON.parse(data__);

                        let d = {"lat": out["centroids"][0], "lon": out["centroids"][1], "labels": out["labels"]};
                        resolve(d);
                    },
                    data: JSON.stringify(acc)
                })
            }).then(
                result => {
                    this.output = result;
                    this.mask = this.output["labels"];
                });
        };

        /**
         *
         * @returns {string}
         */
        this.name = function () {
            return "Cluster (DBSCAN)";
        };

        /**
         *
         */
        this.toString = function () {
            return "Minimum Samples for cluster " + this.min_samp + ", EPS: " + this.eps;
        };
    },
};