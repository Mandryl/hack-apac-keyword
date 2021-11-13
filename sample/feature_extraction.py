import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer

def wakatigaki(docs):
  
  wakatigaki_data = docs

  for i, doc in enumerate(docs):
    tagger = MeCab.Tagger('-Owakati')
    wakatigaki_data[i] = tagger.parse(str(doc))
    
  return wakatigaki_data
  

def extract_tfidf_feature(docs, pretrained_vec=None):

    print('---Extract TFIDF feature---')
    
    if pretrained_vec == None:  # train mode
      
      print('Mode: train')

      # tfidf vectolizaiton
      vec = TfidfVectorizer()
      trained_vec = vec.fit(docs)
      tfidf_feature = trained_vec.transform(docs)

      # train result
      print('Vocabulary size: {}'.format(len(vec.vocabulary_)))
      print('TFIDF feature shape(sample x feature): {}'.format(tfidf_feature.shape))

      return tfidf_feature, trained_vec

    else: # Predict mode
      
      print('Mode: predict')

      # tfidf vectolizaiton(use pretrained model)
      tfidf_feature = pretrained_vec.transform(docs)

      # predict result
      print('TFIDF features shape: {}'.format(tfidf_feature.shape))

      return tfidf_feature