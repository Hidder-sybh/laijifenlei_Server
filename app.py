# coding=UTF-8
from flask import Flask, request, send_from_directory
from db_operator.item_db import ItemDb
from PIL import Image
from ASR.ASR import ASR
from AIR.SM_load import GCS
from AIR.AIR import temp_AIR
import json
import io
import base64

# 神经网络初始化
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# air = AIR()


# 此行以下编辑你的代码
#global gcs_load
#gcs_load = GCS()


@app.route('/get_classID/', methods=['GET'])
def get_classID():
    return {
        '1': '可回收垃圾',
        '2': '其他垃圾',
        '3': '有害垃圾',
        '4': '厨余垃圾'
    }


@app.route('/records_post/', methods=['POST', 'GET'])
def records_post():
    '''
    同时接受两个键值
    1.设备搜传输的图片信息: image
    2.设备号信息：Can_ID
    :return: 传入数据库成功/失败的信息
    '''
    if request.method == 'POST':
        if request.files.get("image"):
            img = request.files.get("image").read()
            temp_res = temp_AIR(img)
            print(temp_res)
        else:
            return '未检测到图片'
        Can_ID = '1313d'
        res_id = str(len(temp_res)-1)
        print(res_id)
        res = temp_res[res_id]['Name']
        return res

@app.route('/exact_search/', methods=['GET', 'POST'])
def exact_search():
    result = {}
    if request.method == 'POST':
        item_name = request.form['item_name']
        item = ItemDb()
        result = item.item_search_exact(item_name)
        item.close()
    else:
        result = {'接口返回示例': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                  '如果您发出的物品名不存在': {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
                  }
    return result


@app.route('/exact_search_ID/', methods=['GET', 'POST'])
def exact_search_ID():
    result = {}
    if request.method == 'POST':
        item_ID = request.form['item_ID']
        item = ItemDb()
        result = item.item_search_exact_ID(item_ID)
        item.close()
    else:
        result = {'接口返回示例': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                  '如果您发出的物品名不存在': {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
                  }
    return result


@app.route('/vague_search/', methods=['GET', 'POST'])
def vague_search():
    result = {}
    if request.method == 'POST':
        item_key = request.form['item_key']
        item = ItemDb()
        result = item.items_search_vague(item_key)
        item.close()
    else:
        result = {'接口返回示例': {'items_num': 22,
                             '667': {'Name': '鸡蛋包装盒', 'CLassID': '1'},
                             '668': {'Name': '鸡蛋盒', 'CLassID': '1'},
                             '670': {'Name': '鸡蛋盒包装', 'CLassID': '1'},
                             '675': {'Name': '鸡蛋塑料保护壳', 'CLassID': '1'},
                             '1313': {'Name': '塑料鸡蛋盒', 'CLassID': '1'},
                             '1880': {'Name': '包裹着鸡蛋壳的餐巾纸', 'CLassID': '1'}},
                  '如果您发出的物品不存在': {'item_num': 0},
                  }
    return result


@app.route('/asr_search/', methods=['GET', 'POST'])
def asr_search():
    result = {}
    if request.method == 'POST':
        talk_text = request.form['talk_text']
        result = ASR(talk_text)
    else:
        result = {'接口返回示例': {'鸡蛋': {'ID': 5249, 'Name': '鸡蛋', 'ClassID': 4},
                             '垃圾袋': {'ID': 2668, 'Name': '垃圾袋', 'ClassID': 2}},
                  '如果您发出的物品名不存在': {}
                  }
    return result


@app.route('/get_all_item/', methods=['GET', 'POST'])
def get_all_item():
    result = {}
    if request.method == 'POST':
        class_ID = request.form['class_ID']
        item = ItemDb()
        result = item.items_read_all(class_ID)
        item.close()
    else:
        result = {'接口返回示例': {'items_num': 665,
                             '3958': {'Name': '1号电池', 'CLassID': '3'},
                             '3959': {'Name': '502胶水', 'CLassID': '3'},
                             '3960': {'Name': '5号电池', 'CLassID': '3'},
                             '3961': {'Name': '704粘合剂', 'CLassID': '3'},
                             '3962': {'Name': '7号电池', 'CLassID': '3'}},
                  '如果您发出的ID异常': {}
                  }
    return result


@app.route('/air_search/', methods=['GET', 'POST'])
def air_search():
    result = {}
    if request.method == 'POST':
        if request.files.get("item_picture"):
            img = request.files.get('item_picture').read()
            result = temp_AIR(img)
        else:
            result['1'] = {'ID': -1, 'Name': '未检测到图片', 'ClassID': -1}
    else:
        result['1'] = {'ID': -1, 'Name': '测试用例', 'ClassID': -1}
    print(result)
    return result


@app.route('/update_version/', methods=['GET', 'POST'])
def update_version():
    if request.method == 'POST':
        with open('./Update/version.json') as f:
            version = json.load(f)
        return version
    else:
        return send_from_directory(directory="./Update/", filename="RBelong.apk", as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11233,debug=['True'])