from flask import Flask
from flask_restplus import Api
from .knowledge_base import KnowledgeBase

from .repository import SQLiteRepository, MySQLRepository
from .search_engine.elastic_search_engine import ElasticsearchEngine
from src.config import Config
from ..db_migrate import Migrate
from ..cmd import add_db_command, register_elastic_command

app = Flask(__name__)
api = Api(app, title='Decision Support System',
          description='DSS which provides recommendations on solving common '
                      'issues while working with information security systems')
ns = api.namespace('DSS', description='Get your recommendations or enrich system knowledge-base')

config = Config()
migrate = Migrate(config)

# repository = SQLiteRepository(config)
repository = MySQLRepository(config)
search_engine = ElasticsearchEngine(config)
kb = KnowledgeBase(repository, search_engine, config)

app.cli.add_command(add_db_command(migrate))
register_elastic_command(app, kb)

from src.app import routes
