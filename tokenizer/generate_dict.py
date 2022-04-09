import os
from collections import Counter

"""
    根据语料
    生成dict 文件
"""


class GenerateDict:
    def __init__(self, data_files):
        self.data_files = data_files
        self._parse_file()

    def _parse_file(self):
        if os.path.exists('dict.txt'):
            return
        if len(self.data_files) == 0:
            return
        counter = Counter()
        for file in self.data_files:
            if not os.path.exists(file):
                continue
            f = open(file, encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                word_arr = line.strip().split()
                counter.update(word_arr)
            f.close()
        if len(counter) == 0:
            return
        sorted_arr = sorted(counter.items(), key=lambda item: item[1], reverse=True)
        out_file = open('dict.txt', 'w', encoding='utf-8')
        for word, num in sorted_arr:
            line = word + ' ' + str(num) + '\n'
            out_file.write(line)
        out_file.close()


if __name__ == '__main__':
    data_files = ['data.txt']
    GenerateDict(data_files)
