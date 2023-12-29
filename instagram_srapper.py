from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd

def scroll_to_bottom(driver, element_class="_ap3a._aaco._aacw._aacx._aad7._aade",
                      container_class="x5yr21d.xw2csxc.x1odjw0f.x1n2onr6"):
    # Find the comments container
    comments_div = driver.find_element(By.CLASS_NAME, container_class)

    # Scroll to the bottom of the comments
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comments_div)

def get_comments_count(driver, element_class="_ap3a._aaco._aacw._aacx._aad7._aade"):
    # Find all comments
    comments = driver.find_elements(By.CLASS_NAME, element_class)
    
    # Return the number of comments
    return len(comments)

def instagramLogin(username, password):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(driver, 10)
        username_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='username']")))
        password_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='password']")))

        login_button = driver.find_element(By.CLASS_NAME, "_acan._acap._acas._aj1-")

        # Execute alguma ação no elemento
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        sleep(4)

        return True
    except:
        return False


def scrap_page(driver,page_url):
    driver.get(page_url)
    sleep(2)

    # Scroll to the bottom and get initial comments count
    scroll_to_bottom(driver)
    comments_count = 0

    # Initialize scroll flag
    scroll = True

    while scroll:
        # Scroll to the bottom
        scroll_to_bottom(driver)

        # Get the current comments count
        current_comments_count = get_comments_count(driver)

        # Check if new comments have loaded
        if current_comments_count == comments_count:
            scroll = False
        else:
            comments_count = current_comments_count

        # Print the current comments count
        #print(comments_count)

        # Add a sleep to avoid unnecessary rapid scrolling
        sleep(1)

#************************* Get the comments ************************
def getComments(driver):
    comments= driver.find_elements(By.CLASS_NAME,
                                    "x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj")

    profile_names = []
    for name in comments[1:len(comments)-1:2]:
        profile_names.append(name.text)

    comments_list = []
    for comment in comments[2::2]:
        comments_list.append(comment.text)

    #dictC = dict(zip(profile_names, comments_list))
    df = pd.DataFrame()
    df["profile_name"] = profile_names
    df["comment"] = comments_list

    return df

    # import json
    # # Use json.dump to write dictC to a file
    # with open('dictC.json', 'w', encoding='utf-8') as f:
    #     json.dump(dictC, f)
    


chrome_options = Options()
#chrome_options.add_argument('--headless')

# Crie uma instância do driver do navegador
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)

url_list = ["https://www.instagram.com/p/C1PHrZGouGR/",
            "https://www.instagram.com/p/C1KSPOFNioy/",
            "https://www.instagram.com/p/C1J5PacoaYV/"            
            ]
print("Login...")
if instagramLogin("", ""):
    #Go to the page

    result_dataframe = pd.DataFrame()
    for url in url_list:
        print("Scraping page {}...".format(url))
        scrap_page(driver,url )
        print("Geting comments...")        
        df = getComments(driver)
        df['source'] = url
        result_dataframe = pd.concat([result_dataframe,df])
        print("Exporting...")
        result_dataframe.to_excel("instagram_scrapper_result.xlsx".format(url))

    print("Operation Finished!")
    driver.close()
    




