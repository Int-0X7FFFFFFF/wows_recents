import threading


class Config(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        # 设置时分秒时间
        self.running_interval = 10000000000000

        # 是否根据军团刷新
        self.update_by_clan = True
        # 服务器 0-3 依次是 亚服 毛服 欧服 美服
        self.update_clans = [tuple(), tuple(), tuple(), tuple()]
        # user = (account_id, server(0-3))
        self.update_users = [[], [], [], []]
        # wg api token
        self.wargaming_tokens = []

        # 数据库链接
        self.psql = (
            "postgres://<username>:<password>@<host>:<port>/<db>?sslmode=disable"
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = object.__new__(cls)
        return Config._instance
