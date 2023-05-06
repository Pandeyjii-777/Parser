# from elasticsearch import Elasticsearch
import pandas as pd
import requests
import json
from service.Connections import *


# def init():
#     # es = Elasticsearch("http://localhost:9200")
#     # es.info().body
#     r = requests.put('http://localhost:9200/synonym_test4/',
#         headers = {'Content-type': 'application/json'},
#
#         json = {
#         "settings": {
#             "analysis": {
#             "analyzer": {
#                 "my_synonyms": {
#                 "tokenizer": "whitespace",
#                     "filter": ["lowercase","my_synonym_filter"]
#                     }
#                 },
#             "filter": {
#                 "my_synonym_filter": {
#                 "type": "synonym",
#                     "ignore_case": "true",
#                     "synonyms": ["delhi ,delli", "gurgaon, gurugram", "apple, appel", "แขวงจันท, แขวงจันทรเกษม"]
#                     }
#                 }
#             }
#         },
#
#         "mappings" :{
#         "properties": {
#             "some_text": {
#             "type": "text",
#                 "search_analyzer": "my_synonyms"
#                 }
#             }
#         }
#         }
#     )
#
#     addToDoc(1,"apple")
#     addToDoc(2,"delhi")
#     addToDoc(3,"gurgaon")
#     addToDoc(4,"แขวงจันท")
#
#     print("index Status :" , r)
#     return r
#
#
# def addToDoc(text_id, text):
#     r = requests.put(f"http://localhost:9200/synonym_test4/_doc/{text_id}",
#             headers = {'Content-type': 'application/json'},
#             json = {
#             "some_text": text
#             }
#         )
#     print("text added status", r)
#

def getSynonym(text):
    r = requests.get(esUrl+'synonym_test/_search?pretty',

    headers = {'Content-type': 'application/json'},

    json = {
        "query": {
            "bool": {
                "must": [
                    { "match": { "some_text": text } }
                ]
            }
        }
        }
    )

    parsed = r.json()
    lst = parsed['hits']['hits']
    if len(lst) == 0:
        return ""
    return lst[0]['_source']['some_text']


# reed to run once only
# init()
# print(getAll())
print(getSynonym("แขวงจันทรเกษม"))
# print(getSynonym("Del"))

def getSimilarText(text,pincode,textKey):
    r = requests.get(esUrl+textKey+'/_search?pretty',

    headers = {'Content-type': 'application/json'},

    json = {
        "query": {
            "bool": {
                "must": [
                    { "match": { textKey: text } }
                ],
                "filter": [{
                      "term": {
                        "pincode": pincode
                      }
                    }
                  ]
            }
        }
        }
    )

    parsed = r.json()
    lst = parsed['hits']['hits']
    if len(lst) == 0:
        return ""
    resArr = []
    k= 0
    for i in lst:
        if k == 5:
            break
        k = k + 1
        resArr.append(i['_source'][textKey])
    return resArr