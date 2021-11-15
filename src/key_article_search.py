# Local Module
from src.preprocessing.language_check import is_japanese_check
from src.preprocessing.nltk_download_list import nltk_download_lise
from src.preprocessing.noise_remove import noise_format
from src.preprocessing.data_io import read_dict_csv
from src.preprocessing.normalize_sentence import lemmatize_sentence
from src.paramaters import *
from src.get_news_api import get_newsapi_everything, get_newsapi_sources,newsapi_check_json
from src.deepl_api import translate
from src.out_json import out_create_json,remove_json

# External Module
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tag import pos_tag
import json, copy,sys,re
import os,shutil



def extract_keyword_articlesearch(inputdata):
    target_folder = 'data/newsapi/'
    shutil.rmtree(target_folder)
    os.mkdir(target_folder)
        
    ## Inputデータから分かち書き
    nltk_download_lise()
    
    ## 日本語判定
    lang_flg = is_japanese_check(inputdata)

    ## Japanese Detection
    if lang_flg == True:
        output_data = {"Error：It contained a language other than English."}

    ## English Detection
    else:
        
        # PreProcessing
        predata = noise_format(inputdata)
        lemmatizedata = lemmatize_sentence(predata)
        tokens_l = [w.lower() for w in lemmatizedata]
        dict_readcsv = read_dict_csv(DICT_PATH,0,1,2)
        english_data = [i.replace('\xa0', '')for i in dict_readcsv.English.tolist()]
        japanese_data = [i.replace('\xa0', '')for i in dict_readcsv.Japanese.tolist()]

        # Prepare(照合処理-積集合)
        en_index = []
        jp_out_data = []
        en_out_data = set(tokens_l) & set(english_data)
        en_out_data = list(en_out_data)

        # Result(結果)
        for i in en_out_data:
            en_index.append(english_data.index(i))

        for i in en_index:
            jp_out_data.append(japanese_data[i])
        
        # 文字列作成
        resultstr = ''
        for i in jp_out_data:
            if(resultstr==''):
                resultstr = i
            else:
                resultstr = resultstr + ' OR ' + i 
        
        # NewsAPI 
        everythingdata = get_newsapi_everything(resultstr,NEWS_APIKEY,'',NEWS_EVERYTHING_DOMAIN)
        # sourcedata = get_newsapi_sources('source', NEWS_APIKEY, NEWS_COUNTRY)

        # テスト用のサンプル
        json_open_ja = open('data/newsapi/' + everythingdata[1] + '.json', 'r')
        everythingdata_ja = json.load(json_open_ja)
        json_open_en = open('data/newsapi/' + everythingdata[1] + '.json', 'r')
        everythingdata_en = json.load(json_open_en)
        
        # Json Check
        everythingdata_ja = newsapi_check_json(everythingdata_ja)
        everythingdata_en = newsapi_check_json(everythingdata_en)

        articledata_en = remove_json(everythingdata_ja,False)
        articledata_jp = remove_json(everythingdata_en,True)
        
        # sourcedata = newsapi_check_json(sourcedata)
        articledata_en = articledata_en['articles']
        # DeepLのAPI
        for i in range(len(articledata_en)):
            author = articledata_en[i]['author']
            description=articledata_en[i]['description']
            title=articledata_en[i]['title']
            if(str(author) == "None"):
                author = "None_empty"
            deepl_text =  str(author) + '\n' + str(description) + '\n' + str(title)
            result_text = translate(deepl_text,DEEPL_APIKEY,t_lang="JA")
            list_text = result_text['translations'][0]['text'].splitlines()
            articledata_en[i]['author'] = str(list_text[0])
            articledata_en[i]['description'] = list_text[1]
            articledata_en[i]['title'] = list_text[2]
        articledata_en = r'{ "keyword":' + str(articledata_en)+ r"}"
        parttern = re.compile(r"(<([^>]+)>)")
        text = parttern.sub('',str(articledata_en))
        text = text.replace("'",'"')
        text = text.replace("None", '"None_empty"')
        text = text.replace('""None_empty"_empty"', '"None_empty"')
        keyFormat = json.loads(text)
        # sys.exit(1)
        # articledata_en['articles'] = articledata_en.pop('articles','')
        # # hoge = translate("The PC enthusiast's resource. Power users and the tools they love, without computing religion.", )
        outputjson = out_create_json(jp_out_data,en_out_data,articledata_jp['articles'],keyFormat)
        print(outputjson)
    return outputjson
