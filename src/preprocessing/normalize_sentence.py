from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


## 文字の正規化
def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    lemmatizer_sentence = []
    for word,tag in pos_tag(word_tokenize(sentence)):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatizer_sentence