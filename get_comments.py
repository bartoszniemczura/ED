"""
Script for getting comments from "unofficial" API (the one used by TED talks' pages)
"""

import json
import ted_api
import requests

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest'
}

if __name__ == "__main__":
    if not ted_api.API_key:
        print("Provide your API key inside \"ted_api.py\" script")
        exit(-1)
    talk_ids = [t['talk']['id'] for t in
                ted_api.get_all("https://api.ted.com/v1/talks.json?api-key={0}".format(ted_api.API_key), "talks")[
                    'talks']]
    # talk_ids = [t for t in talk_ids if t > 1959]
    conversation_id = 0
    params = {'per_page': '100000000'}
    for t_id in talk_ids:
        not_found = True
        while not_found:
            resp = requests.get('http://www.ted.com/conversation_forums/' + str(conversation_id), params=params,
                                headers=headers)
            if resp and resp is not "null":
                conversation_dict = resp.json()
                if conversation_dict and conversation_dict['conversation_id'] == t_id:
                    print("found " + str(t_id))
                    not_found = False
                    with open('conversations/conversation_' + str(conversation_id) + '.json', 'w') as file:
                        json.dump(conversation_dict, file, sort_keys=True, indent=4)
            conversation_id += 1
