from src.etl.fdc_api import FDCAPI
from models.food import Food
from models.food_nutrient import FoodNutrient
from db.db_connector import DBConnector
import csv

class ETL:
    @staticmethod
    def extract_from_csv(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]

    @staticmethod
    def transform_and_load(food_names):
        for food_name in food_names:
            new_food_name = food_name.replace("'s", "s")
            
            if Food.find_by_name(new_food_name):
                print(f"Food '{new_food_name}' already exists in the database. Skipping...")
                continue  # Skip insertion for existing records

            else:
                food_data, top_nutrients = FDCAPI.get_food_data(food_name)
                
                if isinstance(food_data, str) and food_data == 'No food found':
                    print(f"No food data found for '{new_food_name}'. Skipping saving to the database.")
                
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

if __name__ == "__main__":
    file_path = 'data/input.csv'
    food_names = ETL.extract_from_csv(file_path)
    ETL.transform_and_load(food_names)
