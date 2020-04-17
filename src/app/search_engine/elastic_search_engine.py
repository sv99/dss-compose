from elasticsearch import Elasticsearch
from .search_engine import SearchEngine


class ElasticsearchEngine(SearchEngine):
    def __init__(self, config):
        self.config = config
        self.engine = Elasticsearch(
            f'http://{config.search_engine_host}:{config.search_engine_port}')

    def add_to_index(self, index, id, text):
        self.engine.index(index=index, id=id, body={'description': text})

    def reindex(self, index, data):
        if self.engine.indices.exists(index):
            self.engine.indices.delete(index)

        for id, text in data:
            self.add_to_index(index, id, text)

    def search(self, index, description):
        res = self.engine.search(
            index=index, body={'query': {'match': {'description': description}}})

        return [int(item['_id']) for item in res['hits']['hits']]
