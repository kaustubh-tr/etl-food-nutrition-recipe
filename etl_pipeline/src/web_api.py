from flask import Flask, jsonify, request
from src.etl.fdc_api import FDCAPI
from etl.etl import ETL
from scraper.scraper import Scraper
from models.food import Food
from models.food_nutrient import FoodNutrient
from models.recipe import Recipe
import csv

app = Flask(__name__)

# Route for triggering ETL and scraping processes simultaneously
@app.route('/etl_and_scraper/<food_name>', methods=['GET'])
def etl_and_scraper(food_name):
    try:
        # Read food names from the input CSV file
        with open('data/input.csv', 'r') as file:
            food_names = [row[0] for row in csv.reader(file)]

        results = []

        for food in food_names:
            new_food_name = food.replace("'s", "s")

            # Perform ETL to save food details into food and foodNutrient tables
            if Food.find_by_name(new_food_name):
                print(f"Food '{new_food_name}' already exists in the database. Skipping ETL...")
            else:
                food_data, top_nutrients = FDCAPI.get_food_data(new_food_name)
                
                if isinstance(food_data, str) and food_data == 'No food found':
                    print(f"No food data found for '{new_food_name}'. Skipping ETL.")
                elif food_data and food_data.get('foods') and len(food_data['foods']) > 0:
                    # Extract relevant data from food_data
                    food_id = None  # Placeholder for auto-generated ID
                    name = new_food_name
                    # name = food_data['foods'][0]['description']  # Assuming 'description' holds the food name

                    # Save food data to Food table
                    food = Food(food_id, name)
                    food_id = food.save_to_db()  # Get auto-generated food ID from database

                    # Save top nutrients to FoodNutrient table if top_nutrients is not None
                    if top_nutrients is not None:
                        for nutrient in top_nutrients:
                            nutrient_name = nutrient['nutrient_name']
                            amount = nutrient['amount']
                            unit_name = nutrient['unit_name']
                            FoodNutrient.save_to_db(food_id, nutrient_name, amount, unit_name)
                    else:
                        print(f"No nutrient data found for food '{new_food_name}'")
                else:
                    print(f"No food data found for '{new_food_name}'")

            # Scrape recipe details and save them into recipe table
            recipe_url = Scraper.redirect_to_first_recipe(new_food_name)
            if recipe_url:
                recipe_name, ingredients, method = Scraper.scrape_recipe_data(recipe_url)
                if recipe_name and ingredients and method:
                    food_id = Recipe.get_food_id(new_food_name)
                    Recipe.save_to_db(food_id, recipe_name, ingredients, method)
                    if new_food_name == food_name:
                        results.append({
                            'food_name': new_food_name,
                            'recipe_name': recipe_name,
                            'ingredients': ingredients,
                            'method': method
                        })
                else:
                    if new_food_name == food_name:
                        results.append({'error': f'Failed to scrape recipe details for {new_food_name}'})
            else:
                if new_food_name == food_name:
                    results.append({'error': f'Recipe URL not found for {new_food_name}'})

        return jsonify({'results': results}), 200

    except Exception as e:
        return jsonify({'error': f'Error in ETL and scraping processes: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)