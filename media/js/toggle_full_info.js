function toggleInfo(e) {
  var parent = getFirstParentByTagAndClassName(e.src(), "div", "*");
  var child = getFirstElementByTagAndClassName("*", "toggle", parent);
  var visible = getStyle(child, "display");
  if(visible == "block") {
    setStyle(child, {'display':'none'});
    setStyle(e.src(), {'background-image':'url(/site_media/img/toggle_closed.gif)'});
  }
  else {
    setStyle(child, {'display':'block'});
    setStyle(e.src(), {'background-image':'url(/site_media/img/toggle_open.gif)'});
  }
}

function initToggleInfo() {
  forEach(getElementsByTagAndClassName("*", "toggle-control"), function(elem) {
    connect(elem, "onclick", toggleInfo);
  });
}

addLoadEvent(initToggleInfo);