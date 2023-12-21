import selenium_search
import url_save

google_url = "https://www.google.com.tw/"
test_url = "https://www.gender.ey.gov.tw/gecdb/Stat_Statistics_DetailData.aspx?sn=nLF9GdMD%2B%2Bv41SsobdVgKw%3D%3D&d=x6hHAJy%2F6kd5%2FI2WaRjP4Q%3D%3D"
test = selenium_search.search(3, google_url)

# test.search_pdf_exist()
# test.search_pdf_exist()

search_keyword_base = ["癌症", "cancer"]
search_keyword_add = ["發生機率", " probability of occurrence", "機率統計", " probability statistics", "種類機率",
                      " type probability", "個案存活機率", " case survival rate"]
search_lst = test.keyword_mix(search_keyword_base, search_keyword_add)
print(search_lst)
exe_time = len(search_lst)
# print(exe_time) # total of 32 keywords
#
# test_skw_b = ["癌症"]
# test_skw_a = ["發生機率"]
# test_sealst = test.keyword_mix(test_skw_b, test_skw_a)
# test_exet = len(test_sealst)
# # print(test_sealst)
#
#
def keyword_sea(kw):
    print("the file is exist or not:", end='')
    print(url_save.file_exist_cheker())

    test.keyword_seacrh(kw)
    url_lst = test.enumerate_all_websites()
    print(url_lst)
    url_save.list_create(kw, url_lst)
    durl = test.data_exist(url_lst)
    print(durl)


for exe_time, kw in enumerate(search_lst):
    print("start searching {}".format(kw))
    keyword_sea(kw)
    test.search_looper(google_url)
