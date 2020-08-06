import pandas as pd
import datetime
import holidays as hol

# # format: MM/DD/YYYY
# START_DATE = '08/10/2020'
# END_DATE = '12/13/2020'
# # ISO code (necessary for holidays, see https://github.com/dr-prodigy/python-holidays)
# COUNTRY = 'MX'
# LOCALE = 'es_MX.utf8'
# # case for date names: lower/upper/title/capitalize/swapcase
# CASE = 'lower'

def get_days(start_date, end_date, separate_weekends=False):
    """gets a list of date indices in an interval"""
    if separate_weekends:
        wkdays = pd.bdate_range(start=start_date, end=end_date)
        sats = pd.date_range(start=start_date, end=end_date, freq='W-SAT')
        suns = pd.date_range(start=start_date, end=end_date, freq='W-SUN')
        return [wkdays, sats, suns]
    else:
        return pd.date_range(start=start_date, end=end_date)

def get_holidays(date_indices, country='MX'):
    """gets a list of strings with holidays for the dates provided"""
    holis = getattr(hol, country)()
    if isinstance(date_indices, list):
        hol_list = []
        for date_index in date_indices:
            hol_list.append([holis.get(date) for date in date_index])
        return hol_list
    else:
        return [holis.get(date) for date in date_indices]

def get_day_names(date_indices, case='lower', locale='es_MX.utf8'):
    """gets the locale-specific names for the dates provided"""
    if isinstance(date_indices, list):
        names_list = []
        for date_index in date_indices:
            names_list.append([getattr(date, case)() for date in date_index.day_name(locale)])
        return names_list
    elif isinstance(date_indices.day_name(locale), str):
        return getattr(date_indices.day_name(locale), case)()
    else:
        return [getattr(date, case)() for date in date_indices.day_name(locale)]

def get_month_names(date_indices, case='lower', locale='es_MX.utf8'):
    """gets the locale-specific names for the months of the dates provided"""
    if isinstance(date_indices, list):
        names_list = []
        for date_index in date_indices:
            names_list.append([getattr(date, case)() for date in date_index.month_name(locale)])
        return names_list
    elif isinstance(date_indices.month_name(locale), str):
        return getattr(date_indices.month_name(locale), case)()
    else:
        return [getattr(date, case)() for date in date_indices.month_name(locale)]

