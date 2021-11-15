from src.preprocessing.language_check import is_japanese_check
from src.preprocessing.noise_remove import noise_format
from src.preprocessing.normalize_sentence import lemmatize_sentence
from src.preprocessing.data_io import read_dict_csv
from src.out_json import create_keyword_json
from src.paramaters import *
def extract_keyword(inputdata):
    # Lunguage Detection
    lang_flg = is_japanese_check(inputdata)

    # Japanese(Error) 
    if lang_flg == True:
        return {'message': 'Error：It contained a language other than English.'}
        
    # English
    else:
        en_index = []
        jp_out_data = []

        # Get Keyword Dictionary
        dict_readcsv = read_dict_csv(DICT_PATH,0,1,2)
        english_data = [i.replace('\xa0', '')for i in dict_readcsv.English.tolist()]
        japanese_data = [i.replace('\xa0', '')for i in dict_readcsv.Japanese.tolist()]

        # PreProcessing
        clearndata = noise_format(inputdata)
        lemmatizedata = lemmatize_sentence(clearndata)
        tokens_l = [w.lower() for w in lemmatizedata]
        
        # English Extract Keyword(Intersection 'AND')
        en_out_data = set(tokens_l) & set(english_data)
        en_out_data = list(en_out_data)
        for i in en_out_data:
            en_index.append(english_data.index(i))
        
        # Japanese Extract Keyword
        for i in en_index:
            jp_out_data.append(japanese_data[i])
        
        # Result Json Create
        resultjson = create_keyword_json(jp_out_data,en_out_data)

        return resultjson
