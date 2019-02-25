import sqlite3
import os
from recipe_scrapers import scrape_me
import json

db_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), '..', 'dbs', 'recipes.db'))  # Should work on every OS
conn = sqlite3.connect(db_path)

def format_response(d):
    return json.dumps(d,indent = 4) + '\n'


def returnScraped():
    scraper = scrape_me(
        'https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/')
    
    return format_response({scraper.title(), scraper.total_time(),
          scraper.ingredients(), scraper.instructions()})


def main():
    add_recipe('https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/')

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

