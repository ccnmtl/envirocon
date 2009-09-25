var team_markers = getElementsByTagAndClassName('div','teamoptions');
var status_boxes = getElementsByTagAndClassName('td','teamstatus');
var draggers = [];
var droppers = [];
forEach(team_markers,function(elt){
    draggers.push(new Draggable(elt, 
				{revert:true,
				 scroll:window
				}
			       )
		 );
});

forEach(status_boxes,function(elt){
    droppers.push(new Droppable(elt,
				{accept:['teamoptions'],
				 hoverclass:'hovering',
				 ondrop:function(element,group,e) {
				     //necessary to de-ick MochiKit's D&D styling
				     setNodeAttribute(element,'style','');
				     appendChildNodes(elt,element);
				     saveNewTurn(elt,element);
				 }
				})
		 );
});

function saveNewTurn(group_elt, team_elt) {
    var d = {
	'assignment_id':group_elt.getAttribute('data-assn'),
	'team_id':team_elt.getAttribute('data-team'),
	'set_turn':'true'
    };
    var marker = team_elt.firstChild;
    if ($('teamstatus-'+d['team_id']+'-'+d['assignment_id']).getAttribute('data-status')) {
	addElementClass(marker,'on');
	marker.title = 'published';
    } else {
	removeElementClass(marker,'on');
	marker.title = 'draft';
    }
    if (marker.getAttribute('data-current') != d['assignment_id']) {
	marker.setAttribute('data-current',d['assignment_id']);
	var def = doXHR('/set_turn/',
	                {method:'POST',
                         sendContent:queryString(d),
                         headers:[["Content-type","application/x-www-form-urlencoded"]]
			});
	def.addErrback(function(){alert('There was an error trying to save the team turn.  After checking your network configuration, contact the system administrator.');});
    }
}