import requests
import json
import time

baseUrl = "http://127.0.0.1/api/" # 图床API地址
token = "8961576c9090ef0902c4b89406f8d557"  # 管理员Token
outDate = 3  # 删除超过#个月的图片

def get_list(page=1):
    try:
        res = json.loads(requests.post(baseUrl + "images", data={"page": str(page), "token": token}).text)
    except Exception:
        raise AssertionError("获取图片列表时出错：网络请求失败或返回的数据不是JSON格式")
    else:
        return res


def delete_image(_id, pathname=""):
    try:
        res = json.loads(requests.post(baseUrl + "delete", data={"id": str(_id), "token": token}).text)
    except Exception:
        raise AssertionError("删除图片时出错：网络请求失败或返回的数据不是JSON格式")
    else:
        if res["msg"] == "删除成功!":
            print("已删除", _id, pathname)
        else:
            raise UserWarning(res["msg"])


try:
    last_page = get_list(1)["data"]["last_page"]
except KeyError:
    raise AssertionError("无法获取图片列表，请检查Token")

i = last_page
today = time.gmtime()
while i > 0:
    images = get_list(i)["data"]["data"]
    for j in images:
        k = time.strptime(j["upload_date"], "%Y-%m-%d %H:%M:%S")
        if today.tm_mon - k.tm_mon >= outDate:
            delete_image(j["id"], j["pathname"])
    i -= 1
