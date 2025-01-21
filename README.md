## Amazon Scraper Overview
The scraper is designed to collect data from Amazon product pages for smartphones. It will extract the following details for each product:

 **Smartphone Title (Name):** The name of the mobile phone, cleaned up to remove extra spaces or characters.
 
**Price:** The price of the smartphone listed on Amazon.

**User Rating:** The average user rating of the product, typically displayed as a number out of 5 stars.

**RAM:** The amount of RAM the smartphone has.

**Storage:** The storage capacity of the smartphone.

**Page Number:** To navigate through multiple pages of search results and collect data from different listings.

## User Rating Filter
The scraper should only collect data for smartphones that have a **user rating of 4 stars or higher.**

This can be achieved by checking the user rating value for each phone on the Amazon page. If the rating is 4 or above, the product will be included in the output.
Steps to Implement the Scraper.

Web Scraping Library: Use libraries like requests or selenium to fetch the HTML of Amazon pages, and BeautifulSoup to parse the HTML and extract the relevant data.

Data Extraction: Identify the HTML elements where the phone name, price, rating, RAM, and storage are located. 
These details can be found in various tags such as **span, div, and a.** You can use BeautifulSoup to extract them.

User Rating Filtering: Once the user rating is extracted, check if it is greater than or equal to 4. If it meets this condition, save the data; otherwise, discard it.

Pagination Handling: To scrape data from multiple pages of search results, you can loop through page numbers and repeat the process, extracting data from each page.
