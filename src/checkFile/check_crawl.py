
import json
import os
import pdb
class FileChecker:
    def __init__(self, directory, expected_files=None):
        if expected_files is None:
            expected_files = ['praw_reddit.jsonl', 'rq_arxiv_mathematics.jsonl', 'rq_arxiv_q_finance.jsonl', 'wr_Yahoo.jsonl', 'wr_quora_Movies.jsonl', 'rq_arxiv_computer_science.jsonl', 'rq_arxiv_statistics.jsonl', 'wr_bbc.jsonl', 'wr_quora_Technology.jsonl', 'rq_arxiv_economics.jsonl', 'rq_arxiv_physics.jsonl', 'rq_github.jsonl', 'wr_quora_Health.jsonl', 'wr_wiki.jsonl', 'rq_arxiv_eess.jsonl', 'rq_arxiv_q_biology.jsonl', 'rq_wattpad.jsonl', 'wr_quora_Mathematics.jsonl']
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
        to_file=os.path.join(self.directory,file_name)
        with open( to_file,'r') as f:
            lines=f.readlines()
            if len(lines)<10:
                print(f"file {file_name} has less than 10 lines")
                return False
            else:
                cnt=0
                total=len(lines)
                for line in lines:
                    data = json.loads(line.strip())
                    # if 'rq' in file_name:
                        # pdb.set_trace()
                    if 'text_blocks' in data.keys() and len(data['text_blocks']) > 10:
                        cnt+=1
                if cnt>total/3*1:
                    return True
                else:
                    print(f"file {file_name} has less than 2/3 lines with text_blocks > 10, cnt:{cnt},total:{total},first lines:{lines[0][:100]} ")
                    return False

def test_check_files_exist(directory=None, expected_files=None):
    if directory is None:
        directory = os.path.join('data','2024-01-03')

    json_checker = JsonFileChecker(directory=directory,expected_files=expected_files)

    # 检查文件存在性
    missing_files =json_checker.check_files_exist()
    if missing_files:
        print("missing files:", missing_files)
    else:
        print("no missing files.")
    check_file_content = json_checker.check_file_content
    okay_files, not_okay_files = [], []
    for file in json_checker.expected_files:
        if file in missing_files:
            continue
        if check_file_content(file):
            okay_files.append(file)
        else:
            not_okay_files.append(file)
    print(f"file {not_okay_files} content NOT OK\n")
    print(f"file {okay_files} content are okay\n")


if __name__ == "__main__":
    # check at the root of the project

    # directory = os.path.join('data','2024-02-14')
    test_check_files_exist()


