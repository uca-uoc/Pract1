# TODO: Mirar el robots.txt
# TODO: Mirar servidores para no saturar
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Scraper():
    """Clase para busucar escape rooms en la ciudad deseada.

    Atributos:
        driver (WebDriver): Instancia de Selenium WebDriver.
        city (str): Ciudad objetivo.
        url (str): URL a hacer web scraping.
    """

    def __init__(self, url, city):
        """Constructor de la clase Scapper.
        
        Args:
            url (str): URL inicial a asignar.
            city (str): ciudad inicial a asignar.
        """
        self.driver = webdriver.Chrome()
        self.url = url
        self.city = city.lower()

    def __search_city(self):
        """ Buscar la ciudad especificada en la lista de ciudades y guarda su URL.

        El metodo recorre los elementos de la clase 'city'' y compara sus titulos
        con la ciudad especificada. Si coinciden las ciudades guardamos la URL en
        el objeto 'self.url'.

        Assert:
            Se comprueba si la url contiene el nombre de la ciudad.
        """
        cities_list = self.driver.find_elements(By.CLASS_NAME, "city")

        find_city = False
        i = 0
        while not find_city or i < len(cities_list):
            s_city = cities_list[i].find_elements(By.CLASS_NAME,"title")[0].text
            if s_city.lower() == self.city:
                find_city = True
                self.url = cities_list[i].find_elements(By.TAG_NAME,"a")[0].get_attribute("href")
            i += 1

        assert self.city in self.url
    
    def set_url(self, url):
        self.url = url

    def set_city(self, city):
        self.city = city
    
    def get_url(self):
        return self.url
    
    def get_city(self):
        return self.city

    def scrape(self):
        """Metodo que ejecuta el web scraping.
        
        Este metodo primero obtiene el HTML de la pagina web. Luego
        busca la URL de la ciudad de la cual se quiere extraer informacion.

        TODO: rellenar conforme se avanza en el proyecto

        Finalmente, cerramos la pagina y la sesion para liberar recursos.
        """
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        print(user_agent)

        self.driver.get(self.url)
        self.__search_city()
        
        time.sleep(1)
        self.driver.quit()

    def __search_escape_rooms(self):
        """Busca todos los enlaces de escape rooms en la página de la ciudad."""
        # Hacemos scroll hasta el final para cargar todos los elementos
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extraemos todos los enlaces <a> que contienen 'escape-room'
        a_tags = self.driver.find_elements(By.TAG_NAME, "a")
        links = set()  # Evitamos duplicados

        for a in a_tags:
            href = a.get_attribute("href")
            if href and "escape-room" in href:
                links.add(href)

        self.escape_room_links = sorted(links)  # Guardamos los enlaces

