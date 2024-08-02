import requests
import re
from bs4 import BeautifulSoup

## Data Extraction from Academic Calendar

urls = [
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28137",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28134",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28136",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28138",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28141",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28140",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28139",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28401",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28392",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28393",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28396",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28397",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28398",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28399",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28394",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28395",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28400",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28106",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28111",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28114",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28117",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28120",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28123",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28125",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28128",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28131",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28109",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28113",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28116",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28122",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28119",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28124",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28127",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28130",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28133",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28108",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28112",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28115",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28118",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28121",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28349",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28126",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28129",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28132",
    "https://academiccalendars.romcmaster.ca/preview_program.php?catoid=56&poid=28110",
]
for URL in urls:
    # Parse the HTML
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract Program Title
    prog_title = [soup.find('h1').get_text()]
    prog_index = 1
    index = 0
    big_dict = dict()
    dic = dict()
    general_note = []
    counter = 1

    # Get The Index of Next Section Below Requirements
    while index < len(soup.findAll('div', class_ = 'acalog-core')):
        if soup.findAll('div', class_ = 'acalog-core')[index].find('h2') and "Note" in soup.findAll('div', class_ = 'acalog-core')[index].find('h2').get_text():
            if soup.findAll('div', class_ = 'acalog-core')[index].find('p'):
                general_note += [soup.findAll('div', class_ = 'acalog-core')[index].find('p').get_text()]
            elif soup.findAll('div', class_ = 'acalog-core')[index].find('ol', start = "1"):
                for note in soup.findAll('div', class_ = 'acalog-core')[index].findAll('ol', start = "1"):
                    general_note += [str(counter) + "." + note.get_text()]
        if soup.findAll('div', class_ = 'acalog-core')[index].find('h2') and "Requirements" in soup.findAll('div', class_ = 'acalog-core')[index].find('h2').get_text():
            break
        index += 1
    index += 1
    # Loop Through All "acalog-core" div class 
    while index < len(soup.findAll('div', class_ = 'acalog-core')):
        flag = False
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
            try:
                units = soup.findAll('div', class_ = 'acalog-core')[index].find('h4').get_text()
            except AttributeError:
                try:
                    units = soup.findAll('div', class_ = 'acalog-core')[index].find('h5').get_text()
                except AttributeError:
                    if soup.findAll('div', class_ = 'acalog-core')[index].find('h2') and "Requirements" in soup.findAll('div', class_ = 'acalog-core')[index].find('h2').get_text():
                        prog_title += [soup.findAll('div', class_ = 'acalog-core')[index].find('h2').get_text()]
                        flag = True
            # Empty Course List, Must Be Plain Text, Format and Extract
            if len(course_list) == 0:
                for u in ul:
                    items = u.findAll('li')
                    for item in items:
                        pt = item.get_text().split('\n')
                        course_list += pt
            # Duplicate Keys Differentiation, Use List of Tuples, fst = Course_List & snd = Note_List
            if units not in dic:
                dic[units] = [(course_list, note_list, flag)]
            else:
                dic[units] = dic[units] + [(course_list, note_list, flag)]
        # h3 Tags Are the Level and Total Units
        else: 
            dic = dict()
            level_units = soup.findAll('div', class_ = 'acalog-core')[index].get_text()
        index += 1
        big_dict[level_units] = dic

    ## Import Data Into Excel
    import xlsxwriter
    import os
    file_path = (prog_title[0] + ".xlsx").replace('/', '_')
    if not os.path.exists(file_path):
        # Create a new Excel file and add a worksheet
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
    # File path for the Excel file
    headers = ['PROGRAM', 'LEVEL', 'Total Units', 'Sub-Units', 'Required Courses', 'Term Offered (from Scheduling)', 'Section-Notes', 'General-Notes']
    worksheet.write_row(0, 0, headers)
    # Update Program Title
    worksheet.write('A2', prog_title[0]) 
    excel_col = 2
    for key, value in big_dict.items():
        # Check to See If There's Any Additional Info After 'units'
        k = key.split(":")
        year = k[0]
        total_units = k[1]
        if "(" in key:
            kk = total_units.split('(')
            year += ' (' + kk[1]
            total_units = kk[0]
        # Update Level
        worksheet.write('B' + str(excel_col), year)
        # Update Total Units In That Level
        worksheet.write('C' + str(excel_col), total_units)
        for ke, val in value.items():
            # Update Sub Units
            worksheet.write('D' + str(excel_col), ke)
            for va in val:
                if va[2]:
                    worksheet.write('A' + str(excel_col), prog_title[prog_index])
                    prog_index += 1
                for v in va[0]:
                    # Update Required Courses
                    worksheet.write('E' + str(excel_col), v)
                    if va[1] is not None:
                        for n in va[1]:
                            # Update Section Notes, If Any
                            worksheet.write('G' + str(excel_col), n)
                    excel_col += 1
        gn = ""
        for note in general_note:
            gn += note + "\n"
    merge_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter'
    })
    worksheet.merge_range(1, 7, excel_col, 7, gn, merge_format)
    workbook.close()
    print(URL + " completed")
