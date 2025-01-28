from libs import OpenPyXlWrapper as Excel
import pprint

# workbook = Excel.load("./templates/__template.xlsx")
# sheet = Excel.get_sheet_by_name(workbook, "Sheet1")
# data = Excel.load_sheet_as_dictionary(sheet, header_row=2, fill_blank=True)
# data = Excel.load_sheet_as_array(sheet, header_row=1, fill_blank=True)
# pprint.pprint(data)

workbook = Excel.load("./test.xlsx")
sheet = Excel.get_sheet_by_name(workbook, "Sheet1")
print(Excel.find_row(sheet, search_row="A", search_str="#"))
