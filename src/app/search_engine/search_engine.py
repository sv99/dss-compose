from elasticsearch import Elasticsearch
from abc import ABC, abstractmethod


class SearchEngine(ABC):
    engine: Elasticsearch

    @abstractmethod
    def add_to_index(self, index, id, text):
        pass

    @abstractmethod
    def reindex(self, index, data):
        pass

    @abstractmethod
    def search(self, index, description):
        pass
