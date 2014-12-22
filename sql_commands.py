"""
SQL commands used by other scripts
"""

# SELECTS


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
SELECT name1, name2, name FROM
(SELECT name1, name2, theme_id FROM
(SELECT user_comments_reply.name AS name1, users.name AS name2, talk_id AS comment_talk_id FROM
(SELECT user_comments.name AS name, user_comments.comment_id AS comment_id,
user_comments.parent_comment, comments.user_id AS parent_user_id, comments.talk_id AS talk_id FROM
(SELECT name, c1.comment_id AS comment_id, c1.parent_id AS parent_comment FROM `users`
LEFT OUTER JOIN comments AS c1 ON c1.user_id=users.user_id WHERE c1.parent_id!=0) AS user_comments
LEFT JOIN comments ON user_comments.parent_comment=comments.comment_id) AS user_comments_reply
LEFT JOIN users ON user_comments_reply.parent_user_id=users.user_id) AS user_user
LEFT JOIN talk_themes ON talk_themes.talk_id=comment_talk_id) AS user_user_theme_talk
LEFT JOIN themes ON themes.id=theme_id"""

TALKS_THEMES = """
SELECT names_themes.name, themes.name FROM
(SELECT id, name, talk_themes.theme_id AS theme_id FROM talks
LEFT JOIN talk_themes ON talk_themes.talk_id=talks.id) AS names_themes
LEFT JOIN themes ON themes.id=names_themes.theme_id"""

TALKS_THEMES_MAX = """
SELECT names_themes.name, themes.name FROM
  (SELECT id, name, theme_id FROM talks
    LEFT JOIN talk_themes ON talk_id=id) AS names_themes
    LEFT JOIN themes ON themes.id=talk_themes.theme_id"""

TALKS_RATINGS_HIGHEST = """
SELECT d.talk_id AS talk1, t.talk_id AS talk2, d.name AS rating_name FROM
ratings_temp AS t
LEFT JOIN
ratings_temp AS d ON t.name = d.name WHERE t.talk_id != d.talk_id"""

TALKS_RATINGS = """
SELECT d.talk_id AS talk1, t.talk_id AS talk2, d.name AS rating_name FROM
ratings AS t
LEFT JOIN
ratings AS d ON t.name = d.name WHERE t.talk_id != d.talk_id"""


# INSERTS

ADD_USER = """INSERT INTO users VALUES (%s,%s,%s,%s, %s)"""

SAVE_COMMENT = """INSERT INTO comments VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""