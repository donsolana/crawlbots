#Import scrapy
import scrapy
import pandas as pd

# Import the CrawlerProcess
from scrapy.crawler import CrawlerProcess
#set urls
url_ikeja = "https://hotels.ng/hotels-in-lagos/ikeja?price-filter=12000,120000"
url_lekki = "https://hotels.ng/hotels-in-lagos/lekki?price-filter=12000,120000"
url_ikoyi = "https://hotels.ng/hotels-in-lagos/ikoyi?price-filter=12000,120000"
url_vi = "https://hotels.ng/hotels-in-lagos/victoria-island?price-filter=12000,120000"


# Create the Spider class
class HNGcrawler(scrapy.Spider):
    name = 'HNGcrawler'
    # start_requests method
    def start_requests( self ):
        urls = [url_vi, url_ikeja, url_ikoyi, url_lekki]
        for url in urls:
          yield scrapy.Request(url ,callback = self.parse_getlinks)
          
    

    def parse_getlinks(self, response):
        # getlinks
        l = response.xpath('//nav[@class="listing-pagination"]')
        links = l.xpath("./ul/li/a/@href").extract()[:-1]
        #follow link
        for link in links:
          yield response.follow(url = link, callback = self.parse)
        

    def parse(self, response):
        #parse hotel name
        hotels_divs = response.xpath('//div[@class="listing-hotels"]')
        
        for i in range(len(hotels_divs)):
            hotel = hotels_divs[i]
            name = hotel.xpath('.//h2[@class="listing-hotels-name"]/text()').extract_first()
            price = hotel.xpath('.//p[contains(@class, "listing-hotels-prices-discount")]/text()').extract_first()
            location = hotel.xpath('.//span/a[1]/text()').extract_first()
            address = hotel.xpath('.//p[@itemprop="address"]/text()').extract_first()
            kind = hotel.xpath('.//div[contains(@class, "property-badge")]/text()').extract_first()
            hotelslag[name] = [price, location, address, kind]
            

hotelslag = {}
              
 # Run the Spider
process = CrawlerProcess()
process.crawl(HNGcrawler)
process.start()


##convert to dataframe
df = pd.DataFrame.from_dict(hotelslag).transpose()
hotels_lag = df.rename(columns={0: 'Price', 1: 'Town', 2: 'address',3: 'Type' })

#convert to csv
hotels_lag.to_csv("hotels_lagos.csv")
