function toggleInfo(e) {
  var parent = getFirstParentByTagAndClassName(e.src(), "div", "*");
  var child = getFirstElementByTagAndClassName("*", "toggle", parent);
  var visible = getStyle(child, "display");
  if(visible == "block") {
    setStyle(child, {'display':'none'});
  }
  else {
    setStyle(child, {'display':'block'});
  }
}

function initToggleInfo() {
  forEach(getElementsByTagAndClassName("*", "toggle-control"), function(elem) {
    connect(elem, "onclick", toggleInfo);
  });
}

addLoadEvent(initToggleInfo);