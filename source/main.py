from scraper import Scraper

if __name__ == "__main__":
    escape_bcn = Scraper('https://escapeup.es/', 'Barcelona')
    escape_bcn.scrape()
