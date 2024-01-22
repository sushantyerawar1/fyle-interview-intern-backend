-- Write query to get number of assignments for each state


SELECT state, count(*) AS Count
FROM assignments 
GROUP BY state;

