import requests
from bs4 import BeautifulSoup
import json
from carleader_bot.src.schemas import CarInfo


# Function to scrape a website and find elements by class value
def scrape_and_find_by_class(url, class_name):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all elements with the specified class value
        target_elements = soup.find_all(class_=class_name)

        # Check if any elements were found
        if not target_elements:
            print(f"No elements found with class value '{class_name}'.")
        return target_elements

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# Example usage
url_to_scrape = "https://carleader.it/auto_elenco.php"
BASE_URL = "https://carleader.it/"
class_links = "col-lg-12 col-md-12 col-sm-12 col-xs-12 pagination_container"
class_cars_info = "car_listings sidebar margin-top-20 clearfix"
class_cars_container = "inventory margin-bottom-20 clearfix scroll_effect fadeIn"
pages = scrape_and_find_by_class(url_to_scrape, class_links)


def find_pages(pages_element):
    found_links = set()
    for ul in pages_element.find_all("ul"):
        for li in ul.find_all("li"):
            for a in li.find_all("a"):
                found_links.add(a.get("href"))
    return found_links


links = find_pages(pages[0])

mapping = {
    "MOTORE": "engine",
    "ALIMENTAZIONE": "power_type",
    "TRAZIONE": "traction",
    "CAMBIO": "gearbox",
    "CLASSE": "type",
    "COLORE ESTERNI": "color_exterior",
    "COLORI INTERNI": "color_interior",
    "KM": "mileage",
    "IMMATRIC": "registration",
    "POSTI": "seats",
    "PORTE": "doors",
    "POTENZA Kw (Cv)": "power",
    "TIPOLOGIA": "category",
    "GARANZIA": "warranty",
    "ID VEICOLO": "id",
    "ESPOSIZIONE": "exposition",
}


def get_name_price(url):
    class_ = "inventory-heading margin-bottom-10 clearfix"
    row = scrape_and_find_by_class(url, class_)[0]
    name_price = row.find_all("h2")
    name = name_price[0].text
    price = float("".join(filter(str.isdigit, name_price[1].text)))
    return name, price


def get_car_data(cars_list_url):
    cars_info = []
    cars_container = scrape_and_find_by_class(cars_list_url, class_cars_container)
    cars_links = [c.find("a").get("href") for c in cars_container]

    for link in cars_links:
        car_name, price = get_name_price(BASE_URL + link)
        car_info = {"link": link, "name": car_name, "price": price}
        car_data = scrape_and_find_by_class(BASE_URL + link, "technical")
        all_data = car_data[0].find_all("tr")
        for el in all_data:
            tds = el.find_all("td")
            if len(tds) == 2:
                name = (
                    tds[0]
                    .text.replace(":", "")
                    .replace(".", "")
                    .replace("#", "")
                    .strip()
                )
                car_info[mapping[name]] = tds[1].text
        cars_info.append(car_info)
    return cars_info


urls = [BASE_URL + el if el != "#" else url_to_scrape for el in links]

cars_parsed = []
for u in urls:
    cars = [CarInfo(**el) for el in get_car_data(u)]
    cars_parsed.extend(cars)


with open("cars.json", "w") as f:
    json.dump([car.__dict__ for car in cars_parsed], f)
