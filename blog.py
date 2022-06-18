import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name")
parser.add_argument("--ingredients")
parser.add_argument("--meals")

argument = parser.parse_args()
base_name = argument.file_name


def create_base():
    global argument
    connector = sqlite3.connect(base_name)
    my_cursor = connector.cursor()
    my_cursor.execute("CREATE TABLE measures (measure_id INT PRIMARY KEY, measure_name VARCHAR(30) UNIQUE);")
    my_cursor.execute(
        "CREATE TABLE ingredients (ingredient_id INT PRIMARY KEY, ingredient_name VARCHAR(30) NOT NULL UNIQUE);")
    my_cursor.execute("CREATE TABLE meals (meal_id INT PRIMARY KEY, meal_name VARCHAR(30) NOT NULL UNIQUE);")
    my_cursor.execute("INSERT INTO measures (measure_id, measure_name) VALUES (1, 'ml'), (2, 'g'),"
                      "(3, 'l'), (4, 'cup'), (5, 'tbsp'), (6, 'tsp'), (7, 'dsp'), (8, '') ")
    my_cursor.execute("INSERT INTO ingredients (ingredient_id, ingredient_name) VALUES (1, 'milk'), (2, 'cacao'),"
                      "(3, 'strawberry'), (4, 'blueberry'), (5, 'blackberry'), (6, 'sugar') ")
    my_cursor.execute("INSERT INTO meals (meal_id, meal_name) VALUES (1, 'breakfast'), (2, 'brunch'),"
                      "(3, 'lunch'), (4, 'supper') ")
    connector.commit()
    my_cursor.execute("CREATE TABLE recipes (recipe_id INT PRIMARY KEY, recipe_name VARCHAR(30) NOT NULL, "
                      "recipe_description VARCHAR(30));")
    my_cursor.execute("PRAGMA foreign_keys = ON;")
    my_cursor.execute("CREATE TABLE serve (serve_id INT PRIMARY KEY, recipe_id INT NOT NULL, meal_id INT NOT NULL,"
                      "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(meal_id) REFERENCES "
                      "meals (meal_id));")
    my_cursor.execute("CREATE TABLE quantity (quantity_id INT PRIMARY KEY, measure_id INT NOT NULL, "
                      "ingredient_id INT NOT NULL, recipe_id INT NOT NULL, quantity INT NOT NULL,"
                      "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(measure_id) REFERENCES "
                      "measures (measure_id), FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id));")
    index_of_recipe = 0
    index_of_serve = 0
    index_of_quantity = 0

    while True:
        print("Pass the empty recipe name to exit.")
        name_of_recipe = input("Recipe name:")
        if name_of_recipe == "":
            break
        index_of_recipe += 1
        desc_of_recipe = input("Recipe description:")
        index_of_meals = input("1) breakfast  2) brunch  3) lunch  4) supper \n When the dish can be served:")
        my_cursor.execute(f"INSERT INTO recipes (recipe_id, recipe_name, recipe_description) VALUES (?, ?, ?);",
                          (index_of_recipe, name_of_recipe, desc_of_recipe))
        for i in index_of_meals.split():
            index_of_serve += 1
            my_cursor.execute(f"INSERT INTO serve (serve_id, recipe_id, meal_id) VALUES (?, ?, ?);",
                              (index_of_serve, index_of_recipe, i))
        while True:
            ingredients_quantity = input("Input quantity of ingredient <press enter to stop>: ").split()
            if len(ingredients_quantity) == 0:
                break
            if len(ingredients_quantity) == 2:
                quantity = ingredients_quantity[0]
                measure_id = 8
                argument = '%' + ingredients_quantity[1] + '%'
                my_cursor.execute(
                    f"SELECT ingredient_id FROM ingredients WHERE ingredient_name like '%s'" % argument)
                rows = my_cursor.fetchall()
                if len(rows) > 1:
                    print("The ingredient is not conclusive!")
                    continue
                ingredient_id = int(str(rows[0]).replace(",", "").replace("(", "").replace(")", ""))
                index_of_quantity += 1
                my_cursor.execute(
                    f"INSERT INTO quantity (quantity_id, quantity, recipe_id, measure_id, ingredient_id) VALUES (?, ?, ?, ?, ?);",
                    (index_of_quantity, quantity, index_of_recipe, measure_id, ingredient_id))

            if len(ingredients_quantity) == 3:
                quantity = ingredients_quantity[0]
                argument = ingredients_quantity[1] + '%'
                my_cursor.execute(
                    f"SELECT measure_id FROM measures WHERE measure_name like '%s'" % argument)
                rows = my_cursor.fetchall()
                if len(rows) > 1:
                    print("The measure is not conclusive!")
                    continue
                measure_id = int(str(rows[0]).replace(",", "").replace("(", "").replace(")", ""))
                argument = '%' + ingredients_quantity[2] + '%'
                my_cursor.execute(
                    f"SELECT ingredient_id FROM ingredients WHERE ingredient_name like '%s'" % argument)
                rows = my_cursor.fetchall()
                if len(rows) > 1:
                    print("The ingredient is not conclusive!")
                    continue
                ingredient_id = int(str(rows[0]).replace(",", "").replace("(", "").replace(")", ""))
                index_of_quantity += 1
                my_cursor.execute(
                    f"INSERT INTO quantity (quantity_id, quantity, recipe_id, measure_id, ingredient_id) VALUES (?, ?, ?, ?, ?);",
                    (index_of_quantity, quantity, index_of_recipe, measure_id, ingredient_id))
    connector.commit()
    connector.close()


def search_base():
    global argument
    connector = sqlite3.connect(base_name)
    my_cursor = connector.cursor()
    set_of_meals = set()
    set_of_ingredients = set()
    set_of_recipe_served = set()
    set_of_recipe_with_ingredients = set()
    current_set = set()
    ingredients_list = argument.ingredients.split(',')
    meals_list = argument.meals.split(',')
    for i in range(0, len(meals_list)):
        current_name = meals_list[i].replace(" ", "")
        my_cursor.execute(
                    f"SELECT meal_id FROM meals WHERE meal_name = '%s'" % current_name)
        rows = my_cursor.fetchall()
        set_of_meals.add(int(str(rows[0]).replace(",", "").replace("(", "").replace(")", "")))
    for meal_id in set_of_meals:
        my_cursor.execute(
                    f"SELECT recipe_id FROM serve WHERE meal_id = '%s'" % meal_id)
        rows = my_cursor.fetchall()
        for row in rows:
            set_of_recipe_served.add(int(str(row).replace(",", "").replace("(", "").replace(")", "")))
    for i in range(0, len(ingredients_list)):
        current_name = ingredients_list[i].replace(" ", "")
        my_cursor.execute(
                    f"SELECT ingredient_id FROM ingredients WHERE ingredient_name = '%s'" % current_name)
        rows = my_cursor.fetchall()
        if len(rows) > 0:
            set_of_ingredients.add(int(str(rows[0]).replace(",", "").replace("(", "").replace(")", "")))
        else:
            set_of_ingredients.add(7)
    for ingredient_id in set_of_ingredients:
        my_cursor.execute(
                    f"SELECT recipe_id FROM quantity WHERE ingredient_id = '%s'" % ingredient_id)
        rows = my_cursor.fetchall()
        for row in rows:
            current_set.add(int(str(row).replace(",", "").replace("(", "").replace(")", "")))
        if len(set_of_recipe_with_ingredients) == 0:
            set_of_recipe_with_ingredients.update(current_set)
        else:
            result=set_of_recipe_with_ingredients.intersection(current_set)
            set_of_recipe_with_ingredients.clear()
            set_of_recipe_with_ingredients.update(result)
        current_set.clear()
    result = set_of_recipe_with_ingredients & set_of_recipe_served


    if len(result) == 0:
        print("There are no such recipes in the database.")
    else:
        result_string = ""
        current_string = ""
        for result_id in result:
            my_cursor.execute(
                    f"SELECT recipe_name FROM recipes WHERE recipe_id = '%s'" % result_id)
            rows = my_cursor.fetchall()
            current_string = (str(rows[0]).replace(",", "").replace("(", "").replace(")", "").replace("'", ""))
            if result_string == "":
                result_string= result_string+current_string
            else:
                result_string= result_string+", " + current_string
        print("Recipes selected for you: "+ result_string)


    connector.commit()
    connector.close()

if argument.ingredients is None and argument.meals is None:
    create_base()
else:
    search_base()
