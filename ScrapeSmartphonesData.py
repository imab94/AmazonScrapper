import pandas as pd
from bs4 import BeautifulSoup
import requests
from abc import abstractmethod,ABC
import re


class AmazonScrapper(ABC):
    """
    A Amazon scrapper abstract class is used to scrape smartphones title,rating,price, product_link,ram and rom .
    this is having a abstract method which should be implemented by child class (derived class)
    """

    def __init__(self) -> None:
        self.__url = None
        self.__scrape_data = []


    def set_url(self,url):
        self.__url = url


    def get_url(self):
        return self.__url
    

    @abstractmethod
    def scrape_filtered_data(self):
        raise NotImplementedError("this scrape filtered method should be implemented by sub-class.")
    

    def get_scrape_data(self):
        return self.__scrape_data
    

    def _add_to_scrape_data(self, data):
        if isinstance(data, list):
            self.__scrape_data.extend(data)
        else:
            self.__scrape_data.append(data)


    @abstractmethod
    def scrape_unfiltered_data(self):
        raise NotImplementedError("this unfiltered scrape method should be implemented by sub-class")



class Scrapper(AmazonScrapper):
    """
    Implementing scrape method in child class (Scrapper)
    """
    def scrape_filtered_data(self):
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}

        try:
            response = requests.get(self.get_url(),headers=self.headers,timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.content,"html.parser")
                container = soup.select("div.a-section.a-spacing-small.a-spacing-top-small")
                for item in container:
                    title = item.select("span.a-size-medium.a-color-base.a-text-normal")
                    if title:
                        smart_phone_title = title[0].string.split("(")[0]
                        span_item = item.select("span.a-price-whole")
                        aria_label = item.find("span",attrs={"aria-label":True}).text
                        if span_item and len(aria_label)>1:
                            price = int(span_item[0].get_text().replace(",",""))
                            if 15000 <= price <= 150000:
                                actual_price = price 
                                if "out of 5 star" in aria_label:
                                    rating = float(aria_label.split("out of 5 stars")[0])
                                    if rating and rating > 3.0:
                                        user_rating = rating
                                        product_link = item.select("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")[0].attrs['href']
                                        actual_product_link = "https://www.amazon.in" + product_link

                                        try:
                                            product_details_page = requests.get(actual_product_link,headers=self.headers,timeout=10)
                                            if product_details_page.status_code == 200:
                                                product_soup = BeautifulSoup(product_details_page.content, "html.parser")
                                                td_tag = product_soup.select("td.a-size-base.prodDetAttrValue")                                              
                                            else:
                                                print(f"Can't fetch product details with status code - {product_details_page.status_code}")

                                        except Exception as e:
                                            print(f"Request Failed - {e}")
                   
                                        ram_regex = r'\b\d{1,2}GB\b'
                                        rom_regex = r'\b\d{3}GB\b'
                                        ram_storage = re.findall(ram_regex, title[0].string)
                                        ram_format = int(str(ram_storage[0]).split("GB")[0])
                                        rom_storage = re.findall(rom_regex, title[0].string) 
                                        rom_format = int(str(rom_storage[0]).split("GB")[0])
                                        if (ram_storage and rom_storage) and (ram_format > 8 and rom_format > 64):
                                            ram = ram_storage[0]
                                            storage = rom_storage[0]                                                            
                                            self._add_to_scrape_data({
                                                "Name": smart_phone_title.strip(), 
                                                "Price": actual_price, 
                                                "User Rating": user_rating,
                                                "Ram": ram,
                                                "Storage": storage,
                                                "Product Link":actual_product_link,
                                            })
                                        else:
                                            ram = ram_storage[0] if ram_storage else ""
                                            storage = rom_storage[0] if rom_storage else ""
                                            self._add_to_scrape_data({
                                                "Name": smart_phone_title.strip(), 
                                                "Price": actual_price, 
                                                "User Rating": user_rating,
                                                "Ram": ram,
                                                "Storage": storage,
                                                "Product Link":actual_product_link,
                                            })                              


            else:
                self.scrape_filtered_data()

        except Exception as e:
            print(f"Error while filtered Fetching result - {e}")



    def convert_excel_data(self,file_name):
        if self.get_scrape_data():
            df = pd.DataFrame(self.get_scrape_data())
            df.to_excel(f"{file_name}.xlsx",index=False)
            return "Scraping Data Saved successfully into xlsx file"

        else:
            return Exception("No Scraping data found")



    def scrape_unfiltered_data(self):
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}

        try:
            response = requests.get(self.get_url(),headers=self.headers,timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.content,"html.parser")
                container = soup.select("div.a-section.a-spacing-small.a-spacing-top-small")

                for item in container:
                    title = item.select("span.a-size-medium.a-color-base.a-text-normal")
                    if title:
                        smart_phone_title = title[0].string.split("(")[0]
                        span_item = item.select("span.a-price-whole")
                        aria_label = item.find("span",attrs={"aria-label":True}).text
                        if span_item:
                            price = int(span_item[0].get_text().replace(",",""))

                        if "out of 5 star" in aria_label and aria_label is not None:
                            rating = float(aria_label.split("out of 5 stars")[0])
                            if rating is not None:
                                user_rating = rating

                        product_link = item.select("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")[0].attrs['href']
                        if product_link:
                            actual_product_link = "https://www.amazon.in" + product_link
                        
                        ram_regex = r'\b\d{1,2}GB\b'
                        rom_regex = r'\b\d{3}GB\b'
                        ram_storage = re.findall(ram_regex, title[0].string)
                        rom_storage = re.findall(rom_regex, title[0].string) 
                        if ram_storage and rom_storage:
                            ram = ram_storage[0]
                            storage = rom_storage[0]                                                            
                            self._add_to_scrape_data({
                                "Name": smart_phone_title.strip(), 
                                "Price": price, 
                                "User Rating": user_rating,
                                "Ram": ram,
                                "Storage": storage,
                                "Product Link":actual_product_link,
                            })
                        else:
                            ram = ram_storage[0] if ram_storage else ""
                            storage = rom_storage[0] if rom_storage else ""
                            self._add_to_scrape_data({
                                "Name": smart_phone_title.strip(), 
                                "Price": price, 
                                "User Rating": user_rating,
                                "Ram": ram,
                                "Storage": storage,
                                "Product Link":actual_product_link,
                            })                              

    
      
            else:
                self.scrape_filtered_data()

        except Exception as e:
            print(f"Error while Fetching unfiltered result - {e}")




scraper = Scrapper()
page_number = 4
for i in range(1,page_number+1):
    url_path = f"https://www.amazon.in/s?k=smartphones&page={i}&crid=RDSH72EOQJCB&qid=1718608716&sprefix=%2Caps%2C358&ref=sr_pg_{i}"
    scraper.set_url(url_path)
    scraper.scrape_filtered_data()
    # scraper.scrape_unfiltered_data()

print(scraper.convert_excel_data("filtered_amazon_data"))


        

    
