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
      def.addErrback(function(){alert('There was an error trying to save.  After checking your network configuration, contact the system administrator.');});
      
  }

  GameSystemAdmin.prototype.init = function() {
      try {
	  connect('shockform','onsubmit',this,'saveShock');
	  connect('shockselect','onchange',this,'loadShock');
	  this.loadShock();
      } catch(e) {
	  ///NO ADMIN (E.G. during student login)
      }
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
	  //preload the array, because forEach does it by
	  //index, but we are undermining the index list
	  //out from under it.
	  var arr = [];
	  forEach(this.assignment_form.elements,function(elt) {
	      arr.push(elt);
	  });
	  forEach(arr,function(elt) {
	      if (elt.parentNode.getAttribute('id') != 'navbuttons') {
		  elt.disabled = true;
		  if (elt.tagName.toLowerCase()=='textarea') {
		      var value = elt.value;
		      ///WOW, IE NEVER FAILS TO SUCK!
		      ///without a TD wrapper, we get Unknown Error
		      ///when setting innerHTML
		      var TAG = (/MSIE/.test(navigator.userAgent))?TD:P;
		      var wrapper = TAG({'class':'response'});
		      if (hasElementClass(elt,'mceNoEditor')) {
			  value = value.replace("\n","<br />");
		      }
		      wrapper.innerHTML = value;
		      swapDOM(elt,wrapper);
		  }
	      }
	  });
      } else {
	  /*actually, check out the MAJOR HACKITUDE
            that is in tiny_mce_init.js that tests for
            editable_view!
           */
      }
  }
  GameSystemClass.prototype.saveState = function(evt, next) {
      if (tinyMCE) {tinyMCE.triggerSave();}
      var def = false;
      try {
	  //easy default
	  if (this.textarea_default) {
              if (game_variables.length == 1) {
		  this.my_vars[game_variables[0]] = this.textarea_default.value; 
              }
	  }
	  def = doXHR(this.action,
		      {method:'POST',
                       sendContent:queryString({data:serializeJSON(this.my_vars),
						turn_id:this.turn_id,
						published:this.published
					       }),
                       headers:[["Content-type","application/x-www-form-urlencoded"]]
		      });
      } 
      catch (err) {
	  console.log(this);
	  console.log(err);
      }
      finally {
	  if (evt) evt.stop();
	  if (!this.quiet) {
	    if (this.published=='Submit') {
	      def.addCallback(function(response) {
	          var doc = JSON.parse(response.responseText, null);
	          window.location = doc.redirect;
	      });
	    } else {
	      def.addCallback(function() {
		  alert('Draft saved.');
		  removeElement('last-submitted'); //could fail
	      });
	    }
      }
    }
    return def;
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
  GameSystemClass.prototype.loadState = function(state, protected_state) {
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

     if (this.windowloaded) {
	  this.stateLoaded();
     } else {
	 addLoadEvent(bind(this.stateLoaded,this));
     }

     if (protected_state && protected_state.length) {
         showElement('instructor-debug');
         var ul = $('instructor-debug-list');
         for (var i=0;i<protected_state.length; i++) {
             var p = protected_state[i];
             var txt = '';
             if (p.page_id) 
                 txt += p.page_id;
             if (p.value) 
                 txt += ': '+p.value;
             if (txt) 
                 ul.appendChild(LI({},txt));
         }
     }
  }

  window.GameSystem = new GameSystemClass();
  window.GameSystem.init();
  addLoadEvent(function() {
      GameSystem.windowloaded = true;
      if (!GameSystem.loaded) {
	  GameSystem.loadState({});
      }
  });


}
