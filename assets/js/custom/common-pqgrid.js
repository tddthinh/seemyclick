const commonPQGrid = {
    filter: {
        filterWidget(options) {
            let filter = {
                type: 'select',
                on: true,
                attr: "multiple",
                style: "height:18px;",
                condition: "range",
                valueIndx: "value",
                labelIndx: "label",
                listeners: ['change'],
                init: function (ui) {
                    const {column, dataIndx} = ui;
                    $(this).pqSelect({
                        checkbox: true,
                        radio: true,
                        width: '100%'
                    });
                    pqselect = $(this).data('paramquery-pqSelect');
                    $search_div1 = pqselect.$popupCont.find(".pq-select-search-div1").detach();
                    pqselect.$popupCont.find(".ui-icon.ui-icon-search").after($search_div1);
                },
                ...options
            }
            return filter;
        },
        selectFilter(grid, dataIndx) {
            let column = grid.getColumn({
                dataIndx: dataIndx
            });
            let valueToLabel = _.mapValues(_.keyBy(column.editor.options, "value"), "label")
            let uniqData = _.uniq(_.flatMap(grid.getData({ dataIndx: [dataIndx] }), dataIndx));
            let options = _.flatMap(uniqData, e => { return { value: e, label: valueToLabel[e] } })
            let filter = column.filter;
            filter.cache = null;
            filter.options = options;
        },
        checkboxFilter(grid, dataIndx) {
            let column = grid.getColumn({
                dataIndx: dataIndx
            });
            let filter = column.filter;
            filter.cache = null;
            filter.options = [
                { value: true, label: "Y" },
                { value: false, label: "N" }
            ];
        },
        textFilter(grid, dataIndx) {
            let column = grid.getColumn({
                dataIndx: dataIndx
            });
            let uniqData = _.uniq(_.flatMap(grid.getData({ dataIndx: [dataIndx] }), dataIndx));
            let options = _.flatMap(uniqData, e => { return { value: e, label: e } })
            let filter = column.filter;
            filter.cache = null;
            filter.options = options;
        },
        apply: function(options){
            let columnModel = options.colModel;
            columnModel.forEach(column => {
                let filterOptions = column.filter;
                column.filter = this.filterWidget(options, filterOptions);
            });
        },
        refresh(grid, dataIndxList = []) {
            let columnModel = grid.options.colModel;
            columnModel.forEach(column => {
                if(dataIndxList.length > 0 && !dataIndxList.includes(column.dataIndx)) return;
                if(column.editor?.type === 'select'){
                    this.selectFilter(grid, column.dataIndx);
                }
                if(column.type === 'checkbox'){
                    this.checkboxFilter(grid, column.dataIndx);
                }
                if(column.type === 'text'){
                    this.textFilter(grid, column.dataIndx);
                }
            });
        }
    },
    render: {
        apply: function(options){
            colModel = options.colModel;
            colModel.forEach(column => {
                if(column.type === 'checkbox'){
                    this.checkbox(column);
                }
            });
        },
        checkbox(column) {
            if(column.cb?.header){
                column.title =  `<input class="form-check-input" type="checkbox"/>${column.title ? `&nbsp;${column.title}` : ''}`;
            }
            column.render = function (ui) {
                return {
                    text: `<input class="form-check-input" type="checkbox" ${!!ui?.cellData ? 'checked' : ''}/>`
                };
            }
        }
    },
    event: {
        addExpandEvent: function(grid){
            let options = grid.options;
            let expand = options.collapsible.expand;
            if(!expand) return;
            grid.on("expandDone",function(){
                setTimeout(() => {
                    expand.apply(this,arguments);
                }, 10);
            });
        },
        addCollapseEvent: function(grid){
            let options = grid.options;
            let collapse = options.collapsible.collapse;
            if(!collapse) return;

            grid.on("collapseDone",function(){
                setTimeout(() => {
                    collapse.apply(this,arguments);
                }, 10);
            });
        },
        apply: function(grid){
            this.addExpandEvent(grid);
            this.addCollapseEvent(grid);
        }
    },
    toolbar: {
        apply: function(options){
            const BUTTONS = {
                add:        `<button type="button" class="btn btn-primary btn-floating" data-mdb-ripple-init data-mdb-tooltip-init title="Add a new row"><i class="fas fa-circle-plus"></i></button>`,
                delete:     `<button type="button" class="btn btn-primary btn-floating" data-mdb-ripple-init data-mdb-tooltip-init title="Delete selected rows"><i class="fas fa-trash-can"></i></button>`,
                copy:       `<button type="button" class="btn btn-primary btn-floating" data-mdb-ripple-init data-mdb-tooltip-init title="Copy selected rows"><i class="far fa-clone"></i></button>`,
                screenshot: `<button type="button" class="btn btn-primary btn-floating" data-mdb-ripple-init data-mdb-tooltip-init title="Screenshot and add as a new row"><i class="fas fa-camera"></i></button>`
            };

            (options?.toolbar?.items || []).forEach(item => {
                if(!item?.button) return;
                item.type = BUTTONS[item.button] || item.type;
                item.listener = { 'click': item.listener || function(){} };
            });
        }
    },
    init(gridId, options) {
        commonPQGrid.render.apply(options);
        commonPQGrid.filter.apply(options);
        commonPQGrid.toolbar.apply(options);
        let grid = pq.grid(gridId, options);
        commonPQGrid.event.apply(grid);

        if(!grid.iRefresh._o_refresh){
            grid.iRefresh._o_refresh = grid.iRefresh.refresh;
        }
        grid.iRefresh.refresh = function(){
            commonPQGrid.filter.refresh(grid);
            grid.iRefresh._o_refresh.apply(this,arguments);
        }

        grid.refresh();
        return grid;
    }
}

if (typeof window !== 'undefined') {
    window.commonPQGrid = commonPQGrid;
}