


function submitProfile(evt) {
    doXHR('/profile/',
	  {'method':"POST",
	   'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
	   'sendContent':"",
	  }
	 );
}