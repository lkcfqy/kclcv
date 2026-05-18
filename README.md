# kclcv

工业图像视觉检测验证原型。当前应用是一个 PyQt5 桌面工具，用来加载图片、调用 YOLO 检测模型，并在界面上显示扎带/卡扣等目标的检测框和数量，供人工核对。

## 当前状态

当前版本是“纯视觉检测”流程，原先与 Excel 解析或工单比对相关的逻辑已经从主应用中移除。`app.py` 会启动桌面 GUI；`cv_engine.py` 会优先寻找本地训练好的 YOLO 权重，如果没有找到真实模型，则降级为模拟模式。

真实模型默认查找路径：

- `best_colab.pt`
- `runs/detect/train-2/weights/best.pt`

如果两个文件都不存在，程序仍可启动，但检测结果只是占位模拟，不具备实际识别意义。

## 主要文件

- `app.py`：PyQt5 桌面界面入口。
- `cv_engine.py`：YOLO 推理与模拟检测封装。
- `download_dataset.py`：Roboflow 数据集下载脚本。
- `train_yolo_colab.ipynb`：Colab 训练 YOLO 的参考笔记本。
- `*.docx` / `*.xlsx`：项目说明、验收计划和历史参考资料。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install pyqt5 opencv-python ultralytics roboflow
python app.py
```

如需使用真实检测，请先把训练好的权重放到 `best_colab.pt`，或放到 `runs/detect/train-2/weights/best.pt`。

## 训练与数据

`train_yolo_colab.ipynb` 记录了在 Colab 中安装依赖、下载 Roboflow 数据集、训练 `yolov8x.pt` 并保存权重的流程。`download_dataset.py` 目前包含项目特定的 Roboflow 配置；公开复用前建议改为从环境变量读取 API Key，避免把密钥写进代码。

## 注意事项

- 当前推理只过滤 `Clip` 和 `strap` 两类目标，代码中对应 `classes=[1, 8]`。
- 当前置信度阈值为 `0.10`，偏向“宁可多检出，后续人工核对”。
- 模拟模式下，因为主界面传入的期望数量为 0，通常不会产生有效检测框。

## 许可证

当前仓库未包含独立 `LICENSE` 文件。如需公开复用或分发，请先补充明确的开源许可证。
