# FileHash
pyhton program to scan files, hash them and store those with metadata in dbms:MariaDB

Configuration:
1. install python3
2. install MariaDB
3. install mysql-connector for python3
4. sudo mysql (or mysql -uroot) < createuser.sql
5. mysql -uFileHash ... < createdb.sql
6. ./FileHash.py scan <dirs>
7. ./FileHash report [ 0 | 1 | + ]
