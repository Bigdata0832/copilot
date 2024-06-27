from elasticsearch import Elasticsearch

ES = [{"host": "104.155.197.221", "port": "9201"}]
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
                                "gte": "2024-06-11",
                                "lte": "2024-06-12",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    },
                    {
                        "query_string": {
                            "query": "((\"PChome\" OR (\"網家\" OR \"網家則\" OR \"網家漲\" OR \"網家哥\" OR \"網家元\" OR \"咖網家\")) NOT \"news\" NOT \"菜單\")",
                            "fields": ["title", "content"]
                        }
                    }
                ]
            }
        },
        "aggs": {
            "rv": {
                "sum": {"field": "count.comment"}
            }
        },
        "sort": [
            {"count.comment": "desc"},
            {"posttime": {"order": "desc"}},
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

    es_resp = es_conn.search(index=["blog", "sm", "bbs", "news"], body=q)
    data = es_resp["hits"]["hits"]

    # 以第一次搜索結果為基礎，提取需要的條件 (例如所有的文檔ID)
    doc_ids = [item['_id'] for item in data]
    print(len(doc_ids))
    return doc_ids, data

def second_search_based_on_first_result(doc_ids):
    q2 = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "terms": {
                            "_id": doc_ids
                        }
                    },
                    {
                        "match": {
                            "content": "PChome"
                        }
                    }
                ]
            }
        },
        "sort": [
            {"count.comment": "desc"},
            {"posttime": {"order": "desc"}},
            "post.id"
        ],
        "from": 0,
        "size": 1000,
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
        }
    }

    es_resp2 = es_conn.search(index=["blog", "sm", "bbs", "news"], body=q2)
    data2 = es_resp2["hits"]["hits"]
    
    # Extract title and content from data
    res = []
    for item in data2:
        source = item.get('_source', {})
        title = source.get('title', '')
        content = source.get('content', '')
        res.append(f"{title}\n{content}")
    return res

# 執行第一次搜索並獲取文檔ID和數據
doc_ids, first_data = keypo_textlist()

# 基於第一次搜索的結果進行第二次搜索
cleaned_text_list = second_search_based_on_first_result(doc_ids)
print(len(cleaned_text_list))
c = 0
for item in cleaned_text_list:
    if "PChome" in item:
        c+=1

print(c)
