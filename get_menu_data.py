#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

URL = "https://menus.campus-dining.com/eliorna/d1031"

def scrape_recipe_names(url: str):
    # Fetch the page
    resp = requests.get(url)
    resp.raise_for_status()  # raise if non-200

    # Parse HTML
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all <div class="k10-recipe__name">
    recipe_divs = soup.find_all("div", class_="k10-course__message")

    # Print their text content
    print(f"Found {len(recipe_divs)} recipe names:\n")
    for div in recipe_divs:
        name = div.get_text(strip=True)
        if name:
            print(name)

if __name__ == "__main__":
    scrape_recipe_names(URL)
