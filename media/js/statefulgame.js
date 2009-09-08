if (typeof GameSystem == 'undefined') {

  function GameSystemClass() {
     this.my_vars = {};
     this.turn_id = null;
     this.textarea_default = false;
     this.action = '/save_assignment';
  }
  GameSystemClass.prototype.saveState = function() {
     if (this.textarea_default) {
        if (game_variables.length == 1) {
            this.my_vars[game_variables[0]] = this.textarea_default.value; 
        }
     }
     doXHR(this.action,{method:'POST',
                        sendContent:{data:serializeJSON(this.my_vars),
                                     turn_id:this.turn_id
                                    },
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
     forEach(document.getElementsByTagName('input'), function(elt) {
        if (elt.name=='turn_id') {
            self.turn_id = elt.value;
        }
        if (elt.name=='data') {
           self.textarea_default = elt;
        }        
     });
     var assignment_form = $('assignment-form');
     if (assignment_form) {
        this.action = assignment_form.action;
        assignment_form.action = 'javascript:GameSystem.saveState();';
     }    
  }

  

  window.GameSystem = new GameSystemClass();


}