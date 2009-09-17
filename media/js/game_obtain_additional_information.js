/* for the Obtain Additional Information exercise (week 1) */

var report_vars = {}

function validateReports(e) {
  checkboxes = formContents(e.src());
  // formContents returns [listOfNames, listOfValues];
  // blank checkboxes are not reported.
  // ergo: the # of checked boxes == the # of "reports" in listOfNames
  var count = 0;
    var vals = {};
  for(var i=0; i<checkboxes[0].length; i++){
    if(checkboxes[0][i] == "reports") { 
	count++; 
	vals[checkboxes[1][i]]=1;
    }
  }
  if(count > 5) {
    alert("You have selected more than five reports.\nPlease review your selections.");
    e.stop();
    return false;
  }
  if(count < 5) {
    alert("You have selected fewer than five reports.\nPlease review your selections.");
    e.stop();
    return false;
  }
    //delete old
    for (a in report_vars) {
	delete report_vars[a];
    }
    //enter new
    for (a in vals) {
	report_vars[a] = vals[a];
    }
    //overridden from stopFormListener, so we call it ourselves
    GameSystem.saveState(e);
    e.stop()
}

function initValidateReports() {
    var assn_form = $("assignment-form");
  connect(assn_form, "onsubmit", validateReports);
    GameSystem.stopFormListener();

  //connect(GameSystem, "beforesavestate", validateReports);
    report_vars = GameSystem.getVariable('additional_information');
    forEach (assn_form.elements, function(elt) {
	elt.checked = (elt.value in report_vars);
    });
}

addLoadEvent(initValidateReports);