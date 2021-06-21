from db_operator.load_db import Load


class UserDb(object):

    def __init__(self):
        """
        在此类初始化时就已经自动连接目标数据库
        """
        self.db_load = Load('cfg/RcDb.json')
        # db_operator是pymysql库中pymysql.connect()的返回对象
        self.db_operator = self.db_load.get_DB_operator()
        # db_cur与pymysql库中cursor用法完全一致
        self.db_cur = self.db_load.get_DB_cur()
        # 操作表名
        self.table_items = 'user'

    """
    此行以下编辑你要写的功能模块,注意要注释完整
    """