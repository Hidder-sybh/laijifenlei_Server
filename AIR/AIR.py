import base64, requests, json
from db_operator.item_db import ItemDb


def temp_AIR(image):
    url = 'http://api.tianapi.com/txapi/imglajifenlei/index'
    key = '6fda4f8543d58907405dc57896532b64'
    headers = 'Content-Type: application/x-www-form-urlencoded'
    post_image = str(base64.b64encode(image), encoding='utf-8')
    datas = {
        'key': key,
        'img': post_image
    }
    res = requests.post(url=url, data=datas).text
    # res = '{"code":200,"msg":"success","newslist":[{"name":"鼠标","trust":89,"lajitype":0,"lajitip":"鼠标是可回收垃圾，常见包括各类废金属、玻璃瓶、饮料瓶、电子产品等。投放时应注意轻投轻放、清洁干燥、避免污染。"},{"name":"摩托车","trust":57,"lajitype":4,"lajitip":"摩托车的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"},{"name":"电脑外设","trust":38,"lajitype":4,"lajitip":"电脑外设的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"},{"name":"铜斑蛇","trust":19,"lajitype":4,"lajitip":"铜斑蛇的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"},{"name":"锹形虫","trust":0,"lajitype":4,"lajitip":"锹形虫的垃圾分类系统暂时无法判别，请重新尝试拍摄物体的主要特征。"}]}'
    get_res = json.loads(res)
    result = {}
    if int(get_res['code']) == 200:
        item_list = list(get_res['newslist'])
        i = 0
        ID = -1
        for item in item_list:
            if int(item['lajitype']) != 4:
                if i >= 1:
                    break
                ClassID = int(item['lajitype'])
                # 可回收
                if ClassID == 0:
                    ID = 1
                # 有害
                elif ClassID == 1:
                    ID = 3
                # 厨余垃圾
                elif ClassID == 2:
                    ID = 4
                # 其他垃圾
                elif ClassID == 3:
                    ID = 2
                temp = {
                    'ClassID': ID,
                    'Name': item['name']
                }
                result[str(i)] = temp
                i += 1
        print(res)
        return result
    else:
        print(res)
        return {'Name': 'ERROR'}
