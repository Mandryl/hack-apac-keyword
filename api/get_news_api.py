from newsapi import NewsApiClient
import json,os

def get_newsapi_everything(keyword,newsapi_key,countryname="",domainname=""):
    newsapi = NewsApiClient(api_key='97e1a5c542ad46548c5a75d0ee4603d1')
    if countryname=="" and domainname=="":
        all_articles = newsapi.get_everything(q=keyword,
                                      sort_by='relevancy'
        )   
    elif countryname == "" and not domainname=="":
        domain_join = ','.join(domainname)
        all_articles = newsapi.get_everything(q=keyword,
                                        sort_by='relevancy',
                                        domains= domain_join
                                        )
        # domains='cnn.com,nikkei.com/'
    elif not countryname == "" and not domainname=="":
        all_articles = newsapi.get_everything(q=keyword,
                                        sort_by='relevancy',
                                        country=countryname
                                        )
    ## ドメインと国が両方入っている場合
    else:
        domain_join = ','.join(domainname)
        all_articles = newsapi.get_everything(q=keyword,
                                        sort_by='relevancy',
                                        country=countryname,
                                        domains=domain_join,
                                        )

    with open('data/newsapi/'+ keyword+ '.json', 'w') as f:
        json.dump(all_articles, f, indent=2,ensure_ascii=False)
    return all_articles

def get_newsapi_sources(jsonfile,newsapi_key,countryname=""):
    newsapi = NewsApiClient(api_key='97e1a5c542ad46548c5a75d0ee4603d1')
    if countryname =="":
        sourcesdata = newsapi.get_sources()
        sourcefile = jsonfile+ "_all.json"
    else:
        sourcesdata = newsapi.get_sources(country=countryname)
        sourcefile = jsonfile+ "_" + countryname + ".json"

    ## source json output
    with open('data/newsapi/'+ sourcefile, 'w') as f:
        json.dump(sourcesdata, f,indent=2, ensure_ascii=False)
    return sourcesdata

## jsonの結果確認
def newsapi_check_json(jsondata):
    empty_json :dict = {}
    try:
        if jsondata['totalResults']=='0':
            print("The number of hits was zero.")
            return empty_json
        else:
            return jsondata
    except:
        print('Error:API側の制限が超えました。確認してください。')
    return 

## Sourceの利用記事
# def source_select_article():
    

# with open('/Users/sakamotokazuki/workspace/openshift-hack/'+ keyword + '.json', 'w') as f:
#     json.dump(top_headlines, f, ensure_ascii=False)

# /v2/everything
# all_articles = newsapi.get_everything(q=keyword,
#                                       sort_by='relevancy',
#                                       domains='cnn.com,nikkei.com/',
#                                       country='jp'
#                                      )

# /v2/top-headlines/sources
# sources = newsapi.get_sources()
