# Tables

The database consisted of the following tables:

## <ins>EMP</ins>

| Attributes | Description |
| ---------- | ----------- |
| EMPNO | int, unique, primary key |
| ENAME | str |
| JOB | str |
| MGR | int, null |
| SAL | int |
| COMM | int, null |
| DEPTNO | int, foreign key |

## <ins>DEPT</ins>

| Attributes | Description |
| ---------- | ----------- |
| DEPTNO | int, unique, primary key |
| DNAME | str |
| LOC | str |
