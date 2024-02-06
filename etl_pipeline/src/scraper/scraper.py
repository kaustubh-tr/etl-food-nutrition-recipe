import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from db.db_connector import DBConnector

class Scraper:
    @staticmethod
    def scrape_recipe_data(recipe_url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/100.0.4896.75 Safari/537.36'}
            # Send a GET request to the recipe URL
            recipe_response = requests.get(recipe_url, headers=headers)
            print(recipe_response)
            if recipe_response.status_code == 200:
                # Parse the recipe page
                recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')
                
                # Extract recipe name, ingredients, and method
                recipe_name = recipe_soup.find('h1', id='article-heading_1-0', class_='comp type--lion article-heading mntl-text-block').text.strip()
                
                ingredients_div = recipe_soup.find('div', id='mntl-structured-ingredients_1-0')
                ingredients_list = [ingredient.text.strip() for ingredient in ingredients_div.find_all('li')] if ingredients_div else []
                ingredients = [f"- {ingredient}" for ingredient in ingredients_list]
                ingredients = '\n'.join(ingredients)

                method_div = recipe_soup.find('div', id='recipe__steps_1-0')
                method_list = [method.text.strip() for method in method_div.find_all('p', class_='comp mntl-sc-block mntl-sc-block-html')] if method_div else []
                methods = [f"- {method}" for method in method_list]
                method = '\n'.join(methods)
                
                return recipe_name, ingredients, method
            else:
                print("Failed to fetch recipe page:", recipe_response.status_code)
        except Exception as e:
            print("Error scraping recipe data:", e)
        return None, None, None

    @staticmethod
    def redirect_to_first_recipe(food_name):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/100.0.4896.75 Safari/537.36'}
            # Send a GET request to the search page URL with the food name as a query parameter
            search_url = f"https://www.allrecipes.com/search?q={food_name}"
            search_response = requests.get(search_url, headers=headers)
            print(search_response)
            
            if search_response.status_code == 200:
                # Parse the search results page
                search_soup = BeautifulSoup(search_response.content, 'html.parser')
                
                # Find the first recipe URL
                recipe_link = search_soup.find('a', id='mntl-card-list-items_1-0', class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')
                
                if recipe_link:
                    # Extract the href attribute from the <a> tag
                    recipe_url = recipe_link['href']
                    print("Recipe URL:", recipe_url)
                    return recipe_url
                else:
                    print("No recipe found on the search page")
            else:
                print("Failed to fetch search results page:", search_response.status_code)
        except Exception as e:
            print("Error redirecting to first recipe:", e)
        return None

if __name__ == "__main__":
    recipe_url = Scraper.redirect_to_first_recipe(food_name)
    if recipe_url:
        print("Redirected to:", recipe_url)
        recipe_name, ingredients, method = Scraper.scrape_recipe_data(recipe_url)
        print("Recipe Name:", recipe_name)
        print("Ingredients:", ingredients)
        print("Method:", method)
    else:
        print("No recipe found for the given food name")

# cd path/to/etl_pipeline
# export PYTHONPATH=$(pwd)
# python src/etl.py