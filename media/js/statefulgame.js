if (typeof GameSystem == 'undefined') {

  function GameSystemClass() {
     this.my_vars = {};
     this.turn_id = null;
     this.textarea_default = false;
     this.action = '/save_assignment';
     this.loaded = false;
      ///which submit value was clicked?
     this.published = 'Submit';
  }
  GameSystemClass.prototype.saveState = function(evt) {
      //easy default
     if (this.textarea_default) {
        if (game_variables.length == 1) {
            this.my_vars[game_variables[0]] = this.textarea_default.value; 
        }
     }
     doXHR(this.action,{method:'POST',
                        sendContent:queryString({data:serializeJSON(this.my_vars),
						 turn_id:this.turn_id,
						 published:this.published
						}),
                        headers:[["Content-type","application/x-www-form-urlencoded"]]
        });
     return false;
  }

  GameSystemClass.prototype.getVariable = function(var_name) {
     if (typeof this.my_vars[var_name] != 'undefined') {
        return this.my_vars[var_name];
     }
  }

  GameSystemClass.prototype.loadState = function(state) {
     var self = this;
     update(this.my_vars, state);
     ///ASSUME: document is loaded by now!
     var assignment_form = $('assignment-form');
     if (assignment_form) {
	 forEach(assignment_form.elements, function(elt) {
             if (elt.name=='turn_id') {
		 self.turn_id = elt.value;
             }
             if (elt.name=='data') {
		 //easy default
		 self.textarea_default = elt;
		 if (game_variables.length == 1 && typeof self.my_vars[game_variables[0]]!='undefined') {
		     elt.value = self.my_vars[game_variables[0]];
		 }
             }        
	 });
        this.action = assignment_form.action;
        assignment_form.onsubmit = bind(GameSystem.saveState,GameSystem);
     }
     this.loaded = true;
  }

  

  window.GameSystem = new GameSystemClass();

  addLoadEvent(function() {
      if (!GameSystem.loaded) {
	  GameSystem.loadState({});
      }
  });


}