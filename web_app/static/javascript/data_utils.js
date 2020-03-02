let data_utils = {
    data_manager: class {
        constructor(id, names) {
            this.id = id;
            this.names = names;
            this.data = [];
            this.loaded = 0;
        }

        load() {
            let p = [];
            let l_data = [];

            for (let i = 0; i < this.names.length; i++) {
                console.log(i);

                p.push($.getJSON(this.names[i], function (d) {
                    l_data.push(d);
                }));
            }
            return Promise.all(p).then(() => {
                this.data = l_data;
            });
        }

    },
};