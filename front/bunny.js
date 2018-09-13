//Bunny.js - A micro-framework for applications that need state switching
//Programmer: Jorge Martin

Bunny = {}

//State
Bunny.state = function(input) {
	this.template = document.getElementById(input.template).innerHTML;

	if (input.load) {
		this.load = input.load;
	} else {
		this.load = function() {return {}};
	}

	if (input.dom) {
		this.dom = input.dom;
	} else {
		this.dom = function() {};
	}

	this.render = function(el) {
		var params = this.load();
		el.innerHTML = Mustache.render(this.template, params);	
		this.dom();	
	}

	this.exit = function() {
		if (input.exit) {
			input.exit();
		}	
	}
}	

Bunny.stateSwitcher = function(el) {
	this.el = document.getElementById(el);
	this.states = [];
	this.state = "";

	this.add = function(name, state) {
		this.states.push([name, state]);
	};

	this.switch = function(name) {
		var current = 0;

		//Select state from array	
		for (var i=0; i<this.states.length; i++) { 
			if (this.state == this.states[i][0]) {
				current = i;
				break;
			}
		}

		//Exit Current State
		if (current) {
			this.states[current][1].exit();	
		}

		//Push new state
		for (var i=0; i<this.states.length;i++) {
			if (name == this.states[i][0]) {
				this.state = name;
				this.states[i][1].render(this.el);	
				break;
			}
		}
	};
}

Bunny.rest = function(method, url, params) {
	return new Promise(function(resolve, reject) {
	url = "http://" + url;
	
	//Create body
	//Format: [[key, value], [key, value]]	
	var body = "";

	if (method.toLowerCase() != "get") {
	for(var i=0; i<params.length; i++) {
		var equal = params[i][0] + "=" + params[i][1];	

		//Add amperstand to end	
		if(i != (params.length - 1)) {
			equal +="&";
		}

		//Add equal to body
		body +=equal;	
	}}
	
	//Setup XHR
	var xhr = new XMLHttpRequest();	
	xhr.onload = function() {
		if (this.status == 200) {	
			resolve(xhr.responseText);
		}
	}

	//Send Request
	xhr.open(method, url, true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.send(body)
	});
}

