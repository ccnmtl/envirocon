var funding_vars = {};

var starting_budget = 0;
var budget = 0;

var eligible = [];

function updateBudget() {
  budget = starting_budget;
  forEach(getElementsByTagAndClassName("input", "fund"), function(elem) {
    if(elem.checked) {
      cost = parseFloat($(elem.id + "-cost").innerHTML) * 1000000;  // costs are in millions
      budget = budget - cost;
    }
  });

  updateBudgetDisplay();
}

function resetBudget() {
  budget = starting_budget;
  updateBudgetDisplay();
}

function calculateCosts(e) {
  var cost = getCost(e.src().id);
  var checked = e.src().checked;
  
  /* uncheck others in the group */
  if(checked) {
    var id = e.src().id;
    var group = "";
    var one = "";
    var two = "";
    var regained = 0;
    if(id.indexOf("-low") != -1) {
      group = id.substr(0, id.indexOf("-low"));
      one = "-med";
      two = "-high";
    }
    if(id.indexOf("-med") != -1) {
      group = id.substr(0, id.indexOf("-med"));
      one = "-low";
      two = "-high";
    }
    if(id.indexOf("-high") != -1) {
      group = id.substr(0, id.indexOf("-high"));
      one = "-low";
      two = "-med";
    }
    
    if($(group+one).checked) {
      $(group+one).checked = false;
      regained = getCost(group+one);
    }
    if($(group+two).checked) {
      $(group+two).checked = false;
      regained = getCost(group+two);
    }
    budget = budget - cost + regained;
  }

  else {
    budget = budget + cost;
  }

  updateBudgetDisplay();
}

function validateFundingChoices(e) {
  if(budget < 0) {
    alert("You have agreed to fund more interventions than your budget will allow.\nPlease review your choices.");
    e.stop();
    return false;
  }
  checkboxes = formContents(e.src());
  var vals = {};
  for(var i=0; i<checkboxes[0].length; i++){
    if(checkboxes[0][i] == "fund") {
      vals[checkboxes[1][i]]=1;
    }
  }
  //alert(pts);

  //delete old
  for (a in funding_vars) {
	delete funding_vars[a];
  }
  //enter new
  for (a in vals) {
    funding_vars[a] = vals[a];
  }

  //overridden from stopFormListener, so we call it ourselves
  GameSystem.saveState(e);
  e.stop()
}

function updateBudgetDisplay() {
  $("budget").innerHTML = format_money(budget);
  if(budget < 0) {
    setStyle("budget", {'color':'red'});
  }
  else {
    setStyle("budget", {'color':'white'});
  }
}

function getCost(id) {
  return parseFloat($(id + "-cost").innerHTML) * 1000000;  // costs are in millions
}

// stolen from mvsim (with minor modifications)
function format_money(amount) {
   var sign = "";
   if(amount < 0) { sign = "-"; }
   amount = Math.abs(amount);
   var left = Math.floor(amount*100+0.50000000001)
   //var right = left % 100;
   //if(right<10) { right = "0" + right; }
   left = Math.floor(left/100).toString()
   strCash = sign + "$" + left.split("").reverse().join("").
             replace(/(\d{3})/g,"$1,").replace(/,$/,"").
             split("").reverse().join("");
   return strCash;
}


function initFunding() {
  starting_budget = parseFloat($("budget").innerHTML.replace(/,/g,'').replace(/\$/g,''));
  forEach(getElementsByTagAndClassName("input", "fund"), function(elem) {
    connect(elem, "onclick", calculateCosts);
  });
  var assn_form = $("assignment-form");
  connect(assn_form, "onreset", resetBudget);
  connect(assn_form, "onsubmit", validateFundingChoices);
  GameSystem.stopFormListener();
  
  // load saved state
  funding_vars = GameSystem.getVariable(game_variables[0]);
  forEach (assn_form.elements, function(elt) {
	elt.checked = (elt.value in funding_vars);
  });

  updateBudget();  // run once after loading saved data
  
  // disable ineligible interventions, if any
  if(typeof ineligible == 'object') {
    for(var i=0; i<ineligible.length; i++) {
      $(ineligible[i]).disabled = true;
    }
  }
}

addLoadEvent(initFunding);