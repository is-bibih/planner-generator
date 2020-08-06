import io
import re
import datetime
import pandas as pd
from PyPDF2 import PdfFileMerger
from cairosvg import svg2pdf

from configparser import ConfigParser

config = ConfigParser()
config.read('../config.ini')
PLACEHOLDER = config['files']['placeholder']
MONTH_PATTERN = config['files']['month_pattern']
WKDAY_TEMPLATE = config['files']['wkday_template']
WKEND_TEMPLATE = config['files']['wkend_template']

def make_svgs(indices, month_names, month_numbers, day_names, day_numbers, weekend=False):
    """make the .svg files for the planner pages"""
    svgs = []
    for i in indices:
        replace_dict = {
            'month': month_names[i[0]],
            'day1': day_numbers[i[0]],
            'day1name': day_names[i[0]],
            'day2': day_numbers[i[1]],
            'day2name': day_names[i[1]]
        }
        if weekend:
            replace_dict['day3'] = day_numbers[i[2]]
            replace_dict['day3name'] = day_names[i[2]]
        images = {
            PLACEHOLDER: MONTH_PATTERN.format(month_numbers[i[0]])
        }
        template = WKEND_TEMPLATE if weekend else WKDAY_TEMPLATE
        svg = replace_in_file(replace_dict, images, template)
        svgs.append(svg)
    return svgs

def get_days(start_date, end_date, separate_weekends=False):
    """gets a list of date indices in an interval"""
    if separate_weekends:
        wkdays = pd.bdate_range(start=start_date, end=end_date)
        sats = pd.date_range(start=start_date, end=end_date, freq='W-SAT')
        suns = pd.date_range(start=start_date, end=end_date, freq='W-SUN')
        return [wkdays, sats, suns]
    else:
        return pd.date_range(start=start_date, end=end_date)

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

def replace(content, fields_values, pattern=r'$${}$$'):
    """replaces fields with their values in a svg string"""
    for field, value in fields_values.items():
        content = content.replace(pattern.format(field), value)
    return content
 
def remove_sodipodi(content, regex=r'sodipodi:absref="\S+"\s+'):
    """removes sodipodi absolute references to images
    (for inkscape svgs)"""
    matches = re.compile(regex).finditer(content)
    for match in matches:
        start, end = match.span()
        content = content[:start] + content[end:]
    return content

def replace_in_file(fields_values, images, path):
    """replaces image references in a svg string"""
    with open(path) as template:
        content = template.read()
        # replace text fields
        content = replace(content, fields_values)
        # remove absolute references
        content = remove_sodipodi(content)
        # replace images
        content = replace(content, images, pattern='{}')
        return content

