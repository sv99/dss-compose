import os
from pathlib import Path


class Config:
    db_host = 'localhost'
    db_port = None
    db_name = 'dss.db'

    search_engine_host = os.getenv('ELASTIC_HOST', 'localhost')
    # search_engine_host = 'localhost'
    search_engine_port = 9200

    fill_data_script_path = (Path('src') / 'data.sql').absolute()

    n_recommendations = 5
