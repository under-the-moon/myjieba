"""
生成 HMM 参数
（A, B, pi） 发射概率、转移概率、初始概率
"""

import os
from math import log
import json

MIN_FLOAT = -3.14e100


class GenerateProb:
    def __init__(self, data_files):
        self.data_files = data_files
        self.STATUS = 'BMES'
        # 初始概率
        self.PI = {}
        # 发射概率
        self.A = {}
        # 转移概率
        self.B = {}
        self._parse_file()

    def _parse_file(self):
        if len(self.data_files) == 0:
            return
        for file in self.data_files:
            if not os.path.exists(file):
                continue
            f = open(file, encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                word_arr = line.strip().split()
                labels = []
                for index, word in enumerate(word_arr):
                    if len(word) == 1:
                        label = 'S'
                    else:
                        label = 'B' + 'M' * (len(word) - 2) + 'E'
                    # 取第一个字
                    if index == 0:
                        key = label[0]
                        if key in self.PI:
                            self.PI[key] += 1
                        else:
                            self.PI[key] = 1
                    # 对于每一个词统计发射数
                    for i, item in enumerate(label):
                        ch = word[i]
                        if item not in self.A:
                            self.A[item] = {}
                            self.A[item][ch] = 1
                        else:
                            if ch not in self.A[item]:
                                self.A[item][ch] = {}
                                self.A[item][ch] = 1
                            else:
                                self.A[item][ch] += 1

                    labels.extend(label)
                # 统计B
                for i in range(1, len(labels)):
                    pre_status = labels[i - 1]
                    cur_status = labels[i]
                    if pre_status not in self.B:
                        self.B[pre_status] = {}
                        self.B[pre_status][cur_status] = 1
                    else:
                        if cur_status not in self.B[pre_status]:
                            self.B[pre_status][cur_status] = {}
                            self.B[pre_status][cur_status] = 1
                        else:
                            self.B[pre_status][cur_status] += 1
            f.close()
        # 计算 PI A B
        self.__calc_params()

    def __calc_params(self):
        # 统计PI
        total = 0.
        for key, value in self.PI.items():
            total += value
        for state in self.STATUS:
            if state not in self.PI:
                self.PI[state] = MIN_FLOAT
            else:
                self.PI[state] = log(self.PI[state] / total)
        # 统计 B
        for key, item in self.B.items():
            total = 0.
            for inner_key, value in item.items():
                total += value
            for inner_key, value in item.items():
                item[inner_key] = log(value / total)

        # 统计 A
        for key, item in self.A.items():
            total = 0.
            for inner_key, value in item.items():
                total += value
            for inner_key, value in item.items():
                item[inner_key] = log(value / total)


if __name__ == '__main__':
    data_files = ['data.txt']
    prob = GenerateProb(data_files)
    data = {
        'PI': prob.PI,
        'B': prob.B,
        'A': prob.A
    }
    if not os.path.exists('prob.json'):
        print('write prob to json')
        with open('prob.json', 'w') as f:
            json.dump(data, f)
