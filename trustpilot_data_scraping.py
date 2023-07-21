from bs4 import BeautifulSoup
import requests
import csv
#imported libraries - BeautifulSoup will handle all relevant functions for scraping the data from the website pages
#requests will pull the data from the specificed url
#csv will be used later to export the data to a readable .csv file

def scrape_trustpilot_pages(start_page, end_page): #defined scrape_trustpilot_pages function with a tuple including the specified start and end page to scrape
    all_reviews = [] #list for data to appended into

    for page in range(start_page, end_page + 1):
        url = f"https://uk.trustpilot.com/review/www.waylandgames.co.uk?page={page}" #specified url
        response = requests.get(url) 
        soup = BeautifulSoup(response.content, 'html.parser') #soup function will pull data from response function for use with bs4 package

        reviews = soup.find_all('div', {'class': 'styles_reviewCardInner__EwDq2'}) #reviews function using soup.findall with specified element from webpage to find content within specified review cards

        for review in reviews:
            try:
                content = review.find('p', {'data-service-review-text-typography': 'true'}).text.strip() #content function will search for specified element, if none found and AttributeError occurs, will put "N/A"
            except AttributeError:
                content = "N/A"

            rating = review.find('div', {'class': 'styles_reviewHeader__iU9Px'})['data-service-review-rating'] #rating function will find specified element for review stars and pull rating from inspect element

            try:
                author = review.find('span', {'data-consumer-name-typography': 'true'}).text.strip() #similar to content function, when AttributeError is encountered with author name, put "Anonymous"
            except AttributeError:
                author = "Anonymous"

            all_reviews.append({ #append all data pulled from the above functions for use with exporting to csv
                "content": content,
                "rating": rating,
                "author": author
            })

    return all_reviews

def save_to_csv(all_reviews, filename): #defined save_to_csv function using all_reviews list
    keys = all_reviews[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f: #encoded in utf-8 to avoid UniCode errors
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(all_reviews)

all_reviews = scrape_trustpilot_pages(1, 10) #pulling data from page 1 to page 10
save_to_csv(all_reviews, "data_scraping_trustpilot.csv") #exports data to readable csv