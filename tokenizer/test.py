import jieba
import tokenizer

sentence = '我说北京是中国首都'

data = list(jieba.cut(sentence))
print('jieba:', data)
data = tokenizer.cut(sentence)
print('tokenizer:', data)
