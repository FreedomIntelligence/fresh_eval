

import os

class FileChecker:
    def __init__(self, directory, expected_files=None):
        if expected_files is None:
            expected_files
        self.directory = directory
        self.expected_files = expected_files

    def check_files_exist(self):
        missing_files = [file for file in self.expected_files if not os.path.exists(os.path.join(self.directory, file))]
        return missing_files

    def check_file_content(self, file_name):
        # 具体实现留给子类
        raise NotImplementedError("This method should be implemented by subclasses.")



class TextFileChecker(FileChecker):
    def check_file_content(self, file_name):
        # 实现检查文本文件内容的逻辑
        pass

class JsonFileChecker(FileChecker):
    def check_file_content(self, file_name):
        # check file length > 10:
        with open(file_name,'r') as f:
            lines=f.readlines()
            if len(lines)<10:
                print()
        # 实现检查JSON文件结构的逻辑
        # pass

print('he')



# 假设我们有一个需求，需要检查某个目录下是否存在特定的文本文件和JSON文件
directory = "/path/to/your/directory"
expected_files = ["config.json", "readme.txt"]

# 实例化检查器
text_checker = TextFileChecker(directory, [expected_files[1]])
json_checker = JsonFileChecker(directory, [expected_files[0]])

# 检查文件存在性
missing_files = text_checker.check_files_exist() + json_checker.check_files_exist()
if missing_files:
    print("以下文件缺失:", missing_files)
else:
    print("所有预期文件均存在。")

# 检查文件内容
# 这里需要具体实现 check_file_content 方法的逻辑
# text_checker.check_file_content("readme.txt")
# json_checker.check_file_content("config.json")

# missing_files = [file for file in self.expected_files if not os.path.exists(os.path.join(self.directory, file))] return missing_files
# missing_files = text_checker.check_files_exist() + json_checker.check_files_exist() if missing_files: print("以下文件缺失:", missing_files) else: print("所有预期文件均存在。")
