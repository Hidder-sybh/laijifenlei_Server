import json
import pymysql


class Load:
    def __init__(self, load_path):
        self.DB_hosts = ''
        self.DB_port = ''
        self.DB_user = ''
        self.DB_password = ''
        self.DB = ''
        self.load_db_link(load_path)
        self.DB_operator = pymysql.connect(host=self.DB_hosts, port=self.DB_port, user=self.DB_user,
                                           passwd=self.DB_password,
                                           db=self.DB)
        self.cur = self.DB_operator.cursor()

    # 读取数据库连接信息
    def load_db_link(self, load_path):
        with open(load_path) as file_obj:
            group = json.load(file_obj)
        self.DB_hosts = group['hosts']
        self.DB_port = group['port']
        self.DB_user = group['user']
        self.DB_password = group['password']
        self.DB = group['db']

    def get_DB_operator(self):
        return self.DB_operator

    def get_DB_cur(self):
        return self.cur

    # 关闭连接
    def close(self):
        self.DB_operator.close()
