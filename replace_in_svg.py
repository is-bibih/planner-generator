import re

TEMPLATE_PATH = './test.svg'
OUTPUT_PATH = './test-output.svg'
IMAGES_PATH = './images/'

# dict of values to place instead of placeholders
fields_values = {
    'month': 'owo-month',
    'day1': 'owo-day1',
    'day2': 'owo-day2',
    'day3': 'owo-day3'
}

# dict of images to replace
images = {
    'pax_tux.png': 'TuxFlat.svg'
}

def replace(content, fields_values, regex=r'\$\$\S+\$\$'):
    matches = re.compile(regex).finditer(content)
    for match in matches:
        start, end = match.span()
        field = match.group(0)[2:-2] if regex == r'\$\$\S+\$\$' else match.group(0)
        content = content[:start] + fields_values[field] + content[end:]
    return content
 
def replace_images(content, image_dict):
    for old_img, new_img in image_dict.items():
        matches = re.compile(old_img).finditer(content)
        for match in matches:
            start, end = match.span()
            content = content[:start] + new_img + content[end:]
    return content

def remove_sodipodi(content, regex=r'sodipodi:absref="\S+"\s+'):
    matches = re.compile(regex).finditer(content)
    for match in matches:
        start, end = match.span()
        content = content[:start] + content[end:]
    return content

with open(TEMPLATE_PATH) as template:
    content = template.read()
    # replace text fields
    content = replace(content, fields_values)
    # remove absolute references
    content = remove_sodipodi(content)
    # replace images
    content = replace_images(content, images)

# write file
with open(OUTPUT_PATH, 'w') as output:
    output.write(content)

