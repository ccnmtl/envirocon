//var plot_sectors_state = GameSystem.getVar('plot_sectors');
//GameSystem.saveState();

//get/set a select element value
///does NOT support multi-select (assumes single)
function selectVal(select_elt,val) {
	///nicer, if only IE didn't SUCK
	//return select_elt.value = val;
	var opt_i = select_elt.options.length;
	while (--opt_i >= 0) {
	    if (val && select_elt.options[opt_i].value == val) {
		select_elt.options[opt_i].selected = true;//write
		return val;
	    } else if (select_elt.options[opt_i].selected) {
		return select_elt.options[opt_i].value;//read
	    }
	}
    }

TableSortCasts["Select"] = function(cell){ 
    try { 
	return Number(selectVal(cell.getElementsByTagName('select')[0]));
    } catch(e) {return 0;}
}

var myPlots = new (function() {
    this.updateLocalState = function() {
	var elts = this.form.elements;
	var a = elts.length;
	while (--a >= 0) {
	    if (!hasElementClass(elts[a],'game-system')) {
		this.state[elts[a].name] = selectVal(elts[a]);
	    }
	}
	this.updateChart();
    };
    this.initialize = function() {
	this.form = GameSystem.getForm();
	this.state = GameSystem.getVariable('game_plot_sectors');
	for (a in this.state) {
	    selectVal(this.form.elements[a],this.state[a]);
	}
	this.updateChart();
    }
    this.googleChartURL = function(chart_data) {
	/* sample URL
         http://chart.apis.google.com/chart?cht=s&chd=t:12,87,75,41,23,96,68,71,34,9|98,60,27,34,56,79,58,74,18,76|84,23,69,81,47,94,60,93,64,54&chxt=x,y&chxl=0:|0|20|30|40|50|60|70|80|90|10|1:|0|25|50|75|100&chs=400x125";
         */
	var d ={x:[],y:[],lbl:[]};
	for (k in chart_data) {
	    d.x.push(chart_data[k][0]*10);
	    d.y.push(chart_data[k][1]*10);
	    d.lbl.push('o,'+chart_data[k][2]+',1,'+(d.x.length-1)+',10');
	    //d.x.push(chart_data[k][0]*10);
	    //d.y.push(chart_data[k][1]*10);
	    //d.lbl.push('f'+k+',0000FF,0,'+(d.x.length-1)+',10,0');
	}
	var url = "http://chart.apis.google.com/chart?";
	var args = {
	    cht:'s',//scatterplot
	    chd:'t:'+d.x.join(',')+'|'+d.y.join(','),
	    chxt:'x,y',
	    chxl:'0:|0|1|2|3|4|5|6|7|8|9|10|1:|0|2|4|6|8|10|3:|Relevance|',
	    chs:'300x125',
	    chm:d.lbl.join('|')
	};
	return url+queryString(args);
    }
    this.updateChart = function() {
	$('scatterplot').src = this.googleChartURL(this.getChartData());
    }
    this.colors = ['#597687','#ba9850','#7c5d4c',
		   '#56592b','#646464','#70444a',
		   '#a06134','#699746','#cb7e57',
		   '#85896f','#0a7d96','#6a6688',];
    this.getChartData = function() {
	var self = this;
	var data = {};
	function trim(str) {
	    return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	}
	forEach($('chart-data').getElementsByTagName('tr'),function(row) {
	    var tds = row.getElementsByTagName('td');
	    var selects = row.getElementsByTagName('select');
	    var innerText = ((tds[0].textContent) ? tds[0].textContent : tds[0].innerText);
	    var key = trim(innerText);
	    data[key] = [selectVal(selects[0]), selectVal(selects[1])];
	    if (!row.style.backgroundColor) {
		row.style.backgroundColor = self.colors.shift();
	    }
	    data[key].push(Color.fromBackground(row).toHexString().substr(1).toUpperCase());
	});
	return data;
    }

})();

forEach(document.getElementsByTagName('select'),function(elt) {
    connect(elt,'onchange',myPlots,'updateLocalState');
});

function initPlots() {
    myPlots.initialize();
}

connect(GameSystem, 'stateLoaded', initPlots);