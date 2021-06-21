# coding=UTF-8

from db_operator.load_db import Load


class ItemDb(object):
    """
    1可回收垃圾
    2其他垃圾
    3有害垃圾
    4厨余垃圾
    """

    def __init__(self):
        """
        在此类初始化时就已经自动连接目标数据库
        """
        self.db_load = Load('cfg/RcDb.json')
        # db_operator是pymysql库中pymysql.connect()的返回对象
        self.db_operator = self.db_load.get_DB_operator()
        # db_cur与pymysql库中cursor用法完全一致
        self.db_cur = self.db_load.get_DB_cur()
        self.table_items = 'items'

    def item_search_exact_ID(self, item_ID):
        """
        通过ID准确搜索
        :param item_ID: 物品ID
        :return: 返回一个字典，包含该垃圾ID以及所属所有类别{'ID':1,'Name':xxx,'ClassID':1/2/3/4,}
        """
        result = {}
        sql = 'SELECT * FROM items WHERE ID = ' + str(item_ID)
        self.db_cur.execute(sql)
        search_results = self.db_cur.fetchall()
        if len(search_results) != 0:
            result['ID'] = search_results[0][0]
            result['Name'] = search_results[0][1]
            result['ClassID'] = int(search_results[0][2])
        else:
            return {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
        return result

    def item_search_exact(self, item_name: str):
        """
        搜索数据库某个物品所属垃圾类别
        :param item_name: 物品名称
        :return: 返回一个字典，包含该垃圾ID以及所属所有类别{'ID':1,'Name':xxx,'ClassID':1/2/3/4,}
        """
        result = {}
        sql = 'SELECT * FROM items WHERE Name = ' + '"' + item_name + '"'
        self.db_cur.execute(sql)
        search_results = self.db_cur.fetchall()
        if len(search_results) != 0:
            result['ID'] = search_results[0][0]
            result['Name'] = search_results[0][1]
            result['ClassID'] = int(search_results[0][2])
        else:
            return {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1, }
        return result

    def items_search_vague(self, item_key: str):
        """
        搜索含有指定关键字条目
        :param item_key: 该批物品的共同含有的字符（鸡蛋，鸡蛋壳，鸡蛋黄，鸡蛋清）
        :return: 所有符合搜索条件的物品条目格式{'item_ID':{"item_name":"xxx","CLASSID":1/2/3/4},....}
        """
        result = {}
        sql = 'SELECT * FROM items WHERE Name LIKE "%' + item_key + '%"'
        self.db_cur.execute(sql)
        search_result = self.db_cur.fetchall()
        if len(search_result) != 0:
            result['items_num'] = len(search_result)
            for item in search_result:
                result[str(item[0])] = {"Name": item[1], 'CLassID': item[2]}
        else:
            return {'item_num': 0}
        return result

    def items_read_all(self, ClassID: str):
        """
        一次性读取数据库所有内容(为减小数据量，只返回ID，与物品名)
        :param ClassID: 需要获取的物品类别默认为0所有
        :return: 字典形式，格式为{'item_ID':{"item_name":"xxx","CLASSID":1/2/3/4},....}
        """
        result = {}
        sql = ''
        if ClassID == '0':
            sql = 'SELECT * FROM items'
        else:
            sql = 'SELECT * FROM items where ClassID_1 = "' + str(ClassID) + '"'
        self.db_cur.execute(sql)
        search_result = self.db_cur.fetchall()
        if len(search_result) != 0:
            result['items_num'] = len(search_result)
            for item in search_result:
                result[str(item[0])] = {"Name": item[1], 'CLassID': item[2]}
        else:
            return {'item_num': 0}
        return result

    def items_add(self, item_name: str, item_Class: dir()):
        """
        向数据库添加物品条目
        此函数不面向客户使用，用于后台数据管理
        :param item_name: 物品名称
        :param item_Class: 此参数类型为字典为垃圾所属类别
        :return: 添加条目的信息
        """
        pass

    def item_edit(self, ID):
        """
        编辑某个物品信息
        此函数不面向客户使用，用于后台数据管理
        :param ID: 物品ID
        :return:字典修改后的信息{'ID':1,'Name':xxx,'C1':true/false,'C2':true/false,'C3':true/false,'C4':true/false}
        """
        pass

    def item_del(self, ID):
        """
        用于删除某一个物品条目
        此函数不面向客户使用，用于后台数据管理
        :param ID: 要删除的物品ID
        :return: 字典，被删除的物品信息{'ID':1,'Name':xxx,'C1':true/false,'C2':true/false,'C3':true/false,'C4':true/false}
        """
        pass

    def add_operator_record(self, operator_user, operator_action):
        """
        记录后台数据的修改（只对后台管理对数据库的更改操作记录）
        :param operator_user: 操作管理员
        :param operator_action: 具体操作内容
        :return: 无
        """
        pass

    def close(self):
        self.db_load.close()
