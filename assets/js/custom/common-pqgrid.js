const commonPQGrid = {
    filter: {
        filterWidget(grid, options) {
            let filter = {
                type: 'select',
                on: true,
                attr: "multiple",
                style: "height:18px;",
                condition: "range",
                valueIndx: "value",
                labelIndx: "label",
                listeners: ['change'],
                init: function () {
                    $(this).pqSelect({
                        checkbox: true,
                        radio: true,
                        width: '100%'
                    });
                    pqselect = $(this).data('paramquery-pqSelect')
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
        refresh(grid) {
            let columnModel = grid.options.colModel;
            columnModel.forEach(column => {
                let filterOptions = column.filter;
                column.filter = this.filterWidget(grid, filterOptions);
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
    init(gridId, options) {
        commonPQGrid.render.apply(options);
        let grid = pq.grid(gridId, options);

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