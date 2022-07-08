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


#

def BHJC(img1, img2):
    predictor = Predictor("C:/Users/Administrator/Desktop/yaoganjieyi2/yaoganjieyi/static_model/BianHuaJianCe/1024x1024", use_gpu=False)
    res = predictor.predict((img1, img2))
    # res = predictor.predict('demo_data/img.png')

    img = res['label_map']
    img = np.array(img * 255).astype("uint8")

    img = Image.fromarray(img)
    img.save('static/temp/bianhuajiance.jpg')
    return 'static/temp/bianhuajiance.jpg'
    class WindowGenerator:
        def __init__(self, h, w, ch, cw, si=1, sj=1):
            self.h = h
            self.w = w
            self.ch = ch
            self.cw = cw
            if self.h < self.ch or self.w < self.cw:
                raise NotImplementedError
            self.si = si
            self.sj = sj
            self._i, self._j = 0, 0

        def __next__(self):
            # 列优先移动（C-order）
            if self._i > self.h:
                raise StopIteration

            bottom = min(self._i + self.ch, self.h)
            right = min(self._j + self.cw, self.w)
            top = max(0, bottom - self.ch)
            left = max(0, right - self.cw)

            if self._j >= self.w - self.cw:
                if self._i >= self.h - self.ch:
                    # 设置一个非法值，使得迭代可以early stop
                    self._i = self.h + 1
                self._goto_next_row()
            else:
                self._j += self.sj
                if self._j > self.w:
                    self._goto_next_row()

            return slice(top, bottom, 1), slice(left, right, 1)

        def __iter__(self):
            return self

        def _goto_next_row(self):
            self._i += self.si
            self._j = 0

    def recons_prob_map(patches, ori_size, window_size, stride):
        """从裁块结果重建原始尺寸影像"""
        h, w = ori_size
        win_gen = WindowGenerator(h, w, window_size, window_size, stride, stride)
        prob_map = np.zeros((h, w), dtype=np.float)
        cnt = np.zeros((h, w), dtype=np.float)
        # XXX: 需要保证win_gen与patches具有相同长度。此处未做检查
        for (rows, cols), patch in zip(win_gen, patches):
            prob_map[rows, cols] += patch
            cnt[rows, cols] += 1
        prob_map /= cnt
        return prob_map

if __name__ == '__main__':
    BHJC(r"C:\Users\Administrator\Desktop\yaoganjieyi2\yaoganjieyi\demo_data\A.png",r"C:\Users\Administrator\Desktop\yaoganjieyi2\yaoganjieyi\demo_data\A.png")