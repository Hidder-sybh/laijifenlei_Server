import ast
import numpy as np
from PIL import Image
import tensorflow.compat.v1 as tf
from tensorflow.python.saved_model import tag_constants
from db_operator.item_db import ItemDb


class GCS(object):
    def __init__(self):
        self.model_path = 'AIR/model'
        self.signature_key = 'predict_images'
        self.input_size = 456
        self.input_key_1 = 'input_img'
        self.output_key_1 = 'output_score'
        config = tf.ConfigProto(allow_soft_placement=True)
        with tf.get_default_graph().as_default():
            self.sess = tf.Session(graph=tf.Graph(), config=config)
            meta_graph_def = tf.saved_model.loader.load(self.sess, [tag_constants.SERVING], self.model_path)
            self.signature = meta_graph_def.signature_def
            input_images_tensor_name = self.signature[self.signature_key].inputs[self.input_key_1].name
            output_score_tensor_name = self.signature[self.signature_key].outputs[self.output_key_1].name
            self.input_images = self.sess.graph.get_tensor_by_name(input_images_tensor_name)
            self.output_score = self.sess.graph.get_tensor_by_name(output_score_tensor_name)
            print('网络载入完成')

        self.label_id_name_dict = \
            {
                "0": "一次性快餐盒",
                "1": "污损塑料",
                "2": "烟蒂",
                "3": "牙签",
                "4": "破碎花盆及碟碗",
                "5": "竹筷",
                "6": "剩饭剩菜",
                "7": "大骨头",
                "8": "水果果皮",
                "9": "水果果肉",
                "10": "茶叶渣",
                "11": "菜叶菜根",
                "12": "蛋壳",
                "13": "鱼骨",
                "14": "充电宝",
                "15": "包",
                "16": "化妆品瓶",
                "17": "塑料玩具",
                "18": "塑料碗盆",
                "19": "塑料衣架",
                "20": "快递纸袋",
                "21": "插头电线",
                "22": "旧衣服",
                "23": "易拉罐",
                "24": "枕头",
                "25": "毛绒玩具",
                "26": "洗发水瓶",
                "27": "玻璃杯",
                "28": "皮鞋",
                "29": "砧板",
                "30": "纸板箱",
                "31": "调料瓶",
                "32": "酒瓶",
                "33": "金属食品罐",
                "34": "锅",
                "35": "食用油桶",
                "36": "饮料瓶",
                "37": "干电池",
                "38": "软膏",
                "39": "过期药物"
            }

    # 图像居中
    def center_img(self, img, size=None, fill_value=255):
        h, w = img.shape[:2]
        if size is None:
            size = max(h, w)
        shape = (size, size) + img.shape[2:]
        background = np.full(shape, fill_value, np.uint8)
        center_x = (size - w) // 2
        center_y = (size - h) // 2
        background[center_y:center_y + h, center_x:center_x + w] = img
        return background

    # 图像处理
    def preprocess_img(self, img):
        img = Image.open(img)
        resize_scale = 456 / max(img.size[:2])
        img = img.resize(
            (int(img.size[0] * resize_scale), int(img.size[1] * resize_scale)))
        img = img.convert('RGB')
        img = np.array(img)
        img = img[:, :, ::-1]
        img = self.center_img(img, 456)
        img = img[np.newaxis, :, :, :]
        img = np.asarray(img, np.float32) / 255.0
        mean = [0.56719673, 0.5293289, 0.48351972]
        std = [0.20874391, 0.21455203, 0.22451781]
        img[..., 0] -= mean[0]
        img[..., 1] -= mean[1]
        img[..., 2] -= mean[2]
        img[..., 0] /= std[0]
        img[..., 1] /= std[1]
        img[..., 2] /= std[2]
        print("完成了图像处理")
        return img

    def predict(self, image):
        result = {}
        image = self.preprocess_img(image)
        print("开始预测")
        pred_score = self.sess.run([self.output_score], feed_dict={self.input_images: image})
        if pred_score is not None:
            pred_label = np.argmax(pred_score[0], axis=1)[0]
            db = ItemDb()
            result = db.item_search_exact(self.label_id_name_dict[str(pred_label)])
            db.close()
        else:
            result = {'ID': -1, 'Name': "NOT EXIST", 'ClassID': -1}
        return result
