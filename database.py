import sqlite3

class Database:
    def __init__(self, dbname="spdata.db", dbtable="general"):
        self.dbname = dbname
        self.dbtable = dbtable
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()

        # Create a table if there is no desired sqlite database table yet
        self.c.execute("CREATE TABLE IF NOT EXISTS '%s' (category text, importance integer, futility integer, data text)" % self.dbtable)

    # Put the data into database
    def input_data(self, category, importance, data):
        imp = 0
        fut = 0
        self.c.execute("SELECT importance, futility FROM '%s' WHERE data = '%s' and category = '%s'" % (self.dbtable, data, category))
        result = self.c.fetchone()

        if importance > 0:
            imp = importance
        elif importance < 0:
            fut = importance

        if result is None:
            self.c.execute("INSERT INTO '%s' VALUES('%s', %d, %d, '%s')" % (self.dbtable, category, imp, fut, data))
        else:
            imp += result[0]
            fut += result[1]
            self.c.execute("UPDATE '%s' SET 'importance' = %d, 'futility' = %d WHERE data = '%s'" % (self.dbtable, imp, fut, data))

        self.commit()

    # Return the data we have in the database
    def output_data(self):
        self.c.execute("SELECT * FROM '%s'" % self.dbtable)
        dbdata = self.c.fetchall()
        return dbdata

    # It is required to commit before ending of program or before closing of connection
    def commit(self):
        self.conn.commit()

    # It is required to save all the changes before disconnecting
    def close(self):
        self.conn.commit()
        self.c.close()

    # To prevent object from being removed, we should have this destructor so that we can commit changes and disconnect.
    def __del__(self):
        self.close()

# It's a self test (just to make sure functions work in an expected way)
if __name__ == '__main__':
    db = Database("test.db", "test")
    print db.output_data()
    db.input_data("general", 1, "haha")
    db.input_data("general", 1, "haha")
    db = Database("test.db", "test")
    print db.output_data()
    db.input_data("general", -1, "haha")
    db.input_data("general", -1, "haha")
    db.input_data("general", -1, "haha")
    db.input_data("general", -1, "hohoho")
    print db.output_data()
    db.close()
