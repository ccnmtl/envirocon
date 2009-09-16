var currentmap = "basic";
var conflict_boxes = 0;

function changeBaseMap(e) {
  var map = e.src().value;
  swapElementClass("basemap", currentmap, map);
  if($("legend-"+currentmap)) {
    setStyle("legend-"+currentmap, {"display":"none"});
  }
  if($("legend-"+map)) {
    setStyle("legend-"+map, {"display":"block"});
  }
  currentmap = map;
}

function toggleLayer(e) {
  var layer = e.src().value;
  var checked = e.src().checked;
  if(layer == "wb2" || layer == "wb3") {
    // layer-wb#-peace, layer-wb#-humanitarian, layer-wb#-conflict
    if(checked){
      setStyle("layer-"+layer+"-peace", {"display":"block"});
      setStyle("layer-"+layer+"-humanitarian", {"display":"block"});
      setStyle("layer-"+layer+"-conflict", {"display":"block"});
      setStyle("legend-conflict", {"display":"block"});
      conflict_boxes++;
    }
    else {
      setStyle("layer-"+layer+"-peace", {"display":"none"});
      setStyle("layer-"+layer+"-humanitarian", {"display":"none"});
      setStyle("layer-"+layer+"-conflict", {"display":"none"});
      conflict_boxes--;
    }
  }
  else {
    if(checked) {
      setStyle("layer-"+layer, {"display":"block"});
      setStyle("legend-"+layer, {"display":"block"});
      if(layer=="conflict") { conflict_boxes++; }
    }
    else {
      setStyle("layer-"+layer, {"display":"none"});
      if(layer=="conflict") { conflict_boxes--; }
      else { setStyle("legend-"+layer, {"display":"none"}); }
    }
  }

  // hide conflict legend if none of wb2, wb3, or conflict is checked
  if(conflict_boxes==0) {
    setStyle("legend-conflict", {"display":"none"});
  }
}

function initMapController() {
  connect("base-map-dropdown", "onchange", changeBaseMap);
  forEach(getElementsByTagAndClassName("input", "layer-choice"), function(elem) {
    connect(elem, "onclick", toggleLayer);
  });  
}

addLoadEvent(initMapController);