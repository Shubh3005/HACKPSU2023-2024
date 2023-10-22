# weight in kg, height in cm
def calculateBMR(weight, height, age, sex):
    if sex == "Female":
        return 655.1 + (9.563*weight) + (1.850*height) - (4.676*age)
    elif sex == "Male":
        return 66.47 + (13.75*weight) + (5.003*height) - (6.755*age)

def calculateAMR(BMR, exercise_lvl):
    if exercise_lvl == "Sedentary":
        return BMR * 1.2
    elif exercise_lvl == "Light":
        return BMR * 1.375
    elif exercise_lvl == "Moderate":
        return BMR * 1.55
    elif exercise_lvl == "Active":
        return BMR * 1.725
    elif exercise_lvl == "Very Active":
        return BMR * 1.9