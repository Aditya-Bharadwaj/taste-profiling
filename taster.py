import json
import glob, sys
import re
import itertools
import numpy

SWEET_FACTOR_X = 0.9
SWEET_FACTOR_Y = 0.1

RICHNESS_FACTOR_X = 0.5
RICHNESS_FACTOR_Y = 0.7
RICHNESS_FACTOR_Z = 50

SOURNESS_FACTOR_X = 0.1
SOURNESS_FACTOR_Y = 0.25
SOURNESS_FACTOR_Z = 0.5


def sweet(nutrition_data, SWEET_FACTOR_X=0.85, SWEET_FACTOR_Y=0.1):
	try:
		total_weight = nutrition_data['Weight']
		fibtg = 0
		if 'Dietary_Fiber' in nutrition_data:
				fibtg = nutrition_data['Dietary_Fiber']
		sweet_score_x1 = abs(nutrition_data['Sugar'] - fibtg) / total_weight
		sweet_score_y = nutrition_data['Sugar'] / nutrition_data['Carbs'] 
		sweet_score_1 = (SWEET_FACTOR_X * sweet_score_x1) + (SWEET_FACTOR_Y * sweet_score_y)
		#	print(sweet_score_1)
	except Exception as e:
		sweet_score_1 = 0
	return round(sweet_score_1 / 0.998,3) * 10

def rich(nutrition_data, RICHNESS_FACTOR_X=0.5, RICHNESS_FACTOR_Y=0.7,RICHNESS_FACTOR_Z=50):
	try:
		#total_weight = nutrition_data['metric_qty']
		total_weight = nutrition_data['Weight']
		richness_score_x = 0
		if 'Sat_Fat' in nutrition_data:
			richness_score_x = nutrition_data['Sat_Fat'] / nutrition_data['Fat'] #high
		#Why consider sat_fat if we're considering total fat anyway? Would make more sense if total fat wasn't available
		richness_score_y = nutrition_data['Fat'] / total_weight #low
		#Why is this not enough to work off of?
		richness_score_z = 0
		if 'Cholesterol' in nutrition_data:
			richness_score_z = nutrition_data['Cholesterol'] / (total_weight * 1000)
		#I'll admit that this is a good idea anyway
		richness_score_1 = (RICHNESS_FACTOR_X * richness_score_x) + (RICHNESS_FACTOR_Y * richness_score_y) + (RICHNESS_FACTOR_Z * richness_score_z)
	except Exception as e:
		richness_score_1 = 0

	return round((richness_score_1 / 0.992),3) * 10
	## Normalize to butter which has highest score

def salt(dish_nutrition):
	totalweight = dish_nutrition['Weight']
	if totalweight == 0:
		return 0
	#return((dish_nutrition['sodium'] / dish_nutrition['metric_qty']))
	#print((dish_nutrition['sodium'] / dish_nutrition['metric_qty']) / 38.758, end=' | ')
	return ((1000 * dish_nutrition['Sodium'] / totalweight)) / 3.8758

def get_dishes():
	with open('testset.json') as json_file:
		foods_list = json.load(json_file)
	return foods_list

def total_weight(dish_nutrition):
	totalweight = 0
	for nutrient in dish_nutrition:
		if dish_nutrition[nutrient] is not None and 'g' in dish_nutrition[nutrient][0]:
			#print(nutrient,dish_nutrition[nutrient])
			number = re.findall('\d+\.\d+', dish_nutrition[nutrient][0])
			#print(dish_nutrition[nutrient][0],number)	
			numeric_value = float(number[0])
			totalweight += numeric_value
			#print(totalweight)
	return totalweight

def get_nutrients(food):
	nutrients = food['nutrients']
	totalweight = total_weight(nutrients)
	#print(total_weight)
	for nutrient in nutrients:
		if nutrients[nutrient] is not None:
			number = re.findall('\d+\.\d+', nutrients[nutrient][0])
			nutrients[nutrient] = float(number[0])
		else:
			nutrients[nutrient] = 0
	nutrients['Weight'] = totalweight
	return nutrients

def main():
	foods_list = get_dishes()
	for food in foods_list:
		taste_scores = dict()
		nutrients = get_nutrients(food)
		salt_score = salt(nutrients)
		taste_scores['salt'] = salt_score
		sweet_score = sweet(nutrients)
		taste_scores['sweet'] = sweet_score
		richness_score = rich(nutrients)
		taste_scores['rich'] = richness_score
		print(food['dish_name'],taste_scores)

if __name__ == '__main__':
	main()