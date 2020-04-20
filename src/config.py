import os
from pathlib import Path
import mysql.connector as mysql_connector


class Config:
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', None)
    db_name = os.getenv('DB_NAME', 'dss.db')

    # for migration compatibility
    database_host = os.getenv('MYSQL_HOST', 'localhost')
    database_name = os.getenv('MYSQL_DATABASE', 'DSS')
    database_user = os.getenv('MYSQL_USER', 'dssuser')
    database_password = os.getenv('MYSQL_PASSWORD', 'dsspass')
    database_engine = mysql_connector
    database_migrations_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../migrations"))

    search_engine_host = os.getenv('ELASTIC_HOST', 'localhost')
    search_engine_port = 9200

    fill_data_script_path = (Path('src') / 'data.sql').absolute()

    n_recommendations = 5

    # used migrate engine
    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            if default is None:
                raise Exception("Not found attribute: %s" % name)
            else:
                return default
