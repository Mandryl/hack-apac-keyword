import pandas as pd
import numpy as np
import pickle

def read_train_csv(path, text_column=0, category_column=1):
    df = pd.read_csv(path)

    df = df.iloc[:,[text_column, category_column]]
    df.columns = ["Text", "Category"]
    print(df["Category"].value_counts())

    return df


def read_predict_csv(path, text_column=0):
    with open(path, mode="r", encoding="shift-jis", errors="ignore") as f:
        df = pd.read_csv(f)

    df = df.iloc[:,[text_column]]
    df.columns = ["Text"]

    return df

def read_fixedrule_csv(path, category_column=0, keyword_list_column=1):
    df = pd.read_csv(path)

    df = df.iloc[:,[category_column, keyword_list_column]]
    df.columns = ["Category", "Keywordlist"]

    return df


def write_csv(path, df):
    with open(path,mode="w", encoding="shift-jis", errors="ignore", newline="") as f:
        df.to_csv(f, index=False)


def read_object(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)

    return obj


def save_object(path, *args):
    with open(path, "wb") as f:
        pickle.dump(args, f)