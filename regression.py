import urllib.parse as prs
from shutil import copyfile
from operator import itemgetter
import os

import json
import pandas as pd

# file1 = 'JS-2-prod.txt'
# file2 = 'JS-2-staging.txt'

list_of_keys1 = ['pageName', 'channel', 'prevPageName', 'pageView', 'webVersion', 'templateType', 'pageSeries', 'franchise', 'pageSeries', 'playerVersion', 'pageType', 'pageEvent', 'pageURL', 'brandID']


def create_parsed_dicts(file, list_of_var=None):
    """Parse file and create list of dictionaries of url parameters, if key 'pageName' is present"""
    req = []
    firstlines = []
    parsed_urls = []
    with_pageName_urls = []
    # list_of_keys = ['pageName', 'channel', 'prevPageName', 'pageView', 'webVersion', 'templateType', 'pageSeries', 'franchise', 'pageSeries', 'playerVersion', 'pageType', 'pageEvent', 'pageURL', 'brandID']
    list_of_keys = ['activity', 'appName' , 'authSuiteID', 'coppa', 'epmgid', 'offlineMode', 'profileID', 'pv', 'regStatus', 'subscriptionID', 'subscriptionSKU', 'subscriptionStatus', 'tveUsrStat', 'timeSpent', 'TimeStamp', 'authSuiteModalName', 'tvemvpd', 'tvestep', 'videptitle', 'vidfranchise']
    lower_list_of_keys = [i.lower() for i in list_of_keys]
    specified_key_list_of_dicts = []

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
        p = {k.lower(): v for k,v in p.items()}
        specified = {}
        index = [ky for ky,va in p.items() if ky.startswith('get')]
        for k in lower_list_of_keys:
            specified.update({k: p.get(k, p.get(k, "Not Present"))})
        specified_key_list_of_dicts.append({"call": index[0], "p": specified})

    return specified_key_list_of_dicts

def convert_to_dataframe(parsed_dicts, list_of_keys):
    """Converts list of dictionaires to pandas Dataframe"""
    def flatten(kv, prefix=[]):
        for k, v in kv.items():
            if isinstance(v, dict):
                yield from flatten(v, prefix+[str(k)])
            else:
                if prefix:
                    yield '_'.join(prefix+[str(k)]), v
                else:
                    yield str(k), v

    # columns = []
    # indices = [v.keys() for k,v in parsed_dicts[0].items()]
    # print(type(indices))
    # for i in parsed_dicts:
    #     column = [ky for ky, va in i.items() if ky.startswith('get')]
    #     columns.append(column[0])

    # print(indices)
    df = pd.DataFrame({k:v for k, v in flatten(kv)} for kv in parsed_dicts)
    return df

def convert_to_excel(df, file_name):
    """Converts Pandas DataFrame to Excel readable format"""
    df_excel = df.to_excel(file_name)
    return df_excel

def convert_from_chls_to_txt(file_name):
    head, sep, tail = file_name.partition('.')
    copyfile(file_name, head + '.txt')
    # json_friendly = os.rename(file_name, head + '.txt')
    return head + '.txt'




def regression():
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


def spec_compare():
    print("")
    print("")
    print("--------------------PLEASE READ BEFORE MOVING FORWARD----------------------------------------")
    file1 = 'WEBPLEX-7091.chlsj'
    file_converted = convert_from_chls_to_txt(file1)
    parsed = create_parsed_dicts(file_converted)    # print(parsed[0])
    lower_list_of_keys = list(parsed[0].keys())
    # print(parsed[0])
    # return
    print(parsed)
    df = convert_to_dataframe(parsed, lower_list_of_keys)
    # return
    convert_to_excel(df, 'tester.xlsx')
    # param = list_of_keys[0]
    # df.pivot(index='')
    # print(df)


def main():
    program_to_run = input("(1)REGRESSION or (2)SPEC COMPARE: ")
    if program_to_run == '1':
        print("")
        regression()
    elif program_to_run == '2':
        spec_compare()
if __name__ == "__main__":
    program_to_run = input("(1)REGRESSION or (2)SPEC COMPARE: ")
    if program_to_run == '1':
        print("")
        regression()
    elif program_to_run == '2':
        spec_compare()