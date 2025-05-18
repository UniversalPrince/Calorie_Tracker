# calorie_tracker.py

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def calculate_calorie_goal():
    print("=== User Profile ===")
    name = input("Enter your name: ")
    gender = input("Enter your gender (Male/Female/Other): ").capitalize()
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (in kg): "))
    height = float(input("Enter your height (in cm): "))

    print("\nActivity Levels:")
    print("1. Little or no exercise")
    print("2. Light (1-3 times/week)")
    print("3. Moderate (4-5 times/week)")
    print("4. Active (daily exercise)")
    activity = int(input("Select activity level (1-4): "))

    print("\nGoals:")
    print("1. Lose weight")
    print("2. Maintain weight")
    print("3. Gain weight")
    goal = int(input("Select your goal (1-3): "))

    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age

    activity_factors = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725}
    calorie_goal = bmr * activity_factors.get(activity, 1.2)

    if goal == 1:
        calorie_goal -= 300
    elif goal == 3:
        calorie_goal += 300

    print(f"\nHi {name}, your daily calorie goal is approximately {int(calorie_goal)} kcal.")
    return int(calorie_goal), name

def plot_calorie_pie(food_log, calorie_goal):
    labels = [item[0] for item in food_log]
    sizes = [item[1] for item in food_log]

    remaining = calorie_goal - sum(sizes)
    if remaining > 0:
        labels.append("Remaining")
        sizes.append(remaining)

    colors = plt.cm.Paired.colors[:len(sizes)]
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Calorie Distribution (as % of Daily Goal)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def export_to_csv(food_log, calorie_goal, username):
    df = pd.DataFrame(food_log, columns=["Food", "Calories"])
    df["Date"] = datetime.now().strftime("%Y-%m-%d")
    df["User"] = username
    df["Calorie Goal"] = calorie_goal
    df.to_csv("calorie_log.csv", index=False)
    print("\n✅ Data exported to calorie_log.csv — ready for Power BI.")

def food_calorie_tracker(calorie_goal, username):
    total_calories = 0
    food_log = []

    print("\n=== Food Calorie Tracker ===")
    while True:
        food = input("Enter food item (or type 'done' to finish): ").strip()
        if food.lower() == "done":
            break
        try:
            calories = int(input(f"Calories in {food}: "))
            total_calories += calories
            food_log.append((food, calories))
            print(f"Total so far: {total_calories}/{calorie_goal} kcal\n")
        except ValueError:
            print("Please enter a valid number for calories.")

    print("\n=== Daily Summary ===")
    for item, cal in food_log:
        print(f"{item}: {cal} kcal")
    print(f"Total Calories Consumed: {total_calories} kcal")
    print(f"Remaining Calories: {calorie_goal - total_calories} kcal")

    plot_calorie_pie(food_log, calorie_goal)
    export_to_csv(food_log, calorie_goal, username)

if __name__ == "__main__":
    goal, user = calculate_calorie_goal()
    food_calorie_tracker(goal, user)

