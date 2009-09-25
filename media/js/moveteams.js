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
				 }
				})
		 );
});