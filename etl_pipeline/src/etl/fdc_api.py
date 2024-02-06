import requests
from config.config import Config

class FDCAPI:
    @staticmethod
    def get_food_data(food_name):
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={Config.FDC_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            food_data = response.json()
            if food_data.get('foods') and len(food_data['foods']) > 0:
                if 'foodNutrients' in food_data['foods'][0]:
                    food_nutrients = food_data['foods'][0]['foodNutrients'][:6]  # Take only the first 6 nutrients
                    top_nutrients = [{
                        'nutrient_name': nutrient['nutrientName'],
                        'amount': nutrient['value'],
                        'unit_name': nutrient['unitName']
                    } for nutrient in food_nutrients]
                else:
                    top_nutrients = []
                
                return food_data, top_nutrients           
            else:
                return 'No food found', None
        else:
            return None, None
