import pandas as pd
from mysql.connector import MySQLConnection, Error as MySqlError
from configparser import ConfigParser
from collections import namedtuple


User = namedtuple("User", ["id", "email", "password", "creation_date"])

class DataBase:
    def __init__(self):
        try:
            self.conn = None
            self.__dbconfig = self._read_db_config()

            self.conn = MySQLConnection(**self.__dbconfig)
        except MySqlError as error:
            print(f"{error = }")

    def _read_db_config(self, file_name="plikiPython\\projekty Python\\biblioteka_v2\\config.ini", section="mysql"):
        """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """
        
        parser = ConfigParser()
        parser.read(file_name)

        db = {}

        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(f"{section} not found in the {file_name} file")

        return db

    def close_db(self):
        if self.conn is not None:
            self.conn.close()

    def borrow_books(self, user_id: int, books_id: list[str] | tuple[str]):
        with self.conn.cursor() as cursor:
            for i in range(len(books_id)):
                cursor.callproc("borrow_book", (user_id, books_id[i]))
    
    def add_user(self, user_email: str, user_password: str):
        sql = """
        SELECT in_users_table(%s, %s);
        CALL add_user(%s, %s);
        """
        with self.conn.cursor() as cursor:
            result = next(cursor.execute(sql, (user_email, user_password) * 2, multi=True))
            self.conn.commit()
            return 0 == result.fetchone()[0] 

    def delete_user(self, user_email: str, user_password: str):
        sql = """
        CALL delete_user(%s, %s)
        """
        self._execute_query(sql, (user_email, user_password))

    def delete_users_book(self, user_id: int, books_id: list[str] | tuple[str]):
        with self.conn.cursor() as cursor:
            for i in range(len(books_id)):
                cursor.callproc("return_book_to_library", (user_id, books_id[i]))

    def find_book(self, id=-1, title="NULL", subtitle="NULL", authors="NULL", categories="NULL") -> pd.DataFrame:
        if title == "NULL" and subtitle == "NULL" and authors == "NULL" and categories == "NULL":
            sql = "SELECT * FROM books"
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                df = pd.DataFrame.from_records(cursor.fetchall())
                return self._rename_df(df)
        
        with self.conn.cursor() as cursor:
            cursor.callproc("find_book", (id, title, subtitle, authors, categories))
            df = pd.DataFrame.from_records(cursor._stored_results[0].fetchall())
            return self._rename_df(df)

    def find_users_books(self, user_id: int) -> pd.DataFrame:
        with self.conn.cursor() as cursor:
            cursor.callproc("find_users_books", (user_id,))
            df = pd.DataFrame.from_records(cursor._stored_results[0].fetchall())
            return self._rename_df(df.rename(columns={10: "date"}))

    def check_user_exists(self, user_email, user_password) -> bool:
        sql = """
        SELECT in_users_table(%s, %s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (user_email, user_password))
            return 1 in cursor.fetchone()
    
    def return_user_data(self, user_email, user_password) -> User:
        sql = """
        SELECT *
        FROM users
        WHERE user_email = %s AND user_password = %s
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (user_email, user_password))
            result = cursor.fetchone() 
            return User(*result)

    def _rename_df(self, old_df: pd.DataFrame) -> pd.DataFrame:
        return old_df.rename(columns={
            0: "id", 1: "title", 2: "subtitle", 
            3: "authors", 4: "categories", 5: "thumbnail", 
            6: "description", 7: "published_year", 8: "average_rating",
            9: "num_pages"})
    
    def _execute_query(self, sql, values):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, values)
            self.conn.commit()

    def query(self, sql, *args):
        with self.conn.cursor as cursor:
            cursor.execute(sql, args)
            return cursor.fetchall()


if __name__ == "__main__":
    db = DataBase()

    db.find_book(subtitle="No subtitle")

    db.close_db()
    