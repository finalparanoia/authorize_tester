from json import loads, dumps
from requests import session, Response
from os import system
from secrets import token_hex


class UniClient:
    def __init__(self):
        self.session = session()

    # 封装的post
    def post(self, url: str, data: dict or list) -> dict or list or Response:
        return self.pase_proc(self.session.post(url, dumps(data)))

    # 封装的get
    def get(self, url) -> dict or list or Response:
        return self.pase_proc(self.session.post(url))

    # 处理返还生成的Response对象
    @staticmethod
    def pase_proc(resp: Response) -> dict or list or Response:
        if resp.status_code == 200:
            return loads(resp.text)
        else:
            return resp


# Tester类
class Tester:
    def __init__(self, url_root: str):
        self.uc = UniClient()
        self.p = self.uc.post
        self.url_root = url_root
        self.ur = self.url_root

    # 对注册方法的封装
    def register(self, username: str, passwd: str):
        uid = self.p(self.ur + "/register/",
                     {"name": username, "passwd": passwd})["uid"]
        return uid

    # 登录
    def login(self, uid: str, passwd: str):
        data = self.p(self.ur + "/auth/passwd/",
                      {"uid": uid, "passwd": passwd})
        return data

    # 使用token验证授权
    def auth_token(self, tmp_uid: str, token: str):
        data = self.p(self.ur + "/auth/token/",
                      {"tmp_uid": tmp_uid, "token": token})
        return data

    # 注销一个token
    def revoke_one(self, tmp_uid: str, token: str):
        data = self.p(self.ur + "/revoke/tmp_uid/",
                      {"tmp_uid": tmp_uid, "token": token})
        return data

    # 注销全部token
    def revoke_all(self, uid: str, passwd: str):
        data = self.p(self.ur + "/revoke/uid/",
                      {"uid": uid, "passwd": passwd})
        return data

    # 删除账号
    def delete(self, uid: str, passwd: str):
        data = self.p(self.ur + "/delete/",
                      {"uid": uid, "passwd": passwd})
        return data


if __name__ == '__main__':
    t = Tester("http://localhost:8080")
    # 生成用户名密码
    usr = token_hex()
    pwd = token_hex()
    # 注册
    n_uid = t.register(usr, pwd)
    system("pause")
    # 获取令牌
    tmp = t.login(n_uid, pwd)
    # 解析令牌
    t_uid = tmp["tmp_uid"]
    tok = tmp["token"]
    system("pause")
    # 验证令牌
    t.auth_token(t_uid, tok)
    # 注销单个令牌
    t.revoke_one(t_uid, tok)
    # 获取令牌
    t.login(n_uid, pwd)
    t.login(n_uid, pwd)
    t.login(n_uid, pwd)
    t.login(n_uid, pwd)
    system("pause")
    # 注销全部令牌
    t.revoke_all(n_uid, pwd)
    system("pause")
