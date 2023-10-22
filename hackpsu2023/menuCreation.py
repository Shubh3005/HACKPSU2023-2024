# from home import DIETARY_RESTIRICTIONS, DAILY_CALORIE_INTAKE
import csv
DIETARY_RESTIRICTIONS=[]


# # WILL GET FROM calculator with data from for, neccesary calories FIXME
# DAILY_CALORIE_INTAKE = 0

BREAKFAST_PROPORTION = 0.2
LUNCH_PROPORTION = 0.4
DINNER_PROPORTION = 0.4

PROTEIN_PROPORTION = 0.225
CARBS_PROPORTION = 0.55
FATS_PROPORTION = 0.27

# WILL GET FROM FORM --> list for now with random stuff 
# DIETARY_RESTIRICTIONS = ["M", "H"]

normalMet = {
    "Grains" : False,
    "Vegetables" : False,
    "Proteins" : False,
}

# takes in the proportion of daily calories are allocated per breakfast, lunch, and dinner
def caloriesPerTime(amr,proportion):
    return amr*proportion

# takes in the calories allocated per mealtime and returns the number of calories depending on the macronutrient
def caloriesFromMacro(timeCalories, macro):
    if macro == "p" or macro == "Protein":
        return int(PROTEIN_PROPORTION*timeCalories)+1
    elif macro == "c" or macro == "Carbs":
        return int(CARBS_PROPORTION*timeCalories)+1
    elif macro == "f" or macro == "Fats":
        return int(FATS_PROPORTION*timeCalories)+1
    else:
        return None
    

# DO .strip() after every access to a variable!!

##### BREAKFAST #####
breakfastData = []
with open('Breakfast.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        breakfastData.append(row)
    # print(breakfastData)
#####  #####

##### LUNCH #####
lunchData = []
with open('Lunch.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        lunchData.append(row)

##### DINNER #####
dinnerData = []
with open('Dinner.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        dinnerData.append(row)

#####
# 0 --> name
# 1 --> calories
# 2 --> restrictions
# 3 --> macro
# 4 --> type
#####


def stripList(lst):
    newList = []
    for item in lst:
        newList.append(item.strip())
    return newList


# input is the mealtime as a string
# output is a list of foods that the user can eat
# dietary_restrictions is DIETARY_RESTIRICTIONS for now
def checkDietRestrictions(mealtime_dataset, dietary_restrictions):


    foodsAllowed = []
    header = mealtime_dataset[0]# the titles
    # print(mealtime_dataset[1])
    for i in range(1,len(mealtime_dataset)): # going through the rows, starting from index 1 becuase the one previous is the header
        # print(mealtime_dataset[i][2])
        restrictions = (mealtime_dataset[i][2].strip()).split(';') # getting a list of restrictions ("M","H","Gf","V","P","None")
        restrictions = stripList(restrictions)
        
        boolFlag = True
        for r in dietary_restrictions:
            # print(f"r = {r}")
            if r == "NP" and "P" in restrictions:
                boolFlag = False
            if r == "M" and "V" in restrictions:
                continue
            if 'None' not in restrictions and r not in restrictions:
                # print(f"{r} not in restrictions")
                boolFlag = False
            
        if boolFlag == True:
            foodsAllowed.append(mealtime_dataset[i][0])
            # print("appended!")
    # print(foodsAllowed)
    return foodsAllowed


# print(foods)


def createPlan(mealtime_dataset, mealCalories, foodsAllowed):
    plan = []

    ##### MACRO Calorie Counters #####
    mealProteinCalCount = 0
    mealCarbsCalCount = 0
    mealFatsCalCount = 0

    
    # print(f"plan = {plan}")
    mealCalorieCounter = 0
    # STEP 1: CALORIE INTAKE MUST BE MET    
    # for i in range(1,len(mealtime_dataset)): # going through the rows, starting from index 1 becuase the one previous is the header
    i = 1 # i is the row number !!!
    loopNumber = 0
    lengthOfMenu = len(mealtime_dataset) - 1 # have to subtract one to account for the header
    while mealCalorieCounter < mealCalories and loopNumber < lengthOfMenu:
        name = mealtime_dataset[i][0].strip()
        if name in foodsAllowed: 
        # for name in foodsAllowed:
        #     for i in range(1, len(mealtime_dataset)):

            
            # print(f"plan = {plan}")
            cal = mealtime_dataset[i][1].strip()
            # print(f"cal = {cal}")
            cal = int(cal) # total calories of that FOOD
            if mealCalorieCounter + cal - mealCalories > 50: #upper margin is 50 cal
                loopNumber += 1
                continue
            ####
            
            plan.append(name)
            ####
            mealCalorieCounter += cal
            # for step 2:
            normalCategory = mealtime_dataset[i][4].strip()
            normalMet[normalCategory] = True
            
            # for step 3:
            macroCategories = stripList((mealtime_dataset[i][3].strip()).split(';'))
            for macro in macroCategories:
                if macro == "Protein":
                    mealProteinCalCount += caloriesFromMacro(cal, "p")
                elif macro == "Carbs":
                    mealCarbsCalCount += caloriesFromMacro(cal, "c")
                elif macro == "Fats":
                    mealFatsCalCount += caloriesFromMacro(cal, "f")

        i += 1
        i %= lengthOfMenu
        if i == 0:
            i+=1

    # print("plan after step1", plan)

    # STEP 2: MyPlate
    for key in normalMet:
        if normalMet[key] == False: # if category is not met yet, then do a pass
            
            for name in foodsAllowed:
                for j in range(1, len(mealtime_dataset)):

                    if name == mealtime_dataset[j]:
                        normalCategory = mealtime_dataset[i][4].strip()
                        if normalCategory == key:
                            ####
                            
                            plan.append(name)
                            ####


                            normalMet[normalCategory] = True
                            # for step 3
                            
                            foodCal = mealtime_dataset[i][1].strip()
                            foodCal = int(foodCal) # total calories of that FOOD

                            macroCategories = stripList((mealtime_dataset[i][3].strip()).split(';'))
                            for macro in macroCategories:
                                if macro == "Protein":
                                    mealProteinCalCount += caloriesFromMacro(foodCal, "p")
                                elif macro == "Carbs":
                                    mealCarbsCalCount += caloriesFromMacro(foodCal, "c")
                                elif macro == "Fats":
                                    mealFatsCalCount += caloriesFromMacro(foodCal, "f")
    



    # print(f"mealCalorieCounter = {mealCalorieCounter}")

    # # # STEP 3: Macro
    mealProteinCalories = caloriesFromMacro(mealCalories, "p")
    # print(f"mealProteinCalories = {mealProteinCalories}")
    mealCarbsCalories = caloriesFromMacro(mealCalories, "c")
    mealFatsCalories = caloriesFromMacro(mealCalories, "f")
    
    # print(f"mealProteinCalCount = {mealProteinCalCount}")
    proteinRow = 1
    loopNumberProtein = 0
    while mealProteinCalCount < mealProteinCalories and loopNumberProtein < lengthOfMenu:

        # for name in foodsAllowed:
            # for proteinRow in range(1,len(mealtime_dataset)):
        name = mealtime_dataset[proteinRow][0].strip()
        if name in foodsAllowed: 
            macroCategories = stripList((mealtime_dataset[proteinRow][3].strip()).split(';'))
            # print(macroCategories)
            
            if "Protein" in macroCategories:
                
                foodCal = mealtime_dataset[proteinRow][1].strip()
                foodCal = int(foodCal) # total calories of that FOOD
                
                if mealCalorieCounter + foodCal - mealCalories > 50: #upper margin is 50 cal
                    loopNumberProtein += 1
                    continue
                ####
                
                plan.append(name)
                ####
                mealProteinCalCount += caloriesFromMacro(foodCal, "p")
                mealCalorieCounter += foodCal
                
                for macro in macroCategories:
                    if macro == "Carbs":
                        # print("foodCal from carbs",foodCal)
                        mealCarbsCalCount += caloriesFromMacro(foodCal, "c")
                    elif macro == "Fats":
                        mealFatsCalCount += caloriesFromMacro(foodCal, "f")
            
        proteinRow += 1
        proteinRow %= lengthOfMenu
        if proteinRow == 0:
            proteinRow += 1

                    
    carbRow = 1
    loopNumberCarbs = 0
    while mealCarbsCalCount < mealCarbsCalories and loopNumberCarbs < lengthOfMenu:

        name = mealtime_dataset[carbRow][0].strip()
        if name in foodsAllowed: 
            macroCategories = stripList((mealtime_dataset[carbRow][3].strip()).split(';'))
            # print(macroCategories)
            
            if "Carbs" in macroCategories:
                
                foodCal = mealtime_dataset[carbRow][1].strip()
                foodCal = int(foodCal) # total calories of that FOOD
                
                if mealCalorieCounter + foodCal - mealCalories > 50: #upper margin is 50 cal
                    loopNumberCarbs += 1
                    continue
                ####
                plan.append(name)
                ####
                mealCarbsCalCount += caloriesFromMacro(foodCal, "c")
                mealCalorieCounter += foodCal
                
                for macro in macroCategories:
                    if macro == "Protein":
                        # print("foodCal from carbs",foodCal)
                        mealProteinCalCount += caloriesFromMacro(foodCal, "p")
                    elif macro == "Fats":
                        mealFatsCalCount += caloriesFromMacro(foodCal, "f")
            
        carbRow += 1
        carbRow %= lengthOfMenu
        if carbRow == 0:
            carbRow += 1

    fatRow = 1
    loopNumberFats = 0
    while mealCarbsCalCount < mealFatsCalories and loopNumberFats < lengthOfMenu:

        name = mealtime_dataset[fatRow][0].strip()
        if name in foodsAllowed: 
            macroCategories = stripList((mealtime_dataset[fatRow][3].strip()).split(';'))
            # print(macroCategories)
            
            if "Fats" in macroCategories:
                
                foodCal = mealtime_dataset[fatRow][1].strip()
                foodCal = int(foodCal) # total calories of that FOOD
                
                if mealCalorieCounter + foodCal - mealCalories > 50: #upper margin is 50 cal
                    loopNumberFats += 1
                    continue
                ####
                plan.append(name)
                ####
                mealCarbsCalCount += caloriesFromMacro(foodCal, "f")
                mealCalorieCounter += foodCal
                
                for macro in macroCategories:
                    if macro == "Protein":
                        # print("foodCal from carbs",foodCal)
                        mealProteinCalCount += caloriesFromMacro(foodCal, "p")
                    elif macro == "Fats":
                        mealCarbsCalCount += caloriesFromMacro(foodCal, "c")
            
        fatRow += 1
        fatRow %= lengthOfMenu
        if fatRow == 0:
            fatRow += 1
    

    counts = {}
    for m in range(len(plan)):
        count = plan.count(plan[m])
        counts[plan[m]] = count
    plan = list(set(plan))

    for key, value in counts.items():
        if value > 1:
            n = plan.index(key)
            plan[n] = key + f" x {value}"



    
    # print(f"mealCalorieCounter = {mealCalorieCounter}")
    # print(f"mealCalories = {mealCalories}")
    # print(mealProteinCalCount)
    # print(mealProteinCalories)
    return (plan,mealCalorieCounter)




# breakfastCalories = caloriesPerTime(0.2)
# lunchCalories = caloriesPerTime(0.4)
# dinnerCalories = caloriesPerTime(0.4)

# breakfast_foods = checkDietRestrictions(breakfastData, DIETARY_RESTIRICTIONS)
# lunch_foods = checkDietRestrictions(lunchData, DIETARY_RESTIRICTIONS)
# dinner_foods = checkDietRestrictions(dinnerData, DIETARY_RESTIRICTIONS)

# breakfastPlan, bCalories = createPlan(breakfastData, breakfastCalories, breakfast_foods)
# lunchPlan, lCalories = createPlan(lunchData, lunchCalories,lunch_foods)
# dinnerPlan, dCalories = createPlan(dinnerData, dinnerCalories, dinner_foods)

# print(f"breakfastPlan = {breakfastPlan}, Calories: {breakfastCalories}")
# print(f"lunchPlan = {lunchPlan}, Calories: {lunchCalories}")
# # print(f"lunch allowed foods = {lunch_foods}")
# print(f"dinnerPlan = {dinnerPlan}, Calories: {dinnerCalories}")