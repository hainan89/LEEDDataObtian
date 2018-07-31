# import random
# import time
# import logging

from src.GlobalSpace import GlobalSpace;
from src.LogProcess import LogProcess;
import mysql.connector


class CRUDProcess(GlobalSpace):
    """ simulate the action of the browser"""
    
    def __init__(self):
#         socket.setdefaulttimeout()
        self.res = None
        
        self.logger_p = LogProcess("CRUDLog")
        self.logger = self.logger_p.logger

        # initialize the database connection
#         user = 'test'
#         pwd = '123456'
#         host = '127.0.0.1'
#         db = 'houserenting'
        user = self.CFG.cf["db"]["db_user"]
        pwd = self.CFG.cf["db"]["db_pwd"]
        host = self.CFG.cf["db"]["db_host"]
        db = self.CFG.cf["db"]["db_name"]
        
        self.db_cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
        self.db_cursor = self.db_cnx.cursor()
    
    def select(self, tb_name, keys_str, where_str = None, order_str = None):
        select_sql = "select {1} from {0} ".format(tb_name, keys_str)
        if where_str != None:
            select_sql = select_sql + " where ({0})".format(where_str)
        
        if order_str != None:
            select_sql = select_sql + " order by {0} ".format(order_str)
            
        print(select_sql)
        self.db_cursor.execute(select_sql)
        record_list = self.db_cursor.fetchall()
        return record_list
        #end of the select
        
    def insert(self, tb_name, keys_str, values):
        
        if len(values) == 1 :
            val_mark = "%s"
        elif len(values) > 1:
            val_mark = "%s" + " , %s" * (len(values) - 1)
        else:
            return False
        
        insert_sql = "insert into {0} ({1}) values ({2})".format(tb_name, keys_str, val_mark)
        insert_value = values
        
        insert_id = 0
        try:
            self.db_cursor.execute(insert_sql, insert_value)
            self.db_cnx.commit()
#             insert_id = self.db_cnx.insert_id()
            insert_id = self.db_cursor.lastrowid
            self.logger.info("Insert {0} : {1}".format(tb_name, keys_str))
        except mysql.connector.Error as err:
            self.logger.error("Insert {0} Failed : {1}".format(tb_name, err.msg))
            return False
        
        return insert_id
        #end of the insert
        
    def update(self, tb_name, keys_tuple, values, where_str = None):
        if where_str == None:
            self.logger.info("No where_str! Terminated!")
            return
        
        if len(keys_tuple) != len(values):
            self.logger.info("keys dismatch with values")
            return
        
        if len(keys_tuple) <= 0 :
            return False
        elif len(values) == 1:
            update_keys = "{0} = %s".format(keys_tuple[0])
        else:
            update_keys = "{0} = %s".format(keys_tuple[0])
            for item_i in range(1, len(values)):
                update_keys = update_keys + ", {0} = %s".format(keys_tuple[item_i])
            
        update_sql = "update {0} set {1} where ({2})".format(tb_name, update_keys, where_str)
        update_value = values
        
#         print(update_sql)
        try:
            self.db_cursor.execute(update_sql, update_value)
            self.db_cnx.commit()
            self.logger.info("Update {0} : {1}".format(tb_name, where_str))
        except mysql.connector.Error as err:
            self.logger.error("Update {0} Failed : {1}".format(tb_name, err.msg))
            return False
        
        return True
        #end of update
        
    def delete(self, tb_name, where_str):
        if where_str == None:
            self.logger.info("No where_str! Terminated!")
            return
        
        del_sql = "delete from {0} where ({1})".format(tb_name, where_str)
        
        try:
            self.db_cursor.execute(del_sql)
            self.db_cnx.commit()
            self.logger.info("Delete {0} : {1}".format(tb_name, where_str))
        except mysql.connector.Error as err:
            self.logger.error("Delete {0} Failed : {1}".format(tb_name, err.msg))
            return False
        return True
        #end of the delete
    
    def is_unique(self, tb_name, check_map):
        result_list = []
        check_list = []
        for (key, val) in check_map.items():
            if len(check_list) > 0:
                results = self.select(tb_name, 
                                      "PrimaryID",
                                      "{0} = '{1}' and PrimaryID in {2}".format(key, val, tuple(check_list) + (0, -1)))
            else:
                results = self.select(tb_name, 
                                      "PrimaryID",
                                      "{0} = '{1}'".format(key, val))
            
            if len(check_list) == 0: # first, add
                for one_row in results:
                    check_list.append(one_row[0])
            else:
                for one_row in results:
                    current_id = one_row[0]
                    if current_id in check_list:
                        result_list.append(current_id)
                check_list = result_list[:] # 采用切片的方法对list进行 深度复制
                result_list.clear()
            if len(check_list) == 0:
                break
        self.logger.info("is_unique test : {0}:{1}".format(check_map, check_list))
        return check_list
        #end of the is_unique
        
    def close(self):
        self.db_cursor.close()
        self.db_cnx.close()
        self.logger.info("CRUD Process Closed!")
        #end of the close 
"""end class"""