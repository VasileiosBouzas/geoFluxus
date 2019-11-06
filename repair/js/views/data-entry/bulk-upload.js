define(['views/common/baseview', 'underscore', 'models/gdsemodel',
        'collections/gdsecollection', 'collections/geolocations',
        'app-config'],
function(BaseView, _, GDSEModel, GDSECollection, GeoLocations, config){

/**
    *
    * @author Christoph Franke
    * @name module:views/BulkUploadView
    * @augments module:views/BaseView
    */
var BulkUploadView = BaseView.extend(
    /** @lends module:views/BulkUploadView.prototype */
    {

    /**
    * render view for bulk uploading keyflow data
    *
    * @constructs
    * @see http://backbonejs.org/#View
    */
    initialize: function(options){
        BulkUploadView.__super__.initialize.apply(this, [options]);
        _.bindAll(this, 'patchFocusarea');
        _.bindAll(this, 'patchRegion');
        this.caseStudy = options.caseStudy;
        this.render();
    },

    /*
    * dom events (managed by jquery)
    */
    events: {
        "click button.upload": "upload",
        //"click #remove-keyflow": "removeKeyflow",
        //"click button.clear": "clearData",
        "click #refresh-status": "refreshStatus",
        "click #upload-focusarea": "patchFocusarea",
        "click #upload-csregion": "patchRegion"
    },

    render: function(){
        var html = document.getElementById(this.template).innerHTML,
            template = _.template(html),
            _this = this;
        var csAdminUrl = '/admin/login/casestudy/' + this.caseStudy.id + '/change/';
        this.el.innerHTML = template({
            casestudy: this.caseStudy.get('properties').name,
            keyflow: this.model.get('name'),
            csAdminUrl: csAdminUrl
        });
        this.logArea = this.el.querySelector('#upload-log');

        var upsKeyflow = [
                ['activitygroups', gettext('Activity Group')],
                ['activities', gettext('Activities')],
                ['actors', gettext('Actors')],
                ['locations', gettext('Actor Locations')],
                ['flowchains', gettext('Flow Chains')],
                ['flows', gettext('Flows')],
                ['materials', gettext('Materials')],
                ['products', gettext('Products')],
                ['composites', gettext('Composites')],
                ['stocks', gettext('Stocks')],
                ['classifications', gettext('Classifications')],
                ['extradescriptions', gettext('Extra Descriptions')]
            ],
            upsCasestudy = [
                ['arealevels', gettext('Area Levels')],
                ['allareas', gettext('Areas')],
                ['publicationsInCasestudy', gettext('Publications')]
            ],
            upColKeyflow = this.el.querySelector('#keyflow-related-upload').querySelector('.upload-column');
            upColCasestudy = this.el.querySelector('#casestudy-related-upload').querySelector('.upload-column');
        // API routes returning default models without keyflows as well
        // force those to display keyflow related only in here
        this.forceKeyflowRelation = ['materials', 'products', 'wastes'];
        this.geolocations = ['adminLocations'];

        function renderRow(up, column){
            var html = document.getElementById('upload-row-template').innerHTML,
                template = _.template(html),
                div = document.createElement('div'),
                tag = up[0],
                apiUrl = config.api[tag],
                url = apiUrl.format(_this.caseStudy.id, _this.model.id);
            div.innerHTML = template({
                label: up[1], apiTag: tag, url: url,
                templateUrl: url + '?request=template'
            })
            column.appendChild(div);
        }
        upsKeyflow.forEach(function(up){
            renderRow(up, upColKeyflow);
        })
        upsCasestudy.forEach(function(up){
            renderRow(up, upColCasestudy);
        })
        this.refreshStatus();

        // publications row just links to the admin area
        // lazy way: publications is the only case, so i did not make a new template for this
        var pubRow = this.el.querySelector('.upload.row[data-tag="publicationsInCasestudy"]');
        pubRow.querySelector('input').style.display = 'none';
        pubRow.querySelector('button.upload').style.display = 'none';
        pubRow.querySelector('.template').style.display = 'none';
        var div = document.createElement('div'),
            a = document.createElement('a');
        div.innerHTML = gettext('Upload bibtex files') + '&nbsp';
        a.target = '_blank';
        a.innerHTML = gettext('here');
        a.href = '/admin/publications_bootstrap/publication/'
        div.appendChild(a);
        pubRow.querySelector('.row').appendChild(div);

        // hide delete buttons for REPAiR (events are deactivated as well)
        var delButtons = Array.prototype.slice.call(this.el.querySelectorAll('button.clear'));
        delButtons.push(this.el.querySelector('#remove-keyflow'));
        delButtons.forEach(function(btn){
            btn.style.display = 'none';
        })
        this.fillGeom();
    },

    fillGeom: function(){
        var focusarea = this.caseStudy.get('properties').focusarea,
            region = this.caseStudy.get('geometry');
        focusarea = (focusarea) ? JSON.stringify(focusarea): '';
        region = (region) ? JSON.stringify(region): '';
        this.el.querySelector('#focusarea-input').value = focusarea;
        this.el.querySelector('#csregion-input').value = region;
    },

    patchFocusarea: function(){
        var _this = this;
        this.caseStudy.save(
            {focusarea: this.el.querySelector('#focusarea-input').value},
            {
                success: function(res){
                    var msg = gettext('Focusarea updated');
                    _this.log('<p style="color: green;">' + msg + '</p>');
                },
                error: function(res, m){
                    var msg = gettext('Focusarea update failed');
                    msg += ': ' + m.responseText;
                    _this.log('<p style="color: red;">' + msg + '</p>');
                    _this.onError(res);
                },
                patch: true
            }
        )
    },

    patchRegion: function(){
        var _this = this;
        this.caseStudy.save(
            {geom: this.el.querySelector('#csregion-input').value},
            {
                success: function(res){
                    var msg = gettext('Casestudy Region updated');
                    _this.log('<p style="color: green;">' + msg + '</p>');
                },
                error: function(res, m){
                    var msg = gettext('Casestudy Region update failed');
                    msg += ': ' + m.responseText;
                    _this.log('<p style="color: red;">' + msg + '</p>');
                    _this.onError(res);
                },
                patch: true
            }
        )
    },

    removeKeyflow: function(){
        var _this = this;
        function destroyKeyflow(){
            _this.model.destroy({
                data: {
                    'override_protection': true
                },
                processData: true,
                success: function(){
                    document.querySelector('body').style.opacity=0.3;
                    location.reload();
                },
                error: _this.onError
            })
        }

        this.confirm({
            message: gettext('Do you really want to delete the keyflow and <b>ALL</b> of its data?'),
            onConfirm: function(el){
                _this.confirm({
                        message: gettext('Are you sure?'),
                        onConfirm: destroyKeyflow
                    }
                )
            }
        })
    },

    clearData: function(evt){
        var _this = this,
            btn = evt.target,
            tag = btn.dataset['tag'],
            data = {},
            row = this.el.querySelector('.row[data-tag="' + tag +  '"]');

        // query keyflow related only (additionally to route)
        if (this.forceKeyflowRelation.includes(tag))
            data['keyflow'] = this.model.id;

        function destroyModels(collection, cascaded){
            var i = collection.length,
                ie = 0, is = 0,
                u_msg = gettext('Removing data') + ' ' + tag;
            _this.log(u_msg);
            _this.log('-'.repeat(u_msg.length * 1.4));

            if (i === 0){
                _this.log('<p>' + gettext('Nothing to remove') + '</p>');
                _this.loader.deactivate();
                return;
            }
            function done(){
                var msg = '',
                    color = 'green',
                    msgType = 'success';

                var successMsg = is + ' ' + gettext('entries removed') + '  ',
                    errorMsg = ie + ' ' + gettext('entries failed to remove');

                if (is > 0 && ie === 0){
                    msg = successMsg;
                }
                else if (ie > 0 && is === 0){
                    msg += errorMsg;
                    msgType = 'danger';
                    color = 'red';
                }
                else {
                    msg = successMsg + '; ' + errorMsg;
                    msgType = 'warning';
                    color = '#9a9a00';
                }
                var msgWrapper = document.createElement('p');
                msgWrapper.innerHTML = msg;

                var alertDiv = _this.bootstrapAlert(msgWrapper.outerHTML, {
                    parentEl: row,
                    type: msgType,
                    dismissible: true
                })
                alertDiv.querySelector('.close').style.top = '-20px';
                _this.log('<p style="color:' + color + ';">' + msg + '</p>')
                _this.loader.deactivate();
                _this.refreshStatus();
            }
            while (model = collection.first()) {

                model.destroy({
                    data: {
                        'override_protection': cascaded
                    },
                    processData: true,
                    success: function(res){
                        var m_repr = JSON.stringify(res.toJSON());
                        msg = gettext('Successfully deleted') + ' ' + m_repr;
                        _this.log(msg)
                        i -= 1;
                        is += 1;
                        if (i < 1) done();
                    },
                    error: function(m, res){
                        msg = res.responseText || res;
                        _this.log('<p style="color: red;">' + msg + '</p>')
                        i -= 1;
                        ie += 1;
                        if (i < 1) done();
                    }
                });
            }
        }
        var Collection = this.geolocations.includes(tag) ? GeoLocations : GDSECollection;

        var collection = new Collection( {}, {
            apiTag: tag, apiIds: [ this.caseStudy.id, this.model.id ]
        });

        var div = document.createElement('div'),
            checkbox = document.createElement('input');

        checkbox.type = 'checkbox';
        checkbox.style.marginRight = '10px';
        checkbox.style.float = 'left';
        div.innerHTML = gettext('Force CASCADED deletion (delete referencing objects, even if protected)');
        div.style.fontSize = '0.8em';
        div.style.marginTop = '20px';
        div.appendChild(checkbox);

        this.confirm({
            message: gettext('Do you really want to delete the existing data and the related data?'),
            elements: [div],
            onConfirm: function(){
                var cascaded = checkbox.checked;
                _this.loader.activate();
                collection.fetch({
                    data: data,
                    success: function(c){
                        destroyModels(c, checkbox.checked)
                    },
                    error: _this.onError
                })
            }
        })
    },

    log: function(text){
        this.logArea.innerHTML += text + '<br>';
        this.logArea.scrollTop = this.logArea.scrollHeight;
    },

    upload: function(evt){
        var _this = this,
            btn = evt.target,
            tag = btn.dataset['tag'];

        if (!tag) return;

        var row = this.el.querySelector('.row[data-tag="' + tag +  '"]'),
            input = row.querySelector('input[type="file"]'),
            files = input.files,
            encoding = this.el.querySelector('#encoding-select').value;

        if (files.length === 0){
            this.alert(gettext('No file selected to upload!'));
            return;
        }

        var data = {
            'bulk_upload': files[0],
            'encoding': encoding
        }

        var model = new GDSEModel( {}, {
            apiTag: tag, apiIds: [ this.caseStudy.id, this.model.id ]
        });

        function upload(){
            _this.loader.activate();
            var u_msg = gettext('Uploading') + ' ' + files[0].name;
            _this.log(u_msg);
            _this.log('-'.repeat(u_msg.length * 1.4));
            model.save(data, {
                success: function (res) {
                    var res = res.toJSON(),
                        updated = res.updated,
                        created = res.created;
                    _this.log(gettext('Created models:'));
                    if (created.length == 0) _this.log('-');
                    created.forEach(function(m){
                        _this.log(JSON.stringify(m));
                    })
                    _this.log(gettext('Updated models:'));
                    if (updated.length == 0) _this.log('-');
                    updated.forEach(function(m){
                        _this.log(JSON.stringify(m));
                    })
                    var div = document.createElement('div'),
                        title = document.createElement('strong'),
                        msgWrapper = document.createElement('p');
                    title.style.float = 'left';
                    title.style.marginRight = '5px';
                    title.innerHTML = gettext('Success') + '!';
                    div.appendChild(title);
                    div.appendChild(msgWrapper);

                    msgWrapper.innerHTML = res.created.length + ' entries created, ' + res.updated.length + ' entries updated';
                    var alertDiv = _this.bootstrapAlert(div.innerHTML, {
                        parentEl: row,
                        type: 'success',
                        dismissible: true
                    })
                    msgWrapper.style.color = 'green';
                    title.style.color = 'green';
                    // that is not very elegant, but when adding a div to the alert
                    // the close button is shifted
                    alertDiv.querySelector('.close').style.top = '-20px';
                    _this.log(div.innerHTML);
                    _this.loader.deactivate();
                    _this.refreshStatus(tag);
                    // special case: uploading levels removes existing areas
                    if (tag === 'arealevels') _this.refreshStatus('allareas')
                },
                error: function (res, r) {
                    var div = document.createElement('div'),
                        title = document.createElement('strong'),
                        msgWrapper = document.createElement('p'),
                        msg;
                    title.style.float = 'left';
                    title.style.marginRight = '5px';
                    title.innerHTML = gettext('Error') + '!';
                    msgWrapper.style.float = 'left';
                    msgWrapper.style.marginRight = '10px';
                    div.appendChild(title);
                    div.appendChild(msgWrapper);

                    if (res.responseJSON && res.responseJSON.message){
                        msg = res.responseJSON.message;
                        var url = res.responseJSON.file_url;
                        if (url){
                            var download = _this.createDownloadIcon(url);
                            div.appendChild(download);
                        }
                    }
                    else
                        msg += res.responseText;

                    msgWrapper.innerHTML = msg;

                    var alertDiv = _this.bootstrapAlert(div.innerHTML, {
                        parentEl: row,
                        type: 'danger',
                        dismissible: true
                    })
                    alertDiv.style.overflow = 'hidden';
                    alertDiv.querySelector('.close').style.top = '-20px';
                    msgWrapper.style.color = 'red';
                    title.style.color = 'red';
                    _this.log(div.innerHTML)
                    _this.loader.deactivate()
                },
            });
        }

        // special case: uploading levels removes existing areas
        if (tag === 'arealevels'){
            this.confirm({
                message: gettext('Warning: Uploading Area Levels removes all Areas in the casestudy as well. Do you wish to continue?'),
                onConfirm: upload
            })
        }
        else upload()
    },

    createDownloadIcon: function(url){
        var div = document.createElement('div'),
            span = document.createElement('span'),
            a = document.createElement('a');
        span.classList.add('fas', 'fa-save');
        span.style.float = 'left';
        span.style.marginRight = '5px';
        a.setAttribute('href', url);
        a.innerHTML = gettext('Response');
        div.appendChild(a);
        a.appendChild(span);
        return div;
    },

    refreshStatus: function(tag){
        var _this = this,
            rows;

        this.fillGeom();

        if (tag && typeof tag === 'string')
            rows = [this.el.querySelector('.upload.row[data-tag="' + tag + '"]')];
        else
            rows = Array.prototype.slice.call(this.el.querySelectorAll('.upload.row'));

        rows.forEach(function(row){
            var countDiv = row.querySelector('.count'),
                tag = row.dataset['tag'],
                data = {};

            if (!tag) return;

            var Collection = _this.geolocations.includes(tag) ? GeoLocations : GDSECollection;
            var collection = new Collection( {}, {
                apiTag: tag, apiIds: [ _this.caseStudy.id, _this.model.id ]
            });

            // reduce the amount of data returned by paginated collections
            collection.state.pageSize = 1;

            var forceKeyflow = _this.forceKeyflowRelation.includes(tag);

            if (forceKeyflow)
                data['keyflow'] = _this.model.id;

            var count = '?';
            countDiv.innerHTML = gettext('count') + ': ' + count;

            collection.fetch({
                data: data,
                success: function(){
                    // paginated collections return the count
                    // else get the length of the response
                    var count = collection.count || collection.length;
                    countDiv.innerHTML = gettext('count');
                    if (forceKeyflow)
                        countDiv.innerHTML += ' (' + gettext('defaults excluded') + ')'
                    countDiv.innerHTML += ': ' + count;
                }
            });
        });
    }

});
return BulkUploadView;
}
);
