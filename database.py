import sqlite3

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('./user-oaks.db')

        # If 'users' table already exists, pass. Else create table
        if self.connection.execute(
            '''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'users';
            ''').fetchall():
            pass
        else:
            self.connection.execute(
                '''
                CREATE TABLE users(
                    user_name TEXT PRIMARY KEY,
                    user_oak TEXT
                )
                ''')
            self.connection.commit()
    
    def add_user(self, username: str, user_oak: str) -> None:
        self.connection.execute(
            '''
            INSERT INTO users (user_name, user_oak)
            VALUES (?, ?)
            ''',
            (username, user_oak))
        self.connection.commit()
    
    def remove_user(self, username:str) -> None:
        self.connection.execute(
            '''
            DELETE FROM users
            WHERE user_name = ?
            ''',
            (username,)
        )
        self.connection.commit()
    
    def retrieve_user_oak(self, username: str) -> str:
        oak = self.connection.execute(
            '''
            SELECT user_oak
            FROM users
            WHERE user_name = ?
            ''', (username,))
        return oak.fetchone()[0]