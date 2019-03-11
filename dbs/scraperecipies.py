import sqlite3
import os
from recipe_scrapers import scrape_me
import json
import pprint
import time

db_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), '..', 'dbs', 'recipes.db'))  # Should work on every OS
conn = sqlite3.connect(db_path)

def format_response(d):
    return json.dumps(d,indent = 4) + '\n'


def returnScraped(url):
    scraper = scrape_me(url)

    return format_response({scraper.title(), scraper.total_time(),
          scraper.ingredients(), scraper.instructions()})


def main():
    urls = ['https://www.allrecipes.com/recipe/14469/jamies-cranberry-spinach-salad/','https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/',
    'https://www.allrecipes.com/recipe/24087/restaurant-style-buffalo-chicken-wings/',
    'https://www.allrecipes.com/recipe/24332/ultimate-twice-baked-potatoes/',
    'https://www.allrecipes.com/recipe/13651/awesome-sausage-apple-and-cranberry-stuffing/',
    'https://www.allrecipes.com/recipe/17991/stuffed-green-peppers-i/',
    'https://www.allrecipes.com/recipe/13218/absolutely-ultimate-potato-soup/',
    'https://www.allrecipes.com/recipe/13436/italian-sausage-soup-with-tortellini/',
    'https://www.allrecipes.com/recipe/13333/jamies-minestrone/',
    'https://www.allrecipes.com/recipe/22302/cha-chas-white-chicken-chili/',
    'https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/',
    'https://www.allrecipes.com/recipe/220854/chef-johns-italian-meatballs/',
    'https://www.allrecipes.com/recipe/220125/slow-cooker-beef-pot-roast/',
    'https://www.allrecipes.com/recipe/229156/zesty-quinoa-salad/',
    'https://www.allrecipes.com/recipe/15867/chicken-and-dumplings-iii/',
    'https://www.allrecipes.com/recipe/14967/bacon-and-tomato-cups/',
    'https://www.allrecipes.com/recipe/25333/vegan-black-bean-soup/',
    'https://www.allrecipes.com/recipe/216888/good-new-orleans-creole-gumbo/',
    'https://www.allrecipes.com/recipe/219077/chef-johns-perfect-mashed-potatoes/',
    'https://www.allrecipes.com/recipe/223042/chicken-parmesan/',
    'https://www.allrecipes.com/recipe/229960/shrimp-scampi-with-pasta/',
    'https://www.allrecipes.com/recipe/83557/juicy-roasted-chicken/',
    ]
    #for url in urls:
    #    print(returnScraped(url))
    #    time.sleep(2)
    #add_recipe('https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/')
    for url in urls:
        add_recipe(url)

def add_recipe(url):
    scraper = scrape_me(url)
    ingredients = json.dumps(scraper.ingredients())

    query = """
        INSERT
        INTO recipes(ingredients,directions,title,recipe_url)
        VALUES (?,?,?,?)
    """
    c = conn.cursor()
    c.execute(query, [ingredients,scraper.instructions(),scraper.title(),url])
    conn.commit()
if __name__ == '__main__':
    main()

