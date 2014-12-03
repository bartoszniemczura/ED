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
SELECT * FROM (SELECT name, c1.talk_id AS talk_id FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id) AS user_comments"""

TALKS_USERS_GRAPH = """
SELECT name, c1.talk_id AS talk_id
FROM  `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id = users.user_id
"""

TALKS_USERS_FILTERED_GRAPH = """
SELECT DISTINCT filtered_users.name, c2.talk_id FROM (SELECT * FROM (SELECT count(c1.talk_id) AS number_comments, name, users.user_id FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id
GROUP BY name) AS commenting_users WHERE number_comments>5) AS filtered_users
LEFT JOIN comments AS c2 ON filtered_users.user_id=c2.user_id
"""




COMMENTS_THEMES_GRAPH = """
SElECT name1, name2, name from
(SELECT name1, name2, theme_id from
(SELECT user_comments_reply.name as name1, users.name as name2, talk_id as comment_talk_id FROM
(SELECT user_comments.name AS name, user_comments.comment_id AS comment_id,
user_comments.parent_comment, comments.user_id AS parent_user_id, comments.talk_id as talk_id FROM
(SELECT name, c1.comment_id AS comment_id, c1.parent_id AS parent_comment FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id WHERE c1.parent_id!=0) AS user_comments
LEFT JOIN comments ON user_comments.parent_comment=comments.comment_id) AS user_comments_reply
LEFT JOIN users ON user_comments_reply.parent_user_id=users.user_id) as user_user
left join talk_themes on talk_themes.talk_id=comment_talk_id) as user_user_theme_talk
left join themes on themes.id=theme_id"""

TALKS_THEMES = """
SELECT names_themes.name, themes.name from
(SELECT id, name, talk_themes.theme_id as theme_id FROM talks
LEFT JOIN talk_themes ON talk_themes.talk_id=talks.id) as names_themes
LEFT JOIN themes ON themes.id=names_themes.theme_id"""


TALKS_THEMES_MAX = """
SELECT names_themes.name, themes.name from
  (SELECT id, name, theme_id FROM talks
    LEFT JOIN talk_themes ON talk_id=id) as names_themes
    LEFT JOIN themes ON themes.id=talk_themes.theme_id"""

TALKS_RATINGS_HIGHEST = """
select d.talk_id as talk1, t.talk_id as talk2, d.name as rating_name from
ratings_temp as t
left join
ratings_temp as d on t.name = d.name where t.talk_id != d.talk_id"""


TALKS_RATINGS= """
select d.talk_id as talk1, t.talk_id as talk2, d.name as rating_name from
ratings as t
left join
ratings as d on t.name = d.name where t.talk_id != d.talk_id"""


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
    for x, y in c.most_common(10):
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


def comments_themes(cursor):
    cursor.execute(COMMENTS_THEMES_GRAPH)
    print(cursor.description)
    print()
    a = []
    for row in cursor:
        a.append(row)
    a = [tuple(sorted(x[:-1]) + [x[-1]]) for x in a]
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
    for x, y in c.most_common(10):
        print(x[0] + " <-> " + x[1] + " interakcji: " + str(y))
    a = [(user_dict[x[0]], user_dict[x[1]], x[2]) for x in a]
    c = Counter(a)
    for el in c:
        print(el)
    print(c)
    print(len(c))
    with open("comments_themes_gephi_users.csv", "w+", encoding="UTF8") as fh:
        fh.write("id,label\n")
        for elem in user_dict:
            fh.write("{0},{1}\n".format(user_dict[elem], elem))
    with open("comments_themes_gephi_edges.csv", "w+", encoding="UTF8") as fh:
        fh.write("source,target,weight,type,topic\n")
        for elem in c:
            fh.write("{0},{1},{2},undirected,{3}\n".format(elem[0], elem[1], c[elem], elem[2]))


def users_themes(cursor):
    cursor.execute(COMMENTS_THEMES_GRAPH)
    print(cursor.description)
    print()
    a = []
    for row in cursor:
        a.append((row[0], row[1], str(row[2])))
    a = [tuple(sorted(x[:-1]) + [x[-1]]) for x in a]
    users = set([(x[0], str(x[2]).replace(',', '')) for x in a])
    users = users.union([(x[1], x[2].replace(',', '')) for x in a])
    i = 0
    user_dict = {}
    for user in users:
        user_dict[user] = i
        i += 1
    print("set = 127619")
    print("sorted tuples set = 112368")
    c = Counter(a)
    for x, y in c.most_common(10):
        print(x[0] + " <-> " + x[1] + " interakcji: " + str(y))
    a = [(user_dict[(x[0], x[2].replace(',', ''))], user_dict[(x[1], x[2].replace(',', ''))]) for x in a]
    c = Counter(a)
    for el in c:
        print(el)
    print(user_dict)
    print(len(c))
    with open("users_themes_gephi_users.csv", "w+", encoding="UTF8") as fh:
        fh.write("id,label,theme\n")
        for elem in user_dict:
            fh.write("{0},{1},{2}\n".format(user_dict[elem], elem[0]+elem[1], elem[1]))
    with open("users_themes_gephi_edges.csv", "w+", encoding="UTF8") as fh:
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


def talks_themes(cursor):
    cursor.execute(TALKS_THEMES)
    theme_to_talks = defaultdict(list)
    talk_to_themes = defaultdict(list)
    talks = set()
    for row in cursor:
        talks.add(row[0].replace(',', ''))
        theme_to_talks[str(row[1]).replace(',', '')].append(str(row[0]).replace(',', ''))
        talk_to_themes[str(row[0]).replace(',', '')].append(str(row[1]).replace(',', ''))
    i = 0
    talk_dict = {}
    for t in talks:
        talk_dict[t] = i
        i += 1

    with open("talks_themes_nodes.csv", 'w+', encoding="UTF8") as fh:
        fh.write('id,label\n')
        for t in talk_dict:
            fh.write("{0},{1}\n".format(talk_dict[t], t))

    with open("talks_themes_edges.csv", 'w+', encoding="UTF8") as fh:
        fh.write('source,target,label,type\n')
        for t in talk_to_themes:
            themes = talk_to_themes[t]
            for theme in themes:
                # print(theme)
                theme_to_talks[theme].remove(t)
                for talk in theme_to_talks[theme]:
                    fh.write("{0},{1},{2},undirected\n".format(talk_dict[t], talk_dict[talk], theme))


def talks_themes_maxcliques(cursor):
    cursor.execute(TALKS_THEMES)
    theme_to_talks = defaultdict(list)
    talks = set()
    for row in cursor:
        talks.add(row[0].replace(',', ''))
        theme_to_talks[str(row[1]).replace(',', '')].append(str(row[0]).replace(',', ''))
    i = 0
    talk_dict = {}
    for t in talks:
        talk_dict[t] = i
        i += 1

    with open("talks_themes_cliques.csv", 'w+', encoding="UTF8") as fh:
        for t in theme_to_talks:
            for talk in theme_to_talks[t]:
                fh.write("{0} ".format(talk_dict[talk]))
            fh.write(" -1\n")


def talks_ratings(cursor):
    cursor.execute(TALKS_RATINGS)
    talks_edges = []
    talks = set()
    for row in cursor:
        talks.add(row[0])
        talks.add(row[1])
        talks_edges.append(row)

    with open("talks_ratings_all_nodes.csv", 'w+', encoding="UTF8") as fh:
        fh.write('id\n')
        for t in talks:
            fh.write("{0}\n".format(t))

    with open("talks_ratings_all_edges.csv", 'w+', encoding="UTF8") as fh:
        fh.write('source,target,label,type\n')
        for t in talks_edges:
            fh.write("{0},{1},{2},undirected\n".format(t[0], t[1], t[2]))


def minimize_file(filename, output):
    with open(filename, encoding="utf8") as fh:
        content = fh.readlines()
        d = defaultdict(lambda: defaultdict(int))
        j = 0
        for l in content:
            j += 1
            i = 0
            k = ""
            for w in l.split(","):
                if i == 0:
                    k = w
                else:
                    if k in d[w]:
                        d[w][k] += 1
                    else:
                        d[k][w] += 1
                i += 1
        print("Before lines: {0}".format(j))
    i = 0
    with open(output, "w+", encoding="UTF8") as f:
        for w in d.keys():
            if len(d[w]):
                i += 1
                f.write(w)
                for w2 in d[w].keys():
                    f.write(",{0}".format(w2))
                f.write("\n")
    print("After lines: {0}".format(i))

    return d


# def


if __name__ == "__main__":
    # minimize_file("talks_users_filtered.csv", "minimized_talks_user_filtered.csv")
    db = pymysql.connect(host="127.0.0.1", port=10888, user=USER, passwd=PWD, db="igor", charset='utf8')
    cur = db.cursor()
    # 
    # comments(cur)
    # talks_users_filtered(cur)
    # comments_themes(cur)
    talks_themes(cur)
    # talks_ratings(cur)
    # talks_themes_maxcliques(cur)
    cur.close()
    db.close()
    pass
