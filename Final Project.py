#########################################
##### Name: Aliza Palmer ################
##### Uniqname: alizapal ################
#########################################

import requests
import json as jsonpkg
import webbrowser as wb
import Secrets
import json

moviedb_apikey = Secrets.moviedb_apikey
watchmode_apikey = Secrets.watchmode_apikey


CACHE_FILENAME = "Caching_It_Up.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the FIB_CACHE dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict, indent=4, sort_keys=True)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    param_strings = []
    connector = ' '
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key


class Movie:
    def __init__(self, title_ID="None", title="No Title", plot="No Description", release_date="No Year", poster_url = "None", pages="None", page_view =1, genre="None", json=None):
        self.json = json
        if json is None:
            self.title_ID = title_ID
            self.title = title
            self.plot = plot
            self.release_data = release_date
            self.poster_url = poster_url
            self.pages = pages
            self.page_view = page_view
            self.genre = genre
        else:
            try:
                self.title = json["title"]
            except:
                self.title = title

            try:
                self.title_ID = json["id"]
            except:
                self.title_ID = title_ID
            try:
                if len(json["overview"]) > 0:
                    self.plot = json["overview"]
                else:
                    self.plot = "No Description"
            except:
                self.plot = plot
            try:
                if len(json["release_date"]) > 0:
                    self.release_date = json["release_date"][:4]
                else:
                    self.release_date = "No Year"
            except:
                self.release_date = release_date
            try:
                self.poster_url = json["poster_path"]
            except:
                self.poster_url = poster_url
            try:
                self.pages = json["total_pages"]
            except:
                self.pages = pages
            try:
                if len(json["genre_ids"]) > 0:
                    self.genre = json["genre_ids"]
                else:
                    self.genre = ""
            except:
                self.genre = genre
            try:
                self.page_view = json["page"]
            except:
                self.page_view = page_view

    def info(self):
        return f"{self.title} ({self.release_date}) {self.genre} \nDescription: {self.plot}\n" # \n {self.plot}

    def length(self):
        return 0



def call_function(params, limit=50):
    # Modify to check cache

    base_url = "https://api.themoviedb.org/3/search/movie?"
    poster_url = "https://image.tmdb.org/t/p/original/?"

    if limit > 100:
         limit= 100
    params["limit"] = 100

    cache_dict = open_cache()
    unique_key = construct_unique_key(base_url, params)
    try:
        results = cache_dict[unique_key] #
    except:
        response = requests.get(base_url, params)
        json_str = response.text
        results = jsonpkg.loads(json_str)

    # return results, str(base_url + params)
    return results, unique_key, cache_dict # unique key being stored as info2 below


# moviedb_params = {"api_key": moviedb_apikey, "language": "en-US", "include_adult": "false", "query": "Attack"}
# info, info2, info3 = call_function(moviedb_params) #info2 will be the key for the cache
# # print(info["results"][0])

# # Add to the cache_dict given the unique with the results as the value (key, value pair)
# info3[info2] = info
# save_cache(info3) #can just call it

def update_cache(results, unique_key, cache_dict): #Does what line 166 does, to return updated dictionary
    cache_dict[unique_key] = results # cache_dict has been updated to include the new unique key and results
    save_cache(cache_dict)


# Pull numbers to ID genres
genre_url = "https://api.themoviedb.org/3/genre/movie/list?"

genre_params = {"api_key": moviedb_apikey}

genre_response = requests.get(genre_url, genre_params)
# print(genre_response)
genre_str = genre_response.text
genre_results = jsonpkg.loads(genre_str)
# print(genre_results["genres"])
# print(genre_results)


# CACHING TEST
# with open('Caching_Up.json', 'w') as json_file:
#     json.dump(genre_results, json_file)



# Now add the correct genre to the correlating number and create the movie objects
def organize_results(results):
    movies_list = []
    for dict in results["results"]:
        # print(dict["genre_ids"])
        for gns in genre_results["genres"]:
            for i in range(len(dict["genre_ids"])):
                # print(dict["genre_ids"][i])
                if dict["genre_ids"][i] == gns['id']:
                    dict["genre_ids"][i] = gns["name"]

        object = Movie(json=dict)
        object.pages = results["total_pages"] # Adding Page numbers in case I want to add a page scolling feature
        object.page_view = results["page"] # Showing the page being viewed
        # print(object.pages)
        movies_list.append(object)

    list_of_objects = movies_list
    return list_of_objects

# Call and test organize results function
# test_results = organize_results(info)
# print(test_results)
# print(total_pages_number)


# Now add the numbers to the list, display total page numbers, display page currently being viewed
def format_results(list_of_objects):

    count = 1
    i = 0
    obj_type = type(list_of_objects[0])

    print()
    print("MOVIES")
    print("Total Results Pages:", list_of_objects[0].pages)
    print("Viewing Page:", list_of_objects[0].page_view)
    print()

    for i in range(len(list_of_objects)):
        if type(list_of_objects[i]) == obj_type:
            print(f"{count}: {list_of_objects[i].info()}")
            count += 1

# Call and test format_results function
# (format_results(test_results))


###### NOW PREPARE WATCHMODE API TO VIEW STREAMING AVAILABILITY ######

def call_function_II(params, limit=50):

    base_url = 'https://api.watchmode.com/v1/title/title_id/sources/'

    # ("https://api.watchmode.com/v1/title/345534/sources/?apiKey=YOUR_API_KEY"

    if limit > 100:
         limit= 100

    params["limit"] = 100

    cache_dict = open_cache()
    unique_key = construct_unique_key(base_url, params)
    try:
        results = cache_dict[unique_key] #
    except:
        response = requests.get(base_url, params)
        json_str = response.text
        results = jsonpkg.loads(json_str)

    return results, unique_key, cache_dict


# watchmode_params = {}




if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    # pass

    search_dictionary = {}
    previous_input = {}

    while True:

        if len(previous_input) == 0:
            chosen_term = input(f"Enter a search term \nEnter 'exit' to quit \nEnter 'view page' to a select page: " ) # three options

            # Enter a search term
            # Quit
            # View a different page: Code so you can only view another after a term has been searched

            # Can reasonably assume they'll type words. 
            # Put that in the presentation for it & make sure it's a real word that would be searchable 

            if chosen_term.lower() == "exit":
                print("Bye")
                break

            elif chosen_term.lower() == "view page":
                if search_dictionary == {}:
                    print(f"\nPlease search a term first!\n")
                else:
                    while True:
                        chosen_page = input(f"\nEnter a page number: ")
                        # print(type(chosen_page))

                        if not chosen_page.isnumeric or int(chosen_page) > len(org_results) or int(chosen_page) <= 0: # Make sure to pick pages in range of list
                            print("\nPlease enter a number WITHIN the results range.\n") # Otherwise

                        else:
                            search_dictionary["page"] = chosen_page
                            call_results = call_function(search_dictionary)
                            update_cache(call_results[0], call_results[1], call_results[2])
                            org_results = organize_results(call_results[0])
                            format_results(org_results)

            else:
                search_dictionary["api_key"] = Secrets.moviedb_apikey
                search_dictionary["query"] = chosen_term
                search_dictionary["page"] = 1 # page 1 is the default
                call_results = call_function(search_dictionary) # call function returns three things
                # print(call_results)
                update_cache(call_results[0], call_results[1], call_results[2])
                org_results = organize_results(call_results[0])
                # print(org_results)
                format_results(org_results)

        else:
            call_results = call_function(previous_input)
            update_cache(call_results[0], call_results[1], call_results[2])
            org_results = organize_results(call_results[0])
            format_results(org_results)
            print(previous_input)
