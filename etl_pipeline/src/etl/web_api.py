from flask import Flask, jsonify
from db.db_connector import DBConnector

app = Flask(__name__)

# Route for handling GET requests
@app.route('/<food_name>', methods=['GET'])
def get_food_details(food_name):
    # Fetch food details from the database
    food_details = fetch_food_details(food_name)
    
    # If food details are found, return them as JSON response
    if food_details:
        return jsonify(food_details)
    else:
        return jsonify({'error': 'Food not found'}), 404

def fetch_food_details(food_name):
    try:
        # Convert the input food name to lowercase
        food_name_lower = food_name.lower()

        # Connect to the database
        with DBConnector() as db:
            # Query to fetch food details and associated nutrient details
            query = """
                    SELECT f.food_name, fn.nutrient_name, fn.amount, fn.unit_name
                    FROM food AS f
                    JOIN foodNutrient AS fn ON f.id = fn.food_id
                    WHERE LOWER(f.food_name) = %s;  -- Case-insensitive comparison
                    """
            # Execute the query with the lowercase food name
            db.cursor.execute(query, (food_name_lower,))
            # Fetch all rows returned by the query
            rows = db.cursor.fetchall()

            # If rows are found, organize the data into a dictionary
            if rows:
                food_details = {
                    'food_name': rows[0][0],  # Food name is the same for all rows
                    'nutrients': [{
                        'nutrient_name': row[1],
                        'amount': row[2],
                        'unit_name': row[3]
                    } for row in rows]
                }
                return food_details
            else:
                return None  # Food not found in the database
    except Exception as e:
        print("Error fetching food details:", e)
        return None


if __name__ == '__main__':
    app.run(debug=False)
