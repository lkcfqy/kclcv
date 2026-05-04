import cv2
import numpy as np
import random
import os

class CVEngine:
    def __init__(self, model_path=None):
        """
        初始化 CV 引擎。如果检测到训练好的模型文件，就加载真实的 YOLO 模型；
        否则，就使用模拟引擎。
        """
        # 优先寻找 Colab 训练下来的终极模型
        if os.path.exists("best_colab.pt"):
            model_path = "best_colab.pt"
        else:
            model_path = "runs/detect/train-2/weights/best.pt"

        self.use_real_model = os.path.exists(model_path)
        
        if self.use_real_model:
            print(f"🎉 成功找到最新训练好的真实模型: {model_path}，正在加载...")
            from ultralytics import YOLO
            self.model = YOLO(model_path)
        else:
            print(f"⚠️ 未找到真实模型 ({model_path})，引擎已降级为【随机模拟模式】")
        self.is_initialized = True

    def detect(self, image_path, expected_count):
        if self.use_real_model:
            return self._real_detect(image_path)
        else:
            return self._mock_detect(image_path, expected_count)
            
    def _real_detect(self, image_path):
        """真实的 YOLO 推理逻辑"""
        # 原数据集有9个类别（线缆、连接器、标签等）。
        # 我们只关心扎带和卡扣，因此通过 classes=[1, 8] 只过滤出 Clip(类别1) 和 strap(类别8)
        # 将 conf 调低至 0.10，让训练不充分的模型胆子大一点，宁可错杀不愿放过
        results = self.model.predict(source=image_path, conf=0.10, classes=[1, 8], save=False)
        result = results[0]
        
        # ultralytics 自带的 plot() 方法可以把预测的检测框直接画在图上
        result_img = result.plot()
        
        # 获取检测到的扎带数量 (boxes 数组的长度)
        detected_count = len(result.boxes)
        
        print(f"[真实引擎] 图像推理完成，真实的 AI 在画面中发现了 {detected_count} 个扎带/卡扣。")
        return result_img, detected_count

    def _mock_detect(self, image_path, expected_count):
        """模拟检测（没有模型时的占位代码）"""
        img = cv2.imread(image_path)
        if img is None:
            print(f"无法读取图片: {image_path}")
            return None, 0

        is_missing = random.choice([True, False])
        detected_count = expected_count
        if is_missing and expected_count > 0:
            missing_qty = random.randint(1, min(3, expected_count))
            detected_count = expected_count - missing_qty
            print(f"[模拟器] 模拟漏扎了 {missing_qty} 根")

        h, w, _ = img.shape
        result_img = img.copy()

        for i in range(detected_count):
            box_w, box_h = 40, 40
            x1 = random.randint(0, max(1, w - box_w - 1))
            y1 = random.randint(0, max(1, h - box_h - 1))
            x2 = x1 + box_w
            y2 = y1 + box_h
            
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(result_img, f"Tie", (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return result_img, detected_count
