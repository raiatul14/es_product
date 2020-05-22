from elasticsearch import Elasticsearch
from django_es.settings import ES_HOST, ES_PORT


class BaseES:

    def __init__(self):
        self.es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
