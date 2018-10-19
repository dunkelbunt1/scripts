# This script takes a value from a DB and runs .sql scripts in a numeric order

#!/usr/bin/python

import sys
import os
import glob
import MySQLdb
# Here you provide your parameter
DIRECTORY = str(sys.argv[1])
USER= str(sys.argv[2]) 
HOST= str(sys.argv[3])
DB = str(sys.argv[4])
PASSWORT= str(sys.argv[5]) 
    
# Connection to the database and returns the current DB Version.
def get_db_version():
    DATA_BASE_VERSION =-1
    db = MySQLdb.connect(host=HOST,    
                         user=USER,         
                         passwd=PASSWORT,  
                         db=DB)

    cur = db.cursor()
    cur.execute("SELECT version FROM version.versionTable LIMIT 1;") #Adjust to the highest number
    for row in cur.fetchall():
        DATA_BASE_VERSION = row[0]
    db.close()
    return DATA_BASE_VERSION

# Create a List with all sql files with the lowest value first
def get_filtered_sql_files(DATA_BASE_VERSION):
    sqlnumbers =[]
    sqlfiles = []
    result = []
    os.chdir(DIRECTORY)
    for file in glob.glob('*.sql'):
        sqlfiles.append(file)
    #print sqlfiles

    # sorts the list; the lowest number first
    lowest_sqlfiles = sorted(sqlfiles)
    #print lowest_sqlfiles

# Compares the list of SQL files with the database version and gives you the outstanding files back.
    for file in lowest_sqlfiles:
        if compare (file, DATA_BASE_VERSION):
            result.append(file)
    return result # < here is the list of all scripts that will need to run


# This is a function to compare the SQL files against the DB version 
# It takes the first 3 chars and creates an Integer for it
def compare(SQLFILES, DATA_BASE_VERSION):
    SQL_FILE_VERSION = SQLFILES[:3]
    return int(SQL_FILE_VERSION) > int(DATA_BASE_VERSION)

# This function should run every SQL file which is needed to reach the highest number; error in for loop
def update_db_version(OUSTANDING_FILTERED_SQL_FILES):
    SCRIPTS_RUN = []
    #print OUTSTANDING_FILTERED_SQL_FILES
    if len(OUSTANDING_FILTERED_SQL_FILES) > 0:
        for item in OUSTANDING_FILTERED_SQL_FILES:
            #print "OK"
            db = MySQLdb.connect(host=HOST,    
                                 user=USER,         
                                 passwd=PASSWORT,  
                                 db=DB)
            cur = db.cursor()
            fd = open(item , 'r')
            sqlFile = fd.read()
            fd.close()
            cur = db.cursor()
            cur.execute(sqlFile)
            print item
            #print sqlFile
            db.commit()
            db.close()
    else:
        print "NN"
#This is going to update the DB version on position 1 of the highest script number
def set_db_version(OUSTANDING_FILTERED_SQL_FILES):
    db = MySQLdb.connect(host=HOST,    
                         user=USER,         
                         passwd=PASSWORT,  
                         db=DB)

    cur = db.cursor()
    if len(OUSTANDING_FILTERED_SQL_FILES) > 0: #This is needed when there is no Update To run. Otherwise the script will fail

        UPDATED_DB_VERSION = OUSTANDING_FILTERED_SQL_FILES[-1]
        UPDATED_DB_VERSION_INT = int( UPDATED_DB_VERSION[:3])
        insert_statement = "UPDATE version.versionTable SET version = %s LIMIT 1" %(UPDATED_DB_VERSION_INT)

        #print insert_statement
        cur.execute(insert_statement)
        db.commit()
        db.close()
        print "Database is up to date"
    else: 
        print "No new version available"


if __name__ == '__main__':
    if len(sys.argv) != 5:
            DATA_BASE_VERSION = get_db_version() 
            OUSTANDING_FILTERED_SQL_FILES = get_filtered_sql_files(DATA_BASE_VERSION)
            if len(OUSTANDING_FILTERED_SQL_FILES) > 0:
                update_db_version(OUSTANDING_FILTERED_SQL_FILES)
                set_db_version(OUSTANDING_FILTERED_SQL_FILES)
            else:
                print "No need to update"
    else:
        print "You have to enter: directory-with-sql-scripts,  username-for-the-db,  db-host, db-name, db-password"
