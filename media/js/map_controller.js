var currentmap = "basic";
var conflict_boxes = 0;

function updateMap() {
    changeBaseMap(false,$('base-map-dropdown'));
    var show_conflicts = false;
    forEach(getElementsByTagAndClassName("input", "layer-choice"), function(elem) {
	show_conflicts = toggleLayer(false,elem) | show_conflicts;
    });
    // hide conflict legend if none of wb2, wb3, or conflict is checked
    if(show_conflicts) {
	showElement("legend-conflict");
    }
}

function changeBaseMap(evt,elt/*optional*/) {
  elt = (elt)?elt : evt.src();
  var map = elt.value;
  swapElementClass("basemap", currentmap, map);
  if($("legend-"+currentmap)) {
    setStyle("legend-"+currentmap, {"display":"none"});
  }
  if($("legend-"+map)) {
    setStyle("legend-"+map, {"display":"block"});
  }
  currentmap = map;
}

function toggleLayer(evt,elt/*optional*/) {
  elt = (elt) ? elt : evt.src();
  var layer = elt.value;
  var checked = elt.checked;
  var conflict = false;
  if(layer == "wb2" || layer == "wb3") {
    // layer-wb#-peace, layer-wb#-humanitarian, layer-wb#-conflict
    if(checked){
      setStyle("layer-"+layer+"-peace", {"display":"block"});
      setStyle("layer-"+layer+"-humanitarian", {"display":"block"});
      setStyle("layer-"+layer+"-conflict", {"display":"block"});
      setStyle("legend-conflict", {"display":"block"});
	conflict = true;
    }
    else {
      setStyle("layer-"+layer+"-peace", {"display":"none"});
      setStyle("layer-"+layer+"-humanitarian", {"display":"none"});
      setStyle("layer-"+layer+"-conflict", {"display":"none"});
	conflict = false;
    }
  }
  else {
    if(checked) {
      setStyle("layer-"+layer, {"display":"block"});
      setStyle("legend-"+layer, {"display":"block"});
      if(layer=="conflict") { conflict = true; }
    }
    else {
      setStyle("layer-"+layer, {"display":"none"});
      if(layer=="conflict") { conflict = false; }
      else { setStyle("legend-"+layer, {"display":"none"}); }
    }
  }

    return conflict;
}

function initMapController() {
  connect("base-map-dropdown", "onchange", changeBaseMap);
  forEach(getElementsByTagAndClassName("input", "layer-choice"), function(elem) {
    connect(elem, "onclick", updateMap);
  });
    updateMap();
}

addLoadEvent(initMapController);