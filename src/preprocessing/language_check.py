import re

## 日本語判定
def is_japanese_check(str):
    return True if re.search(r'[ぁ-んァ-ン]', str) else False 