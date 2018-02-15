'''
User Profiler
'''

import random
import json
import taster

class Profile:
  def __init__(self, dishlistfile='testset.json', history=20):
    self.flavourlist = ["salt", "sweet", "rich"]

    with open(dishlistfile) as ifile:
      self.items = json.load(ifile)

    self.history = random.sample(self.items, k=history)
    self.taste = self.init_profile()

  def init_profile(self):
    _taste = dict()
    for flavour in self.flavourlist:
      _taste[flavour] = 0.0

    for dish in self.history:
      tastedict = taster.taste(dish)
      print(tastedict)
      for flavour in self.flavourlist:
        _taste[flavour] += tastedict[flavour]

    for flavour in self.flavourlist:
      _taste[flavour] /= len(self.history)

    return _taste

  def dish_titles(self):
    return [food["dish_name"] for food in self.history]

  def __str__(self):
    return str(zip(self.dish_titles(), [taster.taste(food) for food in self.history]))

if __name__ == "__main__":
  print(Profile())
