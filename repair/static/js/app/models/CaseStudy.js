define(["backbone"],

    function(Backbone) {

        var CaseStudy = Backbone.Model.extend({
          
            urlRoot: '/api/casestudy/',
            idAttribute: "id",
            
            defaults: {
                id: '',
                name: ''
            },

        });
        return CaseStudy;
    }
);