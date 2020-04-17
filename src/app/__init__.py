from flask import Flask
from flask_restplus import Api
from .knowledge_base import KnowledgeBase

from src.app.repository.sqlite_repository import SQLiteRepository
from src.app.search_engine.elastic_search_engine import ElasticsearchEngine
from src.config import Config


app = Flask(__name__)
api = Api(app, title='Decision Support System',
          description='DSS which provides recommendations on solving common '
                      'issues while working with information security systems')
ns = api.namespace('DSS', description='Get your recommendations or enrich system knowledge-base')

config = Config()
repository = SQLiteRepository(config)
search_engine = ElasticsearchEngine(config)

kb = KnowledgeBase(repository, search_engine, config)

from src.app import routes
