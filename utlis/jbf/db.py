

import sqlite3
 
# Creates or opens a file called mydb with a SQLite3 DB



def sql_execute():
    db = sqlite3.connect('data/mydb')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()

def upd_img_status(dbfile, id, status, folder):
    try:

        db = sqlite3.connect(dbfile)
        cursor = db.cursor()

        sql = "update Images set status='{}', folder='{}' where id={}".format(status, folder, id)
        print(sql)
        cursor.execute(sql)
        db.commit()

    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def upd_img_notes(dbfile, id, status, notes):
    try:

        db = sqlite3.connect(dbfile)
        cursor = db.cursor()

        #sql = "update Images set status='{}', ai_description='{}' where id={}".format(status, notes, id)
        #print(sql)
        cursor.execute("update Images set status=?, ai_description=? where id=?", [status, notes, id])
        # cursor.execute(sql)
        db.commit()

    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def insert_file(dbfile, source, folder, filename, tags, imageName):
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()

    sql = '''INSERT INTO Images (source, folder, filename, tags, imageName) VALUES(?,?,?,?,?)'''
    cursor.execute(sql, (source, folder, filename, tags, imageName))
    db.commit()
    db.close()

def queryall(dbfile, sql):

    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(dbfile)
        # Get a cursor object
        cursor = db.cursor()

        cursor.execute(sql)
        all_rows = cursor.fetchall()
        return all_rows

#        for row in all_rows:
#            # row[0] returns the first column in the query (name), row[1] returns email column.
#            print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))

    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()




def main():
    pass

if __name__ == "__main__":
    main()
