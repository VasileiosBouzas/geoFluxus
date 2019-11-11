define(['views/common/baseview', 'underscore', 'views/common/flows',
        'collections/gdsecollection', 'models/gdsemodel', 'utils/utils',
        'visualizations/map', 'openlayers', 'bootstrap-select'],

function(BaseView, _, FlowsView, GDSECollection, GDSEModel, utils, Map, ol){
/**
*
* @author Christoph Franke
* @name module:views/FilterFlowsView
* @augments module:views/BaseView
*/
var FilterFlowsView = BaseView.extend(
    /** @lends module:views/FilterFlowsView.prototype */
    {

    /**
    * render view to filter flows, calls FlowsView to render filtered flows on map and in sankey
    *
    * @param {Object} options
    * @param {HTMLElement} options.el                     element the view will be rendered in
    * @param {string} options.template                    id of the script element containing the underscore template to render this view
    * @param {module:models/CaseStudy} options.caseStudy  the casestudy to add layers to
    *
    * @constructs
    * @see http://backbonejs.org/#View
    */
    initialize: function(options){
        var _this = this;
        FilterFlowsView.__super__.initialize.apply(this, [options]);
        _.bindAll(this, 'prepareAreas');

        this.template = options.template;
        this.caseStudy = options.caseStudy;
        this.keyflowId = options.keyflowId;
        this.materials = new GDSECollection([], {
            apiTag: 'materials',
            apiIds: [this.caseStudy.id, this.keyflowId ]
        });
        this.products = new GDSECollection([], {
            apiTag: 'products',
            apiIds: [this.caseStudy.id, this.keyflowId ]
        });
        this.composites = new GDSECollection([], {
            apiTag: 'composites',
            apiIds: [this.caseStudy.id, this.keyflowId ]
        });
        this.processes = new GDSECollection([], {
            apiTag: 'processes'
        });
        this.wastes = new GDSECollection([], {
            apiTag: 'wastes'
        });
        this.activities = new GDSECollection([], {
            apiTag: 'activities',
            apiIds: [this.caseStudy.id, this.keyflowId ],
            comparator: 'name'
        });
        this.activityGroups = new GDSECollection([], {
            apiTag: 'activitygroups',
            apiIds: [this.caseStudy.id, this.keyflowId ],
            comparator: 'name'
        });
        this.actors = new GDSECollection([], {
            apiTag: 'actors',
            apiIds: [this.caseStudy.id, this.keyflowId],
            comparator: 'name'
        })
        this.areaLevels = new GDSECollection([], {
            apiTag: 'arealevels',
            apiIds: [this.caseStudy.id],
            comparator: 'level'
        });
        this.areas = {};

        this.loader.activate();
        var promises = [
            this.activities.fetch(),
            this.activityGroups.fetch(),
            this.materials.fetch(),
            this.products.fetch(),
            this.composites.fetch(),
            this.areaLevels.fetch(),
            this.processes.fetch(),
            this.wastes.fetch()
        ]
        Promise.all(promises).then(function(){
            _this.activities.sort();
            _this.activityGroups.sort();
            _this.loader.deactivate();
            _this.render();
            if (options.callback)
                options.callback();
        })

    },

    /*
    * dom events (managed by jquery)
    */
    events: {
        'click #area-select-button': 'showAreaSelection',
        'change select[name="area-level-select"]': 'changeAreaLevel',
        'change select[name="node-level-select"]': 'resetNodeSelects',
        'change input[name="show-flow-only"]': 'resetNodeSelects',
        'click .area-filter.modal .confirm': 'confirmAreaSelection',
        'click #apply-filters': 'drawFlows'
    },

    /*
    * render the view
    */
    render: function(){
        var _this = this,
            html = document.getElementById(this.template).innerHTML
            template = _.template(html);
        this.el.innerHTML = template({ processes: this.processes, wastes: this.wastes });

        var popovers = this.el.querySelectorAll('[data-toggle="popover"]');
        $(popovers).popover({ trigger: "focus" });

        this.areaModal = this.el.querySelector('.area-filter.modal');
        html = document.getElementById('area-select-modal-template').innerHTML;
        template = _.template(html);
        this.areaModal.innerHTML = template({ levels: this.areaLevels });
        this.areaMap = new Map({
            el: this.areaModal.querySelector('.map'),
        });
        this.areaLevelSelect = this.el.querySelector('select[name="area-level-select"]');
        this.areaMap.addLayer(
            'areas',
            {
                stroke: 'rgb(100, 150, 250)',
                fill: 'rgba(100, 150, 250, 0.5)',
                select: {
                    selectable: true,
                    stroke: 'rgb(230, 230, 0)',
                    fill: 'rgba(230, 230, 0, 0.5)',
                    onChange: function(areaFeats){
                        var modalSelDiv = _this.el.querySelector('.selections'),
                            levelId = _this.areaLevelSelect.value
                            labels = [],
                            areas = _this.areas[levelId];
                        _this.selectedAreas = [];
                        areaFeats.forEach(function(areaFeat){
                            labels.push(areaFeat.label);
                            _this.selectedAreas.push(areas.get(areaFeat.id))
                        });
                        modalSelDiv.innerHTML = labels.join(', ');
                    }
                }
            });
        if (this.areaLevels.length > 0)
            this.changeAreaLevel();

        // event triggered when modal dialog is ready -> trigger rerender to match size
        $(this.areaModal).on('shown.bs.modal', function () {
            _this.areaMap.map.updateSize();
        });
        this.displayLevelSelect = this.el.querySelector('select[name="display-level-select"]');
        this.nodeLevelSelect = this.el.querySelector('select[name="node-level-select"]');
        //this.anonymousSelect = this.el.querySelector('input[name="anonymous"]');
        this.showFlowOnlyCheck = this.el.querySelector('input[name="show-flow-only"]');
        this.groupSelect = this.el.querySelector('select[name="group"]');
        this.activitySelect = this.el.querySelector('select[name="activity"]');
        this.actorSelect = this.el.querySelector('select[name="actor"]');
        this.flowTypeSelect = this.el.querySelector('select[name="level"]');
        this.roleSelect = this.el.querySelector('select[name="role"]');
        //this.aggregateCheck = this.el.querySelector('input[name="aggregateMaterials"]');
        this.processSelect = this.el.querySelector('select[name="process-select"]');
        this.wasteSelect = this.el.querySelector('select[name="waste-select"]');
        this.yearSelect = this.el.querySelector('select[name="year"]');
        this.hazardousSelect = this.el.querySelector('select[name="hazardous"]');
        this.routeSelect = this.el.querySelector('select[name="route"]');
        this.collectorSelect = this.el.querySelector('select[name="collector"]');
        this.cleanSelect = this.el.querySelector('select[name="clean"]');
        this.mixedSelect = this.el.querySelector('select[name="mixed"]');
        this.directSelect = this.el.querySelector('select[name="direct"]');
        //this.avoidableSelect = this.el.querySelector('select[name="avoidable"]');
        $(this.groupSelect).selectpicker();
        $(this.activitySelect).selectpicker();
        $(this.actorSelect).selectpicker();
        $(this.processSelect).selectpicker();
        $(this.wasteSelect).selectpicker();
        this.resetNodeSelects();
        this.renderMatFilter();
        this.renderProFilter();
        this.renderCompFilter();
        this.addEventListeners();
        this.selectedAreas = [];
    },

    drawFlows: function(){
        if (this.flowsView) this.flowsView.close();
        var filter = this.getFilter();
        this.flowsView = new FlowsView({
            el: this.el.querySelector('#flows-render-content'),
            template: 'flows-render-template',
            materials: this.materials,
            actors: this.actors,
            activityGroups: this.activityGroups,
            activities: this.activities,
            caseStudy: this.caseStudy,
            keyflowId: this.keyflowId,
            displayWarnings: true,
            filter: filter
        });
        var displayLevel = this.displayLevelSelect.value;
        this.flowsView.draw(displayLevel);
    },

    resetNodeSelects: function(){
        var level = this.nodeLevelSelect.value,
            hide = [],
            selects = [this.actorSelect, this.groupSelect, this.activitySelect];

        // show the grandparents
        selects.forEach(function(sel){
            sel.parentElement.parentElement.style.display = 'block';
            sel.selectedIndex = 0;
            sel.style.height ='100%'; // resets size, in case it was expanded
        })

        if (level == 'activity'){
            hide = [this.actorSelect];
        }
        if (level == 'activitygroup'){
            hide = [this.actorSelect, this.activitySelect];
        }

        // hide the grandparents
        hide.forEach(function(s){
            s.parentElement.parentElement.style.display = 'none';
        })
        this.renderNodeSelectOptions(this.groupSelect, this.activityGroups);
        if(level != 'activitygroup')
            this.renderNodeSelectOptions(this.activitySelect, this.activities);
        if(level == 'actor')
            this.renderNodeSelectOptions(this.actorSelect);
    },

    changeAreaLevel: function(){
        var levelId = this.areaLevelSelect.value;
        this.selectedAreas = [];
        this.el.querySelector('.selections').innerHTML = this.el.querySelector('#area-selections').innerHTML= '';
        this.prepareAreas(levelId);
    },

    prepareAreas: function(levelId, onSuccess){
        var _this = this;
        var areas = this.areas[levelId];
        if (areas && areas.size() > 0){
            this.drawAreas(areas)
            if (onSuccess) onSuccess();
        }
        else {
            areas = new GDSECollection([], {
                apiTag: 'areas',
                apiIds: [ this.caseStudy.id, levelId ]
            });
            this.areas[levelId] = areas;
            //var loader = new utils.Loader(this.areaModal, {disable: true});
            this.loader.activate();
            areas.fetch({
                success: function(){
                    _this.loader.deactivate();
                    _this.drawAreas(areas);
                    if (onSuccess) onSuccess();
                },
                error: function(res) {
                    _this.loader.deactivate();
                    _this.onError(res);
                }
            });
        }
    },

    drawAreas: function(areas){
        var _this = this;
        this.areaMap.clearLayer('areas');
        areas.forEach(function(area){
            var coords = area.get('geometry').coordinates,
                name = area.get('name');
            _this.areaMap.addPolygon(coords, {
                projection: 'EPSG:4326', layername: 'areas',
                type: 'MultiPolygon', tooltip: name,
                label: name, id: area.id
            });
        })
        this.areaMap.centerOnLayer('areas');
    },

    showAreaSelection: function(){
        $(this.areaModal).modal('show');
    },

    confirmAreaSelection: function(){
        // lazy way to show the selected areas, just take it from the modal
        var modalSelDiv = this.el.querySelector('.selections'),
            selDiv = this.el.querySelector('#area-selections');
        selDiv.innerHTML = modalSelDiv.innerHTML;
        var level = this.nodeLevelSelect.value;
        if (level === 'actor') this.filterActors();
    },

    filterActors: function(){
        var _this = this,
            geoJSONText,
            queryParams = {
                included: 'True',
                fields: ['id', 'name'].join()
            };

        var actors = this.actors,
            activity = this.activitySelect.value,
            group = this.groupSelect.value;

        // take selected activities for querying specific actors
        if(activity >= 0){
            var activities = this.getSelectedNodes(this.activitySelect);
            queryParams['activity__id__in'] = [activities].join(',');
        }
        // or take selected groups if activity is set to 'All'
        else if (group >= 0) {
            var groups = this.getSelectedNodes(this.groupSelect);
            queryParams['activity__activitygroup__id__in'] = [groups].join(',');
        }
        // if there are areas selected merge them to single multipolygon
        // and serialize that to geoJSON
        if (this.selectedAreas && this.selectedAreas.length > 0) {
            var multiPolygon = new ol.geom.MultiPolygon();
            this.selectedAreas.forEach(function(area){
                var geom = area.get('geometry'),
                    coordinates = geom.coordinates;
                if (geom.type == 'MultiPolygon'){
                    var multi = new ol.geom.MultiPolygon(coordinates),
                        polys = multi.getPolygons();
                    polys.forEach( function(poly) {multiPolygon.appendPolygon(poly);} )
                }
                else{
                    var poly = new ol.geom.Polygon(coordinates);
                    multiPolygon.appendPolygon(poly);
                }
            })
            var geoJSON = new ol.format.GeoJSON(),
            geoJSONText = geoJSON.writeGeometry(multiPolygon);
        }
       // area: geoJSONText,
        this.loader.activate({offsetX: '20%'});
        this.actors.postfetch({
            data: queryParams,
            body: { area: geoJSONText },
            success: function(response){
                _this.loader.deactivate();
                _this.actors.sort();
                _this.renderNodeSelectOptions(_this.actorSelect, _this.actors);
                _this.actorSelect.value = -1;
            },
            reset: true
        })
    },

    // filter section: get the selected nodes of selected level
    getSelectedNodes: function(nodeSelect){
        if (!nodeSelect){
            var level = this.nodeLevelSelect.value,
                nodeSelect = (level == 'actor') ? this.actorSelect:
                             (level == 'activity') ? this.activitySelect:
                             this.groupSelect;
        }
        function getValues(selectOptions){
            var values = [];
            for (var i = 0; i < selectOptions.length; i++) {
                var option = selectOptions[i];
                if (option.dataset.divider) continue;
                var id = option.value;
                // ignore 'All' in multi select
                if (id >= 0)
                    values.push(id);
            }
            return values;
        }
        // value will always return the value of the top selected option
        // so if it is > -1 "All" is not selected
        if (nodeSelect.value >= 0){
            selected = nodeSelect.selectedOptions;
            return getValues(selected);
        }
        // "All" is selected -> return values of all options (except "All")
        else {
            // exception: we don't render the actor nodes into the select, if there are too many
            // this.actors contains the filtered actors, return their ids instead
            if (level == 'actor'){
                return this.actors.pluck('id');
            }
            // for group and activity the selected nodes represent the filtering
            return getValues(nodeSelect.options)
        }
    },

    renderNodeSelectOptions: function(select, collection){
        var showFlowOnly = this.showFlowOnlyCheck.checked;
        utils.clearSelect(select);
        var defOption = document.createElement('option');
        defOption.value = -1;
        defOption.text = gettext('All');
        if (collection) defOption.text += ' (' + collection.length + ')';
        select.appendChild(defOption);
        var option = document.createElement('option');
        option.dataset.divider = 'true';
        select.appendChild(option);
        if (collection && collection.length < 2000){
            collection.forEach(function(model){
                var flowCount = model.get('flow_count');
                if (showFlowOnly && flowCount == 0) return;
                var option = document.createElement('option');
                option.value = model.id;
                option.text = model.get('name') + ' (' + flowCount + ' ' + gettext('flows') + ')';
                if (flowCount == 0) option.classList.add('empty');
                select.appendChild(option);
            })
            select.disabled = false;
        }
        else {
            defOption.text += ' - ' + gettext('too many to display');
            select.disabled = true;
        }
        select.selectedIndex = 0;
        $(select).selectpicker('refresh');
    },


    addEventListeners: function(){
        var _this = this;

        function multiCheck(evt, clickedIndex, checked){
            var select = evt.target;
            if(checked){
                // 'All' clicked -> deselect other options
                if (clickedIndex == 0){
                   $(select).selectpicker('deselectAll');
                    select.value = -1;
                }
                // other option clicked -> deselect 'All'
                else {
                    select.options[0].selected = false;
                }
            }
            // nothing selected anymore -> select 'All'
            if (select.value == null || select.value == ''){
                select.value = -1;
            }
            $(select).selectpicker('refresh');
        }

        $(this.groupSelect).on('changed.bs.select', function(evt, index, val){
            multiCheck(evt, index, val);
            var level = _this.nodeLevelSelect.value;

            var filteredActivities = _this.activities;

            // filter activities by group selection if sth different than 'All' is selected
            if (_this.groupSelect.value > 0){
                var groupIds = _this.getSelectedNodes(_this.groupSelect);
                filteredActivities = _this.activities.filterBy({'activitygroup': groupIds});
            }

            _this.renderNodeSelectOptions(_this.activitySelect, filteredActivities);
            // nodelevel actor is selected -> filter actors
            if (level == 'actor')
                _this.filterActors();
        })

        $(this.activitySelect).on('changed.bs.select', function(evt, index, val){
            multiCheck(evt, index, val);
            // nodelevel actor is selected -> filter actors
            if (_this.nodeLevelSelect.value == 'actor')
                _this.filterActors();
        })

        $(this.actorSelect).on('changed.bs.select', multiCheck);

        $(this.processSelect).on('changed.bs.select', multiCheck);
        $(this.wasteSelect).on('changed.bs.select', multiCheck);
    },

    renderMatFilter: function(){
        var _this = this;
        this.selectedMaterial = null;
        // select material
        var matSelect = document.createElement('div');
        matSelect.classList.add('materialSelect');
        var select = this.el.querySelector('.hierarchy-select');

        var compAttrBefore = this.materials.comparatorAttr;
        this.materials.comparatorAttr = 'level';
        this.materials.sort();
        var flowsInChildren = {};
        // count materials in parent, descending level (leafs first)
        this.materials.models.reverse().forEach(function(material){
            var parent = material.get('parent'),
                count = material.get('flow_count') + (flowsInChildren[material.id] || 0);
            flowsInChildren[parent] = (!flowsInChildren[parent]) ? count: flowsInChildren[parent] + count;
        })
        this.materials.comparatorAttr = compAttrBefore;
        this.materials.sort();

        this.matSelect = this.hierarchicalSelect(this.materials, matSelect, {
            onSelect: function(model){
                 _this.selectedMaterial = model;
            },
            defaultOption: gettext('All materials'),
            label: function(model, option){
                var compCount = model.get('flow_count'),
                    childCount = flowsInChildren[model.id] || 0,
                    label = model.get('name') + '(' + compCount + ' / ' + childCount + ')';
                return label;
            }
        });

        var matFlowless = this.materials.filterBy({'flow_count': 0});
        // grey out materials not used in any flows in keyflow
        // (do it afterwards, because hierarchical select is build in template)
        matFlowless.forEach(function(material){
            var li = _this.matSelect.querySelector('li[data-value="' + material.id + '"]');
            if (!li) return;
            var a = li.querySelector('a'),
                cls = (flowsInChildren[material.id] > 0) ? 'half': 'empty';
            a.classList.add(cls);
        })
        this.el.querySelector('#material-filter').appendChild(matSelect);
    },


    renderProFilter: function(){
        var _this = this;
        this.selectedProduct = null;
        // select product
        var proSelect = document.createElement('div');
        proSelect.classList.add('productSelect');
        var select = this.el.querySelector('.hierarchy-select');

        var compAttrBefore = this.products.comparatorAttr;
        this.products.comparatorAttr = 'level';
        this.products.sort();
        var flowsInChildren = {};
        // count materials in parent, descending level (leafs first)
        this.products.models.reverse().forEach(function(product){
            var parent = product.get('parent'),
                count = product.get('flow_count') + (flowsInChildren[product.id] || 0);
            flowsInChildren[parent] = (!flowsInChildren[parent]) ? count: flowsInChildren[parent] + count;
        })
        this.products.comparatorAttr = compAttrBefore;
        this.products.sort();

        this.proSelect = this.hierarchicalSelect(this.products, proSelect, {
            onSelect: function(model){
                 _this.selectedProduct = model;
            },
            defaultOption: gettext('All products'),
            label: function(model, option){
                var compCount = model.get('flow_count'),
                    childCount = flowsInChildren[model.id] || 0,
                    label = model.get('name') + '(' + compCount + ' / ' + childCount + ')';
                return label;
            }
        });

        var proFlowless = this.products.filterBy({'flow_count': 0});
        // grey out materials not used in any flows in keyflow
        // (do it afterwards, because hierarchical select is build in template)
        proFlowless.forEach(function(product){
            var li = _this.proSelect.querySelector('li[data-value="' + product.id + '"]');
            if (!li) return;
            var a = li.querySelector('a'),
                cls = (flowsInChildren[product.id] > 0) ? 'half': 'empty';
            a.classList.add(cls);
        })
        this.el.querySelector('#product-filter').appendChild(proSelect);
    },


    renderCompFilter: function(){
        var _this = this;
        this.selectedComposite = null;
        // select product
        var compSelect = document.createElement('div');
        compSelect.classList.add('compSelect');
        var select = this.el.querySelector('.hierarchy-select');

        var compAttrBefore = this.composites.comparatorAttr;
        this.composites.comparatorAttr = 'level';
        this.composites.sort();
        var flowsInChildren = {};
        // count materials in parent, descending level (leafs first)
        this.composites.models.reverse().forEach(function(composite){
            var parent = composite.get('parent'),
                count = composite.get('flow_count') + (flowsInChildren[composite.id] || 0);
            flowsInChildren[parent] = (!flowsInChildren[parent]) ? count: flowsInChildren[parent] + count;
        })
        this.composites.comparatorAttr = compAttrBefore;
        this.composites.sort();

        this.compSelect = this.hierarchicalSelect(this.composites, compSelect, {
            onSelect: function(model){
                 _this.selectedComposite = model;
            },
            defaultOption: gettext('All composites'),
            label: function(model, option){
                var compCount = model.get('flow_count'),
                    childCount = flowsInChildren[model.id] || 0,
                    label = model.get('name') + '(' + compCount + ' / ' + childCount + ')';
                return label;
            }
        });

        var compFlowless = this.composites.filterBy({'flow_count': 0});
        // grey out materials not used in any flows in keyflow
        // (do it afterwards, because hierarchical select is build in template)
        compFlowless.forEach(function(composite){
            var li = _this.compSelect.querySelector('li[data-value="' + product.id + '"]');
            if (!li) return;
            var a = li.querySelector('a'),
                cls = (flowsInChildren[product.id] > 0) ? 'half': 'empty';
            a.classList.add(cls);
        })
        this.el.querySelector('#comp-filter').appendChild(compSelect);
    },


    // return a model representing the current filter settings
    // overwrites properties of given filter or creates a new one, if not given
    getFilter: function(filter){
        var filter = filter || new GDSEModel();
        filter.set('area_level', this.areaLevelSelect.value);
        var material = this.selectedMaterial;
        filter.set('material', (material) ? material.id : null);
        var product = this.selectedProduct;
        filter.set('product', (product) ? product.id : null);
        var composite = this.selectedComposite;
        filter.set('composite', (composite) ? composite.id : null);
        var direction = this.el.querySelector('input[name="direction"]:checked').value;
        filter.set('direction', direction);
        //filter.set('aggregate_materials', this.aggregateCheck.checked)

        var process_ids = null;
        if (this.processSelect.value != "-1"){
            var values = [];
            var options = this.processSelect.selectedOptions;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                values.push(option.value);
            }
            process_ids = values.join(',')
        }
        filter.set('process_ids', process_ids);

        var waste_ids = null;
        if (this.wasteSelect.value != "-1"){
            var values = [];
            var options = this.wasteSelect.selectedOptions;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                values.push(option.value);
            }
            waste_ids = values.join(',')
        }
        filter.set('waste_ids', waste_ids);

        filter.set('flow_type', this.flowTypeSelect.value);
        filter.set('role', this.roleSelect.value);
        filter.set('year', this.yearSelect.value);
        filter.set('hazardous', this.hazardousSelect.value);
        filter.set('route', this.routeSelect.value);
        filter.set('collector', this.collectorSelect.value);
        filter.set('clean', this.cleanSelect.value);
        filter.set('mixed', this.mixedSelect.value);
        filter.set('direct', this.directSelect.value);
        //filter.set('avoidable', this.avoidableSelect.value);
        //filter.set('anonymize', this.anonymousSelect.checked);

        var areas = [];
        this.selectedAreas.forEach(function(area){
            areas.push(area.id)
        })
        filter.set('areas', areas);

        // get the nodes by level
        // check descending from actors, where sth is selected
        // take this as the actual level
        var levelSelects = [this.actorSelect, this.activitySelect, this.groupSelect],
            nodeLevels = ['actor', 'activity', 'activitygroup'],
            nodeLevel = 'activitygroup',
            selectedNodes = [],
            levelIdx = nodeLevels.indexOf(this.nodeLevelSelect.value); // start at selected level, ignore more granular ones

        for(var i = levelIdx; i < levelSelects.length; i++){
            var select = levelSelects[i];
            nodeLevel = nodeLevels[i];
            // sth is selected
            if (select.value >= 0){
                selectedNodes = this.getSelectedNodes(select);
                break;
            }
        }
        filter.set('filter_level', nodeLevel);
        filter.set('node_ids', selectedNodes.join(','));
        return filter;
    },

    applyFilter: function(filter){
        var _this = this
            areaLevel = filter.get('area_level'),
            areas = filter.get('areas');
        this.showFlowOnlyCheck.checked = false;
        if (this.flowsView) this.flowsView.close();

        this.nodeLevelSelect.value = filter.get('filter_level').toLowerCase();
        this.resetNodeSelects();

        if (areaLevel == null) {
            this.areaLevelSelect.selectedIndex = 0;
            this.changeAreaLevel();
        }
        else {
            this.areaLevelSelect.value = areaLevel;
            var labels = [];
            if (areas && areas.length > 0) {
                this.prepareAreas(areaLevel, function(){
                    areas.forEach(function(areaId){
                        var area = _this.areas[areaLevel].get(areaId);
                        _this.areaMap.selectFeature('areas', areaId);
                        labels.push(area.get('name'));
                        var areasLabel = labels.join(', ');
                        _this.el.querySelector('.selections').innerHTML = areasLabel;
                        _this.el.querySelector('#area-selections').innerHTML = areasLabel;
                    })
                });
            }
            else _this.changeAreaLevel();
        }

        var direction = filter.get('direction'),
            directionOption = document.querySelector('input[name="direction"][value="' + direction.toLowerCase() + '"]')
        directionOption.checked = true;
        this.flowTypeSelect.value = filter.get('flow_type').toLowerCase();
        this.roleSelect.value = filter.get('role').toLowerCase();
        //this.aggregateCheck.checked = filter.get('aggregate_materials');

        var process_ids = filter.get('process_ids');
        if (process_ids == null)
            this.processSelect.value = -1;
        else {
            $(this.processSelect).selectpicker('val', process_ids.split(','))
        }
         $(this.processSelect).selectpicker('refresh');

        var waste_ids = filter.get('waste_ids');
        if (waste_ids == null)
            this.wasteSelect.value = -1;
        else {
            $(this.wasteSelect).selectpicker('val', waste_ids.split(','))
        }
         $(this.wasteSelect).selectpicker('refresh');

        this.yearSelect.value = filter.get('year');
        this.hazardousSelect.value = filter.get('hazardous').toLowerCase();
        this.routeSelect.value = filter.get('route').toLowerCase();
        this.collectorSelect.value = filter.get('collector').toLowerCase();
        this.cleanSelect.value = filter.get('clean').toLowerCase();
        this.mixedSelect.value = filter.get('mixed').toLowerCase();
        this.directSelect.value = filter.get('direct').toLowerCase();
        //this.avoidableSelect.value = filter.get('avoidable').toLowerCase();
        //this.anonymousSelect.checked = filter.get('anonymize');

        // hierarchy-select plugin offers no functions to set (actually no functions at all) -> emulate clicking on row
        var material = filter.get('material'),
            li = this.matSelect.querySelector('li[data-value="' + material + '"]');
        if(li){
            matItem = li.querySelector('a');
            matItem.click();
        }
        // click first one, if no material
        else{
            this.matSelect.querySelector('a').click();
        }

        var product = filter.get('product'),
            li = this.proSelect.querySelector('li[data-value="' + product + '"]');
        if(li){
            proItem = li.querySelector('a');
            proItem.click();
        }
        // click first one, if no material
        else{
            this.proSelect.querySelector('a').click();
        }

        var composite = filter.get('composite'),
            li = this.compSelect.querySelector('li[data-value="' + composite + '"]');
        if(li){
            compItem = li.querySelector('a');
            compItem.click();
        }
        // click first one, if no material
        else{
            this.compSelect.querySelector('a').click();
        }

        // level actor -> filter actors
        var nodeLevel = filter.get('filter_level').toLowerCase(),
            nodeIds = filter.get('node_ids');
        this.resetNodeSelects();
        if(nodeIds) {
            this.nodeLevelSelect.value = nodeLevel;
            var select;
            // actors are special, they are not fetched in bulk and most likely unknown yet
            if (nodeLevel === 'actor'){
                select = this.actorSelect;
                this.actors.fetch(
                    {
                        data: { 'id__in': nodeIds, fields: ['id', 'name'].join() },
                        success: function(){
                            _this.renderNodeSelectOptions(select, _this.actors);
                            // could also just select all of them
                            $(select).selectpicker('val', nodeIds.split(','));
                        },
                        error: _this.onError
                    }
                );
            }
            else{
                select = (nodeLevel === 'activity') ? this.activitySelect : this.groupSelect;
                $(select).selectpicker('val', nodeIds.split(','))
            }
        }
    },

    close: function(){
        if (this.flowsView) this.flowsView.close();
        FilterFlowsView.__super__.close.call(this);
    }

});
return FilterFlowsView;
}
);
