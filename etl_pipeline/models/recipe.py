import psycopg2
from config.config import Config
from db.db_connector import DBConnector

class Recipe:
    def __init__(self, id, food_id, recipe_name, ingredients, method):
        self.id = id
        self.food_id = food_id
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.method = method

    @staticmethod
    def find_by_food_name(food_name):
        try:
            # Connect to the database
            with DBConnector() as db:
                # Query to fetch recipe details for the given food name
                query = """
                    SELECT f.food_name, r.recipe_name, r.ingredients, r.method
                    FROM food AS f
                    JOIN recipe AS r ON f.id = r.food_id
                    WHERE LOWER(f.food_name) = %s;  -- Case-insensitive comparison
                    """
    
                # Execute the query with the food name
                db.cursor.execute(query, (food_name,))
                # Fetch all rows returned by the query
                rows = db.cursor.fetchall()
                if rows:
                    recipes = {
                        'food_name': rows[0][0],  # Food name is the same for all rows
                        'recipe': [{
                            'recipe_name': row[1],
                            'ingredients': row[2],
                            'method': row[3]
                        } for row in rows]
                    }
                    return recipes
                else:
                    return None  # Food not found in the database
        except Exception as e:
            print("Error fetching recipe details:", e)
            return None

    @staticmethod
    def save_to_db(food_id, recipe_name, ingredients, method):
        try:
            # Connect to the database
            with DBConnector() as db:
                # Insert recipe details into the Recipe table
                query = """
                        INSERT INTO recipe (food_id, recipe_name, ingredients, method)
                        VALUES (%s, %s, %s, %s)
                        """
                db.cursor.execute(query, (food_id, recipe_name, ingredients, method))
                db.conn.commit()
                print("Recipe saved successfully.")
        except Exception as e:
            print("Error saving recipe to database:", e)

    @staticmethod
    def get_food_id(food_name):
        try:
            # Connect to the database
            with DBConnector() as db:
                # Query to fetch the food_id for the given food_name
                query = """
                        SELECT id FROM food WHERE food_name = %s;
                        """
                # Execute the query with the food name
                db.cursor.execute(query, (food_name,))
                # Fetch the food_id from the first row returned by the query
                row = db.cursor.fetchone()
                if row:
                    return row[0]  # Return the first column (food_id) from the row
                else:
                    return None  # Food not found in the database
        except Exception as e:
            print("Error fetching food_id:", e)
            return None