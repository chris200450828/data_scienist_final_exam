from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import requests
import url_save

download_dir = r"C:\Users\陳昱辰\PycharmProjects\hw\venv\data_ana"
prefs = {
    "download.default_directory": download_dir,  # Set default download directory
    "download.prompt_for_download": False,  # Don't prompt for download
    "download.directory_upgrade": True,  # Use the native download dialog
    "plugins.always_open_pdf_externally": True  # Always open PDFs externally
}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)  # Add preferences to options
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_experimental_option("detach", True)  # Prevent Chrome from closing when script finishes
driver = webdriver.Chrome(options=options)  # Initialize Chrome driver with options
driver.implicitly_wait(5)


class search:
    def __init__(self, wait_time, url, pdf_count=0, excel_count=0, window_open_statue=False):
        self.url = url  # getting the browser url
        self.window_open_statue = window_open_statue  # check for the window is opened or not
        self.wait_time = wait_time  # wait time of every action
        self.pdf_count = pdf_count  # total pdf count
        self.excel_count = excel_count  # total excel count
        driver.get(self.url)  # set the url and each wait time of action

    def wait(self):
        return WebDriverWait(driver, self.wait_time)  # wait function

    def keyword_seacrh(self, text):
        search = self.wait().until(EC.visibility_of_element_located((By.CLASS_NAME, 'gLFyf')))
        search.send_keys(text)
        search.send_keys(Keys.ENTER)  # search bar in google.com

    def keyword_mix(self, base, add):
        search_list = []  # setting the result list
        opendata_list = ["", " opendata"]  # add 'opendata' to every keyword
        result = ""

        for first in base:
            for second in add:
                for opendata_text in opendata_list:
                    result = first + second + opendata_text  # keyword mix
                    search_list.append(result)
                    result = ""

        return search_list  # mix the keyword to search

    def search_pdf_exist(self):
        try:
            pdf = self.wait().until(EC.presence_of_all_elements_located(
                (By.XPATH, '//a[contains(@href, ".pdf")]')))  # search '//a' in hyperlink that has '.pdf' text
            if len(pdf) > 0:
                # print("pdf file founded, by ", end='') # for debug purpose, show the length of pdf
                for pfile in pdf:
                    self.pdf_count += 1
                    # print(pfile)
                    file_url = pfile.get_attribute('href')
                    self.pdf_downloader(file_url)
                    # print(file_url)# for debug purpose, show the pdf url
                # for pdfs in pdf:
                #     print(pdfs.get_attribute('href'))  #  debug purpose, show the pdf link
                return True
            else:
                return False
        except TimeoutException as Timeouterr:
            return  # print("Timeout:PDF file not found during wait time.") # for debug purpose, if the script catch a pdf it will pop
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def search_xlsx_exist(self):
        try:
            excel_files = self.wait().until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     '//a[contains(@href, ".xlsx") or contains(@href, ".xls") or contains(@href, ".xlsm") or contains(@href, ".ods") or contains(@href, ".csv")]')))
            if len(excel_files) > 0:
                print("Excel file(s) found, by ", end='')
                for excel in excel_files:
                    file_url = file.get_attribute('href')
                    self.excel_downloader(file_url)
                    # print(file_url)
                for file in excel_files:
                    print(file.get_attribute('href'))  # show the excel link
                return True
            else:
                return False
        except TypeError as excel_TE:
            print("List object might be None, caused by Excel searcher")
        except TimeoutException as Timeouterr:
            return  # print("Timeout:Excel file not found during wait time.")
        except Exception as RE:
            print("Unexpected error")

    def enumerate_all_websites(self):
        result_lst = []
        search_result_lst = self.wait().until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MjjYud"]//a')))  # get all the search url
        for link in search_result_lst:
            url = [link.get_attribute('href')]  # this will make the list into two dimension
            # print(url)  # for debug purpose, show the url catched
            if 'https://www.google.com.tw/search' not in url[0]:  # trash remover, remove the keyword getting add ""
                if url_save.file_exist_cheker() == True:
                    url = [i for i in url if
                           i not in url_save.pandas_df_converter()]  # remove the duplicated url from url.xlsx
                else:
                    pass
                result_lst.append(url)
            else:
                pass
        result_lst = list(filter(None, result_lst))  # remove the empty list index
        if not result_lst:
            print("url is empty")
        else:
            print('the url isnt empty {}'.format(result_lst))
            return result_lst  # if result_lst isnt empty then return

    def data_exist(self, url):
        if url != None:
            data_url = []
            for i in range(0, len(url)):
                detect_url = url[i][0]
                self.window_open(detect_url)
                print("process({}/{})".format(i, len(url)))  # show the process
                if self.search_pdf_exist() == True or self.search_xlsx_exist() == True:  # check if the pdf catcher find pdf
                    data_url.append(detect_url)
                    print(detect_url)
                else:
                    pass
                self.window_close()
            return data_url
        else:
            pass

    def pdf_downloader(self, file_url):
        response = requests.get(file_url)  # getting the pdf url
        filename = str(self.pdf_count) + '.pdf'  # setting the file name using the data amount
        with open(os.path.join(download_dir, filename), 'wb') as f:
            f.write(response.content)  # open a file in binary mode and write it as binary ('wb')
        # print(f"File downloaded: {file_url.split('/')[-1]}")

    def excel_downloader(self, file_url):
        response = requests.get(file_url)
        if '.xlsx' in file_url:
            filename = str(self.excel_count) + '.xlsx'
        elif '.xls' in file_url:
            filename = str(self.excel_count) + '.xls'
        elif '.xlsm' in file_url:
            filename = str(self.excel_count) + '.xlsm'
        elif '.csv' in file_url:
            filename = str(self.excel_count) + '.csv'
        elif '.osd' in file_url:
            filename = str(self.excel_count) + '.ods'
        with open(os.path.join(download_dir, filename), 'wb') as f:
            f.write((response.content))

    def search_looper(self, google_url):
        driver.get(google_url)

    def window_open(self, url):
        num_window = len(driver.window_handles)
        driver.execute_script("window.open('" + url + "');")
        if num_window == 2:  # prevent .pdf website crashing the script equal 2 means the window is opened and didnt close and make sure the window is opened properly
            driver.switch_to.window(driver.window_handles[-1])  # open the tab and switch to the last tab handle
            self.window_open_statue = True  # set the window is opened or not
        else:
            pass

    def window_close(self):
        num_window = len(driver.window_handles)
        # print("there are {} windows".format(num_window))
        if num_window >= 2:  # prevent .pdf website crashing the script bigger or equal to 2 means the window is opened and didnt close and make sure the window is opened properly
            try:
                driver.close()
                self.window_open_statue = False  # set the window is opened or not
                driver.switch_to.window(driver.window_handles[0])  # switch to the '0' window
            except Exception as E:
                print(f"An error occurred: {e}")
        else:
            pass
