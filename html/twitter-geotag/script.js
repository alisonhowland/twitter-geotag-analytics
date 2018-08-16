let timeForm = document.getElementById('form');
let startTimeInput = document.getElementById('from');
let endTimeInput = document.getElementById('to');

// Initialized the datepicker
$( function() {
   $( "#datepicker" ).datepicker({ 
   });
} );
$( "#dialog" ).dialog({
    create: function(e, ui) {
        // 'this' is #dialog
        // get the whole widget (.ui-dialog) with .dialog('widget')
        $(this).dialog('widget')
            // find the title bar element
            .find('.ui-dialog-titlebar')
            // alter the css classes
            .removeClass('ui-corner-all')
            .addClass('ui-corner-top');
    }
});

$.datepicker.setDefaults({
       dateFormat: 'yy-mm-dd'
});
// Clear and update the map's existing layers when a date is selected
//     from the datepicker
$('#datepicker').datepicker({
   onSelect: function(dateText, inst) {
      clearExistingLayers();
      locationWMS = getWMSLayerDateFilter(dateText, wmsURL, 'tweets_with_location');
      predictionWMS= getWMSLayerDateFilter(dateText, wmsURL, 'tweets_predicted_locations');
      controlLayers.addOverlay(locationWMS, 'Actual Locations')
      controlLayers.addOverlay(predictionWMS, 'Predicted Locations');
      map.addLayer(locationWMS);
      map.addLayer(predictionWMS);
      // Add as the default layer to load
   }});

function clearExistingLayers() {
   map.removeLayer(locationWMS);
   map.removeLayer(predictionWMS);
   controlLayers.removeLayer(locationWMS);
   controlLayers.removeLayer(predictionWMS);

}

// Datepicker Popups calender to Choose date.
/*
 $( function() {
    var dateFormat = "mm/dd/yy",
      from = $( "#from" )
	.datepicker({
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 1
	})
	.on( "change", function() {
	  to.datepicker( "option", "minDate", getDate( this ) );
	}),
      to = $( "#to" ).datepicker({
	defaultDate: "+1w",
	changeMonth: true,
	numberOfMonths: 1
      })
      .on( "change", function() {
	from.datepicker( "option", "maxDate", getDate( this ) );
      });

    function getDate( element ) {
      var date;
      try {
	date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
	date = null;
      }

      return date;
    }
  } );
  */
function createMap() {

   // initialize the map
   let map = L.map('map', {
      center: [31.77, -92.69], // EDIT latitude, longitude to re-center map
      zoom: 5,  // EDIT from 1 to 18 -- decrease to zoom out, increase to zoom in
      scrollWheelZoom: true,
      zoomControl: false // Disable default position of zoom controle (upper left)
   });

   /*
L.easyButton('<img src="/path/to/img/of/penguin.png">', function(btn, map){
       let antarctica = [-77,70];
       map.setView(antarctica);
}).addTo( map);
*/
   // Add zoom control to the lower right corner
   L.control.zoom({
      position:'topleft'
   }).addTo(map);
   
(function() {
      var control = new L.Control({position:'topleft'});
      control.onAdd = function(map) {
		  var azoom = L.DomUtil.create('a','resetzoom');
		  azoom.innerHTML = "Reset Zoom";
		  L.DomEvent
		     .disableClickPropagation(azoom)
		     .addListener(azoom, 'click', function() {
				       map.setView(map.options.center, map.options.zoom);
				    },azoom);
		  return azoom;
	       };
      return control;
}())
.addTo(map);

   L.control.scale().addTo(map);
   return map;
}

var lastClickedLayer;


function createLayerController() {
   /* Control panel to display map layers */
   let controlLayers = L.control.layers( null, null, {
      position: "topright",
      collapsed: false
   }).addTo(map);

   // Time-based heatmap -- not yet implemented
   /*
let reports = L.esri.Heat.heatmapFeatureLayer({
    url: 'https://services.arcgis.com/rOo16HdIMeOBI4Mb/ArcGIS/rest/services/Graffiti_Reports/FeatureServer/0',
    timeField: 'CreatedDate',
    from: new Date(startTimeInput.value),
    to: new Date(endTimeInput.value),
    radius: 12
  }).addTo(map);
  */
   /* Carto light-gray basemap tiles with labels */
   let light = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.pn g', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a  href="https://carto.com/attribution">CARTO</a>'
   }); // EDIT - insert or remove ".addTo(map)" before last semicolon to display by default
   controlLayers.addBaseLayer(light, 'Light basemap');

   /* Stamen colored terrain basemap tiles with labels */
   let terrain = L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png', {
      attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
   }).addTo(map); // EDIT - insert or remove ".addTo(map)" before last semicolon to display by default
   controlLayers.addBaseLayer(terrain, 'Terrain basemap 1');

   // load a tile layer
   let base =  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
      {
	 attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
	 '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	 'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	 maxZoom: 20,
	 id: 'mapbox.streets',
	 minZoom: 2
      });//.addTo(map);

   controlLayers.addBaseLayer(base, 'Terrain basemap 2');
   let greyBase = L.esri.basemapLayer('Gray');
   let greyLabels = L.esri.basemapLayer('GrayLabels');
   let grey = L.layerGroup([greyBase, greyLabels]);

   controlLayers.addBaseLayer(grey, "Grey basemap");
   return controlLayers;
}

// Create map, base layers, and layer controller
var map = createMap();
var controlLayers = createLayerController();

// Icon and Dialog for date selector 
$('#date-dialog').dialog({
   modal: false, autoOpen: false, closeOnEsc: true,
   open: function() {
	    $("#date-dialog").css("z-index", $(this).parents(".ui-dialog").css("z-index")+1);
 //  position: { my:'left bottom', at:'top', or:'#map' }
   }});

new L.Control.jQueryDialog({
   dialogId: 'date-dialog',
   tooltip: "Filter results by date",
   iconClass: 'fa fa-calendar-alt'
}).addTo(map);

// Define the base URLs for WFS and WMS services
var wfsURL = 'http://192.168.16.32:8080/geoserver/cite/ows';
var wmsURL = 'http://192.168.16.32:8080/geoserver/cite/wms';

// Fetches the WMS info from Geoserver and returns a new WMS Leaflet layer for the GeoJSON dat
// Parameters: name of the geoserver layer (without the preceding store name (e.g. 
//     "predicted_locations" for the info stored in "cite:predcited_locations")
function getWMSLayer(layerName) {
   let wmsLayer = L.tileLayer.wms(wmsURL, {
      layers: 'cite:' + layerName,
      format: 'image/png',
      transparent: true
   });
   return wmsLayer;
}

// Returns a layer consisting of only dates that match the input
function getWMSLayerDateFilter(date, wmsURL, layerName ) {
   let layer = L.tileLayer.wms(wmsURL, {
      layers: 'cite:' + layerName,
      format: 'image/png',
      transparent: true,
      CQL_FILTER: 'ingest_date =' + date
   });
   return layer;
}
/*
   // Returns a layer consisting of data/events within the specified timeframe
   // TODO: 
function dateFilteredWMSLayer(startDate, endDate){
   let layer = L.tileLayer.wms(wmsURL, {
      layers: 'cite:tweets_with_location',
      format: 'image/png',
      transparent: true,
      //      CQL_FILTER:'timestamp AFTER ' + startDate + ' AND timestamp BEFORE ' + endDate
   });
   return layer;
}
*/

      // Create the WMS Layer
      let locationWMS= getWMSLayer('tweets_with_location');
      let predictionWMS= getWMSLayer('tweets_predicted_locations');

      // Create group for tweets contaiing predicted location data
      // Layer groups will hold two layers: the WMS and the WFS layers of the same data.
      //    This will enable us to easily add/remove the WMS and WFS layers upon 
      //    changing zoom levels and/or selecting or deselecting the layer control option

      controlLayers.addOverlay(locationWMS, 'Actual Locations');
      controlLayers.addOverlay(predictionWMS, 'PredictedLocations');
      // Add as the default layer to load
      map.addLayer(locationWMS);
      //let WMSLayer = getWMSLayer();
      // ------------------------------------------------------
      // --- Function that loads the WFS layer to the map ----
      var locationWFS = null;
      var predictionWFS = null;
      function getWFSurl(wfsURL, layerName ) {
	 // define WFS default parameters 
	 let defaultParameters = {
	    service : 'WFS',
	    version : '2.0',
	    request : 'GetFeature',
	    typeName : 'cite:' + layerName,
	    outputFormat : 'text/javascript',
	    format_options : 'callback:getJson' + layerName,
	    maxFeatures: 200,
	    //   format_options :  'callback: getJson',
	    SrsName : 'EPSG:4326'
	 };

	 let parameters = L.Util.extend(defaultParameters);
	 let URL = wfsURL + L.Util.getParamString(parameters);
	 return URL;
      }
// define url for ajax
wfsURLLocations = getWFSurl(wfsURL, 'tweets_with_location');
wfsURLPredictions = getWFSurl(wfsURL, 'tweets_predicted_locations');

// Get the WFS for tweet data with included location information
$.ajax({
   url: wfsURLLocations,
   dataType: 'jsonp',
   jsonpCallback: 'getJsontweets_with_location' ,
   success : function(data) {
      locationWFS = L.geoJson(data, {
	 // letiable to define later: will tell us which layer group we should
	 // add the new layer to 
	 style: function (feature) {
	    return {
	       stroke: false,
	       fillColor: 'FFFFFF',
	       fillOpacity: 0
	    };
	 },
	 // Set the popup text/content for each point
	 onEachFeature: function (feature, layer) {
	    popupOptions = {maxWidth: 200};
	    // Identify whether layer is a prediction or not
	    layer.bindPopup("<b>" + feature.properties.place_name + "</b><br>"
	       + "<b>ID: </b><a href='http://192.168.16.31:5601/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:f81e14c0-91b1-11e8-85bf-677bb0bf1eac,interval:auto,query:(language:lucene,query:%27" + feature.properties.tweet_id + "%27),sort:!(_score,desc))'>" + feature.properties.tweet_id  + "</a><br>"
	       + "<b>Time: </b> " + feature.properties.date +" <br>"
	       + "<b>Tweet:</b> \"" + feature.properties.tweet_text + "\" <br>"
	       + "<b>Hashtags:</b> \"" + feature.properties.hashtags + "\" <br>"
	       ,popupOptions);
	 }
      });

   }
});

// AJAX call for WFS data for predicted locations of tweets
$.ajax({
   url: wfsURLPredictions,
   dataType: 'jsonp',
   jsonpCallback: 'getJsontweets_predicted_locations',
   success : function(data) {
      predictionWFS = L.geoJson(data, {
	 // letiable to define later: will tell us which layer group we should
	 // add the new layer to 
	 style: function (feature) {
	    return {
	       stroke: false,
	       fillColor: 'FFFFFF',
	       fillOpacity: 0
	    };
	 },
	 // Set the popup text/content for each point
	 onEachFeature: function (feature, layer) {
	    popupOptions = {maxWidth: 200};
	    // Identify whether layer is a prediction or not
	    layer.bindPopup("<b>" + feature.properties.place_name + "</b><br>"
	       + "<b>ID: </b><a href='http://192.168.16.31:5601/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:f81e14c0-91b1-11e8-85bf-677bb0bf1eac,interval:auto,query:(language:lucene,query:%27" + feature.properties.tweet_id + "%27),sort:!(_score,desc))'>" + feature.properties.tweet_id  + "</a><br>"
	       + "<b>Time: </b> " + feature.properties.date +" <br>"
	       + "<b>Tweet:</b> \"" + feature.properties.tweet_text + "\" <br>"
	       + "<b>Hashtags:</b> \"" + feature.properties.hashtags + "\" <br>"
	       + "<b>Mentioned Locations: </b> " + feature.properties.mentioned_locations + " <br>"
	       ,popupOptions);
	 }
      });

   }
});

// Create url for WFS call
/*
   // Set the WFS Layer for predicted tweets
let WFSPredictionsURL= setWFSURL(wfsURL, 'tweets_predicted_locations');
let WFSPredictionsLayer= null;
// Create url for WFS call
$.ajax({
   url: WFSPredictionsURL,
   dataType: 'jsonp',
   jsonpCallback: 'getJson',
   success : function (response) {
      WFSPredictionsLayer= L.geoJson(response, {
	 style: function (feature) {
	    return {
	       stroke: false,
	       fillColor: 'FFFFFF',
	       fillOpacity: 0
	    };
	 },
	 // Set the popup text/content for each point
	 onEachFeature: function (feature, layer) {
	    popupOptions = {maxWidth: 200};
	    layer.bindPopup("<b> Predicted location: " + feature.properties.place_name + "</b><br>"
	       + "<b>ID: </b><a href='http://192.168.16.31:5601/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:f81e14c0-91b1-11e8-85bf-677bb0bf1eac,interval:auto ,query:(language:lucene, query:%27" + feature.properties.tweet_id + "%27),sort:!(_score,desc))'>" + feature.properties.tweet_id  + "</a><br>"
	       + "<b>Time: </b> " + feature.properties.date +" <br>"
	       + "<b>Tweet:</b> \"" + feature.properties.tweet_text + "\" <br>"
	       + "<b>Hashtags:</b> \"" + feature.properties.hashtags + "\" <br>"
	       ,popupOptions);
	 }
      });
//                  WFSLayer.addTo(map);
   }
});
*/
map.on('zoomend', function() {
   if (map.getZoom() <13){
      if (map.hasLayer(locationWFS)) {
	 map.removeLayer(locationWFS);
      }
      if (map.hasLayer(predictionWFS)) {
	 map.removeLayer(predictionWFS);
      }
   }
   if (map.getZoom() >= 13) {
      if (map.hasLayer(locationWMS) && map.hasLayer(locationWFS )== false) {
	 map.addLayer(locationWFS);
      }
      if (map.hasLayer(predictionWMS) && map.hasLayer(predictionWFS) == false) {
	 map.addLayer(predictionWFS);
      }
   }
});
/*
map.on('zoomend', function() {
   if (map.getZoom() <13){
      if (map.hasLayer(locationWMS)) {
	 if (map.hasLayer(locationWFS)) {
	    map.removeLayer(locationWFS);
	 }
      }
      if (map.hasLayer(predictionWMS)) {
	 if (map.hasLayer(predictionWFS)) {
	    map.removeLayer(predictionWFS);
	 }
      }
   }
   if (map.getZoom() >= 13){
      if (map.hasLayer(locationWMS)) {
	 if (!map.hasLayer(locationWFS)){
	    map.addLayer(locationWFS);
	 }
      }
      if (map.hasLayer(predictionWMS)) {
	 if(!map.hasLayer(predictionWFS)) {
	    map.addLayer(predictionWFS);
	 }
      }
   }

});
*/
