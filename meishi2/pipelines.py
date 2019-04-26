# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
import os

file_path = 'E:\PyCharm 2019.1.1\Projects\Rec-System\meishi\食谱\蔬菜类\根茎类\\'
class Meishi2Pipeline(object):
    def __init__(self):
        self.wb = Workbook()  # 创建每个食材的Excel表
        self.ws = self.wb.active
        self.ws.append(["Title", "Src", "Main_ing", "Acces", "Mix_ing", "Cooks", "Steps", "Tips", "Types"])  # 设置表头

    def process_item(self, item, spider):  # 具体内容
        line = [item['Title'], item['Src'], item['Main_ing'], item['Acces'],
                item['Mix_ing'], item['Cooks'], item['Steps'], item['Tips'], item['Types']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save(os.path.join(file_path, '折耳根.xlsx'))  # 保存xlsx文件
        return item
