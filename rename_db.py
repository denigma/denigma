"""A module to rename a database.

Usage:
  python rename_db.py <old_db_name> <new_db_name> <user> 

user is by default root
"""
import sys
import MySQLdb


def main(db_old_name, db_new_name, user='root'):
    con = MySQLdb.connect(user='root') # Connection.
    cur = con.cursor() # Cursor.
    com = cur.execute('use {0}'.format(db_old_name)) # Command.
    res = cur.fetchall() # Results.
    for i in res:
        print i[0]
	cur.execute('RENAME TABLE {0}.{2} TO {1}.{2}'.format(db_old_name, db_new_name, i[0]))


if __name__ == '__main__':
    if sys.argv > 1:
        db_old_name = sys.argv[1]
	db_new_name = sys.argv[2]
        user = sys.argv[3]
	print db_old_name, db_new_name, user
	main(db_old_name, db_new_name, user)
