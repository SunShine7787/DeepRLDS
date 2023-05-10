import os
import curl
import wget
import pandas as pd
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.util import converter,concat_csv
option = webdriver.ChromeOptions()
# I use the following options as my machine is a window subsystem linux.
# I recommend to use the headless option at least, out of the 3
# option.add_argument('--headless')
# option.add_argument('--no-sandbox')
# option.add_argument('--disable-dev-sh-usage')
option.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
# option.add_argument('Referer="https://admetmesh.scbdd.com/service/evaluation/cal"')
# option.add_argument("--proxy-server=http://120.71.147.222:8901")

# Replace YOUR-PATH-TO-CHROMEDRIVER with your chromedriver location
driver = webdriver.Chrome('chromedriver.exe', options=option)
path=sys.args[0]
result_dir=path+"result/"
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
for i,file_name in enumerate(os.listdir(path)):
    if file_name.__contains__("mol2"):
        mol2_file=path+'/'+file_name
        smi_str=converter(mol2_file)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        driver.get('https://admetmesh.scbdd.com/service/evaluation/index')  # Getting page HTML through request
        driver.find_element_by_id("smiles").send_keys(smi_str)

        driver.find_element_by_id("submit-btn-1").click()
        pageSource=driver.page_source

        print(type(pageSource))
        print(pageSource)
        page_url=pageSource.split("data: {\'csv_filename\': \"/")[1].split("\"},")[0]
        page_concat_url="https://admetmesh.scbdd.com/"+page_url
        result_path=result_dir+file_name.split(".mol2")[0]+".csv"
        wget.download(page_concat_url,result_path)
        new_csv=pd.read_csv(result_path)
        new_csv[0,"smiles"]=file_name.split(".mol2")[0]
        new_csv.to_csv(result_path)
concat_csv(result_dir)


   
