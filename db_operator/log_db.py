from db_operator.load_db import Load


class LogDb(object):
    """
    此类旨在记录管理人员对后台数据的操作记录
    """

    def __init__(self):
        self.db_load = Load('cfg/RcDb.json')
        # db_operator是pymysql库中pymysql.connect()的返回对象
        self.db_operator = self.db_load.get_DB_operator()
        # db_cur与pymysql库中cursor用法完全一致
        self.db_cur = self.db_load.get_DB_operator()
        self.table_record = 'operator_log'
        self.close = self.db_load.close()

    def get_log_date(self, start_date, days):
        """
        获取一定时间内的操作记录
        :param start_date: 起始日期
        :param days: 天数
        :return: 字典{'日期':{'name':'xxx','operator':'operator_text'}...}
        """
        pass

    def get_log_user(self, user_name):
        """
        查询指定管理员操作记录
        :param user_name: 查询用户名
        :return: 字典{'日期':{'name':'xxx','operator':'operator_text'}...}
        """
        pass

    def get_log_all(self):
        """
        获取所有操作日志
        :return: 字典{'日期':{'name':'xxx','operator':'operator_text'}...}
        """
        pass

    def add_log(self, operator_user, operator_action):
        """
        记录操作，注意虽然没要求提供日期参数，但需要获取此软件运行操作系统时间
        时间格式YYYY-MM-DD HH:MM:SS
        :param operator_user:操作者
        :param operator_action:具体操作行为
        :return:无
        """

