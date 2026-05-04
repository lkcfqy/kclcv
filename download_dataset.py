from roboflow import Roboflow
rf = Roboflow(api_key="duzPi5MSXNEm9qaoFevP")
project = rf.workspace("projects-hr9jy").project("wire-harness-validation-model")
version = project.version(1)
# 自动下载到当前目录，名称取决于数据集名称
dataset = version.download("yolov8")
print("下载完成，数据集路径为:", dataset.location)
