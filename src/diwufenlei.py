"""
变化检测： 两张图片，对比分析出两张图片中的建筑物变化，传入的图片为两张图片。
         构成的元组。（√）
地物分类：遥感影像中感兴趣的类别进行提取和分类。

目标检测：检测操场。

目标提取：提取单张图片中的道路信息，传入的图片可以为待预测图片对应路径构成的列表。（×）

"""

import numpy as np
from PIL import Image
from paddlers.deploy import Predictor


def DWFL(img):
    predictor = Predictor("C:/Users/Administrator/Desktop/yaoganjieyi2/yaoganjieyi/static_model/MuBiaoTiQu/1024x1024", use_gpu=False)
    res = predictor.predict(img)
    # res = predictor.predict('demo_data/img.png')

    img = res['label_map']
    img = np.array(img * 255).astype("uint8")

    img = Image.fromarray(img)
    img.save('static/temp/diwufenlei.jpg')
    return 'static/temp/diwufenlei.jpg'

