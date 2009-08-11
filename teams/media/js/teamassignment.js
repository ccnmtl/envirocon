window.onload = function() {
    teams = document.getElementsByTagName('div');
    var i = teams.length-1;
    do {
	var team = teams[i];
	if (/^\d+$/.test(team.innerHTML)) {
	    team.onclick = getTeamListener(team);
	}
    } while(--i);
    initTeams();
}

function getTeamListener(team) {
    return (function(evt) {
	var oldteam = Number(team.parentNode.getAttribute('data-team'));
	var newteam = team.innerHTML;
	team.parentNode.setAttribute('data-team',newteam);
	var nums = team.parentNode.getElementsByTagName('div');
	for(var j=0;j<nums.length;j++) {
	    if (nums[j]!=team)
		nums[j].setAttribute('class','');
	}
	team.setAttribute('class','on');
	var member_tr = team.parentNode.parentNode.parentNode;
	postMembership(member_tr.getAttribute('data-member'), 
		       team.getAttribute('data-teamid'));
	//updateTeamDiversity(member_tr,oldteam,Number(newteam));
    });    
}

function postMembership(user_id, team_id) {
    var url = document.forms['team-addmember'].action.replace('user_id',user_id);
    if (team_id) { url += team_id; }
    doXHR(url,{method:'POST'});
    
}

TableSortCasts["Team"] = function(cell){
    try {
	return Number(cell.getElementsByTagName('div')[0].getAttribute('data-team'));
    }catch(e) {
	return 0;
    }
};

var Team = null;
function TeamsObject(cols) {
    this.cols = cols;
    var template = function(c){
	var a = [];
	while (--c +1) {a.push([])};
	return a;
    };

    this.count = function() {
	return document.getElementsByTagName('div')[0].getElementsByTagName('div').length;
    }
    this.teams = new Array(this.count()+1);
    for (var i=0;i<this.teams.length;i++) {
	this.teams[i] = {diversity:0,
			 count:0,
			 cols:new template(cols)
			};
    }
    //this.count_row = document.getElementById('teamtable').getElementsByTagName('tr')[1].getElementsByTagName('td');
    //this.diversity_row = document.getElementById('teamtable').getElementsByTagName('tr')[2].getElementsByTagName('td');
}

function updateTeamDiversity(member_tr,oldteam,newteam) {
    var tds = member_tr.getElementsByTagName('td');
    if (oldteam) {
	for(var i=0;i<Team.cols;i++) {//foreach column
	    var col = Team.teams[oldteam].cols[i];
	    var found = col.indexOf(tds[1+i].innerHTML);
	    if (found >=0) col.splice(found,1);
	}
	Team.count_row[oldteam].innerHTML = --Team.teams[oldteam].count;
    }
    if (newteam) {
	for(var i=0;i<Team.cols;i++) {//foreach column
	    Team.teams[newteam].cols[i].push(tds[1+i].innerHTML);
	}
	Team.count_row[newteam].innerHTML = ++Team.teams[newteam].count;
    }
}



function initTeams() {
    Team = new TeamsObject(2/*cols after name*/);
    
}