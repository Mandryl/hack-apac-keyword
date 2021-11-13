# ファイル参照
from preprocessing.language_check import is_japanese
from preprocessing.nltk_download_list import nltk_download_lise
from preprocessing.noise_remove import noise_format
from preprocessing.data_io import read_dict_csv
from preprocessing.normalize_sentence import lemmatize_sentence
from paramaters import *

# 外部モジュール
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tag import pos_tag

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
    print(en_out_data)

    # Result(結果)
    for i in en_out_data:
        en_index.append(english_data.index(i))

    for i in en_index:
        jp_out_data.append(japanese_data[i])
    print(jp_out_data)
