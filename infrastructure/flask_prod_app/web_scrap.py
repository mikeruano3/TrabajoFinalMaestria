import requests
from bs4 import BeautifulSoup
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By as By
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def loginToWebPage(driver):
    url = 'https://elperiodico.com.gt/politica/justicia/2022/08/12/the-economist-jose-ruben-zamora-ha-hecho-una-cruzada-contra-la-corrupcion-en-guatemala/'
    #r = requests.get(url)
    #s = BeautifulSoup(r.text, 'lxml')

    driver.get(url)

    try:
        botonCerrarNotificacion = driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]' )
        botonCerrarNotificacion.click()
    except:
        print('No hay notificacion')
        
    try:        
        button_login = driver.find_element_by_xpath('//*[@id="userbox"]/nav/a[2]/i')
        button_login.click()

        # si necesita ingresar usuario y contraseña para ver mas articulos
        user_name = driver.find_element_by_xpath('//*[@id="user_login"]')
        user_password = driver.find_element_by_xpath('//*[@id="user_pass"]')
        button_accept = driver.find_element_by_xpath('//*[@id="wp-submit"]')
        user_name.clear()
        user_password.clear()
        user_name.send_keys('yoentroalau@gmail.com')
        user_password.send_keys('A@@@1234')
        button_accept.click()
    except:
        print('No hay login')


def navegarArticuloPorPalabra(driver, palabraABuscar, objetoPersona):
    try:
        title = ''
        date = ''
        full_text = ''
        try:
            driver.get(f'https://elperiodico.com.gt/?s={palabraABuscar}&Submit=')
            entradas_anteriores = driver.find_element_by_class_name('nav-previous')
            entradas_anteriores.click()
            link_articulo = driver.find_element_by_xpath('//*[@id="seccion"]/div[1]/div/a[1]')
            link_articulo.click()
        except:
            print('No hay entradas anteriores')
            driver.get(f'https://elperiodico.com.gt/?s={palabraABuscar}&Submit=')
            link_articulo = driver.find_element_by_xpath('//*[@id="seccion"]/div[1]/div/a[1]')
            link_articulo.click()

        try:
            title = driver.find_element_by_class_name('post-title-big').text
        except:
            title = palabraABuscar
        date  = driver.find_element_by_xpath('//*[@id="space-meta"]').text
        formatted_date = re.findall("\d\d-\d\d-\d\d", date)

        articles_body = driver.find_element_by_xpath('//div[@class="flexible-article-content"]')

        articles = articles_body.find_elements(By.TAG_NAME, 'p')

        full_text = ''

        for article in articles:
            full_text = full_text + article.text + ' '

        objetoPersona["title"] = title
        objetoPersona["date"] = date
        objetoPersona["full_text"] = full_text
        objetoPersona["word_to_search"] = palabraABuscar
    except:
        print('Error obteniendo articulo.. :(')
    return objetoPersona

def scrappearPersonaEnElPeriodico(peopleList = [ {"word_to_search": "Jimmy Morales"}, ]):
    driver = webdriver.Chrome('chromedriver',options=chrome_options)

    result = []
    loginToWebPage(driver)
    for people in peopleList:    
        result.append(navegarArticuloPorPalabra(driver, people['word_to_search'], people))

    driver.close()
    return peopleList