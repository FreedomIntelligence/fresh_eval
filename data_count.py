import os
import json
import logging
import datetime

doday=datetime.datetime.now().strftime("%Y-%m-%d")

# 设置日志
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# 指定文件夹路径
folder_path = f'.\data\{doday}'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # print('filename',filename)
    if filename.endswith('.jsonl'):  # 确保文件是JSONL格式
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r',encoding='utf-8') as f:
            lines = f.readlines()

        # 初始化计数器
        total_length, count = 0, 0

        for line in lines:
            data = json.loads(line.strip())

            # 检查text_blocks是否存在并且长度在300到5000之间
            if 'text_blocks' in data:
                length = len(data['text_blocks'])
                if 300 < length <= 5000:
                    total_length += length
                    count += 1

        # 计算平均长度
        if count > 0:
            avg_length = total_length / count
            logger.info(f"File: {filename}, Average Length: {avg_length},count:{count},total_lines:{len(lines)}")
        else:
            logger.error(f"No text blocks in the range of 300-5000 characters in file: {filename}")
