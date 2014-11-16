import json
import pymysql
from collections import Counter
from collections import defaultdict

USER = ""
PWD = ""

COMMENTS_GRAPH = """
SELECT user_comments_reply.name, users.name FROM
(SELECT user_comments.name AS name, user_comments.comment_id AS comment_id,
user_comments.parent_comment, comments.user_id AS parent_user_id FROM
(SELECT name, c1.comment_id AS comment_id, c1.parent_id AS parent_comment FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id WHERE c1.parent_id!=0) AS user_comments
LEFT JOIN comments ON user_comments.parent_comment=comments.comment_id) AS user_comments_reply
LEFT JOIN users ON user_comments_reply.parent_user_id=users.user_id"""

COMMENTS_GRAPH_SIMPLE = """
select * from (SELECT name, c1.talk_id as talk_id FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id) as user_comments"""


TALKS_USERS_GRAPH = """
SELECT name, c1.talk_id AS talk_id
FROM  `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id = users.user_id
"""

TALKS_USERS_FILTERED_GRAPH = """
SELECT DISTINCT filtered_users.name, c2.talk_id from (select * from (SELECT count(c1.talk_id) as number_comments, name, users.user_id FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id
group by name) as commenting_users where number_comments>5) as filtered_users
left join comments as c2 on filtered_users.user_id=c2.user_id
"""


def comments(cursor):
    cursor.execute(COMMENTS_GRAPH)
    print(cursor.description)
    print()
    a = []
    for row in cursor:
        a.append(row)
    a = [tuple(sorted(x)) for x in a]
    users = set([x[0] for x in a])
    users = users.union([x[1] for x in a])
    i = 0
    user_dict = {}
    for user in users:
        user_dict[user] = i
        i += 1
    print("set = 127619")
    print("sorted tuples set = 112368")
    c = Counter(a)
    for x,y in c.most_common(10):
        print(x[0] + " <-> " + x[1] + " interakcji: " + str(y))
    a = [(user_dict[x[0]], user_dict[x[1]]) for x in a]
    c = Counter(a)
    print(len(c))
    with open("comments_gephi_users.csv", "w+", encoding="UTF8") as fh:
        fh.write("id,label\n")
        for elem in user_dict:
            fh.write("{0},{1}\n".format(user_dict[elem], elem))
    with open("comments_gephi_edges.csv", "w+", encoding="UTF8") as fh:
        fh.write("source,target,weight,type\n")
        for elem in c:
            fh.write("{0},{1},{2},undirected\n".format(elem[0], elem[1], c[elem]))


def talks_users(cursor):
    talk_dict = defaultdict(set)
    cursor.execute(TALKS_USERS_GRAPH)
    for row in cursor:
        talk_dict[row[1]].add(row[0])
    # print(dict(talk_dict))
    print(len(talk_dict))
    with open("talks_users.csv", "w+", encoding="UTF8") as fh:
        for k in talk_dict:
            already_were = set()
            for elem in talk_dict[k]:
                already_were.add(elem)
                if len(already_were) == len(talk_dict[k]):
                    break
                fh.write("{0}".format(elem))
                for elem2 in talk_dict[k]:
                    if elem2 not in already_were:
                        fh.write(",{0}".format(elem2))
                fh.write("\n")


def talks_users_filtered(cursor):
    cursor.execute(TALKS_USERS_FILTERED_GRAPH)
    talk_dict = defaultdict(set)
    for row in cursor:
        talk_dict[row[1]].add(row[0])
    # print(dict(talk_dict))
    print(len(talk_dict))
    with open("talks_users_filtered.csv", "w+", encoding="UTF8") as fh:
        for k in talk_dict:
            already_were = set()
            for elem in talk_dict[k]:
                already_were.add(elem)
                if len(already_were) == len(talk_dict[k]):
                    break
                fh.write("{0}".format(elem))
                for elem2 in talk_dict[k]:
                    if elem2 not in already_were:
                        fh.write(",{0}".format(elem2))
                fh.write("\n")

if __name__ == "__main__":
    db = pymysql.connect(host="127.0.0.1", port=10888, user=USER, passwd=PWD, db="igor", charset='utf8')
    cur = db.cursor()

    # comments(cur)
    talks_users_filtered(cur)
    cur.close()
    db.close()
