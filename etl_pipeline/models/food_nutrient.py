from db.db_connector import DBConnector

class FoodNutrient:
    def __init__(self, id, nutrient_name, amount, unit_name):
        self.id = id
        self.nutrient_name = nutrient_name
        self.amount = amount
        self.unit_name = unit_name

    def __str__(self):
        return f"FoodNutrient(id={self.id}, nutrient_name={self.nutrient_name}, amount={self.amount}, unit_name={self.unit_name})"

    @staticmethod
    def save_to_db(food_id, nutrient_name, amount, unit_name):
        query = "INSERT INTO foodNutrient (food_id, nutrient_name, amount, unit_name) VALUES (%s, %s, %s, %s)"
        values = (food_id, nutrient_name, amount, unit_name)
        try:
            db = DBConnector()
            db.execute_query(query, values)
            db.close_connection()
        except Exception as e:
            print(f"An error occurred while saving data to foodNutrient table: {e}")



