import math
from make_dates import *
from replace_in_svg import replace_in_file

# format: MM/DD/YYYY
START_DATE = '08/10/2020'
END_DATE = '12/13/2020'
# weekday template directory
WKDAY_TEMPLATE = './wkday_template.svg'
# weekend template directory
WKEND_TEMPLATE = './wkend_template.svg'
# placeholder image name (not directory if replacing with images in same folder, never relative path)
PLACEHOLDER = 'placeholder.png'
# image name pattern
MONTH_PATTERN = 'month_{}.png'
# ISO code (necessary for holidays, see https://github.com/dr-prodigy/python-holidays)
COUNTRY = 'MX'
LOCALE = 'es_MX.utf8'
# case for date names: lower/upper/title/capitalize/swapcase
CASE = 'lower'

"""
1) get the dates
2) make an svg for each page
    - separate the dates into monday-tuesday, wednesday-thursday, and friday-weekend groups
    - replace banner, month, date (number) and day name in svg template
3) export all svgs to a pdf
4) imposition?
"""

days = get_days(START_DATE, END_DATE)
day_numbers = [str(x) for x in days.day]
day_names = get_day_names(days, case=CASE, locale=LOCALE)
month_numbers = [str(x) for x in days.month]
month_names = get_month_names(days, case=CASE, locale=LOCALE)

n_weeks = math.ceil(len(days)/7)

indices = range(len(days))
mon_tue = zip(indices[0::7], indices[1::7])
wed_thu = zip(indices[2::7], indices[3::7])
fri_wkend = zip(indices[4::7], indices[5::7], indices[6::7])

# mt_svgs = []
# for mon, tue in mon_tue:
#     replace_dict = {
#         'month': month_names[mon],
#         'day1': day_numbers[mon],
#         'day1name': day_names[mon],
#         'day2': day_numbers[tue],
#         'day2name': day_names[tue]
#     }
#     images = {
#         PLACEHOLDER: MONTH_PATTERN.format(month_numbers[mon])
#     }
#     svg = replace_in_file(replace_dict, images, WKDAY_TEMPLATE)
#     mt_svgs.append(svg)
#     print(replace_dict)
replace_dict = {
    'month': month_names[0],
    'day1': day_numbers[0],
    'day1name': day_names[0],
    'day2': day_numbers[1],
    'day2name': day_names[1]
}
images = { PLACEHOLDER: MONTH_PATTERN.format(month_numbers[0]) }
svg = replace_in_file(replace_dict, images, WKDAY_TEMPLATE)

with open('./test-output.svg', 'w') as output:
    output.write(svg)

