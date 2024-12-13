import fdb
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
CHARSET = os.getenv('CHARSET')
BRANCHES = os.getenv('BRANCHES')
DSN_BRANCH = os.getenv('DSN_BRANCH')


def get_db(dbname:str):
    con = fdb.connect(
        dsn=DSN_BRANCH.format(dbname) if dbname != 'office' else DSN_BRANCH,
        user=USER,
        password=PASSWORD,
        charset=CHARSET
        )
    cur = con.cursor()
    return cur


