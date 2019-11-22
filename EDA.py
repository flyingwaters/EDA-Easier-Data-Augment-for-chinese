# @ feng
# @ Time 2019.11.19
# @ content to replace the similar words of chinese words for the EDA
# ! /usr/bin/env python
# coding:utf-8

import jieba
import synonyms

import time
from random import shuffle
import argparse
import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

ap = argparse.ArgumentParser()
ap.add_argument("--num_aug", required=True, type=int, help="生成的个数")
ap.add_argument("--alpha", required=True, type=float, help="每个句子中替换的个数")
args = ap.parse_args()

num = 9
if args.num_aug:
    num = args.num_aug

alpha = 0.1
if args.alpha:
    alpha = args.alpha

f = open('stopwords/HIT_stop_words.txt')
stop_words = list()
for stop_word in f.readlines():
    stop_words.append(stop_word[:-1])

# 去除"\n"

###################
#  任务的特殊性
#  相似词替换
###################
def words_replace(words, n):
    new_words = words.copy()
    # copy 到 new_words
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    # 打乱顺序
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        # return synonyms.nearby(word)[0]
        # 同义
        # 词替换
        if len(synonyms) >= 1:
            synonyms = synonyms[2]
            # 随机返回一个近义词
            # 除去第一个
            if not contain_zh(synonyms):
                '''
                若不是中文，则抛弃掉
                若是中文，则替换掉
                '''
                synonyms = ""
            new_words = [synonyms if word == random_word else word for word in new_words]
            num_replaced += 1
            # 控制num_replaced
        if num_replaced >= n:
            break

    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return new_words

def get_synonyms(word):
    return synonyms.nearby(word)[0]

def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)
    return match


def eda(sentence, alpha_sr=0.1, num_aug = 9):
    seg_list = jieba.cut(sentence)
    seg_list = " ".join(seg_list)
    # 分词后的句子的
    words = list(seg_list.split())
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = num_aug

    n_sr = max(1, int(alpha_sr * num_words))

    # 同义词替换
    for _ in range(num_new_per_technique):
        a_words = words_replace(words, n_sr)
        # 替换n个词
        augmented_sentences.append(' '.join(a_words))

    # shuffle(augmented_sentences)
    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    augmented_sentences.append(seg_list)

    return augmented_sentences

###################
# 读入train_eda 然后eda后， write到新的文件
if __name__ == "__main__":
    f = open("data/train_eda", "r")
    for k in f:
        j = eda(sentence=k, alpha_sr=alpha, num_aug=num)
        file_num = 0
        for o in j:
            file_num += 1
            g = open("data/eda_result_{}".format(file_num), "a")
            g.write(o+"\n")
            g.flush()
    g.close()
    f.close()
    print("ending!!!!!")







