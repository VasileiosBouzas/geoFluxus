require(['d3', 'models/casestudy', 'views/status-quo/flows', 'views/status-quo/targets',
        'views/status-quo/challenges-aims', 'views/status-quo/evaluation',
        'visualizations/mapviewer', 
        'app-config', 'utils/overrides', 'base'
], function (d3, CaseStudy, FlowsView, TargetsView, ChallengesAimsView, 
             EvaluationView, MapViewer, appConfig) {

  renderWorkshop = function(caseStudy){
    var flowsView = new FlowsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('flows'),
      template: 'flows-template'
    })
    var challengesView = new ChallengesAimsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('challenges'),
      template: 'challenges-aims-template'
    })
    var targetsView = new TargetsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('targets'),
      template: 'targets-template'
    })
    var evaluationView = new EvaluationView({ 
      caseStudy: caseStudy,
      el: document.getElementById('evaluation'),
      template: 'evaluation-template'
    })
  };

  renderSetup = function(caseStudy){
    var flowsView = new FlowsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('flows'),
      template: 'flows-template'
    })
    var challengesView = new ChallengesAimsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('challenges'),
      template: 'challenges-aims-template'
    })
    var targetsView = new TargetsView({ 
      caseStudy: caseStudy,
      el: document.getElementById('targets'),
      template: 'targets-template'
    })
    var evaluationView = new EvaluationView({ 
      caseStudy: caseStudy,
      el: document.getElementById('evaluation'),
      template: 'evaluation-template'
    })
  };
  
  var session = appConfig.getSession(
    function(session){
      var mode = session['mode'],
          caseStudyId = session['casestudy'],
          caseStudy = new CaseStudy({id: caseStudyId});
    
      caseStudy.fetch({success: function(){
        if (Number(mode) == 1) {
          renderSetup(caseStudy);
        }
        else {
          renderWorkshop(caseStudy);
        }
      }});
  });
});