import urllib.parse as prs
from operator import itemgetter
import os

import json
import pandas as pd

# file1 = 'JS-2-prod.txt'
# file2 = 'JS-2-staging.txt'

def create_parsed_dicts(file):
    """Parse file and create list of dictionaries of url parameters, if key 'pageName' is present"""
    req = []
    firstlines = []
    parsed_urls = []
    with_pageName_urls = []

    with open(file) as json_file:
        data = json.load(json_file)
        for p in data:
            req.append(p['request'])

    for k in req:
        firstlines.append(k['header']['firstLine'])

    for l in firstlines:
        parsed_urls.append(prs.parse_qs(l))

    for m in parsed_urls:
        for k,v in m.items():
            m[k] = "".join(v)

    for p in parsed_urls:
        if p.get('pageName'):
            with_pageName_urls.append(p)



    return with_pageName_urls

def convert_to_dataframe(parsed_dicts):
    """Converts list of dictionaires to pandas Dataframe"""
    df = pd.DataFrame.from_records(parsed_dicts)
    return df

def convert_to_excel(df, file_name):
    """Converts Pandas DataFrame to Excel readable format"""
    df_excel = df.to_excel(file_name)
    return df_excel

def convert_from_chls_to_txt(file_name):
    head, sep, tail = file_name.partition('.')
    json_friendly = os.rename(file_name, head + '.txt')
    return head




def main():
    print("")
    print("")
    print("--------------------------PLEASE READ BEFORE MOVING FORWARD------------------------------------")
    print("Please be sure you have converted the session chls file to chlsj session format first and also")
    print("be sure that the PRODUCTION and STAGING .chlsj files are in the same folder as this python")
    print('program. Thank You.')
    print("-----------------------------------------------------------------------------------------------")
    print("")
    print("")
    file1 = input('Please enter the name of the PRODUCTION chslj file you want to read: ')
    file2 = input('Please enter the name of the STAGING chslj file you would like to read: ')

    prod_xlsx_name = input('Please enter the xlsx file name you would like to create after reading the PRODUCTION file: ')
    staging_xlsx_name = input('Please enter the xlsx file name you would like to create after reading the STAGING file: ')

    try:
        json_txt_prod = convert_from_chls_to_txt(file1)
        json_txt_prod = json_txt_prod + '.txt'
        json_txt_staging = convert_from_chls_to_txt(file2)
        json_txt_staging = json_txt_staging + '.txt'
    except:
        print("There is something wrong with the chls file")

    prod = create_parsed_dicts(json_txt_prod)
    staging = create_parsed_dicts(json_txt_staging)

    df_prod = convert_to_dataframe(prod)
    df_staging = convert_to_dataframe(staging)

    prod_excel = convert_to_excel(df_prod, prod_xlsx_name)
    staging_excel = convert_to_excel(df_staging, staging_xlsx_name)


if __name__ == "__main__":
    main()