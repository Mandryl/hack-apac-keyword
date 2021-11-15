# Local Module
from src.preprocessing.language_check import is_japanese
from src.preprocessing.nltk_download_list import nltk_download_lise
from src.preprocessing.noise_remove import noise_format
from src.preprocessing.data_io import read_dict_csv
from src.preprocessing.normalize_sentence import lemmatize_sentence
from paramaters import *
from api.get_news_api import get_newsapi_everything, get_newsapi_sources,newsapi_check_json
from api.deepl_api import translate
from src.out_json import out_create_json,remove_json

# External Module
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tag import pos_tag
import json, copy,sys,re


def extract_keyword_articlesearch(inputdata):

    ## Inputデータから分かち書き
    nltk_download_lise()
    inputdata ="Hello,I've had a trouble with my daily life because the amount of time I spend with my family increased due to coronavirus. Actually, my father, Kazuki, has behaved violently to me. After drinking,  he always come into my room and give me a shout. Nowadays even though he don't get drunk, he messes with me. If my behaviour is unfavorable, he punches and kicks me. I hope that the days like before could come back to us and I could go back to school as soon as possible. Help me."

    ## 日本語判定
    lang_flg = is_japanese(inputdata)

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
        for i in en_out_data:
            if(resultstr==''):
                resultstr = i
            else:
                resultstr = resultstr + ' And ' + i 
        
        testresultstr = 'intimidate'

        # NewsAPI 
        # everythingdata = get_newsapi_everything(testresultstr,NEWS_APIKEY,NEWS_EVERYTHING_DOMAIN,'jp')
        # sourcedata = get_newsapi_sources('source', NEWS_APIKEY, NEWS_COUNTRY)

        # テスト用のサンプル
        json_open_ja = open('data/newsapi/' + testresultstr + '.json', 'r')
        everythingdata_ja = json.load(json_open_ja)
        json_open_en = open('data/newsapi/' + testresultstr + '.json', 'r')
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
            deepl_text =  author + '\n' + description + '\n' + title
            result_text = translate(deepl_text,DEEPL_APIKEY,t_lang="JA")
            list_text = result_text['translations'][0]['text'].splitlines()
            
            articledata_en[i]['author'] = list_text[0]
            articledata_en[i]['description'] = list_text[1]
            articledata_en[i]['title'] = list_text[2]
        articledata_en = r'{ "keyword":' + str(articledata_en)+ r"}"
        parttern = re.compile(r"(<([^>]+)>)")
        text = parttern.sub('',str(articledata_en))
        text = text.replace("'",'"')

        keyFormat = json.loads(text)

        # sys.exit(1)
        # articledata_en['articles'] = articledata_en.pop('articles','')
        # # hoge = translate("The PC enthusiast's resource. Power users and the tools they love, without computing religion.", )
        outputjson = out_create_json(jp_out_data,en_out_data,articledata_jp['articles'],keyFormat)
        