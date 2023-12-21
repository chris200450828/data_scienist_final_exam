import openpyxl
import pandas as pd
import os


def list_create(keyword, url_lst):
    if url_lst != None:
        data = []
        for i in range(0, len(url_lst)):
            pair = (keyword, [url_lst[i]])
            data.append(pair)
        save_url_into_DataFrame(data)
    else:
        pass


def save_url_into_DataFrame(data_url):
    file = "url.xlsx"
    if os.path.isfile(file):
        # print("File exists,start remove the duplicated url")
        df = pd.read_excel("url.xlsx")
        if data_url != [] or data_url != None:
            new_df = pd.DataFrame(data_url)
            new_df.columns = ['keyword', 'url']
            new_df['url'] = new_df['url'].astype(str)
            new_df['url'] = new_df['url'].str.strip('[]').str.replace("'", "")  # remove []

            df = df.append(new_df, ignore_index=False)
            df = df.drop_duplicates()
            df = df.reset_index(drop=True)
            df.to_excel('url.xlsx', index=False)
            print("new url saved")
        else:
            return None
    else:
        # print("File does not exist, ", end='')
        df = pd.DataFrame(data_url)
        df.columns = ['keyword', 'url']
        df['url'] = df['url'].astype(str)
        df['url'] = df['url'].str.strip('[]').str.replace("'", "")  # remove []
        df.to_excel('url.xlsx', index=False)
        print("saved")


def pandas_df_converter():
    file = "url.xlsx"
    if os.path.isfile(file):
        # print("File exists,start remove the duplicated url") # for debug perpose
        df = pd.read_excel("url.xlsx")
        url_list = df['url'].tolist()
    return url_list


def file_exist_cheker():
    file = "url.xlsx"
    if os.path.isfile(file):
        print("File exists,start remove the duplicated url")
        return True
    else:
        return False
