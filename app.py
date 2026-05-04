import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from cv_engine import CVEngine

class AntiLeakageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("纯视觉检测验证系统")
        self.setGeometry(100, 100, 1100, 700)
        
        # 1. 初始化模块 (已移除 Excel 解析器)
        self.cv_engine = CVEngine()
        
        self.initUI()
        
    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        
        # ================= 左侧：图像显示区域 =================
        left_layout = QVBoxLayout()
        self.image_label = QLabel("请点击右侧加载测试图片...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #aaa; font-size: 18px; color: #555;")
        self.image_label.setMinimumSize(720, 540)
        left_layout.addWidget(self.image_label)
        
        # ================= 右侧：控制与数据区域 =================
        right_layout = QVBoxLayout()
        right_layout.setSpacing(25)
        
        # 1. 标题
        title = QLabel("视觉检测人工核对系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        right_layout.addWidget(title)
        
        # 2. 数据展示看板
        self.actual_count_label = QLabel("视觉实际检测总数: 0 个")
        self.actual_count_label.setStyleSheet("font-size: 20px; color: #0056b3; font-weight: bold; padding: 15px; border: 2px solid #b8daff; background-color: #cce5ff; border-radius: 5px;")
        right_layout.addWidget(self.actual_count_label)
        
        # 3. 提示信息
        self.result_label = QLabel("待机中")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 30px; background-color: #e9ecef; border-radius: 10px;")
        right_layout.addWidget(self.result_label)
        
        # 4. 操作按钮 (加载图片)
        self.btn_load = QPushButton("加载图片进行检测")
        self.btn_load.setMinimumHeight(60)
        self.btn_load.setStyleSheet("""
            QPushButton {
                font-size: 18px; font-weight: bold; color: white; background-color: #28a745; border-radius: 5px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        self.btn_load.clicked.connect(self.load_image_and_detect)
        right_layout.addWidget(self.btn_load)
        
        right_layout.addStretch() # 底部占位
        
        # 组合布局
        main_layout.addLayout(left_layout, stretch=7)
        main_layout.addLayout(right_layout, stretch=3)
        main_widget.setLayout(main_layout)

    def load_image_and_detect(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择测试图片", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            # 运行 CV 引擎
            self.result_label.setText("正在识别...")
            self.result_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 30px; background-color: #e9ecef; color: black; border-radius: 10px;")
            QApplication.processEvents() # 刷新UI
            
            # expected_count 传入 0，因为已经不再需要比对了
            result_img, detected_count = self.cv_engine.detect(file_path, 0)
            
            if result_img is not None:
                # 更新实际数量显示
                self.actual_count_label.setText(f"视觉实际检测总数: {detected_count} 个")
                
                # 仅展示检测结果供人工验证
                self.result_label.setText(f"检测完毕！请核对画面中的绿框")
                self.result_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 30px; background-color: #17a2b8; color: white; border-radius: 10px;")
                
                # 将处理好的图片显示到界面上
                rgb_image = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                
                # 保持宽高比自适应显示，不拉伸变形
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AntiLeakageApp()
    window.show()
    sys.exit(app.exec_())
