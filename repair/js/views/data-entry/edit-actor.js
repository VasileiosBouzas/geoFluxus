define(['views/common/baseview', 'underscore',
        'collections/gdsecollection', 'models/gdsemodel',
        'collections/geolocations', 'models/geolocation',
        'visualizations/map', 'utils/utils', 'bootstrap'],

function(BaseView, _, GDSECollection, GDSEModel, Locations, Location, Map, utils){
/**
    *
    * @author Christoph Franke
    * @name module:views/EditActorView
    * @augments module:views/BaseView
    */
var EditActorView = BaseView.extend(
    /** @lends module:views/EditActorView.prototype */
    {

    /**
    * callback for uploading the actor
    *
    * @callback module:views/EditActorView~onUpload
    * @param {module:GDSECollection.Model} actor the uploaded actor
    */

    /**
    * render view to edit single actor and its locations
    *
    * @param {Object} options
    * @param {HTMLElement} options.el                                 element the view will be rendered in
    * @param {string} options.template                                id of the script element containing the underscore template to render this view
    * @param {module:collections/GDSECollection.Model} options.model  the actor to edit
    * @param {module:collections/GDSECollection.Model} options.keyflow  the keyflow the actor belongs to
    * @param {module:collections/GDSECollection} options.activities   the activities belonging to the keyflow
    * @param {module:collections/GDSECollection} options.areaLevels   the levels of areas belonging to the casestudy of the keyflow (sorted ascending by level, starting with top-level)
    * @param {module:collections/GDSECollection} options.reasons      possible options for reasons to exclude the actor
    * @param {Object} options.focusarea                               geojson with multipolygon that will be drawn on the map
    * @param {module:views/EditActorView~onUpload=} options.onUpload  called after successfully uploading the actor
    *
    * @constructs
    * @see http://backbonejs.org/#View
    */
    initialize: function(options){
        // workaround for brackets in query params
        $.ajaxSetup({ traditional: true });
        EditActorView.__super__.initialize.apply(this, [options]);
        _.bindAll(this, 'renderLocation');

        this.keyflow = options.keyflow;
        this.keyflowId = this.keyflow.id,
        this.caseStudyId = this.keyflow.get('casestudy');

        this.activities = options.activities;
        this.onUpload = options.onUpload;
        this.focusarea = options.focusarea;
        this.areaLevels = options.areaLevels;
        this.reasons = options.reasons;

        this.hasChangedVal = false;

        this.layers = {
            opLocations: {
                pin: '/static/img/map-marker-red.svg',
                style: {
                    stroke: 'rgb(255, 51, 0)',
                    fill: 'rgba(255, 51, 0, 0.1)',
                    strokeWidth: 2,
                    zIndex: 1
                }
            },
            adminLocations: {
                pin: '/static/img/map-marker-blue.svg',
                style: {
                    stroke: 'rgb(51, 153, 255)',
                    fill: 'rgba(51, 153, 255, 0.1)',
                    strokeWidth: 2,
                    zIndex: 1
                }
            },
            background: {
                style: {
                    stroke: '#3958A4',
                    fill: 'rgba(170, 212, 0, 0.1)',
                    strokeWidth: 1,
                    zIndex: 0
                },
            }
        };

        var _this = this;

        this.adminLocations = new Locations([], {
            apiTag: 'adminLocations',
            apiIds: [ this.caseStudyId, this.keyflowId ]
        });

        this.opLocations = new Locations([], {
            apiTag: 'opLocations',
            apiIds: [ this.caseStudyId, this.keyflowId ]
        });

        this.projection = 'EPSG:4326';

        this.loader.activate();
        var deferreds = [
            this.adminLocations.fetch({ data: { actor: this.model.id } }),
            this.opLocations.fetch({ data: { actor: this.model.id } })
        ]
        var topLevel = this.areaLevels.first();
        if (topLevel) {
            this.topLevelAreas = new GDSECollection([], {
                apiTag: 'areas',
                apiIds: [ this.caseStudyId, topLevel.id ],
                comparator: 'name'
            });
            deferreds.push(this.topLevelAreas.fetch({ data: { field: ['id', 'name'] }}));
        }

            $.when.apply($, deferreds).then(function(){
                if (_this.topLevelAreas) _this.topLevelAreas.sort();
                _this.loader.deactivate();
                _this.render();
        });
    },

    /*
    * dom events (managed by jquery)
    */
    events: {
        'click #upload-actor-button': 'uploadChanges',
        'click #confirm-location': 'locationConfirmed',
        'click #add-operational-button,  #add-administrative-button': 'createLocationEvent',
        'change #included-check': 'toggleIncluded',
        'change input': 'triggerChange',
        'change select': 'triggerChange'
    },

    /*
    * render the view
    */
    render: function(){
        var _this = this;
        var html = document.getElementById(this.template).innerHTML
        var template = _.template(html);
        this.el.innerHTML = template({activities: this.activities,
            actor: this.model,
            reasons: this.reasons});

        this.filterSelect = this.el.querySelector('#included-filter-select');
        this.adminTable = this.el.querySelector('#adminloc-table').getElementsByTagName('tbody')[0];
        this.opTable = this.el.querySelector('#oploc-table').getElementsByTagName('tbody')[0];

        this.initMap();
        this.renderLocations();
        this.setupAreaInput();
    },

    triggerChange: function(){
        this.hasChangedVal = true;
    },

    hasChanged: function(){
        return this.hasChangedVal;
    },

    /*
    * check the models for changes and upload the changed/added ones
    */
    uploadChanges: function(){
        var actor = this.model;
        var _this = this;

        var table = document.getElementById('actor-edit-table'),
            inputs = Array.prototype.slice.call(table.querySelectorAll('input')),
            selects = Array.prototype.slice.call(table.querySelectorAll('select')),
            textareas = Array.prototype.slice.call(table.querySelectorAll('textarea'));
        _.each(inputs.concat(selects).concat(textareas), function(input){
            if (input.name == 'reason' || input.name == 'included') return; // continue, handled seperately (btw 'return' in _.each(...) is equivalent to continue)
            actor.set(input.name, input.value);
        });
        var included = this.el.querySelector('input[name="included"]').checked;
        actor.set('included', included);
        var checked = this.el.querySelector('input[name="reason"]:checked')
        // set reason to null, if included
        var reason = (checked != null) ? checked.value: null;
        actor.set('reason', reason);

        this.loader.activate();

        var onError = function(response){
            _this.loader.deactivate();
            _this.onError(response);
        };

        //actor.save(null, {success: uploadLocations, error: function(model, response){onError(response)}});
        var models = [];
        models.push(actor);
        if (this.adminLocations.length > 0)
            models.push(this.adminLocations.first());
        this.opLocations.each(function(model){models.push(model)});
        function uploadModel(models, it){
            // end recursion if no elements are left and call the passed success method
            if (it >= models.length) {
                _this.loader.deactivate();
                _this.onUpload(actor);
                return;
            };
            var model = models[it];
            // upload or destroy current model and upload next model recursively on success
            var params = {
                success: function(){ uploadModel(models, it+1) },
                error: function(model, response){ onError(response) }
            }
            if (model.markedForDeletion)
                model.destroy(params);
            else {
                var geom = model.get('geometry');
                // workaround: backend doesn't except empty geometries but null as a geometry
                if (geom != null && geom.get('coordinates') == null) model.set('geometry', null);
                model.save(null, params);
            }
        };

        // recursively queue the operational locations to save only when previous one is done (sqlite is bitchy with concurrent uploads)
        uploadModel(models, 0);
    },

    /*
    * initial setup of the map-view
    */
    initMap: function(){
        var _this = this;

        this.globalMap = new Map({
            el: document.getElementById('actors-map'),
        });

    this.localMap = new Map({
        el: document.getElementById('edit-location-map'),
    });

    _.each(this.layers, function(attrs, layername){
        _this.globalMap.addLayer(layername, attrs.style);
        _this.localMap.addLayer(layername, attrs.style);
    });

    // event triggered when modal dialog is ready -> trigger rerender to match size
    $('#location-modal').on('shown.bs.modal', function () {
        _this.localMap.map.updateSize();
    });
    },

    /*
    * add a marker with given location to the map and the table
    */
    renderLocation: function(loc, layername, table){
        if (loc == null)
            return;
        /* add table rows */

        var row = table.insertRow(-1);
        var _this = this;
        var pin = this.layers[layername].pin;

        // checkbox for marking deletion

        var checkbox = document.createElement("input");
        checkbox.type = 'checkbox';
        row.insertCell(-1).appendChild(checkbox);

        checkbox.addEventListener('change', function() {
            row.classList.toggle('strikeout');
            row.classList.toggle('dsbld');
            loc.markedForDeletion = checkbox.checked;
        });

        row.insertCell(-1).innerHTML = loc.get('properties').name;

        // add a marker to the table and the map, if there is a geometry attached to the location
        var markerCell = row.insertCell(-1);
        var geom = loc.get('geometry');
        if (geom != null && geom.get('coordinates') != null){
            var wrapper = document.createElement('span'),
                centerDiv = document.createElement('div'),
                coordDiv = document.createElement('div'),
                img = document.createElement("img");
            var coords = geom.get('coordinates');
            coordDiv.innerHTML = '(' + utils.formatCoords(coords) + ')';
            coordDiv.style.paddingTop = '8px';
            coordDiv.style.fontSize = '80%';
            img.src = pin;
            img.setAttribute('height', '30px');
            img.style.float = 'left';
            centerDiv.appendChild(img);
            markerCell.appendChild(wrapper);
            wrapper.style.whiteSpace = 'nowrap';
            wrapper.style.cursor = 'pointer';
            wrapper.appendChild(centerDiv);
            wrapper.appendChild(coordDiv);

            // zoom to location if marker in table is clicked
            markerCell.addEventListener('click', function(){
                _this.globalMap.centerOnPoint(loc.get('geometry').get('coordinates'),
                    {projection: _this.projection})
            });

            /* add marker */

            this.globalMap.addmarker(coords, {
                icon: pin,
                anchor: [0.5, 1],
                //dragIcon: this.pins.orange,
                projection: this.projection,
                name: loc.get('properties').name,
                onDrag: function(coords){
                    loc.get('geometry').set("coordinates", coords);
                    coordDiv.innerHTML = '(' + utils.formatCoords(coords) + ')';
                    _this.triggerChange();
                },
                layername: layername
            });
        };

        // add area to table and map
        var areaCell = row.insertCell(-1);
        var areaId = loc.get('properties').area,
            levelId = loc.get('properties').level;

        if(areaId != null){
            var area = new GDSEModel({ id: areaId }, {
                apiTag: 'areas',
                apiIds: [ this.caseStudyId, levelId ]
            });
            area.fetch({success: function(){
                var wrapper = document.createElement('span'),
                    symbol = document.createElement('div'),
                    areanameDiv = document.createElement('div');

                symbol.style.float = 'left';
                symbol.classList.add('fa');
                symbol.classList.add('fa-map-o');
                symbol.style.marginRight = '5px';
                symbol.style.fontSize = '1.5em';
                symbol.style.color = _this.layers[layername].style.stroke;
                wrapper.style.whiteSpace = 'nowrap';
                wrapper.style.cursor = 'pointer';

                var name = area.get('properties').name;
                areanameDiv.title = name;
                if (name && name.length > 15) name = name.substring(0, 15) + '...';
                areanameDiv.innerHTML = name;

                wrapper.appendChild(symbol);
                wrapper.appendChild(areanameDiv);
                areaCell.appendChild(wrapper);

                var polyCoords = area.get('geometry').coordinates;
                var poly = _this.globalMap.addPolygon(polyCoords,
                    { projection: _this.projection,
                        layername: layername,
                        tooltip: area.get('properties').name,
                        type: area.get('geometry').type }
                );
                // zoom to location if marker in table is clicked
                areaCell.addEventListener('click', function(){
                    _this.globalMap.centerOnPolygon(poly, { projection: _this.projection })
                });
            }});
        }

        // button for editing the location

        var editBtn = document.createElement('button');
        var pencil = document.createElement('span');
        editBtn.classList.add('btn');
        editBtn.classList.add('btn-primary');
        editBtn.classList.add('square');
        editBtn.style.float = 'right';
        editBtn.appendChild(pencil);
        pencil.classList.add('glyphicon');
        pencil.classList.add('glyphicon-pencil');

        editBtn.addEventListener('click', function(){
            _this.editLocation(loc);
        });

        row.insertCell(-1).appendChild(editBtn);

    },

    /*
    * create location (administrative or operational) on button click
    */
    createLocationEvent: function(event){
        var buttonId = event.currentTarget.id;
        var properties = { actor: this.model.id };
        var type = (buttonId == 'add-administrative-button') ? 'adminLocations': 'opLocations';
        var location = new Location(
            { properties: properties },
            { apiTag: type, apiIds: [ this.keyflow.get('casestudy') ] }
        );
        this.editLocation(location);
    },

    /*
    * set the select options of all selects with higher (=finer) level than
    * the select with given index (as in this.areaSelects with ascending level)
    */
    setAreaChildSelects: function(area, idx){
        var _this = this;
        // last level has no children itself -> return
        var select = this.areaSelects[idx];
        if (idx >= this.areaSelects.length -1 ) return;
        var childSelects = this.areaSelects.slice(idx + 1);
            // clear all selects hierarchally below this level
            _.each(childSelects, function(sel){
                utils.clearSelect(sel);
        });
        if (area == null) return;
        var directChild = childSelects[0];
        var childAreas = new GDSECollection([], {
            apiTag: 'areas',
            apiIds: [ this.caseStudyId, directChild.levelId ],
            comparator: 'name'
        });
        childAreas.fetch({
            data: {
                parent_id: area.id,
                field: ['id', 'name']
            },
            success: function(){ _this.addAreaOptions(childAreas, directChild); }
        });
    },

    /*
    * set the select options of select with given index
    * if options.setParents=true recursively fetch and set options for parent selects as well
    */
    setAreaSelects: function(area, idx, options){
        var options = options || {};
        var _this = this;
        var select = this.areaSelects[idx];
        // don't fetch top level entries, they always stay the same, also serves as end of possible recursion
        if (idx <= 0) {
            select.value = area.id;
            if ( options.onSuccess != null ) options.onSuccess();
            return;
        }

        var parentId = area.get('properties').parent_area,
            parentLevelId = area.get('properties').parent_level;
        // fill this select
        var areas = new GDSECollection([], {
            apiTag: 'areas',
            apiIds: [ this.caseStudyId, select.levelId ],
            comparator: 'name'
        });
        areas.fetch({
            data:  {
                parent_id: parentId,
                field: ['id', 'name']
            },
            success: function(){
                _this.addAreaOptions(areas, select);
                select.value = area.id;
            }
        });

        // if setParents is set to true fetch parent area and recursively call this function again
        if (options.setParents){
            var parentArea = new GDSEModel({ id: parentId }, {
                apiTag: 'areas',
                apiIds: [ this.caseStudyId, parentLevelId ]
            });

            parentArea.fetch({
                success: function(){
                    // proceed recursion with parent select
                    _this.setAreaSelects(parentArea, idx-1, options);
                },
                error: _this.onError
            });
        }
    },

    /*
    * fill given select with given areas, adds an additional option to deselect (with value -1)
    */
    addAreaOptions: function (areas, select){
        var uop = document.createElement('option');
        uop.selected = true;
        uop.text = gettext('select an area');
        uop.value = -1;
        select.appendChild(uop);
        select.style.maxWidth = '200px';
        areas.each(function(area){
            var option = document.createElement('option');
            option.value = area.id;
            option.text = area.get('name');
            select.appendChild(option);
        });
    },

    /*
    * preset the select boxes for top level and connect all area selects
    */
    setupAreaInput: function(){
        var _this = this;
        var table = document.getElementById('location-area-table');
        this.areaSelects = [];

        // fetch geometry of area and draw it on map
        function fetchDraw(area){
            area.fetch({ success: function(){
                var polyCoords = area.get('geometry').coordinates;
                var poly = _this.localMap.addPolygon(
                    polyCoords,
                    {
                        projection: _this.projection,
                        layername: _this.activeType,
                        tooltip: area.get('properties').name,
                        type: area.get('geometry').type
                    }
                );
                _this.localMap.centerOnPolygon(poly, { projection: _this.projection, zoomOffset: -1 })
            }});
        }

        var idx = 0;
        this.areaLevels.each(function(level){
            var row = table.insertRow(-1);
            row.insertCell(-1).innerHTML = level.get('name');
            var select = document.createElement('select');
            select.level = level.get('level');
            select.levelId = level.id;
            _this.areaSelects.push(select);
            row.insertCell(-1).appendChild(select);
            var cur = idx;
            select.addEventListener('change', function(){
                var areaId = select.value;
                // remove polygons, keep markers
                _this.localMap.clearLayer('adminLocations', { types: ['Polygon', 'MultiPolygon'] });
                _this.localMap.clearLayer('opLocations', { types: ['Polygon', 'MultiPolygon'] });
                var area;
                if (areaId >= 0){
                    area = new GDSEModel({ id: areaId }, {
                        apiTag: 'areas',
                        apiIds: [ _this.caseStudyId, level.id ],
                        comparator: 'name'
                    });
                    fetchDraw(area);
                }
                // an area is deselected -> draw parent one (not on top level)
                else if (cur > 0) {
                    var parentSelect = _this.areaSelects[cur-1];
                    area = new GDSEModel({ id: parentSelect.value }, {
                        apiTag: 'areas',
                        apiIds: [ _this.caseStudyId, parentSelect.levelId ]
                    });
                    fetchDraw(area);
                }
                _this.setAreaChildSelects(area, cur);
            });

            idx++;
        });
        if (this.areaSelects.length == 0) return;
        // prefill select of toplevel
        var topLevelSelect = this.areaSelects[0];
        this.addAreaOptions(this.topLevelAreas, topLevelSelect);
    },

    /*
    * initialize the modal for location editing by filling the forms and map with the values of given location
    * open the modal
    */
    editLocation: function(location){
        var _this = this;
        var topLevelSelect = this.areaSelects[0];
        this.editedLocation = location;
        var locationModal = document.getElementById('location-modal');
        var geometry = location.get('geometry');
        var markerId;
        var coordinates = (geometry != null) ? geometry.get("coordinates"): null;
        this.activeType = location.apiTag || location.collection.apiTag;

        var pin = this.layers[this.activeType].pin;

        var inner = document.getElementById('location-modal-template').innerHTML;
        var template = _.template(inner);
        var html = template({properties: location.get('properties'),
            coordinates: (coordinates != null)? utils.formatCoords(coordinates): '-'});
        document.getElementById('location-modal-content').innerHTML = html;
        $(locationModal).modal('show');

        // reset the map
        this.localMap.clearLayer('opLocations');
        this.localMap.clearLayer('adminLocations');
        this.localMap.removeInteractions();

        // clear the selects
        var i = 0;
        this.areaSelects.forEach(function(select){
            // don't clear first select (top level areas don't change), keep first option as well
            if (i > 0) utils.clearSelect(select);
            i++;
        });

        // don't set coordinates directly to location, only on confirmation
        this.tempCoords = coordinates;
        var elGeom = document.getElementById('coordinates');

        var addPointBtn = locationModal.querySelector('#add-point'),
            removePointBtn = locationModal.querySelector('#remove-point');

        // show/hide add/remove point buttons
        function setPointButtons(state){
            if (state == 'add') {
                addPointBtn.style.display = 'block';
                removePointBtn.style.display = 'none';
            }
            else {
                addPointBtn.style.display = 'none';
                removePointBtn.style.display = 'block';
            }
        }

        function removeMarkerCallback(){
            _this.tempCoords = null;
            elGeom.innerHTML = '-';
            setPointButtons('add');
        }

        // add a marker to map
        function addMarker(coords){
            elGeom.innerHTML = utils.formatCoords(coords);
            markerId = _this.localMap.addmarker(coords, {
                icon: pin,
                anchor: [0.5, 1],
                //dragIcon: this.pins.orange,
                projection: _this.projection,
                name: location.get('properties').name,
                onDrag: function(coords){
                    _this.tempCoords = coords;
                    elGeom.innerHTML = utils.formatCoords(coords);
                },
                onRemove: removeMarkerCallback,
                removable: true,
                layername: _this.activeType
            });
            //_this.localMap.centerOnPoint(coords, {projection: _this.projection});
        }

        // connect add/remove point buttons
        var center = this.centroid || [13.4, 52.5];
        addPointBtn.addEventListener('click', function(){
            _this.tempCoords = center;
            addMarker(center);
            _this.localMap.centerOnPoint(center, {projection: _this.projection});
            setPointButtons('remove');
            _this.triggerChange();
        });
        removePointBtn.addEventListener('click', function(){
            _this.localMap.clearLayer(_this.activeType, { types: ['Point'] });
            _this.localMap.removeInteractions();
            removeMarkerCallback();
            _this.triggerChange();
        });

        // initially set marker depending on existing geometry
        if (coordinates != null){
            addMarker(coordinates);
            setPointButtons('remove');
            _this.localMap.centerOnPoint(coordinates, {projection: _this.projection});
        }
        else
            setPointButtons('add');

        // render the area and set up the selects

        var areaId = location.get('properties').area,
            levelId = location.get('properties').level;

        if(areaId != null){
            // find select with level of the area
            var selectIdx = 0;
            for(var select of this.areaSelects){
                if (select.levelId == levelId) break;
                selectIdx++;
            };
            if (selectIdx >= this.areaSelects.length) {
                _this.alert('no level with id ' + levelId + ' found');
                return;
            }
            var select = this.areaSelects[selectIdx];

            var area = new GDSEModel({ id: areaId }, {
                apiTag: 'areas',
                apiIds: [ _this.caseStudyId, levelId ]
            });
            area.fetch({success: function(){
                var polyCoords = area.get('geometry').coordinates[0];
                _this.localMap.addPolygon(polyCoords, {
                    projection: _this.projection, zoomOffset: -1,
                    layername: _this.activeType, tooltip: area.get('properties').name
                });
                // fetch areas of level and fill select (not for top level, always stays the same)
                if (selectIdx > 0){
                    var parentId = area.get('properties').parent_area;
                    var areas =  new GDSECollection([], {
                        apiTag: 'areas',
                        apiIds: [ _this.caseStudyId, levelId ],
                        comparator: 'name'
                    });
                    areas.fetch({
                        data: {
                            parent_id: parentId,
                            field: ['id', 'name']
                        },
                        success: function(){
                            _this.setAreaSelects(
                                area, selectIdx,
                                { setParents: true, onSuccess: function(){ _this.setAreaChildSelects(area, selectIdx); }
                        });
                    }});
                }
                else {
                    select.value = areaId;
                    _this.setAreaChildSelects(area, selectIdx);
                }
            }});

        };
        /*
        // context menu with add/remove
        var items = [
            {
                text: 'Set Location',
                icon: pin,
                callback: function(event){
                    var coords = _this.localMap.toProjection(event.coordinate, _this.projection);
                    if (_this.tempCoords != null){
                        _this.localMap.moveMarker(markerId, event.coordinate, { layername: _this.activeType });
                        elGeom.innerHTML = utils.formatCoords(coords);
                    }
                    else{
                        addMarker(coords);
                        setPointButtons('remove');
                    }
                    _this.tempCoords = coords;
                }
            },
            '-'
        ];
        this.localMap.addContextMenu(items);*/
    },

    /*
    * called when the location modal is confirmed by the user
    * set the changes made to the edited location
    */
    locationConfirmed: function(){
        var location = this.editedLocation;
        if(location == null) return;

        var geometry = location.get('geometry');
        if (geometry != null) geometry.set("coordinates", this.tempCoords);
        else location.setGeometry(this.tempCoords)
        var form = document.getElementById('location-modal-content');
        var inputs = form.querySelectorAll('input');
        var properties = location.get('properties');
        _.each(inputs, function(input){
            //properties.set(input.name) = input.value;
            properties[input.name] = input.value;
        });

        var areaTable = document.getElementById('location-area-table');
        var selects = areaTable.querySelectorAll('select');
        var areaId = null,
            levelId = null;
        // iterate area-selects (sorted hierarchally) and take last one that is filled
        for(var i = 0; i < selects.length; i++){
            var select = selects[i];
            // -1 is "select an area", meaning it is not set
            if (select.value < 0) break;
            areaId = select.value;
            levelId = select.levelId;
        }
        properties.area = areaId;
        properties.level = levelId;

        // location is not in a collection yet (added by clicking add-button) -> add it to the proper one
        if (location.collection == null){
            var collection = (location.apiTag == 'adminLocations') ? this.adminLocations : this.opLocations;
            collection.add(location);
        }
        // rerender all markers (too lazy to add single one)
        this.renderLocations();
    },

    /*
    * render the locations of the given actor as markers inside the map and table
    */
    renderLocations: function(){
        var adminLoc = this.adminLocations.first();

        var _this = this;
        this.adminTable.innerHTML = '';
        this.opTable.innerHTML = '';

        this.globalMap.clearLayer('adminLocations');
        this.globalMap.clearLayer('opLocations');
        this.renderLocation(adminLoc, 'adminLocations', this.adminTable);
        this.opLocations.each(function(loc){_this.renderLocation(loc, 'opLocations', _this.opTable);});

        var addAdminBtn = document.getElementById('add-administrative-button');
        if (adminLoc != null){
            // you may not have more than one admin. location (hide button, if there already is one)
            addAdminBtn.style.display = 'none';
            var geom = adminLoc.get('geometry');
        }
        else addAdminBtn.style.display = 'block';

        var polyOpt = {
            projection: this.projection,
            layername: 'background',
            tooltip: gettext('Focus area'),
            type: 'Multipolygon'
        }

        // add polygon of focusarea to both maps
        if (this.focusarea != null)
            var poly = this.globalMap.addPolygon(this.focusarea.coordinates, polyOpt);
        // zoom to admin area
        if (adminLoc){
            this.globalMap.centerOnPoint(
                adminLoc.get('geometry').get('coordinates'),
                { projection: _this.projection }
            )
        }
        // else zoom to focus area
        else if (this.focusarea){
            this.localMap.addPolygon(this.focusarea.coordinates, polyOpt);
            this.centroid = this.globalMap.centerOnPolygon(poly, { projection: _this.projection });
            this.localMap.centerOnPolygon(poly, { projection: _this.projection });
        };
    },

    toggleIncluded: function(event){
        var display = (event.target.checked) ? 'none': 'block';
        document.getElementById('reasons').style.display = display;
    }

});
return EditActorView;
}
);
