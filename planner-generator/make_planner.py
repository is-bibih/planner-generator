import io
from PyPDF2 import PdfFileMerger
from cairosvg import svg2pdf
from helper_functions import *

from configparser import ConfigParser

config = ConfigParser()
config.read('../config.ini')
OUTPUT = config['files']['output']
START_DATE = config['dates']['start_date']
END_DATE = config['dates']['end_date']
CASE = config['custom']['case']
LOCALE = config['custom']['locale']

days = get_days(START_DATE, END_DATE)
day_names = get_day_names(days, case=CASE, locale=LOCALE)
month_names = get_month_names(days, case=CASE, locale=LOCALE)
day_numbers = [str(x) for x in days.day]
month_numbers = [str(x) for x in days.month]

indices = range(len(days))
mon_tue = zip(indices[0::7], indices[1::7])
wed_thu = zip(indices[2::7], indices[3::7])
fri_wkend = zip(indices[4::7], indices[5::7], indices[6::7])

mt_svgs = make_svgs(mon_tue, month_names, month_numbers, day_names, day_numbers)
wt_svgs = make_svgs(wed_thu, month_names, month_numbers, day_names, day_numbers)
fw_svgs = make_svgs(fri_wkend, month_names, month_numbers,
                    day_names, day_numbers, weekend=True)

text_streams = []
for svgs in zip(mt_svgs, wt_svgs, fw_svgs):
    for svg in svgs:
        text_streams.append(io.StringIO(svg))

pdf_merger = PdfFileMerger()
for stream in text_streams:
    temp_pdf = svg2pdf(file_obj=stream)
    temp_pdf = io.BytesIO(temp_pdf)
    pdf_merger.append(temp_pdf)

with open(OUTPUT, 'wb') as output:
    pdf_merger.write(output)

