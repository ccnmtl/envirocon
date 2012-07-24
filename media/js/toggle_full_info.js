function initToggleInfo() {
  forEach(getElementsByTagAndClassName("*", "toggle-control"), function(elem) {
    connect(elem, "onclick", toggleInfo);
  });
    var toggleall_checkbox = $('toggle-all');
    if (toggleall_checkbox != null) {
        connect(toggleall_checkbox, "onclick", toggleAll);
    }
}

function toggleInfo(e) {
    var parent = getFirstParentByTagAndClassName(e.src(), "div");
    var visible = /toggle_open/.test(getStyle(e.src(),'backgroundImage'));
    if(visible) {
        toggleClose(parent, e.src());
    }
    else {
        toggleOpen(parent, e.src());
    }
}
function toggleOpen(parent, widget) {
    forEach(getElementsByTagAndClassName('*','toggle',parent), function(child) {
        setStyle(child, {'display':'block'});        
    });
    forEach(getElementsByTagAndClassName('*','toggle-control',parent), function(w){
        setStyle(w, {'background-image':'url(/site_media/img/toggle_open.gif)'});
    });
}

function toggleClose(parent, widget) {
    //widget = widget || getFirstElementByTagAndClassName("*", "toggle-control",parent);
    forEach(getElementsByTagAndClassName('*','toggle',parent), function(child) {
        setStyle(child, {'display':'none'});        
    });
    forEach(getElementsByTagAndClassName('*','toggle-control',parent), function(w){
        setStyle(w, {'background-image':'url(/site_media/img/toggle_closed.gif)'});
    });
}

function toggleAll(evt) {
    if (evt.src().checked) {
        forEach(getElementsByTagAndClassName("*", "toggle", 'assignment-form'), toggleOpen);
    } else {
        forEach(getElementsByTagAndClassName("*", "toggle", 'assignment-form'), toggleClose);
    }
}