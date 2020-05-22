from django_es.settings import ES_HOST, ES_PORT
from elasticsearch import Elasticsearch


class DocumentES:

    def __init__(self, mapping_body, index, doc_data):
        self.es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
        self.index = index
        self.mapping_body = mapping_body
        self.doc_data = doc_data

    def create_reset_es_index(self):
        if self.es.indices.exists(self.index):
            self.es.indices.delete(index=self.index)

        self.es.indices.create(index=self.index, ignore=400,
                                body=self.mapping_body)
        self.dump_document_data()

    def dump_document_data(self):
        for data in self.doc_data:
            self.es.index(index='{}'.format(self.index), body=data)
        
        

