define(['backbone', 'underscore', 'collections/layercategories', 
    'collections/layers', 'models/layer', 'visualizations/map', 
    'utils/loader', 'app-config', 'bootstrap-colorpicker'],

function(Backbone, _, LayerCategories, Layers, Layer, Map, Loader, config){
    /**
        *
        * @author Christoph Franke
        * @name module:views/BaseMapsView
        * @augments Backbone.View
        */
    var BaseMapsView = Backbone.View.extend(
        /** @lends module:views/BaseMapsView.prototype */
        {

        /**
        * render view to add layers to casestudy
        *
        * @param {Object} options
        * @param {HTMLElement} options.el                          element the view will be rendered in
        * @param {string} options.template                         id of the script element containing the underscore template to render this view
        * @param {module:models/CaseStudy} options.caseStudy       the casestudy to add layers to
        *
        * @constructs
        * @see http://backbonejs.org/#View
        */
        initialize: function(options){
            var _this = this;
            _.bindAll(this, 'render');
            _.bindAll(this, 'nodeSelected');
            _.bindAll(this, 'nodeChecked');
            _.bindAll(this, 'nodeUnchecked');

            this.template = options.template;
            this.caseStudy = options.caseStudy;

            this.projection = 'EPSG:4326'; 

            var WMSResources = Backbone.Collection.extend({ 
                url: config.api.wmsresources.format(this.caseStudy.id) 
            })

            this.wmsResources = new WMSResources();
            this.layerCategories = new LayerCategories([], { caseStudyId: this.caseStudy.id });

            this.categoryTree = {};
            this.layerPrefix = 'service-layer-';
            this.legendPrefix = 'layer-legend-';

            var loader = new Loader(this.el, {disable: true});
            this.layerCategories.fetch({ success: function(){
                loader.remove();
                _this.initTree();
            }})
        },

        initTree: function(){
            var _this = this;
            var deferred = [],
                layerList = [];
            // put nodes for each category into the tree and prepare fetching the layers
            // per category
            this.layerCategories.each(function(category){
                var layers = new Layers([], { caseStudyId: _this.caseStudy.id, 
                    layerCategoryId: category.id });
                var node = { 
                    text: category.get('name'), 
                    category: category,
                    state: { checked: true }
                };
                _this.categoryTree[category.id] = node;
                layerList.push(layers);
                deferred.push(layers.fetch());
            });
            // fetch prepared layers and put informations into the tree nodes
            $.when.apply($, deferred).then(function(){
                layerList.forEach(function(layers){
                    var catNode = _this.categoryTree[layers.layerCategoryId];
                    var children = [];
                    layers.each(function(layer){
                        var node = { 
                            layer: layer, 
                            text: layer.get('name'), 
                            icon: 'fa fa-bookmark',
                            state: { checked: layer.get('included') } 
                        };
                        children.push(node);
                    });
                    catNode.nodes = children;
                });
                _this.render();
            })
        },

        /*
            * dom events (managed by jquery)
            */
        events: {
            'click #add-layer-button': 'addLayer',
            'click #add-category-button': 'addCategory',
            'click #add-layer-modal .confirm': 'confirmLayer',
            'click #remove-layer-button': 'removeLayer',
            'click #edit-layer-button': 'editName',
            'click #remove-confirmation-modal .confirm': 'confirmRemoval',
            'click #refresh-wms-services-button': 'renderAvailableServices',
            'click #move-layer-up-button': 'moveLayerUp',
            'click #move-layer-down-button': 'moveLayerDown'
        },

        /*
            * render the view
            */
        render: function(){
            var _this = this;
            var html = document.getElementById(this.template).innerHTML,
                template = _.template(html);
            this.el.innerHTML = template();

            this.layerTree = document.getElementById('layer-tree');
            this.buttonBox = document.getElementById('layer-tree-buttons');
            this.zInput = document.getElementById('layer-z-index');
            this.legend = document.getElementById('legend');
            
            html = document.getElementById('empty-modal-template').innerHTML;
            var elConfirmation = document.getElementById('remove-confirmation-modal');
            elConfirmation.innerHTML = _.template(html)({ header: gettext('Remove') });
            this.confirmationModal = elConfirmation.querySelector('.modal');
            this.layerModal = document.getElementById('add-layer-modal');

            this.renderMap();
            this.renderDataTree();
            this.renderAvailableServices();
        },

        renderMap: function(){
            var _this = this;
            this.map = new Map({
                divid: 'base-map', 
                renderOSM: false
            });
            var focusarea = this.caseStudy.get('properties').focusarea;

            this.map.addLayer('focus', {
                stroke: '#aad400',
                fill: 'rgba(170, 212, 0, 0.1)',
                strokeWidth: 1,
                zIndex: 1000
            });
            // add polygon of focusarea to both maps and center on their centroid
            if (focusarea != null){
                var poly = this.map.addPolygon(focusarea.coordinates[0], { projection: this.projection, layername: 'focus', tooltip: gettext('Focus area') });
                this.map.addPolygon(focusarea.coordinates[0], { projection: this.projection, layername: 'focus', tooltip: gettext('Focus area') });
                this.centroid = this.map.centerOnPolygon(poly, { projection: this.projection });
                this.map.centerOnPolygon(poly, { projection: this.projection });
            };
            // get all layers and render them
            Object.keys(this.categoryTree).forEach(function(catId){
                var children = _this.categoryTree[catId].nodes;
                children.forEach(function(node){ _this.addServiceLayer(node.layer) } );
            })
        },

        rerenderDataTree: function(categoryId){
            this.buttonBox.style.display = 'None';
            if (this.layerTree.innerHTML)
                $(this.layerTree).treeview('remove');
            this.renderDataTree(categoryId);
        },

        addServiceLayer: function(layer){
            this.map.addServiceLayer(this.layerPrefix + layer.id, { 
                opacity: 1,
                zIndex: layer.get('z_index'),
                visible: layer.get('included'),
                url: config.views.layerproxy.format(layer.id),
                //params: {'layers': layer.get('service_layers')}//, 'TILED': true, 'VERSION': '1.1.0'},
            });
            var uri = layer.get('legend_uri');
            if (uri) {
                var legendDiv = document.createElement('li'),
                    head = document.createElement('b'),
                    img = document.createElement('img');
                legendDiv.id = this.legendPrefix + layer.id;
                head.innerHTML = layer.get('name');
                img.src = uri;
                this.legend.appendChild(legendDiv);
                legendDiv.appendChild(head);
                legendDiv.appendChild(img);
                if (!layer.get('included'))
                    legendDiv.style.display = 'none';
            }
        },

        /*
        * render the hierarchic tree of layers
        */
        renderDataTree: function(categoryId){
            if (Object.keys(this.categoryTree).length == 0) return;

            var _this = this;
            var dataDict = {};
            var tree = [];

            _.each(this.categoryTree, function(category){
                tree.push(category)
            })

            require('libs/bootstrap-treeview.min');
            
            function select(event, node, silent){ 
              $(_this.layerTree).treeview('selectNode',  [node.nodeId, { silent: silent }]);
            }
      
            $(this.layerTree).treeview({
                data: tree, showTags: true,
                selectedBackColor: '#aad400',
                expandIcon: 'glyphicon glyphicon-triangle-right',
                collapseIcon: 'glyphicon glyphicon-triangle-bottom',
                onNodeSelected: this.nodeSelected,
                onNodeUnselected: function(event, node){ select(event, node, true) },
                onNodeChecked: this.nodeChecked,
                onNodeUnchecked: this.nodeUnchecked,
                // workaround for misplaced buttons when collapsing parent node -> select the collapsed node
                onNodeCollapsed: function(event, node){ select(event, node, false) },
                onNodeExpanded: function(event, node){ select(event, node, false) },
                showCheckbox: true
            });
            
            var selectNodeId = 0;

            // look for and expand and select node with given category id
            if (categoryId){
                // there is no other method to get all nodes or to search for an attribute
                var nodes = $(this.layerTree).treeview('getEnabled');
                _.forEach(nodes, function(node){
                    if (node.category && (node.category.id == categoryId)){
                        selectNodeId = node.nodeId; 
                        return false;
                    }
                })
            }
            // select first one, if no slectID is given
            $(this.layerTree).treeview('selectNode', selectNodeId);
            
        },

        /*
        * event for selecting a node in the layer tree
        */
        nodeSelected: function(event, node){
            if (this.selectedNode)
                $(this.layerTree).treeview('unselectNode', [this.selectedNode.nodeId, { silent: true }]);
            var addBtn = document.getElementById('add-layer-button'),
                removeBtn = document.getElementById('remove-layer-button'),
                downBtn = document.getElementById('move-layer-down-button'),
                upBtn = document.getElementById('move-layer-up-button');
            this.selectedNode = node;
            if (node.layer != null) {
                addBtn.style.display = 'None';
                this.zInput.style.display = 'inline';
                this.zInput.value = node.layer.get('z_index');
                downBtn.style.display = 'inline';
                upBtn.style.display = 'inline';
            }
            else {
                addBtn.style.display = 'inline';
                this.zInput.style.display = 'None';
                downBtn.style.display = 'None';
                upBtn.style.display = 'None';
            }
            var li = this.layerTree.querySelector('li[data-nodeid="' + node.nodeId + '"]');
            if (!li) return;
            this.buttonBox.style.top = li.offsetTop + 'px';
            this.buttonBox.style.display = 'inline';
        },
        
        nodeChecked: function(event, node){
            // layer checked
            if (node.layer != null){
                node.layer.set('included', true);
                node.layer.save();
                this.map.setVisible(this.layerPrefix + node.layer.id, true);
                var legendDiv = document.getElementById(this.legendPrefix + node.layer.id);
                if (legendDiv) legendDiv.style.display = 'inline';
                //$(this.layerTree).treeview('checkNode', [node.parentId, { silent: true }]);
            }
            // category checked
            else {
                //node.nodes.forEach(function(child){
                    //$(_this.layerTree).treeview('checkNode', [child.nodeId]);
                //})
            }
        },
        
        nodeUnchecked: function(event, node){
            // layer unchecked
            if (node.layer != null){
                node.layer.set('included', false);
                node.layer.save();
                this.map.setVisible(this.layerPrefix + node.layer.id, false);
                var legendDiv = document.getElementById(this.legendPrefix + node.layer.id);
                if (legendDiv) legendDiv.style.display = 'none';
            }
            // category unchecked
            else {
                //node.nodes.forEach(function(child){
                    //console.log(child.nodeId)
                    //console.log(_this.layerTree)
                    //$(_this.layerTree).treeview('uncheckNode', [child.nodeId]);
                //})
                // checking unchecking the children often produces database locks 
                // (thanks to sqlite, see code above)
                // just leaving it always checked now
                $(this.layerTree).treeview('checkNode', [node.nodeId, { silent: true }]);
            }
        },

        renderAvailableServices: function(){
            var _this = this;
            this.wmsResources.fetch({ success: function(){
                var html = document.getElementById('wms-services-template').innerHTML,
                    template = _.template(html),
                    el = document.getElementById('wms-services');
                el.innerHTML = template({ resources: _this.wmsResources });
            }})
        },

        addLayer: function(){
            // uncheck all checkboxes
            var checked = this.layerModal.querySelectorAll('input[name=layer]:checked');
            checked.forEach(function(checkbox){checkbox.checked = false;})
            $(this.layerModal).modal('show'); 
        },

        addCategory: function(){
            var _this = this;
            function onConfirm(name){
                var category = new _this.layerCategories.model(
                    { name: name }, { caseStudyId: _this.caseStudy.id })
                category.save(null, { success: function(){
                    var catNode = { 
                        text: name, 
                        category: category,
                        state: { checked: true }
                    };
                    catNode.nodes = [];
                    _this.categoryTree[category.id] = catNode;
                    _this.rerenderDataTree(category.id);
                }})
            }
            this.getName({ 
                title: gettext('Add Category'),
                onConfirm: onConfirm
            });
        },

        confirmLayer: function(){
            var _this = this;
            var category = this.selectedNode.category,
                catNode = this.categoryTree[category.id];
            
            var checked = this.layerModal.querySelectorAll('input[name=layer]:checked');
            
            var newLayers = [];
            
            checked.forEach(function(checkbox){
                var wmsLayerId = checkbox.dataset.layerid,
                    wmsLayerName = checkbox.dataset.layername;
                var layer = new Layer({ 
                    name: wmsLayerName, 
                    included: true,
                    wms_layer: wmsLayerId,
                    style: null
                }, { caseStudyId: _this.caseStudy.id, layerCategoryId: category.id });
                newLayers.push(layer);
            })
            
            function onSuccess(){
                newLayers.forEach(function(layer){
                    var layerNode = { text: layer.get('name'),
                        icon: 'fa fa-bookmark',
                        layer: layer,
                        state: { checked: layer.get('included') } };
                    catNode.nodes.push(layerNode);
                    _this.rerenderDataTree(category.id);
                    _this.addServiceLayer(layer);
                })
            }
            
            // upload the models recursively (starting at index it)
            function uploadModel(models, it){
              // end recursion if no elements are left and call the passed success method
              if (it >= models.length) {
                onSuccess();
                return;
              };        
              var params = {
                success: function(){ uploadModel(models, it+1) }
              }
              var model = models[it];
              model.save(null, params);
            };
            
            // start recursion at index 0
            uploadModel(newLayers, 0);
        },
        
        removeLayer: function(){
            if (!this.selectedNode) return;
            var model = this.selectedNode.layer || this.selectedNode.category,
                message = (this.selectedNode.layer) ? gettext('Do you really want to delete the selected layer?') :
                          gettext('Do you really want to delete the selected category?');
            this.confirmationModal.querySelector('.modal-body').innerHTML = message; 
            $(this.confirmationModal).modal('show'); 
        },
        
        confirmRemoval: function(){
            var _this = this;
            $(this.confirmationModal).modal('hide'); 
            var is_category = (this.selectedNode.category != null);
            var model = this.selectedNode.layer || this.selectedNode.category;
            model.destroy({ success: function(){
                var selectCatId = 0;
                // remove category from tree (if category was selected)
                if (_this.selectedNode.category) {
                    _this.selectedNode.nodes.forEach(function(node){
                        _this.map.removeLayer(_this.layerPrefix + node.layer.id);
                    })
                    delete _this.categoryTree[model.id];
                }
                // remove layer from category (if layer was selected)
                else {
                    _this.getTreeLayerNode(model, { pop: true })
                    selectCatId = model.get('category');
                    _this.map.removeLayer(_this.layerPrefix + model.id);
                    var legendDiv = document.getElementById(_this.legendPrefix + model.id);
                    if (legendDiv) legendDiv.parentElement.removeChild(legendDiv);
                }
                _this.selectedNode = null;
                _this.rerenderDataTree(selectCatId);
            }});
            
        },
        
        getTreeLayerNode: function(layer, options){
            var options = options || {};
            var catNode = this.categoryTree[layer.get('category')];
            var nodes = catNode.nodes;
            for (var i = 0; i < nodes.length; i++){
                var node = nodes[i];
                if (node.layer === layer) {
                    if (options.pop) nodes.splice(i, 1);
                    return node;
                }
            }
            return;
        },
        
        editName: function(){
            var _this = this;
            var model = this.selectedNode.layer || this.selectedNode.category;
            function onConfirm(name){
                model.set('name', name);
                model.save(null, { success: function(){
                    var node = _this.selectedNode.category ? _this.categoryTree[model.id]:
                                _this.getTreeLayerNode(model);
                    node.text = name;
                    var selectCatId = _this.selectedNode.category? model.id: model.get('category');
                    _this.rerenderDataTree(selectCatId);
                }})
            };
            this.getName({ 
                name: model.get('name'), 
                title: gettext('Edit Name'),
                onConfirm: onConfirm
            })
        },
        
        moveLayerUp: function(){
            var _this = this;
            var layer = this.selectedNode.layer;
            var newVal = Number(this.zInput.value) + 1;
            layer.set('z_index', newVal);
            this.buttonBox.style.pointerEvents = 'none';
            layer.save(null, { success: function(){
                _this.buttonBox.style.pointerEvents = 'auto';
                _this.zInput.value = newVal;
                _this.map.setZIndex(_this.layerPrefix + layer.id, newVal);
            }});
        },
        
        moveLayerDown: function(){
            var _this = this;
            var layer = this.selectedNode.layer;
            var newVal = Number(this.zInput.value) - 1;
            if (newVal > 0){
                this.zInput.value = newVal;
                layer.set('z_index', newVal);
                this.buttonBox.style.pointerEvents = 'none';
                layer.save(null, { success: function(){
                    _this.buttonBox.style.pointerEvents = 'auto';
                    _this.zInput.value = newVal;
                    _this.map.setZIndex(_this.layerPrefix + layer.id, newVal);
                }});
            }
        },

        /*
        * open modal dialog to enter a name
        * options: onConfirm, name, title
        */
        getName: function(options){

            var options = options || {};

            var div = document.getElementById('edit-category-modal'),
                inner = document.getElementById('empty-modal-template').innerHTML;
                template = _.template(inner),
                html = template({ header:  options.title || '' });

            div.innerHTML = html;
            var modal = div.querySelector('.modal');
            var body = modal.querySelector('.modal-body');

            var row = document.createElement('div');
            row.classList.add('row');
            var label = document.createElement('div');
            label.innerHTML = gettext('Name');
            var input = document.createElement('input');
            input.style.width = '100%';
            input.value = options.name || '';
            body.appendChild(row);
            row.appendChild(label);
            row.appendChild(input);

            modal.querySelector('.confirm').addEventListener('click', function(){
                if (options.onConfirm) options.onConfirm(input.value);
                $(modal).modal('hide');
            });

            $(modal).modal('show');
        },

        /*
        * remove this view from the DOM
        */
        close: function(){
            this.undelegateEvents(); // remove click events
            this.unbind(); // Unbind all local event bindings
            this.el.innerHTML = ''; //empty the DOM element
        },

    });
    return BaseMapsView;
}
);