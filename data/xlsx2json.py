# -*- coding: utf-8 -*-

import json
import collections
import xlrd
import os
import sys
import codecs

class Xlsx2Json():

    def __init__(self, model_name):
        self.data_list = []
        self.worksheet = xlrd.open_workbook(model_name + '.xlsx').sheet_by_index(0)
        self.titles = collections.defaultdict()

        if self.worksheet.ncols > 0:
            for col in range(self.worksheet.ncols):
                self.titles[col] = self.worksheet.cell_value(0, col)          # Key: index, Value: title text

    def data_to_list(self):
        for row_index in range(1, self.worksheet.nrows):
            data_dict = collections.defaultdict()
            for column_index in range(self.worksheet.ncols):
                data_dict[self.titles[column_index]] = self.worksheet.cell_value(row_index, column_index)
            self.data_list.append(data_dict)

    def output_file(self):
        with codecs.open(model_name + '_out' + '.json', 'w', 'utf-8') as json_file:
            json.dump(self.data_list, json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    model_name = sys.argv[1]
    file_path = './' + model_name + '.xlsx'

    if not os.path.exists(file_path):
        print ('Please check the model name in args.')
    else:
        proc = Xlsx2Json(model_name)
        proc.data_to_list()
        proc.output_file()