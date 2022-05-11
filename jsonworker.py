import PyPDF2
import json
pdf_file = open('1.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
def get_data(page_content):
    _dict = {}
    page_content_list = page_content.splitlines()
    for line in page_content_list:
        if ':' not in line:
            continue
        key, value = line.split(':')
        _dict[key.strip()] = value.strip()
    return _dict

page_data = get_data(page_content)
json_data = json.dumps(page_data, indent=4)
print(json_data)