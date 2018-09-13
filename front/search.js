query = ""

Search = {
	template : "search",
	load : function() {
		var out = {}

		return out;
	},
	dom: function() {
		//Seach when user submits query
		var form = document.getElementById("searchform")
		form.addEventListener("submit", function(e) {
			e.preventDefault();
			query = document.getElementById("query").value;
			states.switch("result");	
		})
	}
}

Result = {
	template: "results-temp",
	dom : function() {
		//Send Query
		params = [["query", query], ["page", 1]]
		Bunny.rest("POST", "localhost:8080/", params)
		.then(function(res) {
			//Get Results
			var out = "";
			var template = document.getElementById("result").innerHTML;	
			results = JSON.parse(res);
			
			//Render Template		
			for (i=0;i<results.length;i++) {
				var result = results[i]	
				var params = {
					"link": result[1],
					"title": result[1]
				}	
	
				out += Mustache.render(template, params);	
			}
		
			//Inform user if there are no results	
			if (!results[0]) {
				out = "<h2>No results found</h2>";
				out +="<a href='/'>Search Again</a>";
			}

			//Render Page
			result_div = document.getElementById("results");
			result_div.innerHTML = out;
			console.log(out)	
		})
	}
}

//Setup Bunny.js
var search_state = new Bunny.state(Search)
var result_state = new Bunny.state(Result)
var states = new Bunny.stateSwitcher("content");
states.add("search", search_state);
states.add("result", result_state);

states.switch("search");
