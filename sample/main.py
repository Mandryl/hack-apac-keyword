from paramaters import *
from data_io import read_train_csv, read_predict_csv, write_csv, read_object, save_object, read_fixedrule_csv
from feature_extraction import wakatigaki, extract_tfidf_feature
from classification import svm_classification_train, svm_classification_predict, rulebase_classification, get_accuracy_score
import pandas as pd
from copy import copy

from sklearn.cluster import KMeans

mode = 'train'  # choose 'train' or 'predict'


if mode == 'train': # train mode

    # prepare train data 
    df = read_train_csv(train_input_path)
    
    # extract tfidf feature
    wakatigaki_data = wakatigaki(copy(df['Text']))
    features, trained_vec = extract_tfidf_feature(wakatigaki_data)


    kmeans_model = KMeans(n_clusters=10, verbose=1, random_state=42, n_jobs=-1)
    kmeans_model.fit(trained_vec)

    # train classification model
    category_label = copy(df['Category'])
    trained_classifier, pred_y, test_index = svm_classification_train(features, category_label)

    # show result of both rulebase classification and machine learning classification
    fixed_classification_rules = read_fixedrule_csv(fixedrule_data_path)
    rulebase_classified_df = rulebase_classification(df['Text'][test_index], fixed_classification_rules)

    merged_y = copy(pred_y)
    for index, row in rulebase_classified_df.iterrows():
        if row['Category'] is not None:
            merged_y[index] = row['Category']

    print("Only machine learning accuracy: {:.2f}".format(get_accuracy_score(category_label[test_index], pred_y)))
    print("Rulebase combination accuracy: {:.2f}".format(get_accuracy_score(category_label[test_index], merged_y)))

    # save trained feature and classification model
    save_object(train_model_save_path, trained_vec, trained_classifier)

else: # predict mode

    # prepare predict data
    df = read_predict_csv(predict_input_path)
    
    # APIから取得する
    # rulebase classification
    fixed_classification_rules = read_fixedrule_csv(fixedrule_data_path)
    rulebase_classified_df = rulebase_classification(df['Text'], fixed_classification_rules)

    # load pretrained model(feature and classifier)
    trained_vec, trained_classifier = read_object(pretrained_model_path)
    
    # extract tfidf feature
    wakatigaki_data = wakatigaki(df['Text'])
    features = extract_tfidf_feature(wakatigaki_data, trained_vec)
    
    # predict with pretrained_model 
    predict_df = svm_classification_predict(features, trained_classifier)
    
    # merge rulebase classification and machine learning classification result
    mergedresult_df = predict_df
    for index, row in rulebase_classified_df.iterrows():
        if row['Category'] is not None:
            mergedresult_df.loc[index, :] = ""
            mergedresult_df['TopCategory1'][index] = row['Category']
            mergedresult_df['TopCategory1 Probability'][index] = 1.0

    # output predict result
    merged_df = pd.concat([df, mergedresult_df], axis=1)
    write_csv(predict_output_path, merged_df)
