from menuCreation import *
import caloricIntakeCalc
from flask import Flask, redirect, url_for, request
from flask import render_template
import csv

app = Flask(__name__)
# DIETARY_RESTIRICTIONS = []
# DAILY_CALORIE_INTAKE = 0
@app.route('/', methods=['GET',"POST"])
def index():
    return render_template("index.html")

@app.route('/menus', methods=["GET", "POST"])
def getInformation():
    if request.method == "POST":
        age = float(request.form.get("age"))
        weight = float(request.form.get("height"))/ 2.205 # converts from lbs to kg
        height = float(request.form.get("weight")) * 2.54 # converts from in. to cm
        exercise_lvl = request.form["exercise"]
        dietary_restrictions = request.form.getlist("dietary-restriction")
        # diet could be made up of: "Meatless", "Vegan", "Gluten-free", "Pork", "Halal"
        for item in dietary_restrictions:
            if item == "Meatless":
                DIETARY_RESTIRICTIONS.append("M")
            elif item == "Vegan":
                DIETARY_RESTIRICTIONS.append("V")
            elif item == "Gluten-free":
                DIETARY_RESTIRICTIONS.append("Gf")
            elif item == "Pork":
                DIETARY_RESTIRICTIONS.append("NP")
            elif item == "Halal":
                DIETARY_RESTIRICTIONS.append("H")
        sex = request.form["sex"]
        bmr = caloricIntakeCalc.calculateBMR(weight, height, age, sex)
        # print(bmr)
        amr = caloricIntakeCalc.calculateAMR(bmr, exercise_lvl)
        # print(amr)
    breakfastCalories = caloriesPerTime(amr,0.2)
    lunchCalories = caloriesPerTime(amr,0.4)
    dinnerCalories = caloriesPerTime(amr,0.4)

    breakfast_foods = checkDietRestrictions(breakfastData, DIETARY_RESTIRICTIONS)
    lunch_foods = checkDietRestrictions(lunchData, DIETARY_RESTIRICTIONS)
    dinner_foods = checkDietRestrictions(dinnerData, DIETARY_RESTIRICTIONS)

    breakfastPlan, bCalories = createPlan(breakfastData, breakfastCalories, breakfast_foods)
    lunchPlan, lCalories = createPlan(lunchData, lunchCalories,lunch_foods)
    dinnerPlan, dCalories = createPlan(dinnerData, dinnerCalories, dinner_foods)
    # print(breakfastPlan)
    return render_template('menus.html',
                           bP=breakfastPlan, 
                           bC=bCalories,

                           lP=lunchPlan,
                           lC=lCalories,

                           dP = dinnerPlan,
                           dC = dCalories,
                           )
    

app.run(port=5002)