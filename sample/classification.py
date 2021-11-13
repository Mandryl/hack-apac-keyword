from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import pandas as pd
from copy import copy


# train parameter
train_shuffle_num = 10

# predict parameter
extract_top_category = 3


def svm_classification_train(X, y):

    print("---SVM classification training---")

    max_accuracy_test = 0
    for shuffle in range(train_shuffle_num):

      print("-Train shuffle{}-".format(shuffle+1))

      # train test split
      x_train, x_test, y_train, y_test, _, test_index = train_test_split(X, y, np.array(range(X.shape[0])), test_size=0.1, random_state=None, stratify=y)
      
      # train
      svc_model = SVC(C=10, kernel='rbf', random_state=1, probability=True)
      svc_model = OneVsRestClassifier(svc_model)
      svc_model.fit(x_train, y_train)

      # train data accuracy
      pred_train = svc_model.predict(x_train)
      accuracy_train = accuracy_score(y_train, pred_train)
      print("Train data accuracy: {:.2f}".format(accuracy_train))

      # test data accuracy
      pred_test = svc_model.predict(x_test)
      accuracy_test = accuracy_score(y_test, pred_test)
      print("Test data accuracy:  {:.2f}".format(accuracy_test))

      # choose best model
      if accuracy_test > max_accuracy_test:
        best_svc_model = svc_model
        best_model_x_test = x_test
        best_model_y_test = y_test
        best_model_test_index = test_index
        max_accuracy_train = accuracy_train
        max_accuracy_test = accuracy_test 

    print("[Best score] Train: {:.2f}, Test: {:.2f}".format(max_accuracy_train, max_accuracy_test))

    # test data predict probability with best model
    print("-Test data predict probability-")
    best_model_pred_test = best_svc_model.predict(best_model_x_test)
    best_model_pred_test_proba = best_svc_model.predict_proba(best_model_x_test)

    section_data_num = np.zeros(10)
    section_accuracy = np.zeros(10)
    cumulative_data_num = np.zeros(10)
    cumulative_accuracy = np.zeros(10)
    for index, target_prob in enumerate(np.linspace(0.9, 0.0, 10)):
      upper_prob = target_prob + 0.1
        
      # each section score
      section_data = (target_prob < np.max(best_model_pred_test_proba, axis=1)) & (np.max(best_model_pred_test_proba, axis=1) <= upper_prob)
      section_data_num[index] = np.count_nonzero(section_data)
      section_accuracy[index] = accuracy_score(best_model_y_test[section_data], best_model_pred_test[section_data])
        
      # cumulative score
      cumulative_data = (target_prob < np.max(best_model_pred_test_proba, axis=1))
      cumulative_data_num[index] = np.count_nonzero(cumulative_data)
      cumulative_accuracy[index] = accuracy_score(best_model_y_test[cumulative_data], best_model_pred_test[cumulative_data])

      print("Predict probability: {:.1f}-{:.1f}, Section data num: {:3.0f}({:3.0f}%), Section accuracy: {:.2f}, Cumulative data num: {:3.0f}({:3.0f}%), Cumulative accuracy: {:.2f}".format(target_prob, upper_prob, section_data_num[index], 100*section_data_num[index]/best_model_pred_test_proba.shape[0], section_accuracy[index], cumulative_data_num[index], 100*cumulative_data_num[index]/best_model_pred_test_proba.shape[0], cumulative_accuracy[index]))

    # top n category accuracy
    print("-Top n category accuracy-")
    best_model_pred_test_sorted = best_model_pred_test_proba.argsort(axis=1)[:, ::-1]
    best_model_pred_test_sorted_classlabel = np.empty((best_model_pred_test_sorted.shape[0], best_model_pred_test_sorted.shape[1]), dtype=object)

    for i in range(best_model_pred_test_sorted.shape[0]):
      for j in range(best_model_pred_test_sorted.shape[1]):
        best_model_pred_test_sorted_classlabel[i,j] = best_svc_model.classes_[best_model_pred_test_sorted[i,j]]

    cumulative_accuracy = 0
    for n in range(best_model_pred_test_sorted.shape[1]):
      accuracy = accuracy_score(best_model_pred_test_sorted_classlabel[:,n], best_model_y_test)
      cumulative_accuracy = cumulative_accuracy + accuracy
      print("Top{} category accuracy: {:.2f}, Cumulative accuracy: {:.2f}".format(n+1, accuracy, cumulative_accuracy))

    # each class reult
    print("-Each class result-")
    cumulative_accuracy = 0
    for category in set(best_model_y_test):
      print("Category: {}, Num: {}, Accuracy: {:.2f}".format(category, np.sum(best_model_y_test==category), accuracy_score(best_model_y_test[best_model_y_test==category], best_model_pred_test[best_model_y_test==category])))
      cumulative_accuracy += accuracy_score(best_model_y_test[best_model_y_test==category], best_model_pred_test[best_model_y_test==category])
    print("Category average accuracy: {:.2f}".format(cumulative_accuracy/len(set(best_model_y_test))))

    return best_svc_model, best_model_pred_test, best_model_test_index


def svm_classification_predict(X, pretrained_model):

    print("---SVM classification predict---")

    # predict
    predict_proba = pretrained_model.predict_proba(X)

    # sort with predict probability
    pred_sorted = np.sort(predict_proba, axis=1)[:, ::-1]
    pred_sorted_arg = predict_proba.argsort(axis=1)[:, ::-1]
    pred_sorted_classlabel = np.empty((pred_sorted_arg.shape[0], pred_sorted.shape[1]), dtype=object)
    for i in range(pred_sorted_arg.shape[0]):
      for j in range(pred_sorted_arg.shape[1]):
        pred_sorted_classlabel[i,j] = pretrained_model.classes_[pred_sorted_arg[i,j]]

    # make result dataframe 
    cols = []
    predict_df = pd.DataFrame(index=[], columns=[])

    for n in range(extract_top_category):
      target_rank_header = 'TopCategory{}'.format(n+1)
      target_rank_proba_header = 'TopCategory{} Probability'.format(n+1)

      predict_df[target_rank_header] = pred_sorted_classlabel[:,n]
      predict_df[target_rank_proba_header] = pred_sorted[:,n].round(decimals=3)      

    return predict_df

def rulebase_classification(X, fixed_classification_rules):

    cols = ['Text', 'Category']
    rulebase_classified_df = pd.DataFrame(index=[], columns=cols)
    rulebase_classified_df['Text'] = X
    rulebase_classified_df = rulebase_classified_df.reset_index()
    rulebase_classified_df['Category'] = None

    sum_count = {}
    for index, text in enumerate(X):
      for _, row in fixed_classification_rules.iterrows():
          result = [True if keyword in text else False for keyword in row['Keywordlist'].split(",")]
    
          if any(result):
            rulebase_classified_df['Category'][index] = row['Category']            
            
            if row['Category'] in sum_count:
              sum_count[row['Category']] += 1
            else:
              sum_count[row['Category']] = 1
            
            break

    print("Fixed rule calssification result: {}".format(sum_count))

    return rulebase_classified_df


def get_accuracy_score(y1, y2):
  score = accuracy_score(y1, y2)

  return score

from paramaters import *
from data_io import write_csv, read_object, save_object, read_fixedrule_csv
from feature_extraction import wakatigaki, extract_tfidf_feature
from classification import svm_classification_train, svm_classification_predict, rulebase_classification, get_accuracy_score
import pandas as pd
from copy import copy
from sklearn.cluster import KMeans
from numpy import *
# prepare train data
df = read_clustering_csv(clustering_input_path)
# extract tfidf feature
wakatigaki_data = wakatigaki(df['Text'])
features, trained_vec = extract_tfidf_feature(wakatigaki_data)
clusters = KMeans(n_clusters=15, random_state=0).fit_predict(features)
cls = pd.Series(clusters)
merged_df = pd.concat([df, cls], axis=1)
merged_df.columns = ["Text", "Cluster"]
write_csv(clustering_tfidf_path, merged_df)

