require([
  'd3',
  'visualizations/mapviewer',
], function (d3, MapViewer) {
  var evaluationmap = new MapViewer({
    divid: 'evaluationmap', 
    baseLayers: {"Stamen map tiles": new L.tileLayer('http://{s}tile.stamen.com/toner-lite/{z}/{x}/{y}.png', {
          subdomains: ['','a.','b.','c.','d.'],
          attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>'
        })},
    overlayLayers: {}
  });
  
  var stamen = L.tileLayer('http://{s}tile.stamen.com/toner-lite/{z}/{x}/{y}.png', {
    subdomains: ['','a.','b.','c.','d.'],
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>'
  });
  
  var mapviewer = new MapViewer({
    divid: 'mapviewer',
    baseLayers: {"Stamen map tiles": stamen},
    overlayLayers: {
      "PRODUCTION - Manufacture glass": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/0", useCors: false}),
      "Production Network": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/1", useCors: false}),
      "PRODUCTION - Manufacture beverages": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/2", useCors: false}),
      "Production to Distribution Network": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/3", useCors: false}),
      "DISTRIBUTION - Beverages": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/4", useCors: false}),
      "Distribution to Retail Network": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/5", useCors: false}),
      "RETAIL": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/6", useCors: false}),
      "Retail to Households Network": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/7", useCors: false}),
      "RETAIL + CONSUMPTION - Restaurants": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/8", useCors: false}),
      "CONSUMPTION Neighbourhood centers": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/9", useCors: false}),
      "Household to Facilities Network": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/10", useCors: false}),
      "WASTE MANAGEMENT - Collection": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/11", useCors: false}),
      "WASTE MANAGEMENT - Treatment and disposal": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/12", useCors: false}),
      "WASTE MANAGEMENT - Recovery sorted materials": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/13", useCors: false}),
      "Municipalities": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/14", useCors: false}),
      "AMA Focus Area": L.esri.featureLayer({url: "https://arcgis.labs.vu.nl/arcgis/rest/services/DemoGDSE/MapServer/15", useCors: false}),
    }
  });
});