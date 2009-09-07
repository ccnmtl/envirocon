/* for the Obtain Additional Information exercise (week 1) */

function validateReports(e) {
  checkboxes = formContents(e.src());
  // formContents returns [listOfNames, listOfValues];
  // blank checkboxes are not reported.
  // ergo: the # of checked boxes == the # of "reports" in listOfNames
  var count = 0;
  for(var i=0; i<checkboxes[0].length; i++){
    if(checkboxes[0][i] == "reports") { count++; }
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
}

function initValidateReports() {
  connect("assignment-form", "onsubmit", validateReports);
}

addLoadEvent(initValidateReports);