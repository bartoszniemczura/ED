import json
import requests


def get_all(url, list_id):
    params = {'limit': '100'}
    resp = requests.get(url, params=params)
    resp_dict = resp.json()
    params['offset'] = resp_dict['counts']['this']
    total = resp_dict['counts']['total']
    print(total)
    print(params['offset'])
    while params['offset'] < total:
        resp = requests.get(url, params=params)
        resp_temp_dict = resp.json()
        params['offset'] += resp_temp_dict['counts']['this']
        print(params['offset'])
        resp_dict[list_id].extend(resp_temp_dict[list_id])
    return resp_dict


def write_json(filename, json_dict):
    with open(filename, "w+") as fh:
        json.dump(json_dict, fh, sort_keys=True, indent=4)

if __name__ == "__main__":
    result_list_talks = get_all("https://api.ted.com/v1/talks.json?api-key=jpddab739995meq3gsnwbrc7&fields=theme_ids,name,description,events,rating_word_ids,tags,media", "talks")["talks"]
    write_json("talks.json", result_list_talks)
    # result_list_themes = get_all("https://api.ted.com/v1/themes.json?api-key=jpddab739995meq3gsnwbrc7&fields=related_talks", "themes")["themes"]
    # write_json("themes.json", result_list_themes)
    # result_list_tags = get_all("https://api.ted.com/v1/tags.json?api-key=jpddab739995meq3gsnwbrc7", "tags")["tags"]
    # write_json("tags.json", result_list_tags)
    # result_list_ratings = requests.get("https://api.ted.com/v1/ratings.json?api-key=jpddab739995meq3gsnwbrc7").json()["ratings"]
    # write_json("ratings.json", result_list_ratings)
    # result_list_speakers = get_all("https://api.ted.com/v1/speakers.json?api-key=jpddab739995meq3gsnwbrc7&fields=talks", "speakers")["speakers"]
    # write_json("speakers.json", result_list_speakers)

