import unittest
from datetime import datetime, timedelta
from app.utils.widmark import calculate_bac

# Compared value using https://www.drinkdriving.org/bac-calculator.php

class TestCalculateBAC(unittest.TestCase):

    def test_calculate_bac_male(self):
        weight = 70  # kg
        abv = 5  # 5% alcohol by volume
        volume = 568  # ml
        gender = "male"
        time = datetime.now() - timedelta(hours=1)
        
        bac = calculate_bac(weight, abv, volume, gender, time)
        self.assertAlmostEqual(bac,  0.03207, places=3)

    def test_calculate_bac_female(self):
        weight = 60  # kg
        abv = 8  # 8% alcohol by volume
        volume = 568  # ml
        gender = "female"
        time = datetime.now() - timedelta(hours=2)
        
        bac = calculate_bac(weight, abv, volume, gender, time)
        self.assertAlmostEqual(bac, 0.07864, places=3)

    def test_calculate_bac_no_burn_off(self):
        weight = 80  # kg
        abv = 4  # 8% alcohol by volume
        volume = 568  # ml
        gender = "male"
        time = datetime.now()
        
        bac = calculate_bac(weight, abv, volume, gender, time)
        self.assertAlmostEqual(bac,  0.03295, places=3)

if __name__ == '__main__':
    unittest.main()