from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_vk_id(url):
    s = Service('D:\Test Programs\GetVK_id\chrome\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get('https://regvk.com/id/')
    field = driver.find_element('id','enter')
    field.send_keys(url)
    driver.find_element('name','button').click()
    main_page = driver.page_source
    vk_id = ((main_page.split('пользователя:')[1]).split('<')[0])
    driver.close()
    return vk_id

