import re

TEMPLATE_PATH = './test.svg'
OUTPUT_PATH = './test-output.svg'
IMAGES_PATH = './images/'

# re to match "$$expression$$"
placeholder = re.compile(r'\$\$\S+\$\$')

# list of values to place instead of placeholders
fields_values = {
    'month': 'owo-month',
    'day1': 'owo-day1',
    'day2': 'owo-day2',
    'day3': 'owo-day3'
}

def replace(content, fields_values, regex=r'\$\$\S+\$\$'):
    placeholder = re.compile(regex)
    matches = placeholder.finditer(content)
    for match in matches:
        start, end = match.span()
        field = match.group(0)[2:-2] if regex == r'\$\$\S+\$\$' else match.group(0)
        print(field)
        content = "".join((content[:start], fields_values[field], content[end:]))
    return content

# replace placeholder fields with their values
with open(TEMPLATE_PATH) as template:
    content = template.read()
    # replace text
    content = replace(content, fields_values)

# write file
with open(OUTPUT_PATH, 'w') as output:
    output.write(content)
