# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from openpyxl import Workbook
import sqlite3


class TutorialPipeline(object):
    def __init__(self):
        self.fp=open('data.txt',"w")
        self.file = open('data.json', 'w', encoding='utf-8')

        #excel
        self.wb=Workbook()
        self.ws=self.wb.active
        self.ws.append(['标题','链接','图片'])

        #sqlite3
        self.db='27270.db'
        self.dbconn=None
        try:
            self.dbconn=sqlite3.connect(self.db)
            self.con=self.dbconn.cursor()
            print("数据库已连接")
            sql="create table  if not EXISTS website(url text PRIMARY KEY,title text not NULL,pic  text )"
            self.con.execute(sql)
            print("数据表初始化成功.")
        except  Exception as e:
            print("数据库初始化失败")

    def process_item(self, item, spider):
        self.save_excel(item)
        # self.save_sqlit(item)
        # self.save_file(item)
        return item

    # saving data to a file
    def save_file(self,item):
        str1="pic: "+item['pic']+","+" link: "+item['link']+"\n"
        self.fp.write(str1)

        #读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #写入文件
        self.file.write(line)

    # save data  to a sqlite file
    def save_sqlit(self,item):
        sql=' insert or ignore into website VALUES("%s","%s","%s")'%(item['link'],item['title'],item['pic'])
        try:
            self.con.execute(sql)
            print("插入成功.")
        except:
            print("插入失败.")

    # save data to excel
    def save_excel(self,item):
        line = [item['title'], item['link'], item['pic']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('27270.xlsx')  # 保存xlsx文件

    def close_spider(self,spider):
        self.fp.flush()
        self.fp.close()
        self.dbconn.commit()
        self.dbconn.close()
