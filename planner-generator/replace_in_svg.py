import re

def replace(content, fields_values, pattern=r'$${}$$'):
    for field, value in fields_values.items():
        content = content.replace(pattern.format(field), value)
    return content
 
def remove_sodipodi(content, regex=r'sodipodi:absref="\S+"\s+'):
    matches = re.compile(regex).finditer(content)
    for match in matches:
        start, end = match.span()
        content = content[:start] + content[end:]
    return content

def replace_in_file(fields_values, images, path):
    with open(path) as template:
        content = template.read()
        # replace text fields
        content = replace(content, fields_values)
        # remove absolute references
        content = remove_sodipodi(content)
        # replace images
        content = replace(content, images, pattern='{}')
        return content

