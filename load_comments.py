import json
import os
from pprint import pprint
import pymysql


USER = ""
PWD = ""

def save_conversation(cursor, conversation_id, talk_id, fields, type):
    cursor.execute("""INSERT INTO conversation VALUES (%s,%s,%s,%s)""", (conversation_id, talk_id, type, fields))


def save_comment(cursor, comment):
    if 'comment_id' not in comment.keys():
        return

    add_user(cur, comment)
    cursor.execute("""INSERT INTO comments VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                   (comment["comment_id"], \
                    data["conversation_id"], \
                    comment["discussion_id"], \
                    comment["parent_id"], \
                    comment["comment"], \
                    comment["user_id"], \
                    comment["date"], \
                    comment["level"], \
                    comment["score"], \
                    comment["deleted"], \
                    comment["deleted_reason"], \
                    comment["replies"], \
                    comment["date_activity"], \
                    comment["expired"]))

    for key in comment["children"]:
        save_comment(cursor, comment["children"][key])


def add_user(cursor, comment):
    if 'user_id' not in comment.keys():
        return
    result = cursor.execute("""SELECT user_id FROM users WHERE user_id = """ + str(comment["user_id"]))
    if not result:
        cursor.execute("""INSERT INTO users VALUES (%s,%s,%s,%s, %s)""", \
                       (comment["user_id"], \
                        comment["profile_id"], \
                        comment["name"], \
                        comment["profile_score"], \
                        comment["profile_pic"]))


db = pymysql.connect(host="127.0.0.1", port=10888, user=USER, passwd=PWD, db="igor", charset='utf8')
cur = db.cursor()

from os import walk
for (dirpath, dirnames, filenames) in walk('conversations'):
    i = filenames.index('conversation_566.json')
    while i < len(filenames):
        name = filenames[i]
        i += 1
        with open(os.path.join(dirpath, name), 'r') as file:
            data = json.load(file)
            print(name)

            if data and data.get('discussion_thread', None) and data['discussion_thread'].get('thread', None):
                comments = data["discussion_thread"]["thread"][0]
                for key in comments:
                    comment = comments[key]
                    save_comment(cur, comment)

db.commit()
