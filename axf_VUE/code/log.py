import logging


# 实例，最终操作对象
logger = logging.getLogger(__name__)
# 处理者
file_handler = logging.FileHandler("log.txt")
file_formatter = logging.Formatter("%(levelname)s - %(asctime)s -% >%(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.error("haha")
# 格式化
# 过滤器
# 设置格式化

