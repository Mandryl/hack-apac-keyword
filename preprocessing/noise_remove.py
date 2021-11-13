import re, string
## ノイズ除去
def noise_format(sentence):
    # ーーー＠の後に任意の数の数字、文字や_が続くものを削除
    normalizetext=''
    normalizetext=re.sub('(@[A-Za-z0-9_]+)','', sentence)
    normalizetext= normalizetext.translate(str.maketrans('', '', string.punctuation))
    return normalizetext