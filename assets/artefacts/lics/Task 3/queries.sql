mysql;
USE COMPANY1;

-- Query 1 --------------------------------------------------------------------
-- List all Employees whose salary is between 1,000 AND 2,000. 
-- Show the Employee Name, Department and Salary

SELECT 
  ENAME as "Employee Name",
  DNAME as "Department",
  SAL as "Salary"
FROM EMP
JOIN DEPT
  ON EMP.DEPTNO = DEPT.DEPTNO 
WHERE SAL BETWEEN 1000 AND 2000;

-- NOTES
-- DNO is an alternative identifier for a department, that could have been used.
-- Either INNER or LEFT JOIN would work as the filter is on the left table,
-- and the right table is purely complementary.


-- Query 2 --------------------------------------------------------------------
-- Count the number of people in department 30 who receive a salary and the 
-- number of people who receive a commission

SELECT 
  SUM(CASE 
    WHEN SAL > 0 THEN 1 
    ELSE 0 
  END) as "Amount who received Salary",
  SUM(CASE
    WHEN COMM > 0 THEN 1
    ELSE 0
  END) as "Amount who received Commission"
FROM EMP
WHERE DEPTNO = 30
GROUP BY DEPTNO;

-- NOTES
-- By using CASEs, we can filter specific values from being 
-- included in specific aggregation functions, despite those values 
-- being included in a group, and used in other aggregation functions in the
-- same query. The use of CASE statements in this query was to filter non positive 
-- values from being counted.
-- SUM was used to count as a matter of taste, as peformance wise the approach is
-- identical to using COUNT. Any values that need to be counted are given a 
-- value of 1, while those that are not are given a value of 0, so the summation 
-- is essentially identical to counting.  
-- Alternatively, the COUNT function could be used in place of the SUM functions, 
-- but the ELSE CASEs would need to return NULL instead of 0, as the COUNT function 
-- counts any non-null values, including 0.  


-- Query 3 -----------------------------------------------------------------------
-- Find the name and salary of employees in Dallas

SELECT 
  ENAME as "Employee Name",
  SAL as "Salary"
FROM EMP
JOIN DEPT
  ON EMP.DEPTNO = DEPT.DEPTNO 
WHERE DEPT.DEPTNO = 20;

-- NOTES
-- The WHERE clause could check that EMP.LOC = "DALLAS" instead,
-- but it's usually better practise to use primary keys in clauses where possible,
-- as SQL is optimised around indexes, which primary keys create. This is especially
-- important for large tables. 


-- Query 4 -------------------------------------------------------------------------
-- List all departments that do not have any employees

SELECT DNAME as "Department"
FROM EMP
RIGHT JOIN DEPT
  ON EMP.DEPTNO = DEPT.DEPTNO
GROUP BY DEPT.DEPTNO
HAVING COUNT(EMPNO) = 0;

-- NOTES
-- DNO is an alternative identifier for a department, that could have been used.
-- RIGHT JOIN is used as the DEPT table contains departments not mentioned in the
-- EMP table. 
-- GROUP BY is used in order to create filters with aggregation functions 
-- using HAVING.
-- COUNT was used as it doesn't count null values, so if COUNT(EMPNO) = 0, then
-- there is no non null values in the EMPNO column for rows in the group.
-- EMPNO was chosen over ENAME to take advantage of SQL's indexing optimisations.


-- Query 5 -------------------------------------------------------------------------
-- List the department number and average salary of each department

SELECT 
  DEPT.DEPTNO as "Department Number", 
  ROUND(AVG(SAL), 2) as "Average Salary"
FROM EMP
JOIN DEPT
  ON EMP.DEPTNO = DEPT.DEPTNO
GROUP BY DEPT.DEPTNO;

-- NOTES
-- ROUND has been used to round the average to a monetary value.
-- DEPT.DEPTNO has been used instead of DNAME for grouping 
-- to take advantage of SQL indexing.
-- INNER JOIN has been used to ignore departments with no employees, and 
-- employees with no departments.