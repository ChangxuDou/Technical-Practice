SELECT * FROM sql_blog.posts;
CREATE FULLTEXT INDEX idx_title_bogy ON posts(title,body);
SHOW INDEX FROM posts;
-- Natural Language Mode
SELECT * ,MATCH (title,body) AGAINST('react redux')
FROM posts
WHERE MATCH (title,body) AGAINST('react redux'); -- Search for the relavant result which has one or both keywords

-- Boolean language Mode
SELECT * ,MATCH (title,body) AGAINST('react redux')
FROM posts
WHERE MATCH (title,body) AGAINST('react - redux + form' IN BOOLEAN MODE);
-- + must have this keyword - means don't have this keyword 

-- Search for the exact phrase
-- WHERE MATCH (title,body) AGAINST('"handling a form"' IN BOOLEAN MODE);

-- Search for the relavant result which has one or both keywords
-- WHERE MATCH (title,body) AGAINST('react redux' IN BOOLEAN MODE);




