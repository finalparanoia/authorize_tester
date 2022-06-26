from json import loads, dumps
from requests import session, Response
from secrets import token_hex


def pause():
    input("请按任意键继续...")


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
    print("生成随机的用户名和密码\n用户名: {}\n密码: {}\n".format(usr, pwd))
    # 注册
    n_uid = t.register(usr, pwd)
    print("注册\n获得UID: {}\n".format(n_uid))
    # pause()
    # 获取令牌
    tmp = t.login(n_uid, pwd)
    # 解析令牌
    t_uid = tmp["tmp_uid"]
    tok = tmp["token"]
    print("获取并解析临时UID和授权码\n临时UID: {}\n授权码: {}\n".format(t_uid, tok))
    # pause()
    # 验证令牌
    s_c = t.auth_token(t_uid, tok)
    print("验证令牌，服务器返还: {}\n".format(s_c))
    # 注销单个令牌
    s_c = t.revoke_one(t_uid, tok)
    print("撤销单个令牌，服务器返还: {}\n".format(s_c))
    # 获取令牌
    c = 0
    resp_list = []
    while True:
        resp = t.login(n_uid, pwd)
        print("{}. 临时UID: {}\n   授权码: {}".format(c, tmp["tmp_uid"], tmp["token"]))
        c += 1
        if c > 5:
            break
    # pause()
    # 注销全部令牌
    s_c = t.revoke_all(n_uid, pwd)
    print("撤销全部令牌，服务器返还: {}\n".format(s_c))
    resp = t.delete(n_uid, pwd)
    print("删除账号，服务器返还: {}\n".format(resp))
    # pause()
