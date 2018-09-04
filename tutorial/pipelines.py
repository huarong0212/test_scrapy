from scrapy.conf import settings
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import mysql.connector
import json

class TutorialPipeline(object):
    #插入的sql语句
    feed_key = ['title','version','grade','subject','publishing']

    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='123456', database='stack_db', )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item.get('title')
        version = item.get('version')
        grade = item.get('grade')
        subject = item.get('subject')
        publishing = item.get('publishing')
        insert_sql = """
            insert into stack_questions(`title`, `version`, `grade`, `subject`,`publishing`)
            VALUES (%s, %s, %s, %s,%s);
        """
        self.cursor.execute(insert_sql, (title[0], version[0], grade[0], subject[0], publishing[0]))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()