"""
Script for reading files acquired through official TED api and saving the data to database
"""

import json
import pymysql
import sys


USER = ""
PWD = ""
DB_NAME = "igor"


def save_talk(cursor, talk_id, name, description, event_id, language_code, event_name, recording_date, publishing_date,
              tags_dict, theme_ids, duration):
    cleaned_tags = set([ta.lower().strip() for ta in tags_dict.values()])
    for tag_name in cleaned_tags:
        cursor.execute("""INSERT INTO talk_tags VALUES (%s,%s)""", (talk_id, tag_name))

    for theme_id in theme_ids:
        cursor.execute("""INSERT INTO talk_themes VALUES (%s,%s)""", (talk_id, theme_id))

    cursor.execute("""INSERT INTO talks VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                   (talk_id, name, description, event_id, language_code, event_name, recording_date, publishing_date,
                    duration))


def save_theme(cursor, theme_id, name, description, shortsummary):
    cursor.execute("""INSERT INTO themes VALUES (%s,%s,%s,%s)""", (theme_id, name, description, shortsummary))


def save_tag(cursor, name):
    cursor.execute("""INSERT INTO tags VALUES (%s)""", name)


def save_rating(cursor, rating_id, talk_id, rating, name):
    cursor.execute("""INSERT INTO ratings VALUES (%s,%s,%s,%s)""", (rating_id, talk_id, rating, name))


def save_speaker(cursor, speaker_id, title, firstname, lastname, description, whotheyare, talks):
    cursor.execute("""INSERT INTO speakers VALUES (%s,%s,%s,%s,%s,%s)""",
                   (speaker_id, title, firstname, lastname, description, whotheyare))
    for t in talks:
        cursor.execute("""INSERT INTO talk_speakers VALUES (%s,%s)""", (t['talk']['id'], speaker_id))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ['ratings', 'tags', 'themes', 'talks', 'speakers']:
        print("Usage: {0} <Task>\nTask is one of: ratings, tags, themes, talks, speakers")
        exit(-1)
    db = pymysql.connect(host="127.0.0.1", port=10888, user=USER, passwd=PWD, db=DB_NAME, charset='utf8')
    cur = db.cursor()
    task = sys.argv[2]
    if task == "ratings":
        print("Ratings")
        with open("ratings.json") as fh:
            ratings = json.load(fh)
            for r in ratings:
                print(r['name'])
                save_rating(cur, r['ratingid'], r['talkid'], r['rating'], r['name'])
    elif task == "tags":
        print("Tags")
        with open("tags.json") as fh:
            tags = json.load(fh)
            for tag in set([t['tag']['name'].lower().strip() for t in tags]):
                print(tag)
                save_tag(cur, tag)
    elif task == "themes":
        print("Themes")
        with open("themes.json") as fh:
            themes = json.load(fh)
            for t in themes:
                print(t['theme']['name'])
                save_theme(cur, t['theme']['id'], t['theme']['name'], t['theme']['description'],
                           t['theme']['shortsummary'])
    elif task == "talks":
        print("Talks")
        with open("talks.json") as fh:
            talks = json.load(fh)
            for t in talks:
                print(t['talk']['name'])
                save_talk(cur, t['talk']['id'],
                          t['talk']['name'],
                          t['talk']['description'],
                          t['talk']['event_id'],
                          t['talk']['native_language_code'],
                          t['talk']['event']['name'],
                          t['talk']['recorded_at'],
                          t['talk']['published_at'],
                          t['talk']['tags'],
                          t['talk']['theme_ids'],
                          t['talk']['media']['duration'])
    elif task == "speakers":
        print("Speakers")
        with open("speakers.json") as fh:
            speakers = json.load(fh)
            for r in speakers:
                r = r['speaker']
                print(r['firstname'] + " " + r["lastname"])
                save_speaker(cur, r['id'], r['title'], r['firstname'], r['lastname'], r['description'], r['whotheyare'],
                             r['talks'])

    db.commit()
