import sqlite3
import enum


class QueryCode(enum.Enum):
    CREATE = 1,
    INSERT = 2,
    READ = 3,
    UPDATE = 4


class DatabaseConn(sqlite3.Connection):

    def __init__(self, host):
        self.host = host
        self.connection = None
        
    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if exc_tb or exc_type or exc_val:
        #     if self.query_code == QueryCode.CREATE:
        #         pass
        #     elif self.query_code == QueryCode.INSERT:
        #         pass
        #     elif self.query_code == QueryCode.READ:
        #         pass
        #     elif self.query_code ==
        # else:
        self.connection.commit()
        self.connection.close()
