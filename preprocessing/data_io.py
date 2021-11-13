import pandas as pd

## 辞書の読み込み
def read_dict_csv(path, jp_column, en_column,category_column):
    df = pd.read_csv(path)
    df = df.iloc[:,[jp_column,en_column, category_column, ]]
    df.columns = ["Text", "English","Japanese"]
    return df