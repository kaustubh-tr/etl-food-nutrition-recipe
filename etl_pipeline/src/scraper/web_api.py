from flask import Flask, jsonify
from scraper import Scraper
from models.recipe import Recipe

app = Flask(__name__)

# Route for handling GET requests for recipes
@app.route('/scraper/recipe/<food_name>', methods=['GET'])
def get_recipe(food_name):
    try:
        # Call the redirect_to_first_recipe method to get the recipe URL
        recipe_url = Scraper.redirect_to_first_recipe(food_name)
        
        # If recipe URL is found, call scrape_recipe_data to get recipe details
        if recipe_url:
            recipe_name, ingredients, method = Scraper.scrape_recipe_data(recipe_url)
            
            # If recipe details are found, save to database and return as JSON response
            if recipe_name and ingredients and method:
                food_id = Recipe.get_food_id(food_name)
                Recipe.save_to_db(food_id, recipe_name, ingredients, method)
                
                # print the recipe
                recipes = Recipe.find_by_food_name(food_name)
                if recipes:
                    return jsonify(recipes)
                else:
                    return jsonify({'error': 'Failed to fetch recipe from database'}), 500
            else:
                return jsonify({'error': 'Recipe details not found or could not be scraped'}), 404
        else:
            return jsonify({'error': 'Recipe URL not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error getting recipe: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
