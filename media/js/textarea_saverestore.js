/* for games with multiple textareas */

var text_vars = {}

function saveRestore(e) {
  boxes = formContents(e.src());
  // formContents returns [listOfNames, listOfValues];
  var vals = {};

  //delete old
  for (a in text_vars) {
	delete text_vars[a];
  }
  //enter new
  for (a in boxes) {
    //alert(boxes[a]);
    text_vars[a] = boxes[a];
  }
  
  //alert(text_vars);
  
  //overridden from stopFormListener, so we call it ourselves
  GameSystem.saveState(e);
  e.stop()
}

function initSaveRestore() {
    var assn_form = $("assignment-form");
    connect(assn_form, "onsubmit", saveRestore);
    GameSystem.stopFormListener();

    text_vars = GameSystem.getVariable(game_variables[0]);

    if(text_vars[0]) {
      for(var i=0; i<text_vars[0].length; i++){
        var name = text_vars[0][i];
        var val = text_vars[1][i];
        if($(name)) {
          $(name).value = val;
        }
      }
    }
}

addLoadEvent(initSaveRestore);