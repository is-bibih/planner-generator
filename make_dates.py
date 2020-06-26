import pandas as pd
import datetime
import holidays as hol

# format: MM/DD/YYYY
START_DATE = '08/10/2020'
END_DATE = '12/13/2020'
# ISO code (necessary for holidays, see https://github.com/dr-prodigy/python-holidays)
COUNTRY = 'MX'
LOCALE = 'es_MX.utf8'
# case for date names: lower/upper/title/capitalize/swapcase
CASE = 'lower'

# lists of weekdays, saturdays and sundays
wkdays = pd.bdate_range(start=START_DATE, end=END_DATE)
sats = pd.date_range(start=START_DATE, end=END_DATE, freq='W-SAT')
suns = pd.date_range(start=START_DATE, end=END_DATE, freq='W-SUN')

# lists of holidays
holis = getattr(hol, COUNTRY)()
wkd_hol = [holis.get(date) for date in wkdays]
sat_hol = [holis.get(date) for date in sats]
sun_hol = [holis.get(date) for date in suns]

# names for the days of the week 
wkd_names = [getattr(date, CASE)() for date in wkdays.day_name(LOCALE)]
sat_name = getattr(sats[0].day_name(LOCALE), CASE)()
sun_name = getattr(suns[0].day_name(LOCALE), CASE)()

