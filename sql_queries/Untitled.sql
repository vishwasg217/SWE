SELECT p.*, CONCAT(u.first_name, ' ', u.last_name) AS author_name 
FROM 
(
	SELECT p.*, COUNT(v.post_id) AS votes
FROM posts AS p
LEFT JOIN votes as v
ON p.id = v.post_id
GROUP BY p.id
) AS p
JOIN users as u
ON p.author_id = u.id