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
            self.cursor = self.conn.cursor()
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
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
    
    def add_user(self, user_email: str, user_password: str):
        sql = """
        SELECT in_users_table(%s, %s);
        CALL add_user(%s, %s);
        """
        result = next(self.cursor.execute(sql, (user_email, user_password) * 2, multi=True))
        return 0 == result.fetchone()[0] 

    def delete_user(self, user_email: str, user_password: str):
        sql = """
        CALL delete_user(%s, %s)
        """
        self._execute_query(sql, (user_email, user_password))

    def delete_users_book(self, user_id: int, book_id: int):
        sql = """
        CALL return_book_to_library(%s, %s)
        """
        self._execute_query(sql, (user_id, book_id))

    def find_book(self, book_id=-1, book_title="NULL", book_subtitle="NULL", book_authors="NULL", book_categories="NULL") -> pd.DataFrame:
        sql = """
        CALL find_book(%s, %s, %s, %s, %s)
        """
        result = next(self.cursor.execute(sql, (book_id, book_title, book_subtitle, book_authors, book_categories), multi=True))
        df = pd.DataFrame.from_records(result)
        df.rename(columns={
            0: "book_id", 1: "title", 2: "subtitle", 
            3: "authors", 4: "categories", 5: "thumbnail", 
            6: "description", 7: "published_year", 8: "average_rating",
            9: "num_pages"}, inplace=True)
        
        return self._set_dtypes(df)

    def find_users_books(self, user_id: int) -> pd.DataFrame:
        sql = """
        CALL find_users_books(%s)
        """
        result = next(self.cursor.execute(sql, (user_id,), multi=True))
        df = pd.DataFrame.from_records(result)
        df.rename(columns={
            0: "book_id", 1: "title", 2: "subtitle", 
            3: "authors", 4: "categories", 5: "thumbnail", 
            6: "description", 7: "published_year", 8: "average_rating",
            9: "num_pages"}, inplace=True)
        
        return self._set_dtypes(df)

    def check_user_exists(self, user_email, user_password) -> bool:
        sql = """
        SELECT in_users_table(%s, %s)
        """
        result = next(self.cursor.execute(sql, (user_email, user_password), multi=True))
        return 1 in result.fetchone()
    
    def return_user_data(self, user_email, user_password) -> User:
        sql = """
        SELECT *
        FROM users
        WHERE user_email = %s AND user_password = %s
        """
        self.cursor.execute(sql, (user_email, user_password))
        result = self.cursor.fetchone() 
        return User(*result)

    def _execute_query(self, sql, values):
        self.cursor.execute(sql, values)
        self.conn.commit()

    def _set_dtypes(self, old_df: pd.DataFrame) -> pd.DataFrame:
        df = old_df
        df["book_id"] = df["book_id"].astype("int32")
        df["title"] = df["title"].astype("category")
        df["subtitle"] = df["subtitle"].astype("category")
        df["authors"] = df["authors"].astype("category")
        df["categories"] = df["categories"].astype("category")
        df["thumbnail"] = df["thumbnail"].astype("category")
        df["description"] = df["description"].astype("category")
        df["published_year"] = df["published_year"].astype("int16")
        df["num_pages"] = df["num_pages"].astype("int16")

        return df

    def query(self, sql, *args):
        result = next(self.cursor.execute(sql, args, multi=True))
        return result.fetchall()


if __name__ == "__main__":
    db = DataBase()

    db.return_user_data(user_email="maciek987@gmail.com", user_password="123456")

    db.close_db()
    