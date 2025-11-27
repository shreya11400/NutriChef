from flask import Flask, render_template, request, jsonify, session
import random
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "nutrichef_secret_key_2025_enhanced"

# Enhanced Ingredient calorie database with nutritional info
ingredient_database = {
    "rice": {"calories": 206, "carbs": 45, "protein": 4, "fat": 0.5, "category": "grains"},
    "flour": {"calories": 364, "carbs": 76, "protein": 10, "fat": 1, "category": "grains"},
    "onion": {"calories": 40, "carbs": 9, "protein": 1, "fat": 0.1, "category": "vegetables"},
    "tomato": {"calories": 22, "carbs": 5, "protein": 1, "fat": 0.2, "category": "vegetables"},
    "potato": {"calories": 110, "carbs": 26, "protein": 3, "fat": 0.2, "category": "vegetables"},
    "peas": {"calories": 81, "carbs": 14, "protein": 5, "fat": 0.4, "category": "vegetables"},
    "beans": {"calories": 31, "carbs": 7, "protein": 2, "fat": 0.1, "category": "vegetables"},
    "paneer": {"calories": 265, "carbs": 4, "protein": 18, "fat": 20, "category": "dairy"},
    "chicken": {"calories": 239, "carbs": 0, "protein": 27, "fat": 14, "category": "meat"},
    "egg": {"calories": 78, "carbs": 0.6, "protein": 6, "fat": 5, "category": "protein"},
    "milk": {"calories": 42, "carbs": 5, "protein": 3, "fat": 1, "category": "dairy"},
    "curd": {"calories": 60, "carbs": 4, "protein": 3, "fat": 4, "category": "dairy"},
    "butter": {"calories": 102, "carbs": 0, "protein": 0.1, "fat": 12, "category": "dairy"},
    "oil": {"calories": 119, "carbs": 0, "protein": 0, "fat": 14, "category": "fats"},
    "spinach": {"calories": 23, "carbs": 4, "protein": 3, "fat": 0.4, "category": "vegetables"},
    "garlic": {"calories": 149, "carbs": 33, "protein": 6, "fat": 0.5, "category": "vegetables"},
    "ginger": {"calories": 80, "carbs": 18, "protein": 2, "fat": 0.8, "category": "vegetables"},
    "cheese": {"calories": 113, "carbs": 1, "protein": 7, "fat": 9, "category": "dairy"},
    "bread": {"calories": 80, "carbs": 15, "protein": 3, "fat": 1, "category": "grains"},
    "honey": {"calories": 21, "carbs": 5, "protein": 0, "fat": 0, "category": "sweeteners"},
    "sugar": {"calories": 16, "carbs": 4, "protein": 0, "fat": 0, "category": "sweeteners"},
    "corn": {"calories": 86, "carbs": 19, "protein": 3, "fat": 1, "category": "vegetables"},
    "capsicum": {"calories": 40, "carbs": 9, "protein": 2, "fat": 0.2, "category": "vegetables"},
    "mushroom": {"calories": 22, "carbs": 3, "protein": 3, "fat": 0.3, "category": "vegetables"},
    "lentils": {"calories": 116, "carbs": 20, "protein": 9, "fat": 0.4, "category": "protein"},
    "oats": {"calories": 389, "carbs": 66, "protein": 17, "fat": 7, "category": "grains"},
    "coconut": {"calories": 354, "carbs": 15, "protein": 3, "fat": 33, "category": "fruits"},
    "fish": {"calories": 200, "carbs": 0, "protein": 22, "fat": 12, "category": "seafood"},
    "pasta": {"calories": 130, "carbs": 25, "protein": 5, "fat": 1, "category": "grains"},
    "tomato sauce": {"calories": 29, "carbs": 6, "protein": 1, "fat": 0.2, "category": "sauces"},
    "cream": {"calories": 52, "carbs": 1, "protein": 1, "fat": 5, "category": "dairy"},
    "beef": {"calories": 250, "carbs": 0, "protein": 26, "fat": 17, "category": "meat"},
    "pork": {"calories": 260, "carbs": 0, "protein": 25, "fat": 18, "category": "meat"},
    "chocolate": {"calories": 546, "carbs": 60, "protein": 5, "fat": 31, "category": "sweets"},
    "coffee": {"calories": 2, "carbs": 0, "protein": 0, "fat": 0, "category": "beverages"},
    "tea": {"calories": 2, "carbs": 0, "protein": 0, "fat": 0, "category": "beverages"},
    "carrot": {"calories": 41, "carbs": 10, "protein": 1, "fat": 0.2, "category": "vegetables"},
    "cabbage": {"calories": 25, "carbs": 6, "protein": 1, "fat": 0.1, "category": "vegetables"},
    "apple": {"calories": 95, "carbs": 25, "protein": 0, "fat": 0.3, "category": "fruits"},
    "banana": {"calories": 89, "carbs": 23, "protein": 1, "fat": 0.3, "category": "fruits"},
    "shrimp": {"calories": 99, "carbs": 0, "protein": 24, "fat": 1, "category": "seafood"},
    "eggplant": {"calories": 25, "carbs": 6, "protein": 1, "fat": 0.2, "category": "vegetables"},
    "broccoli": {"calories": 35, "carbs": 7, "protein": 2, "fat": 0.4, "category": "vegetables"},
    "lettuce": {"calories": 15, "carbs": 3, "protein": 1, "fat": 0.2, "category": "vegetables"},
    "cauliflower": {"calories": 25, "carbs": 5, "protein": 2, "fat": 0.3, "category": "vegetables"},
    "quinoa": {"calories": 120, "carbs": 21, "protein": 4, "fat": 2, "category": "grains"},
    "olive oil": {"calories": 119, "carbs": 0, "protein": 0, "fat": 14, "category": "fats"},
    "yogurt": {"calories": 59, "carbs": 4, "protein": 10, "fat": 0.4, "category": "dairy"},
    "tofu": {"calories": 76, "carbs": 2, "protein": 8, "fat": 4, "category": "protein"},
    "bell pepper": {"calories": 31, "carbs": 6, "protein": 1, "fat": 0.3, "category": "vegetables"},
    "zucchini": {"calories": 17, "carbs": 3, "protein": 1, "fat": 0.3, "category": "vegetables"},
    "soy sauce": {"calories": 8, "carbs": 1, "protein": 1, "fat": 0, "category": "sauces"},
    "vinegar": {"calories": 18, "carbs": 0, "protein": 0, "fat": 0, "category": "sauces"},
    "lemon": {"calories": 29, "carbs": 9, "protein": 1, "fat": 0.3, "category": "fruits"},
    "lime": {"calories": 30, "carbs": 11, "protein": 1, "fat": 0.2, "category": "fruits"},
    "cucumber": {"calories": 15, "carbs": 4, "protein": 1, "fat": 0.1, "category": "vegetables"},
    "avocado": {"calories": 160, "carbs": 9, "protein": 2, "fat": 15, "category": "fruits"},
    "sweet potato": {"calories": 86, "carbs": 20, "protein": 2, "fat": 0.1, "category": "vegetables"},
    "turkey": {"calories": 189, "carbs": 0, "protein": 29, "fat": 7, "category": "meat"},
    "salmon": {"calories": 208, "carbs": 0, "protein": 22, "fat": 13, "category": "seafood"},
    "tuna": {"calories": 132, "carbs": 0, "protein": 29, "fat": 1, "category": "seafood"},
    "bacon": {"calories": 541, "carbs": 1, "protein": 37, "fat": 42, "category": "meat"},
    "sausage": {"calories": 324, "carbs": 2, "protein": 14, "fat": 29, "category": "meat"},
    "nuts": {"calories": 607, "carbs": 21, "protein": 20, "fat": 54, "category": "protein"},
    "berries": {"calories": 57, "carbs": 14, "protein": 1, "fat": 0.3, "category": "fruits"},
    "orange": {"calories": 62, "carbs": 15, "protein": 1, "fat": 0.2, "category": "fruits"},
    "grape": {"calories": 69, "carbs": 18, "protein": 1, "fat": 0.2, "category": "fruits"},
    "pomegranate": {"calories": 83, "carbs": 19, "protein": 2, "fat": 1, "category": "fruits"},
    "mango": {"calories": 60, "carbs": 15, "protein": 1, "fat": 0.4, "category": "fruits"}
}

# Enhanced substitutes with health benefits
substitutes = {
    "sugar": {"name": "honey", "benefit": "Natural antioxidants, lower glycemic index"},
    "butter": {"name": "olive oil", "benefit": "Heart-healthy monounsaturated fats"},
    "cream": {"name": "greek yogurt", "benefit": "Higher protein, lower fat"},
    "rice": {"name": "quinoa", "benefit": "Complete protein, more fiber"},
    "paneer": {"name": "tofu", "benefit": "Lower calories, plant-based protein"},
    "white bread": {"name": "whole wheat bread", "benefit": "More fiber, nutrients"},
    "pasta": {"name": "zucchini noodles", "benefit": "Low carb, more vitamins"},
    "potato": {"name": "sweet potato", "benefit": "More fiber, vitamin A"},
    "mayonnaise": {"name": "avocado", "benefit": "Healthy fats, vitamins"},
    "sour cream": {"name": "plain yogurt", "benefit": "Probiotics, lower fat"},
    "beef": {"name": "mushroom", "benefit": "Low calorie, plant-based"},
    "chicken": {"name": "tofu", "benefit": "Plant-based, cholesterol-free"},
    "pork": {"name": "turkey", "benefit": "Leaner protein, lower fat"},
    "fried": {"name": "baked/grilled", "benefit": "Lower fat, fewer calories"}
}

# Dietary restrictions mapping
dietary_categories = {
    "vegetarian": ["meat", "seafood", "poultry"],
    "vegan": ["meat", "seafood", "poultry", "dairy", "egg"],
    "gluten_free": ["grains"],
    "low_carb": ["grains", "sweeteners", "fruits"],
    "dairy_free": ["dairy"]
}

# Enhanced Recipe Database with cooking time and instructions
recipes = [
    # Indian Cuisine
    {
        "name": "Paneer Butter Masala", 
        "ingredients": ["paneer", "tomato", "butter", "cream", "onion", "garlic", "ginger"], 
        "calories": 420, 
        "cuisine": "Indian",
        "cooking_time": 30,
        "difficulty": "Medium",
        "instructions": [
            "Sauté onions, garlic, and ginger until golden",
            "Add tomatoes and cook until soft",
            "Blend into a smooth paste",
            "Add butter, cream, and spices",
            "Add paneer cubes and simmer for 10 minutes"
        ],
        "tags": ["vegetarian", "rich", "creamy"]
    },
    {
        "name": "Chicken Biryani", 
        "ingredients": ["chicken", "rice", "onion", "yogurt", "garlic", "ginger"], 
        "calories": 520, 
        "cuisine": "Indian",
        "cooking_time": 60,
        "difficulty": "Hard",
        "instructions": [
            "Marinate chicken with yogurt and spices",
            "Partially cook rice with whole spices",
            "Layer chicken and rice in a pot",
            "Cook on low heat for 30 minutes",
            "Garnish with fried onions and herbs"
        ],
        "tags": ["non-vegetarian", "festive", "aromatic"]
    },
    {
        "name": "Dal Tadka", 
        "ingredients": ["lentils", "onion", "tomato", "garlic", "ginger"], 
        "calories": 280, 
        "cuisine": "Indian",
        "cooking_time": 25,
        "difficulty": "Easy",
        "instructions": [
            "Cook lentils until soft",
            "Temper with spices in oil",
            "Add onions, tomatoes and cook",
            "Combine with lentils and simmer"
        ],
        "tags": ["vegetarian", "healthy", "protein-rich"]
    },
    
    # French Cuisine
    {
        "name": "Ratatouille", 
        "ingredients": ["eggplant", "tomato", "onion", "zucchini", "bell pepper"], 
        "calories": 260, 
        "cuisine": "French",
        "cooking_time": 45,
        "difficulty": "Medium",
        "instructions": [
            "Slice all vegetables thinly",
            "Layer in a baking dish",
            "Add herbs and olive oil",
            "Bake until tender and golden"
        ],
        "tags": ["vegetarian", "vegan", "healthy"]
    },
    {
        "name": "French Onion Soup", 
        "ingredients": ["onion", "cheese", "bread", "butter"], 
        "calories": 320, 
        "cuisine": "French",
        "cooking_time": 50,
        "difficulty": "Medium",
        "instructions": [
            "Caramelize onions slowly in butter",
            "Add broth and simmer",
            "Top with bread and cheese",
            "Broil until cheese is bubbly"
        ],
        "tags": ["vegetarian", "comfort-food"]
    },
    
    # Italian Cuisine
    {
        "name": "Margherita Pizza", 
        "ingredients": ["flour", "cheese", "tomato", "olive oil", "basil"], 
        "calories": 450, 
        "cuisine": "Italian",
        "cooking_time": 35,
        "difficulty": "Medium",
        "instructions": [
            "Prepare pizza dough and let rise",
            "Roll out dough and add toppings",
            "Bake in hot oven until crispy",
            "Garnish with fresh basil"
        ],
        "tags": ["vegetarian", "classic", "cheesy"]
    },
    {
        "name": "Pasta Alfredo", 
        "ingredients": ["pasta", "cream", "cheese", "butter", "garlic"], 
        "calories": 490, 
        "cuisine": "Italian",
        "cooking_time": 25,
        "difficulty": "Easy",
        "instructions": [
            "Cook pasta al dente",
            "Make creamy sauce with cheese",
            "Combine pasta with sauce",
            "Garnish with parsley"
        ],
        "tags": ["vegetarian", "creamy", "rich"]
    },
    
    # Chinese Cuisine
    {
        "name": "Fried Rice", 
        "ingredients": ["rice", "egg", "onion", "carrot", "soy sauce"], 
        "calories": 350, 
        "cuisine": "Chinese",
        "cooking_time": 20,
        "difficulty": "Easy",
        "instructions": [
            "Use day-old cooked rice",
            "Scramble eggs and set aside",
            "Stir-fry vegetables",
            "Combine all ingredients and season"
        ],
        "tags": ["quick", "versatile", "asian"]
    },
    {
        "name": "Vegetable Chow Mein", 
        "ingredients": ["flour", "onion", "carrot", "cabbage", "soy sauce"], 
        "calories": 370, 
        "cuisine": "Chinese",
        "cooking_time": 25,
        "difficulty": "Medium",
        "instructions": [
            "Cook noodles according to package",
            "Stir-fry vegetables until crisp",
            "Add noodles and sauce",
            "Toss everything together"
        ],
        "tags": ["vegetarian", "noodles", "stir-fry"]
    },
    
    # American Cuisine
    {
        "name": "Cheeseburger", 
        "ingredients": ["beef", "cheese", "bread", "onion", "tomato"], 
        "calories": 520, 
        "cuisine": "American",
        "cooking_time": 20,
        "difficulty": "Easy",
        "instructions": [
            "Form beef patties and season",
            "Grill or pan-fry to desired doneness",
            "Toast buns and assemble burger",
            "Add cheese, vegetables, and condiments"
        ],
        "tags": ["non-vegetarian", "classic", "comfort-food"]
    },
    {
        "name": "Avocado Quinoa Bowl", 
        "ingredients": ["quinoa", "avocado", "tomato", "lemon", "olive oil", "cucumber"], 
        "calories": 380, 
        "cuisine": "Continental",
        "cooking_time": 20,
        "difficulty": "Easy",
        "instructions": [
            "Cook quinoa according to package instructions",
            "Dice avocado, tomato, and cucumber",
            "Mix with lemon juice and olive oil",
            "Combine with quinoa and season"
        ],
        "tags": ["vegan", "gluten-free", "healthy", "quick"]
    }
]

@app.route('/')
def home():
    session.setdefault('favorites', [])
    session.setdefault('dietary_restrictions', [])
    session.setdefault('cooking_time_filter', 120)
    return render_template('index.html', ingredients=list(ingredient_database.keys()))

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        user_ingredients = set(data.get("ingredients", []))
        cuisine_filter = data.get("cuisine", "all")
        dietary_restrictions = data.get("dietary_restrictions", [])
        max_cooking_time = data.get("max_cooking_time", 120)
        
        logger.info(f"Recipe request: {user_ingredients}, {cuisine_filter}, {dietary_restrictions}")

        # Filter by cuisine first
        if cuisine_filter == "all":
            filtered_recipes = recipes.copy()
        else:
            filtered_recipes = [r for r in recipes if r["cuisine"].lower() == cuisine_filter.lower()]
        
        # Apply dietary restrictions
        if dietary_restrictions:
            filtered_recipes = apply_dietary_restrictions(filtered_recipes, dietary_restrictions)
        
        # Apply cooking time filter
        filtered_recipes = [r for r in filtered_recipes if r.get("cooking_time", 60) <= max_cooking_time]
        
        # Score recipes by ingredient matches and other factors
        scored_recipes = []
        for recipe in filtered_recipes:
            recipe_ingredients = set(recipe["ingredients"])
            matches = user_ingredients.intersection(recipe_ingredients)
            match_score = len(matches) / len(recipe_ingredients) if recipe_ingredients else 0
            
            # Bonus for recipes with fewer missing ingredients
            missing_ingredients = list(recipe_ingredients - user_ingredients)
            missing_penalty = len(missing_ingredients) * 0.1
            
            # Adjust score based on cooking time (shorter = better)
            time_score = max(0, 1 - (recipe.get("cooking_time", 60) / 120))
            
            final_score = (match_score * 0.7) + (time_score * 0.3) - missing_penalty
            
            if final_score > 0.1:  # Only include recipes with reasonable match
                scored_recipes.append({
                    **recipe,
                    "match_score": final_score,
                    "missing_ingredients": missing_ingredients,
                    "matched_ingredients": list(matches),
                    "match_percentage": int(final_score * 100)
                })
        
        # Sort by best matches first
        scored_recipes.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Calculate detailed nutritional information
        nutritional_info = calculate_nutritional_info(user_ingredients)
        
        # Find suggested substitutes with benefits
        suggested_subs = {}
        for ingredient in user_ingredients:
            if ingredient in substitutes:
                suggested_subs[ingredient] = substitutes[ingredient]
        
        # If no matches found, provide some random recipes from filtered list
        if not scored_recipes and filtered_recipes:
            random_recipes = random.sample(filtered_recipes, min(3, len(filtered_recipes)))
            scored_recipes = [{**r, "match_score": 0.1, "missing_ingredients": r["ingredients"], 
                             "matched_ingredients": [], "match_percentage": 10} for r in random_recipes]
        
        return jsonify({
            "recipes": scored_recipes[:8],
            "nutritional_info": nutritional_info,
            "substitutes": suggested_subs,
            "total_recipes_found": len(scored_recipes)
        })
        
    except Exception as e:
        logger.error(f"Error in get_recipe: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

def apply_dietary_restrictions(recipes_list, restrictions):
    """Filter recipes based on dietary restrictions"""
    filtered_recipes = []
    
    for recipe in recipes_list:
        include_recipe = True
        
        # Get all ingredients' categories for this recipe
        recipe_categories = set()
        for ingredient in recipe["ingredients"]:
            if ingredient in ingredient_database:
                recipe_categories.add(ingredient_database[ingredient]["category"])
        
        # Check against each restriction
        for restriction in restrictions:
            if restriction in dietary_categories:
                forbidden_categories = dietary_categories[restriction]
                if any(category in recipe_categories for category in forbidden_categories):
                    include_recipe = False
                    break
        
        if include_recipe:
            filtered_recipes.append(recipe)
    
    return filtered_recipes

def calculate_nutritional_info(ingredients):
    """Calculate detailed nutritional information for selected ingredients"""
    total_calories = 0
    total_carbs = 0
    total_protein = 0
    total_fat = 0
    categories = {}
    
    for ingredient in ingredients:
        if ingredient in ingredient_database:
            info = ingredient_database[ingredient]
            total_calories += info["calories"]
            total_carbs += info["carbs"]
            total_protein += info["protein"]
            total_fat += info["fat"]
            
            # Track categories
            category = info["category"]
            categories[category] = categories.get(category, 0) + 1
    
    return {
        "total_calories": total_calories,
        "total_carbs": round(total_carbs, 1),
        "total_protein": round(total_protein, 1),
        "total_fat": round(total_fat, 1),
        "category_breakdown": categories,
        "ingredient_count": len(ingredients)
    }

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    try:
        recipe = request.json.get("recipe")
        if recipe and not any(fav.get('name') == recipe.get('name') for fav in session.get('favorites', [])):
            session['favorites'].append(recipe)
            session.modified = True
            logger.info(f"Added favorite: {recipe.get('name')}")
        return jsonify({"success": True, "favorites": session['favorites']})
    except Exception as e:
        logger.error(f"Error saving favorite: {str(e)}")
        return jsonify({"error": "Failed to save favorite"}), 500

@app.route('/get_favorites')
def get_favorites():
    return jsonify({"favorites": session.get('favorites', [])})

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    try:
        recipe_name = request.json.get("recipe_name")
        session['favorites'] = [r for r in session.get('favorites', []) if r.get('name') != recipe_name]
        session.modified = True
        logger.info(f"Removed favorite: {recipe_name}")
        return jsonify({"success": True, "favorites": session['favorites']})
    except Exception as e:
        logger.error(f"Error removing favorite: {str(e)}")
        return jsonify({"error": "Failed to remove favorite"}), 500

@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    try:
        preferences = request.json
        session['dietary_restrictions'] = preferences.get('dietary_restrictions', [])
        session['cooking_time_filter'] = preferences.get('cooking_time_filter', 120)
        session.modified = True
        return jsonify({"success": True, "message": "Preferences saved"})
    except Exception as e:
        logger.error(f"Error saving preferences: {str(e)}")
        return jsonify({"error": "Failed to save preferences"}), 500

@app.route('/get_ingredient_info/<ingredient_name>')
def get_ingredient_info(ingredient_name):
    """Get detailed information about a specific ingredient"""
    if ingredient_name in ingredient_database:
        return jsonify({
            "success": True,
            "ingredient": ingredient_name,
            "info": ingredient_database[ingredient_name]
        })
    else:
        return jsonify({
            "success": False,
            "error": "Ingredient not found"
        }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
