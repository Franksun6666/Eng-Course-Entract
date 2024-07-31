import requests
import re
from bs4 import BeautifulSoup

# Data Extraction from Academic Calendar

# url_list= []
# for URL in url_list:

# Parse the HTML
URL = "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28131"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Extract Program Title
prog_title = soup.find('h1').get_text()
index = 3
big_dict = dict()
dic = dict()

# Loop Through All "acalog-core" div class 
while index < len(soup.findAll('div', class_ = 'acalog-core')):
    # Extract Subsection In A Specific Level
    if not soup.findAll('div', class_ = 'acalog-core')[index].find('h3'):
        text = soup.findAll('div', class_ = 'acalog-core')[index].get_text()
        ul = soup.findAll('div', class_ = 'acalog-core')[index].findAll('ul')
        course_list = []
        note_list = []
        # Loop Through the Unordered List
        for u in ul:
            # Items Are Course Codes List
            items = u.findAll('li', class_ = "acalog-course")
            # Notes Are the Optional Note At The Bottom of Each Section
            notes = u.findAll('li', class_ = "acalog-adhoc acalog-adhoc-after")
            for item in items:
                # If there's A "-" In the Item, It Must Be A Course Code + Course Title, Extract Only the Course Code 
                if "-" in item.get_text():
                    course_list.append(re.sub(r'\s*-.*', '', item.get_text(), flags = re.DOTALL))
            # Extract Notes, If Any
            for note in notes:
                if "Note:" in note.get_text():
                    note_list.append(note.get_text().replace('\xa0', ' ').replace('\n', ''))
        # Extract Subunits
        units = soup.findAll('div', class_ = 'acalog-core')[index].find('h4').get_text()
        # Empty Course List, Must Be Plain Text, Format and Extract
        if len(course_list) == 0:
            for u in ul:
                items = u.findAll('li')
                for item in items:
                    pt = item.get_text().split('\n')
                    course_list += pt
        # Duplicate Keys Differentiation, Use List of Tuples, fst = Course_List & snd = Note_List
        if units not in dic:
            dic[units] = [(course_list, note_list)]
        else:
            dic[units] = dic[units] + [(course_list, note_list)]
    # h3 Tags Are the Level and Total Units
    else: 
        dic = dict()
        level_units = soup.findAll('div', class_ = 'acalog-core')[index].get_text()
    index += 1
    big_dict[level_units] = dic

import xlsxwriter
import os

file_path = 'example.xlsx'
if not os.path.exists(file_path):
    # Create a new Excel file and add a worksheet
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    print("111111")
# File path for the Excel file
headers = ['PROGRAM', 'LEVEL', 'Total Units', 'Sub-Units', 'Required Courses', 'Term Offered (from Scheduling)', 'Notes']
worksheet.write_row(0, 0, headers)
worksheet.write('A2', prog_title) 
excel_col = 2
for key, value in big_dict.items():
    k = key.split(":")
    year = k[0]
    total_units = k[1]
    if "(" in key:
        # word = " ".join(k)
        kk = total_units.split('(')
        year += ' (' + kk[1]
        total_units = kk[0]
    worksheet.write('B' + str(excel_col), year)
    worksheet.write('C' + str(excel_col), total_units)
    for ke, val in value.items():
        worksheet.write('D' + str(excel_col), ke)
        for va in val:
            for v in va[0]:
                worksheet.write('E' + str(excel_col), v)
                if va[1] is not None:
                    for n in va[1]:
                        worksheet.write('G' + str(excel_col), n)
                excel_col += 1
workbook.close()