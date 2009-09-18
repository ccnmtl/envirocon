var starting_budget = 0;
var budget = 0;

function tallyCosts() {
  forEach(getElementsByTagAndClassName("input", "fund"), function(elem) {
    budget = starting_budget;
    if(elem.checked) {
      cost = parseFloat($(elem.id + "-cost").innerHTML) * 1000000;  // costs are in millions
      budget = budget - cost;
    }
  });

  $("budget").innerHTML = format_money(budget);
  if(budget < 0) {
    setStyle("budget", {'color':'red'});
  }
  else {
    setStyle("budget", {'color':'white'});
  }
}

function calculateCosts(e) {
  cost = parseFloat($(e.src().id + "-cost").innerHTML) * 1000000;  // costs are in millions
  checked = e.src().checked;
  if(checked) {
    budget = budget - cost;
  }
  else {
    budget = budget + cost;
  }
  $("budget").innerHTML = format_money(budget);
  if(budget < 0) {
    setStyle("budget", {'color':'red'});
  }
  else {
    setStyle("budget", {'color':'white'});
  }
}

function validate() {
  if(budget < 0) {
    alert("You have agreed to fund more interventions than your budget will allow.  Please review your choices.");
    return false;
  }
  return true;
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
  budget = starting_budget;
  forEach(getElementsByTagAndClassName("input", "fund"), function(elem) {
    connect(elem, "onclick", calculateCosts);
  });
  connect("assignment-form", "onreset", tallyCosts);
  tallyCosts();  // run once on load after loading saved data
}

addLoadEvent(initFunding);