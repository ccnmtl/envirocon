function toggleInfo(e) {
  var parent = getFirstParentByTagAndClassName(e.src(), "div");
  var child = getFirstElementByTagAndClassName("*", "toggle", parent);
  var visible = getStyle(child, "display");
  if(visible == "block") {
      toggleClose(child, e.src());
  }
  else {
      toggleOpen(child, e.src());
  }
}

function initToggleInfo() {
  forEach(getElementsByTagAndClassName("*", "toggle-control"), function(elem) {
    connect(elem, "onclick", toggleInfo);
  });
    var toggleall_checkbox = $('toggle-all');
    if (toggleall_checkbox != null) {
        connect(toggleall_checkbox, "onclick", toggleAll);
    }
}

function toggleOpen(child, widget) {
    widget = widget || getFirstElementByTagAndClassName(
        "*", "toggle-control",
        getFirstParentByTagAndClassName(child, "div"));
    setStyle(child, {'display':'block'});
    setStyle(widget, {'background-image':'url(/site_media/img/toggle_open.gif)'});
}

function toggleClose(child, widget) {
    widget = widget || getFirstElementByTagAndClassName(
        "*", "toggle-control",
        getFirstParentByTagAndClassName(child, "div"));
    setStyle(child, {'display':'none'});
    setStyle(widget, {'background-image':'url(/site_media/img/toggle_closed.gif)'});
}

function toggleAll(evt) {
    if (evt.src().checked) {
        forEach(getElementsByTagAndClassName("*", "toggle", 'assignment-form'), toggleOpen);
    } else {
        forEach(getElementsByTagAndClassName("*", "toggle", 'assignment-form'), toggleClose);
    }
}

addLoadEvent(initToggleInfo);