from datetime import datetime
from typing import Optional
MALE_RATIO=0.68
FEMALE_RATIO=0.55
BURN_RATE=0.015

def calculate_bac(weight: float,abv,volume,gender,time:datetime):
    """Calculate Blood Alcohol Content"""
    dose=volume*abv*0.789
    gender_ratio=MALE_RATIO
    if gender=="female":
        gender_ratio=FEMALE_RATIO

    bac=dose/((weight*1000)*gender_ratio)
    burned_off=calculate_burn_off(time)

    return bac-burned_off



def calculate_burn_off(datetime:datetime):
    """Calculate the burn off rate"""
    now=datetime.now()
    delta=now-datetime
    hours=delta.total_seconds()/3600
    return hours*BURN_RATE