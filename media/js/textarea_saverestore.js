/* for games with multiple textareas */

var text_vars = {}

function saveRestore(e) {
  if (tinyMCE) {tinyMCE.triggerSave();}
  boxes = formContents(e.src());
  // formContents returns [listOfNames, listOfValues];

  //delete old
  //for (a in text_vars) {
	//delete text_vars[a];
  //}

  //enter new
  for (var i=0; i<boxes[0].length; i++) {
    text_vars[boxes[0][i]] = boxes[1][i];
  }

  //overridden from stopFormListener, so we call it ourselves
  if(GameSystem.published == "DefaultNext") {
    GameSystem.quiet = true;
    var def = GameSystem.saveState(e);
    def.addCallback(function() {
      document.location = "page3";
    });
  }
  else if(GameSystem.published == "DefaultPrev") {
    GameSystem.quiet = true;
    var def = GameSystem.saveState(e);
    def.addCallback(function() {
      document.location = "page2";
    });
  }
  else {
    GameSystem.saveState(e);
  }
  e.stop()
}

function initSaveRestore() {
    var assn_form = $("assignment-form");
    connect(assn_form, "onsubmit", saveRestore);
    GameSystem.stopFormListener();

    text_vars = GameSystem.getVariable(game_variables[0]);

    for(a in text_vars) {
      if($(a)) {
        $(a).value = text_vars[a];
      }
    }

    // fix tinyMCE load bugginess
    forEach(getElementsByTagAndClassName("textarea", "wysiwyg"), function(elt) {
        if (tinyMCE && (tinyMCE.get(elt.id))) {
            tinyMCE.get(elt.id).load();
        }
    });
}

connect(GameSystem, 'stateLoaded', initSaveRestore);