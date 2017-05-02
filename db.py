import mysql.connector
from mysql.connector import MySQLConnection
from configparser import ConfigParser
# filename = 'db_config.ini'


def read_db_config(filename='db_config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for key, val in items:
            db[key] = val
    else:
        raise Exception("%s not found in the file %s") % (section, filename)

    return db


class DB:

    def __init__(self, host=None, database=None, user=None, password=None, filename='db_config.ini'):
        # if host is None or database is None or user is None or password is None:
        #     raise Exception('Enter all needed data for connection')
        # else:
        #     self.connect = mysql.connector.connect(host=host,
        #                                            database=database,
        #                                            user=user,
        #
        # self.connect = mysql.connector.connect(host=host,
        #                                             database=database,
        #                                             user=user,
        #                                             password=password)
        db_config = read_db_config()
        self.connect = MySQLConnection(**db_config)
        if self.connect.is_connected():
            self.cursor = self.connect.cursor()
        else:
            Exception("incorrect data")

    def fetch_table(self):
        return self.cursor.execute("SELECT * FROM main;")

    def fetch_row(self):
        self.cursor.execute("SELECT * FROM main;")
        return self.cursor.fetchone()

    # def fetch_post_text(self, post_id):
    #     query = "SELECT post_text FROM main WHERE id=%s;" % post_id
    #     return self.cursor.fetchone(query)

    # def insert_post_text(self, post_id, user_token, user_secret, post_text):
    #     query = "INSERT INTO main(id, token, secret, post_text) VALUES (%s,%s, %s, %s);" % \
    #             (post_id, user_token, user_secret, post_text)
    #     return self.cursor.execute(query)

    def insert_post_id(self, post_id, user_token, user_secret):
        query = "INSERT INTO main(id, token, secret) VALUES ('%s', '%s', '%s');" % \
                (post_id, user_token, user_secret)
        self.cursor.execute(query)
        self.connect.commit()
        return True

    def fetch_post_ids(self, user_token, user_secret):
        query = "SELECT id FROM main WHERE token = '%s' AND secret = '%s' ;" % (user_token, user_secret)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_post_id(self, post_id):
        query = "DELETE FROM main WHERE id = '%s';" % post_id
        self.cursor.execute(query)
        self.connect.commit()
        return True