//var plot_sectors_state = GameSystem.getVar('plot_sectors');
//GameSystem.saveState();

TableSortCasts["Select"] = function(cell){ 
    try { 
	return cell.getElementsByTagName('select')[0].value;
    } catch(e) {return 0;}
}

var myPlots = new (function() {
    this.updateLocalState = function() {
	var elts = this.form.elements;
	for (a in elts) {
	    if (elts[a].value && !hasElementClass(elts[a],'game-system')) {
		this.state[elts[a].name] = elts[a].value;
	    }
	}
    };
    this.initialize = function() {
	this.form = GameSystem.getForm();
	this.state = GameSystem.getVariable('game_plot_sectors');
	for (a in this.state) {
	    this.form.elements[a].value = this.state[a];
	}
    }

})();

forEach(document.getElementsByTagName('select'),function(elt) {
    connect(elt,'onchange',myPlots,'updateLocalState');
});

myPlots.initialize();