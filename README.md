# **🍽️ NutriChef – Smart Recipe & Nutrition Recommendation System**

NutriChef is a Flask-based intelligent recipe recommendation system that suggests dishes based on user-provided ingredients, dietary preferences, cuisine filters, and cooking time limits.
It also provides **nutritional breakdown**, **healthy substitutes**, and allows users to **save favorite recipes**.

---

## ⭐ **Features**

### 🔍 **Smart Recipe Matching**

* Suggests recipes based on available ingredients
* Scores recipes using intelligent matching
* Shows missing ingredients + match percentage
* Filters by cuisine (Indian, Italian, Chinese, etc.)
* Filters by dietary restrictions (vegan, gluten-free, low-carb…)

### 🥗 **Nutrition Analysis**

* Calculates total calories, carbs, protein, and fats
* Category breakdown: vegetables, grains, dairy, etc.

### 🔄 **Healthy Substitutes**

Provides ingredient substitution with:

* Health benefits
* Lower-calorie options
* Healthier alternatives (e.g., butter → olive oil)

### ❤️ **Favorites System**

* Save recipes to user session
* Remove favorites anytime

### 🍳 **Detailed Recipe Metadata**

Each recipe includes:

* Ingredients
* Instructions
* Cuisine
* Cooking time
* Difficulty
* Tags

---

## 📁 **Project Structure**

```
NutriChef/
│── app.py
│── templates/
│   └── index.html
│── static/
│   ├── css/
│   ├── js/
│── README.md
```

---

## 🚀 **How to Run the Project**

### **1. Install Dependencies**

Make sure you have Python 3.8+ installed.

```bash
pip install flask
```

### **2. Run the Flask Server**

```bash
python app.py
```

### **3. Open in Browser**

Go to:

```
http://localhost:5000
```

---

## 🔧 **API Endpoints**

### **POST /get_recipe**

Get recipe recommendations.

#### Request Body:

```json
{
  "ingredients": ["tomato", "rice"],
  "cuisine": "Italian",
  "dietary_restrictions": ["vegan"],
  "max_cooking_time": 30
}
```

#### Response:

* Matched recipes
* Nutritional info
* Suggested substitutes

---

### **POST /save_favorite**

Stores recipe in session.

### **POST /remove_favorite**

Removes a recipe from favorites.

### **GET /get_favorites**

Returns all saved favorites.

### **GET /get_ingredient_info/<ingredient>**

Get calorie and nutrition info for any ingredient.

---

## 🧠 **Core Logic Overview**

### ✔ Ingredient Matching Algorithm

* Checks overlap between user ingredients & recipe ingredients
* Calculates a match score (0–100%)
* Applies cooking time filters
* Uses penalties for missing ingredients
* Sorts recipes by best match

### ✔ Nutritional Calculator

Summarizes:

* Total calories
* Carbs
* Protein
* Fats
* Category distribution

### ✔ Dietary Filter

Excludes recipes based on:

* vegan
* vegetarian
* dairy-free
* gluten-free
* low-carb

---

## 📌 **Technologies Used**

* **Python**
* **Flask**
* **HTML/CSS/JS**
* **Session Storage**
* **Jinja Templates**

---

## 📜 **Future Improvements (Optional)**

If you like, I can add these:

🔹 AI-based recipe generation
🔹 Calorie-based meal planner
🔹 User accounts + login system
🔹 MongoDB/Firebase integration
🔹 Weekly grocery list generator
🔹 Mobile UI optimization
