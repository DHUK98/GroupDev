let data_utils = {
    data_manager: class {
        constructor(id, names) {
            this.id = id;
            this.names = names;
            this.data = [];
        }

        load() {
            for (let i = 0; i < this.names.length; i++) {
                let path = this.get_path_for(id,this.names[i]);
                $.getJSON(path, function (j) {
                    data = j;
                });
            }
        }

        get_path_for(id, name) {
            let p = "{{ url_for('static', filename='stations/1/2') }}".replace("1", id).replace("2", name);
        }
    }
};