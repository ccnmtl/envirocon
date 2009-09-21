if (typeof GameSystem == 'undefined') {


  GameSystemAdmin = function() {
      
  }  
  GameSystemAdmin.prototype.loadShock = function() {
      var select = $('shockselect');
      var frm_name = document.forms['shockform'].elements['shock_name'];
      var frm_outcome = document.forms['shockform'].elements['shock_outcome'];
      if (!select.value) {
	  frm_name.disabled = false;
	  frm_outcome.disabled = false;
      } else {
	  var shock_li = $('shock-'+select.value);
	  if (shock_li) {
	      var vals = shock_li.innerHTML.split('|');
	      frm_name.value = vals[0];
	      frm_outcome.value = vals[1];
	      
	      frm_name.disabled = true;
	      frm_outcome.disabled = true;
	  }
      }
  }
  GameSystemAdmin.prototype.saveShock = function(evt) {
      var form = evt.src();
      var def = doXHR(form.action,{method:'POST',
                      sendContent:queryString(formContents(form)),
                      headers:[["Content-type","application/x-www-form-urlencoded"]]
                      });
      evt.stop();
      def.addCallback(function(){alert('Shock Saved!');});
      
  }

  GameSystemAdmin.prototype.init = function() {
      connect('shockform','onsubmit',this,'saveShock');
      connect('shockselect','onchange',this,'loadShock');
      this.loadShock();
  }
  function GameSystemClass() {
      //this.files = "";
      this.my_vars = {};
      this.turn_id = null;
      this.textarea_default = false;
      this.action = '/save_assignment';
      this.loaded = false;
      ///which submit value was clicked?
      this.published = 'Submit';
      this.admin = new GameSystemAdmin();
  }
  GameSystemClass.prototype.getForm = function() {
      return $('assignment-form');
  }
  GameSystemClass.prototype.stopFormListener = function() {
      return disconnect(this.formlistener);
  }    

  GameSystemClass.prototype.stateLoaded = function() {
      ///defined globally in the game template
      if (!editable_view) {
	  forEach(this.assignment_form.elements,function(elt) {
	      elt.disabled = true;
	      if (elt.tagName.toLowerCase()=='textarea') {
		  var value = elt.value;
		  var wrapper = P();
		  wrapper.innerHTML = value;
		  swapDOM(elt,wrapper);
	      }
	  });
      }
  }
  GameSystemClass.prototype.saveState = function(evt) {
      if (tinyMCE) {tinyMCE.triggerSave();}
      try {
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
      } 
      catch (e) {
	  console.log(this);
	  console.log(e);
      }
      finally {
	  //return false;
	  if (evt) evt.stop();
      }
  }

  GameSystemClass.prototype.getVariable = function(var_name) {
     if (typeof this.my_vars[var_name] != 'undefined') {
        return this.my_vars[var_name];
     } else {
	return this.my_vars[var_name] = {};
     }
  }
  GameSystemClass.prototype.init = function() {
      this.assignment_form = this.getForm();
      this.formlistener = connect(this.assignment_form,'onsubmit',bind(this.saveState,GameSystem));
      this.admin.init();
  }
  GameSystemClass.prototype.loadState = function(state) {
     var self = this;
     update(this.my_vars, state);
     ///ASSUME: document is loaded by now!
     //this.assignment_form = this.getForm();
     if (this.assignment_form) {
	 forEach(this.assignment_form.elements, function(elt) {
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
        this.action = this.assignment_form.action;
     }
     this.loaded = true;
      this.stateLoaded();

  }

  window.GameSystem = new GameSystemClass();
  window.GameSystem.init();
  addLoadEvent(function() {
      if (!GameSystem.loaded) {
	  GameSystem.loadState({});
      }
  });


}