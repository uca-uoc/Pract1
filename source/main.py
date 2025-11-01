from scraper import Scraper

if __name__ == "__main__":
    url = "https://escapeup.es/ciudad/barcelona/"
    city = "Barcelona"

    scraper = Scraper(url, city)
    try:
        scraper.scrape()
        print(f"\nTotal de enlaces encontrados: {len(scraper.escape_room_links)}\n")
        df = scraper.extract_room_details()
        print(df.head())
    finally:
        scraper.close()
