# etl_food_nutrition_recipe

---

## Usage Instructions

### 1. Food Nutrition Information:

To retrieve nutrition information for a specific food, follow these steps:

#### a. Run ETL Process:
   Execute the `etl.py` script located in the `src/etl` directory:
   ```
   python src/etl/etl.py
   ```

#### b. Run Web API:
   Run the `web_api.py` script in the `src/etl` directory:
   ```
   python src/etl/web_api.py
   ```

### 2. Recipe Information:

To retrieve the recipe for a specific food, ensure that the food details are saved in the database before searching. Follow these steps:

#### a. Run Scraper:
   Execute the `web_api.py` script located in the `src/scraper` directory:
   ```
   python src/scraper/web_api.py
   ```

### 3. Food Detail and Recipe Storage:

To simultaneously store food details and retrieve the recipe for all food names in the `input.csv` file, follow these steps:

#### a. Run Combined Web API:
   Execute the `web_api.py` script located in the `src` directory:
   ```
   python src/web_api.py
   ```

---

This README section provides clear instructions for users to interact with the provided functionality. It's organized into three subsections, each outlining the steps needed to achieve a specific task related to food nutrition information and recipe retrieval. Users can easily follow these instructions to utilize the provided scripts effectively.
