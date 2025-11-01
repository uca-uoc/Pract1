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

    def __search_escape_rooms(self):
        """Busca todos los enlaces de escape rooms en la página de la ciudad."""
        SCROLL_PAUSE_TIME = 5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        links = set()
        for a in self.driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")
            if href and "escape-room" in href and "blog" not in href:
                links.add(href)
        self.escape_room_links = sorted(links)

    def extract_room_details(self):
        """Abre cada enlace y extrae los detalles principales del escape room."""
        for i, url in enumerate(self.escape_room_links):
            print(f"[{i+1}/{len(self.escape_room_links)}] Extrayendo datos de: {url}")
            self.driver.get(url)
            time.sleep(1.5)

            data = {"url": url}

            # Extraemos el nombre desde el header
            try:
                header = self.driver.find_element(By.CSS_SELECTOR, "div.game_container div:nth-child(2) h1 span.game")
                name = header.text.strip()
                if not name:
                    continue
                data["name"] = name
            except:
                continue  # si no encuentra el nombre, saltamos este escape room

            # Extraemos los detalles del contenedor principal
            try:
                container = self.driver.find_element(By.CSS_SELECTOR, ".details_container.details_component.orange")
                details = container.find_elements(By.CSS_SELECTOR, ".detail")
                for j, detail in enumerate(details, start=1):
                    text = detail.text.strip()
                    if text:
                        data[f"extra_{j}"] = text
            except:
                pass

            self.rooms_data.append(data)
            self._export()  # guardamos solo si el escape room es válido

        print(f"\n✅ Datos guardados en {self.csv_path} ({len(self.rooms_data)} filas válidas)")
        return pd.DataFrame(self.rooms_data)
    
    def _export(self):
        """Guarda los datos válidos en el CSV."""
        df = pd.DataFrame(self.rooms_data)
        # Eliminamos filas con valores None o NaN en 'name'
        df = df.dropna(subset=["name"])
        df = df[df["name"].str.strip() != ""]
        df.to_csv(self.csv_path, index=False, encoding="utf-8-sig")

    def scrape(self):
        """Ejecuta la búsqueda inicial de enlaces."""
        print("Abriendo la página:", self.url)
        self.driver.get(self.url)
        try:
            self.__search_city()
        except Exception:
            print("No se buscó ciudad específica; se usa la URL directa.")
        time.sleep(1)
        self.__search_escape_rooms()

    def close(self):
        self.driver.quit()




