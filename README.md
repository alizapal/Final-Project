# Final-Project

Movies and Streaming

Two API are required to run the Final Project code. One from the Movie Database (tmdb) API and the other from the Watchmode API. The key will need to be written to a separate python file named Secrets.py. In the Secrets.py file, save the keys to the variable names moviedb_apikey and watchmode_apikey.

When the code is run, the user will be asked:
- Enter a search term
- Enter "exit" to quit
- Enter 'view page' to a select page 
- Enter 'stream' to see availability

The view page and stream functions cannot be used until a search term has been entered.
It is assumed that the user will enter a real searchable word, otherwise an error will be presented. If so, restart the program

Depending on the search term, the number of results and pages available to view will vary. Each page will show a max of 20 results. 

Movie Results will include:
- Movies names
- Genres
- Desciptions
- Movie ID Number

If the user enters "view page" they will be asked to:
- Enter 'search' to search another term
- Example: 2
- Enter a page number

When entering a page number, it is expected that the user will enter a numeric value, anything else will throw an error and the program will need to be restarted.

If the user enter "stream" (to see streaming availability) the user will be asked to:
- Enter 'search' to search another term
- Example: 578 
- Enter Movie ID #

The Movie ID Number can be found at the bottom of each movie result displayed. When entering a movie ID number is expected that the user will enter a numeric value, anything else will throw an error and the program will need to be started.

Streaming Results will include:
- A list of streaming services where the chosen movie title is available.

Some titles may not be available for streaming, in that case, a statement will be returned to indicate so.


