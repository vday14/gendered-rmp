// EECS 486 Final Project Visual

var App = new Vue(
{
	el: '#app',

	// professorInfo[ID] -> name, rating, top 10 words, gender, gender predicted, top sim
	data:
	{
		professorInfo: {},
		professorNames: {},
		searchText: '',
		displayProfessorPage: false,
		professorImgSrc: '',
		SEARCH_KEY: 'AIzaSyCb6fjNMoMdS7KSLgefN27O-rlY-gYoTX0', // For custom Google search engine
		SEARCH_ID: '015167407967361263262:ngfy4sdyv9k', // For custom Google search engine
		ID: 0 // Professor ID
	},

	methods:
	{
		// Creates a professor hash where professors[professorID] = name
		readJSON: function()
		{
			console.log(this.professors);
		},

		loadHomepage: function()
		{
			this.searchText = '';
			this.displayProfessorPage = false;
		},

		searchByName: function()
		{
			var text = this.searchText.toLowerCase();

			var matches = Object.keys(this.professorNames).filter(
			    s => s.includes(text)
			);

			// Useful: http://googlecode.blogspot.com/2012/02/image-results-now-available-from-custom.html
			// Useful: http://nbviewer.jupyter.org/github/twistedhardware/mltutorial/blob/master/notebooks/data-mining/4.%20Google%20Custom%20Search.ipynb
			if (matches.length == 1) {
				this.displayProfessorPage = true;
				this.ID = this.professorNames[matches[0]];
				str = matches[0].replace(/\s/g, "+");
				var query = "umich+professors+" + str;
				var googleSearch = "https://www.googleapis.com/customsearch/v1?key=" + this.SEARCH_KEY + "&cx=" + this.SEARCH_ID + "&q=" + query + "&searchType=image&num=1&callback=?";
				$.getJSON(googleSearch, data => {
				    //data is the JSON string
				    this.professorImgSrc = data["items"][0]["link"];
				});
			}
			else {
				alert("Professor could not be found!");
				this.displayProfessorPage = false;
			}
		},

	},


	/******************************************************/
	/********************* PARSE JSON *********************/
	/******************************************************/


	mounted() 
	{
		var profs = {};
		var profNames = {};

		$.ajaxSetup({
		    async: false
		});

		$.getJSON('professors.json', function(data) {
			$.each( data, function( key, val ) {
				profs[key] = {'name': val.name, 'rating': val.score};
				profNames[val.name.toLowerCase()] = key;
			});
		});

		$.getJSON('profQueries.json', data => {
			$.each( data, function( key, val ) {
				if (key in profs)
				{
					if (val.gender == 0) {
						profs[key].gender = "img/male.png";
					}
					else {
						profs[key].gender = "img/female.png";
					}

					if (val.predicted_gender == 0) {
						profs[key].predictedGender = "img/male.png";
					}
					else {
						profs[key].predictedGender = "img/female.png";
					}

					profs[key].similarProfs = [];
					$.each(val.top_10, function(simKey, val)
					{
						profs[key].similarProfs.push(profs[simKey].name);
					});	
				}
			});
		});

		$.getJSON('profTerms.json', data => {
			$.each( data, function( key, val ) {
				if (key in profs)
				{
					var termFreq = val.terms;
					var keys = Object.keys(termFreq);
					profs[key].frequentTerms = keys.sort(function(a, b) {
					    return termFreq[b] - termFreq[a];
					})

					profs[key].randomTerms = profs[key].frequentTerms.filter(function(a) { 
  						return a.length > 4;
					}).slice(0, 10);

					profs[key].frequentTerms = profs[key].frequentTerms.slice(0, 10);

					// profs[key].randomTerms = keys.sort(() => .5 - Math.random()).slice(0, 10);
				}
			});
		});

		this.professorInfo = profs;
		this.professorNames = profNames;
	}
});