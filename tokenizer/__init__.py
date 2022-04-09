from math import log
import hmm


class Tokenizer:
    def __init__(self):
        self.initialized = False
        self.FREQ, self.total = {}, 0
        self.initialize()

    def initialize(self):
        freq_dict = {}
        total = 0
        f = open('dict.txt', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            word_freq = line.split()
            if len(word_freq) < 2:
                continue
            word, freq = word_freq[0:2]
            freq = int(freq)
            freq_dict[word] = freq
            total += freq
            for ch in range(len(word)):
                sub_word = word[:ch + 1]
                if sub_word not in freq_dict:
                    freq_dict[sub_word] = 0
        f.close()
        self.FREQ, self.total = freq_dict, total
        self.initialized = True

    def check_initialized(self):
        if not self.initialized:
            self.initialize()

    def get_DAG(self, sentence):
        self.check_initialized()
        DAG = {}
        N = len(sentence)
        for k in range(N):
            tmplist = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.FREQ:
                if self.FREQ[frag]:
                    tmplist.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not tmplist:
                tmplist.append(k)
            DAG[k] = tmplist
        return DAG

    def calc(self, sentence, DAG, route):
        N = len(sentence)
        route[N] = (0, 0)
        logtotal = log(self.total)
        for idx in range(N - 1, -1, -1):
            route[idx] = max((log(self.FREQ.get(sentence[idx:x + 1]) or 1) -
                              logtotal + route[x + 1][0], x) for x in DAG[idx])

    def __cut_DAG(self, sentence):
        DAG = self.get_DAG(sentence)
        route = {}
        self.calc(sentence, DAG, route)
        x = 0
        N = len(sentence)
        result = []
        buf = ''
        while x < N:
            y = route[x][1] + 1
            tmp_word = sentence[x:y]
            if y - x == 1:
                buf += tmp_word
            else:
                if buf:
                    if len(buf) == 1:
                        result.append(buf)
                    else:
                        if buf not in self.FREQ:
                            # HMM 分词
                            recognized = hmm.cut(buf)
                            for elem in recognized:
                                result.append(elem)
                        else:
                            for elem in buf:
                                result.append(elem)
                    buf = ''
                result.append(tmp_word)
            x = y
        if buf:
            if len(buf) == 1:
                result.append(buf)
            elif buf not in self.FREQ:
                # HMM 分词
                recognized = hmm.cut(buf)
                for elem in recognized:
                    result.append(elem)
            else:
                for elem in buf:
                    result.append(elem)
        return result

    def cut(self, sentence, HMM=True):
        if HMM:
            cut_block = self.__cut_DAG
        else:
            raise NotImplemented("error not implement")

        return cut_block(sentence)


tk = Tokenizer()
cut = tk.cut
