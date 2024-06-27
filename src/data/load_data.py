"""
elasticsearch==5.4.0
"""

from elasticsearch import Elasticsearch

ES = [{"host": "104.155.197.221","port": "9201"}]
es_conn = Elasticsearch(ES, timeout=180)

def keypo_textlist():
    """待修正，之後可能不會用到這個，而是直接接收API的資料，這裡作為模擬"""
    q = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "posttime": {
                                "gte": "2024-06-11", # 6/14, 1/14, 5/20, 6/11
                                "lte": "2024-06-12",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    },
                    {
                        "query_string": {
                            "query": "((\"PChome\" OR (\"網家\" OR \"網家則\" OR \"網家漲\" OR \"網家哥\" OR \"網家元\" OR \"咖網家\")) NOT \"news\" NOT \"菜單\")",
                            "fields": [
                                "title",
                                "content"
                            ]
                        }
                    }
                ]
            }
        },
        "aggs": {
            "rv": {
                "sum": {
                    "field": "count.comment"
                }
            }
        },
        "sort": [
            {
                "count.comment": "desc"
            },
            {
                "posttime": {
                    "order": "desc"
                }
            },
            "post.id"
        ],
        "from": 0,
        "size": 2000,
        "_source": {
            "include": [
                "title",
                "posttime",
                "author.name",
                "site*",
                "count*",
                "url",
                "content",
                "sentiment",
                "site.type"
            ]
        },
        "highlight": {
            "fields": {
                "title": {
                    "fragment_size": 200,
                    "boundary_scanner": "sentence",
                    "type": "unified"
                },
                "content": {
                    "fragment_size": 200,
                    "boundary_scanner": "sentence",
                    "type": "unified"
                },
                "content_jieba": {
                    "fragment_size": 200,
                    "boundary_scanner": "sentence",
                    "type": "unified"
                },
                "content_wildcard": {
                    "fragment_size": 200,
                    "boundary_scanner": "sentence",
                    "type": "unified"
                }
            },
            "tags_schema": "styled"
        }
    }

    es_resp = es_conn.search(index=["blog","sm","bbs","news"], body=q)
    data = es_resp["hits"]["hits"]
    data = data[:2]

    # Extract title and content from data
    res = []
    for item in data:
        source = item.get('_source', {})
        title = source.get('title', '')
        content = source.get('content', '')
        res.append(f"{title}\n{content}")
    return res