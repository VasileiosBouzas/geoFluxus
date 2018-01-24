define(['browser-cookies'],
  function (cookies) {
  
    /**
     * global configuration file
     * @module config
     */
    var config = {
      URL: '/' // base application URL
    };
    
    /**
     * callback for session
     *
     * @callback module:config~onSuccess
     * @param {Object} json -  fetched session object
     */
    
    /** 
     * fetch the current session object from the server 
     *
     * @param {module:config~onSuccess} callback - called when session object is successfully fetched
     * 
     * @method getSession
     * @memberof module:config
     */
    config.getSession = function(callback){
    
      //var sessionid = cookies.get('sessionid');
      //console.log(sessionid)
      fetch('/login/session', {
          headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          credentials: 'include'
        }).then(response => response.json()).then(json => callback(json));
    }
    
    /** urls to resources in api
     * @name api
     * @memberof module:config
     */
    config.api = {
      base:                 '/api', // base Rest-API URL
      stakeholders:         '/api/stakeholders/',
      publications:         '/api/publications/',
      casestudies:          '/api/casestudies/',
      materials:            '/api/materials/',
      keyflows:             '/api/keyflows/',
      qualities:            '/api/qualities',
      reasons:              '/api/reasons',
      keyflowsInCaseStudy:  '/api/casestudies/{0}/keyflows',
      activitygroups:       '/api/casestudies/{0}/keyflows/{1}/activitygroups',
      activities:           '/api/casestudies/{0}/keyflows/{1}/activities',
      actors:               '/api/casestudies/{0}/keyflows/{1}/actors',
      adminLocations:       '/api/casestudies/{0}/keyflows/{1}/administrativelocations',
      opLocations:          '/api/casestudies/{0}/keyflows/{1}/operationallocations',
      activitiesInGroup:    '/api/casestudies/{0}/keyflows/{1}/activitygroups/{2}/activities',
      actorsInActivity:     '/api/casestudies/{0}/keyflows/{1}/activitygroups/{2}/activities/{3}/actors',
      products:             '/api/casestudies/{0}/keyflows/{1}/products',
      activityToActivity:   '/api/casestudies/{0}/keyflows/{1}/activity2activity/',
      groupToGroup:         '/api/casestudies/{0}/keyflows/{1}/group2group/',
      actorToActor:         '/api/casestudies/{0}/keyflows/{1}/actor2actor/',
      groupStock:           '/api/casestudies/{0}/keyflows/{1}/groupstock/',
      activityStock:        '/api/casestudies/{0}/keyflows/{1}/activitystock/',
      actorStock:           '/api/casestudies/{0}/keyflows/{1}/actorstock/',
      arealevels:           '/api/casestudies/{0}/levels',
      areas:                '/api/casestudies/{0}/levels/{1}/areas',
    };
  
    return config;
  }
);
