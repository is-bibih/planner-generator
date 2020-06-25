import pandas as pd

# format: MM/DD/YYYY
START_DATE = '08/10/2020'
END_DATE = '12/13/2020'

wkdays = pd.bdate_range(start=START_DATE, end=END_DATE)
sats = pd.date_range(start=START_DATE, end=END_DATE, freq='W-SAT')
suns = pd.date_range(start=START_DATE, end=END_DATE, freq='W-SUN')
