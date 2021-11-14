import json
from os import linesep
def out_create_json(keyword_jp:list,keyword_en:list,article_jp,article_en):
    createjson = r'{ "keyword":[ {'
    tmpjson = ""
    count = 0
    keyword_length = len(keyword_jp)
    
    # Keyword
    for i in keyword_jp:
        createjson = createjson + r'"id":"' + str(count + 1) + r'",'
        createjson = createjson + r'"keyword_jp":"' + i + r'",'
        createjson = createjson + r'"keyword_en":"' + keyword_en[count] + r'"'
        if(keyword_length==count + 1):
            createjson = createjson + r"}]," 
        else:
            createjson = createjson + r"},{"
        count = count + 1
    createjson = createjson + r'"articles":['
        
    # Article
    count = 0
    # print(article_en)
    for i in article_en['keyword']:
        createjson = createjson + r"{"
        createjson = createjson + r'"source":' + str(i['source']).replace("'", '"') + r","

        # jp
        createjson = createjson + r'"transrate_en":{'
        createjson = createjson + r'"title":"' + article_jp[count]['title'] + r'",'
        createjson = createjson + r'"description":"' + str(article_jp[count]['description']) + r'",'
        createjson = createjson + r'"url":"' + article_jp[count]['url'] + r'"'
        createjson = createjson + r"},"

        # en
        createjson = createjson + r'"original":{'
        createjson = createjson + r'"title":"' + i['title'] + r'",'
        createjson = createjson + r'"description":"' + i['description'] + r'",'
        createjson = createjson + r'"url":"' + i['url'] + r'"'
        createjson = createjson + r"}"
        count = count + 1

        # 最終行
        if(count == len(article_en['keyword'])):
            createjson = createjson + r"}"
        else:
            createjson = createjson + r"},"
    
    createjson = createjson + r"]}"
    return createjson


def remove_json(newsjsondata:dict,translate_flg:bool):
    #  print(jsondata['articles'][0]['publishedAt'])
    for i in range(len(newsjsondata['articles'])):
        del newsjsondata['articles'][i]['publishedAt']
        del newsjsondata['articles'][i]['content']
        del newsjsondata['articles'][i]['urlToImage']
        if(translate_flg):
            del newsjsondata['articles'][i]['source']
    with open('data/newsapi/test1.json', 'w') as f:
        
        json.dump(newsjsondata, f, indent=2,ensure_ascii=False)
    return newsjsondata


def create_keyword_json(keyword_jp:list,keyword_en:list):
    createjson = r'{ "keyword":[ {'
    count = 0
    keyword_length = len(keyword_jp)

    for i in keyword_jp:
        createjson = createjson + r'"id":"' + str(count + 1) + r'",'
        createjson = createjson + r'"keyword_jp":"' + i + r'",'
        createjson = createjson + r'"keyword_en":"' + keyword_en[count] + r'"'
        if(keyword_length==count + 1):
            createjson = createjson + r"}]" 
        else:
            createjson = createjson + r"},{"
        count = count + 1
    
    createjson = createjson + r'}'
    keyFormat = json.loads(createjson) # String-->json convert 
    outputjson = json.dumps(keyFormat,indent=2, ensure_ascii=False)# Formatting
    
    return outputjson