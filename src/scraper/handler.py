import src.scraper.provider_fotocasa as provider
import src.scraper.requester as requester
import src.scraper.constant as constant

if __name__ == "__main__":
    provider.human_get(constant.BASE_URL, 'Barcelona Capital, Barcelona')
    #requester.get('https://www.fotocasa.es/es/comprar/viviendas/barcelona-capital/todas-las-zonas/l/2?combinedLocationIds=724%2C9%2C8%2C232%2C376%2C8019%2C0%2C0%2C0&gridType=3&latitude=41.3854&longitude=2.17754&sortType=publicationDate')
