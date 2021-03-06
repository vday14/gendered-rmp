Process: run crawler code --> json object called professors.json 
--> run preprocessing code --> json object called profTerms.json 
--> run query code --> json objects called profQueries.json and profRocchio.json
--> frontend

Crawler files:
Notes:
To run the crawler, run the following command in the terminal:
python Crawler.py {number of professor profiles}
Example: python Crawler.py 20

Where 20 is the number of professor profiles you want to scrape. Please use a multiple of 20 (because 20 professor profiles
are loaded each time "Load more" is clicked). Any non-multiple of 20 will be rounded down.
Please use a number between 20 and 200.
This will open a Google chrome browser. Ensure that the chromedriver executable is in the project directory.
Make sure to immediately close any pop-up ads that overlay the html, otherwise the crawler will exit with an error.

The crawler will write the html to ratemyprofessor.html. It will then scrape all RMP professor urls to professor profiles
and write these links to professor_urls.txt. Next the program will follow these links and parse the html, finally writing
the Professor json object to professors.json.

NOTE: Selenium must be installed.

Preprocessing files: 
To run, use the command: "python3 preprocess.py"
This will create a JSON object called profTerms.json to be run by vectorspace.py

Query files: vectorspace.py
Notes: run using command "python3 vectorspace.py"

Frontend files:
Notes: Launch the tool by opening index.html. Professors can be searched for with an exact substring match of their name.
if only one professor matches, it will open the professor's page. The Google Image API is limited to 100 calls per day,
so only 100 professor images will render. To view the results from a different dataset, replace the JSON files
inside UserInterface/
