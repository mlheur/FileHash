# FileHash
python program to scan files, hash them and store those with metadata in dbms:MariaDB

Configuration:
1. install python3
2. install MariaDB
3. install mysql-connector for python3
4. sudo mysql (or mysql -uroot) < createuser.sql
5. mysql -uFileHash ... < createdb.sql
6. ./FileHash.py scan <dirs>
7. ./FileHash report [ 0 | 1 | + ]

from fresh opensus42.2 on WSL
       sudo visudo
       sudo vigr
       alias zypper='sudo zypper -n'
       zypper install python3 python-mysql-connector-python git ksh
       cd /u01
       scp -pr rdbms:/home/marc/.ssh ~/
       scp -pr rdbms:/home/marc/.my.cnf ~/
       git clone git@github.com:mlheur/FileHash.git
       cd FileHash
       scp -pr rdbms:/work/dev/FileHash/lib/mysql lib/
