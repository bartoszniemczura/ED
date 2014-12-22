"""
Script for reading crawled TED comments files and saving them to database
"""

import json
import os

import pymysql

from sql_commands import ADD_USER, SAVE_COMMENT


USER = ""
PWD = ""
DB_NAME = "igor"


def save_comment(cursor, comment):
    if 'comment_id' not in comment.keys():
        return

    add_user(cur, comment)
    cursor.execute(SAVE_COMMENT,
                   (comment["comment_id"],
                    data["conversation_id"],
                    comment["discussion_id"],
                    comment["parent_id"],
                    comment["comment"],
                    comment["user_id"],
                    comment["date"],
                    comment["level"],
                    comment["score"],
                    comment["deleted"],
                    comment["deleted_reason"],
                    comment["replies"],
                    comment["date_activity"],
                    comment["expired"]))

    for key in comment["children"]:
        save_comment(cursor, comment["children"][key])


def add_user(cursor, comment):
    if 'user_id' not in comment.keys():
        return
    result = cursor.execute("""SELECT user_id FROM users WHERE user_id = """ + str(comment["user_id"]))
    if not result:
        cursor.execute(ADD_USER,
                       (comment["user_id"],
                        comment["profile_id"],
                        comment["name"],
                        comment["profile_score"],
                        comment["profile_pic"]))


if __name__ == "__main__":
    db = pymysql.connect(host="127.0.0.1", port=10888, user=USER, passwd=PWD, db=DB_NAME, charset='utf8')
    cur = db.cursor()

    from os import walk

    for (dirpath, dirnames, filenames) in walk('conversations'):
        i = 0  # filenames.index('conversation_566.json')
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
