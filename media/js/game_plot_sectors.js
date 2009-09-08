//var plot_sectors_state = GameSystem.getVar('plot_sectors');
//GameSystem.saveState();

TableSortCasts["Select"] = function(cell){ 
    try { 
	return cell.getElementsByTagName('select')[0].value;
    } catch(e) {return 0;}
}

forEach(document.getElementsByTagName('select'),function(elt) {
    connect(elt,'onchange',
});