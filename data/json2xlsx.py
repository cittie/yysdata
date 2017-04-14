import json
import collections
import xlsxwriter
import os
import sys

class Json2Xlsx():

    def __init__(self, model_name):
        self.titles = collections.defaultdict(int)
        self.current_column = 0
        self.current_row = 1

        with open(model_name + '.json') as json_file:
            self.data = json.load(json_file)

        self.workbook = xlsxwriter.Workbook(model_name + '.xlsx')
        self.worksheet = self.workbook.add_worksheet()

    def data_to_line(self):
        for ele in self.data:
            for key, value in ele.items():
                if key not in self.titles:
                    self.worksheet.write(0, self.current_column, key)     # Add title to first row
                    self.titles[key] = self.current_column                  # Pair title and column position
                    self.current_column += 1
                self.worksheet.write(self.current_row, self.titles[key], value)
            self.current_row += 1                                           # write each element to a single line

    def close_file(self):
        self.workbook.close()

if __name__ == '__main__':
    model_name = sys.argv[1]
    file_path = './' + model_name + '.json'

    if not os.path.exists(file_path):
        print 'Please check the model name in args.'
    else:
        proc = Json2Xlsx(model_name)
        proc.data_to_line()
        proc.close_file()