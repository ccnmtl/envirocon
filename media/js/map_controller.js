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
    else {
      hideElement("legend-conflict");
    }
}

function changeBaseMap(evt,elt/*optional*/) {
  elt = (elt)?elt : evt.src();
  var map = elt.value;
  swapElementClass("basemap", currentmap, map);
  if($("legend-"+currentmap)) {
    hideElement("legend-"+currentmap);
  }
  if($("legend-"+map)) {
    showElement("legend-"+map);
  }
  currentmap = map;
}

function toggleLayer(evt,elt/*optional*/) {
  elt = (elt) ? elt : evt.src();
  var layer = elt.value;
  var checked = elt.checked;
  var conflict = false;
  if(layer == "wb2" || layer == "wb3") {
    if(checked){
      showElement("layer-"+layer+"-conflict");
      showElement("legend-conflict");
      conflict = true;
    }
    else {
      hideElement("layer-"+layer+"-conflict");
      conflict = false;
    }
  }
  else {
    if(checked) {
      showElement("layer-"+layer);
      showElement("legend-"+layer);
      if(layer=="conflict") { conflict = true; }
    }
    else {
      hideElement("layer-"+layer);
      if(layer=="conflict") { conflict = false; }
      else { hideElement("legend-"+layer); }
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