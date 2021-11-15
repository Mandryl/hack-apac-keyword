import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

# with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json') as j:
#     config = json.load(j)

DEEPL_TRANSLATE_EP = 'https://api-free.deepl.com/v2/translate'
DEEPL_TRANSLATE_EP = 'https://api-free.deepl.com/v2/translate'
T_LANG_CODES = ["DE", "EN", "FR", "IT", "JA", "ES",
                "NL", "PL", "PT-PT", "PT-BR", "PT", "RU", "ZH"]
S_LANG_CODES = ["DE", "EN", "FR", "IT",
                "JA", "ES", "NL", "PL", "PT", "RU", "ZH"]

def translate(text,api_key,s_lang='',t_lang='JA'):
    
    # check paramater
    if t_lang not in T_LANG_CODES:
        print((
            f'ERROR: Invalid target language code "{t_lang}". \n'
            f'Alloed lang code are following. \n{str(T_LANG_CODES)}'
        ))
        sys.exit(1)

    if s_lang != '' and s_lang not in S_LANG_CODES:
        print((
            f'WARNING: Invalid source Language code "{s_lang}". \n'
            'The source language is automatically determined in this request. \n'
            f'Allowed source lang code are following. \n{str(S_LANG_CODES)} \n\n'
        ))
        s_lang = ''

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; utf-8'
    }

    params = {
        'auth_key': api_key,
        'text': text,
        'target_lang': t_lang
    }

    if s_lang != '':
        params['source_lang'] = s_lang

    req = urllib.request.Request(
        DEEPL_TRANSLATE_EP,
        method='POST',
        data=urllib.parse.urlencode(params).encode('utf-8'),
        headers=headers
    )
    dump_json =''
    res_json :dict = {}

    try:
        with urllib.request.urlopen(req) as res:
            res_json = json.loads(res.read().decode('utf-8')) 
            # dump_json = json.dumps(res_json, indent=2, ensure_ascii=False)   
    except urllib.error.HTTPError as e:
        print("error:" + e)

    with open("../data/test.json", 'w') as f:
        json.dump(res_json,f,indent=2,ensure_ascii=False)

    return res_json

