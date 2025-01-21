from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}

smart_phone_list = []
def scrape__smartphone_data(url,page_num):
    # smart_phone = []
    try:
        data = requests.get(url,headers=headers,timeout=10)
        if data.status_code == 200:
            soup = BeautifulSoup(data.content,"html.parser")
            container = soup.select("div.a-section.a-spacing-small.a-spacing-top-small")
            # print(container)
            for item in container:
                span_class = item.select("span.a-price-whole")
                if span_class:
                    for i in span_class:
                        if len(i)>=1:
                            price = int(i.string.replace(",",""))
                            # print(price)
                            if 10000 <= price <= 150000: 
                                actual_price = price
                                aria_label = item.find("span",attrs={"aria-label":True})
                                if aria_label is not None:
                                    aria_label = aria_label.text
                                    if "out of 5 stars" in aria_label:
                                        # print(aria_label)
                                        rating = float(aria_label.split("out of 5 stars")[0])
                                        # print(rating)
                                        if rating is not None:
                                            if rating > 3.0:
                                                user_rating = rating
                                                heading = item.select("span.a-size-medium.a-color-base.a-text-normal")
                                                if heading:
                                                    # print(heading)
                                                    for hed in heading:
                                                        smartphone_title =  hed.string.split("(")[0]
                                                        # print(smartphone_title)
                                                        if smartphone_title is not None:
                                                            ram_regex = r'\b\d{1,2}GB\b'
                                                            rom_regex = r'\b\d{3}GB\b'
                                                            ram_storage = re.findall(ram_regex, hed.text)
                                                            rom_storage = re.findall(rom_regex, hed.text)                                                    
                                                            if ram_storage and rom_storage:
                                                                ram = ram_storage[0]
                                                                storage = rom_storage[0]                                                            
                                                                smart_phone_list.append({
                                                                    "Name": smartphone_title.strip(), 
                                                                    "Price": actual_price, 
                                                                    "User Rating": user_rating,
                                                                    "Ram": ram,
                                                                    "Storage": storage,
                                                                    "Page Completed":page_num
                                                                })
                                                            else:
                                                                ram = ram_storage[0] if ram_storage else ""
                                                                storage = rom_storage[0] if rom_storage else ""
                                                                smart_phone_list.append({
                                                                    "Name": smartphone_title.strip(), 
                                                                    "Price": actual_price, 
                                                                    "User Rating": user_rating,
                                                                    "Ram": ram,
                                                                    "Storage": storage,
                                                                    "Page Completed":page_num
                                                                })

            df = pd.DataFrame(smart_phone_list)
            df.to_excel("AmazonScrapeData.xlsx",index=False)

                                                        

        else:
            scrape__smartphone_data(url,page_num)
        
    except Exception as e:
        # pass
        print(e)


page_number = 6
for i in range(1,page_number+1):
    url_path = f"https://www.amazon.in/s?k=smartphones&page={i}&crid=RDSH72EOQJCB&qid=1718608716&sprefix=%2Caps%2C358&ref=sr_pg_{i}"
    scrape__smartphone_data(url_path,i)