
from django.core.management.base import BaseCommand, CommandError
from product_es.models import *
import os
import sys
from product_es.create_indexes import DocumentES


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        index = 'product_es'
        mapping_body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "substring": {
                            "filter": [
                                "lowercase"
                            ],
                            "tokenizer": "substring"
                        },
                    },
                    "tokenizer": {
                        "substring": {
                            "token_chars": [
                                "letter",
                                "digit",
                                "whitespace",
                                "punctuation",
                                "symbol"
                            ],
                            "min_gram": "1",
                            "type": "ngram",
                            "max_gram": "30"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "substring"

                    },
                    "sku": {
                        "type": "text"
                    },
                    "tax_code": {
                        "type": "double"
                    },
                    "tax_rate": {
                        "type": "float"
                    }
                }
            }
        }
        try:
            doc_data = []
            product_objs = Product.objects.all()
            for product in product_objs:
                doc_data.append(self.create_doc_map(product))
            document_es = DocumentES(mapping_body, index, doc_data)
            document_es.create_reset_es_index()

            print('dumped...product')

        except Exception as e:
            print("line number of error is {}".format(
                    sys.exc_info()[2].tb_lineno) + str(e))

    def create_doc_map(self, product):
        doc_body = {}
        if product:
            return {
                "name": product.name,
                "sku": product.sku,
                "tax_code": product.tax_code.code if product.tax_code else 0,
                "tax_rate": product.tax_code.tax_percentage if product.tax_code else 0
            }
        return doc_body
