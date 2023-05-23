
-- The issue in the given sql statement is that it is missing GROUP BY clause. 
-- The GROUP BY clause is needed here to specify how the data should be grouped before calculating the averge
-- How to modify: it should group the data by UserId, and then get the averge order amount by user 
-- and only users have at least one order will be included

-- here is the modified code:

SELECT UserId, AVG(Total) AS AvgOrderTotal
FROM Invoices
GROUP BY UserId
HAVING COUNT(OrderId) >= 1