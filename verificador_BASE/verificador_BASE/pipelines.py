# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class VerificadorBasePipeline(object):
#     def process_item(self, item, spider):
#         return item
#from scrapy import signals
#from scrapy.exporters import CsvItemExporter
#from scrapy.xlib.pydispatch import dispatcher
#from importlib import reload

# CSVDir = '/media/cbranco/2ndDisk/minhasCoisas/verificador_BASE/'
#
# def item_type(item):
#     return type(item).__name__.replace('Item','').lower()  # TeamItem => team
#
#
# class VerificadorBasePipeline(object):
#     SaveTypes = ['VerificadorBaseItem','VerificadorErrorItem']
#     def __init__(self):
#         dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
#         dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
#
#     def spider_opened(self, spider):
#         self.files = dict([ (name, open(CSVDir+name+'.csv','w+b')) for name in self.SaveTypes ])
#         self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
#         [e.start_exporting() for e in self.exporters.values()]
#
#     def spider_closed(self, spider):
#         [e.finish_exporting() for e in self.exporters.values()]
#         [f.close() for f in self.files.values()]
#
#     def process_item(self, item, spider):
#         what = item_type(item)
#         if what in set(self.SaveTypes):
#             self.exporters[what].export_item(item)
#         return item

# class MultiCSVItemPipeline(object):
#     # Subfolder path, where the csv files are stored
#     CSVPath = "csv_data/"
#     # All allowed items
#     SaveTypes = ['VerificadorErrorItem','VerificadorBaseItem']
#     # List for already checked csv headers
#     CheckedHeaders = []
#
#     def __init__(self):
#         import sys
#         reload(sys)
#         #sys.setdefaultencoding('utf8')
#         dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
#         dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
#
#     def spider_opened(self, spider):
#         # Check if items exists and create new ones if not
#         for file in set(self.SaveTypes):
#             f = open(self.CSVPath + file + '.csv', 'a+')
#             f.close()
#
#     def spider_closed(self, spider):
#         #  not needed anymore
#         # [e.finish_exporting() for e in self.exporters.values()]
#         # [f.close() for f in self.files.values()]
#         pass
#
#     def process_item(self, item, spider):
#         what = item_type(item)
#         if what in set(self.SaveTypes):
#             try:
#                 # Check if csv file contains header, but only those, that aren't checked
#                 if what not in self.CheckedHeaders:
#                     self.check_header(what, item)
#                 self.write_item_to_row(item, what)
#             except Exception as e:
#                 logging.error("########################################################")
#                 logging.error("Error writing to " + what + ".csv file ")
#                 logging.error("Error Message: " + e.message)
#                 logging.error("Error Reason: " + e.reason)
#                 logging.error("Error Object: " + e.object)
#                 logging.error("########################################################")
#         return item
#
#     def write_item_to_row(self, item, what):
#         """
#         Write a single item to a row in csv file
#         :param item:
#         :param what:
#         :return:
#         """
#         ofile = open(self.CSVPath + what + '.csv', "ab")
#         writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#         item_dict = item.__dict__['_values']
#         row = []
#         for k in item_dict:
#             d = item_dict[k]
#             # Ig item is not a list join the element to string, replace all delimiters and set encoding to utf-8
#             if not isinstance(d, types.ListType):
#                 value = ''.join(item_dict[k]).replace('\t', '').replace('\n', '').encode('utf8')
#             else:
#                 value = ','.join(item_dict[k]).replace('\t', '').replace('\n', '').encode('utf8')
#             row.append(value)
#         writer.writerow(row)
#         ofile.close()
#
#     def check_header(self, what, item):
#         """
#         Check if the file contains header elements and create if missing
#         :param what:
#         :param item:
#         :return:
#         """
#         try:
#             with open(self.CSVPath + what + '.csv', 'ab+') as csvfile:
#                 writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#                 item_dict = item.__dict__['_values']
#                 # If file is empty, create new csv header
#                 if os.stat(self.CSVPath + what + '.csv').st_size == 0:
#                     self.write_csv_header(item_dict, writer)
#                 else:
#                     # Read first row and check header elements
#                     read_csv = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#                     first_row = read_csv.next()
#                     # if not all headers are set in the csv file, print warning
#                     if not self.check_key_in_csv_header(item_dict, first_row):
#                         # TODO: Add missing header to the csv file
#                         logging.warning("Wrong headers for file " + what + ".csv")
#                 self.CheckedHeaders.append(what)
#                 csvfile.close()
#                 return True
#         except Exception as e:
#             logging.error(e.message)
#             return False
#
#     @staticmethod
#     def write_csv_header(item_dict, writer):
#         """
#         Write header of a csv file.
#         Header is writen from each keys in the scrapy item
#         :param item_dict:
#         :param writer:
#         :return:
#         """
#         first_row = []
#         for k in item_dict:
#             # Join each Key to a string, delete delimiters and encode to utf-8
#             value = ''.join(k).replace('\t', '').replace('\n', '').encode('utf8')
#             first_row.append(value)
#         writer.writerow(first_row)
#
#     @staticmethod
#     def check_key_in_csv_header(item_dict, row):
#         """
#         Check, for each item key, if it's contained in the first line of the csv
#         k (key) stands for each dictionary key of the scrapy item.
#         :param item_dict:
#         :param row:
#         :return:
#         """
#         for k in item_dict:
#             if k not in row:
#                 return False
#         return True
