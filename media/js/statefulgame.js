if (typeof GameSystem == 'undefined') {

  function GameSystemClass() {
     //this.files = "";
     this.my_vars = {};
     this.turn_id = null;
     this.textarea_default = false;
     this.action = '/save_assignment';
     this.loaded = false;
      ///which submit value was clicked?
     this.published = 'Submit';
  }
  GameSystemClass.prototype.getForm = function() {
      return $('assignment-form');
  }
  GameSystemClass.prototype.saveState = function(evt) {
      try {
	  //easy default
	  if (this.textarea_default) {
              if (game_variables.length == 1) {
		  this.my_vars[game_variables[0]] = this.textarea_default.value; 
              }
	  }
	  console.log(this.my_vars);
	  doXHR(this.action,{method:'POST',
                             sendContent:queryString({data:serializeJSON(this.my_vars),
						      turn_id:this.turn_id,
						      published:this.published
						     }),
                             headers:[["Content-type","application/x-www-form-urlencoded"]]
			    });
      } 
      catch (e) {
	  console.log(e);
      }
      finally {
	  return false;
      }
  }

  GameSystemClass.prototype.getVariable = function(var_name) {
     if (typeof this.my_vars[var_name] != 'undefined') {
        return this.my_vars[var_name];
     } else {
	return this.my_vars[var_name] = {};
     }
  }

  GameSystemClass.prototype.loadState = function(state) {
     var self = this;
     update(this.my_vars, state);
     ///ASSUME: document is loaded by now!
     var assignment_form = this.getForm();
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

  GameSystemClass.prototype.loadFiles = function(files) {
    //var self = this;
    //if(files) {
    //  this.files = files;
    //}
    //alert(this.files);
    //if($('files_panel')) {
    //  alert("whee");
    var html = "";
    for(var i=0; i<files.length; i++) {
      html += "<a href='../" + files[i] + "'>" + files[i] + "</a><br />";
    }    
      $('files_panel').innerHTML = html;
    //}
  }


  window.GameSystem = new GameSystemClass();

  addLoadEvent(function() {
      if (!GameSystem.loaded) {
	  GameSystem.loadState({});
	  //GameSystem.loadFiles();
      }
  });


}