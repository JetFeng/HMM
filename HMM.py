# # -*- coding:utf-8 -*-
# import jieba
# import codecs
# import numpy as np
# import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# #获取预料语料库中的一个个不同的词组(带词性)
# text=[]
# # 去除词性标注，只保存词组
# phrase=[]
# # /获取语料库中从前往后的所有词组的词性
# characters=[]
#
# def pre_process(corpusPath):
#     fr=codecs.open(corpusPath,'r','utf-8')
#     content=fr.read()
#     content = content.replace(u'\n', u'')
#     content = content.replace(u'\r', u'')
#
#     text = [w for w in content.split(u' ')]
#     for w in text:
#         if re.findall(r'/',w):
#             phrase.append((w.split(r'/'))[0])
#             characters.append('/'+(w.split(r'/'))[1])
#     # for i,j in enumerate(phrase):
#     #     print j,' ',
#     #     if i > 500:
#     #         break
#     # print '-----------------'
#     # for i,j in enumerate(characters):
#     #     print j,' ',
#     #     if i > 500:
#     #         break
#     characters_unique=list(set(characters))
#     phrase_unique=list(set(phrase))
#     ch_len=len(characters_unique)
#     ph_len=len(phrase_unique)
#
#     #统计每个词性出现的概率
#     dic_ch_poss={}
#     for ch in characters_unique:
#         dic_ch_poss[ch]=float(characters.count(ch))/characters.count()
#     #隐藏状态转移矩阵
#     d1 = np.zeros((ch_len,ch_len),float)
#     dic={}
#     for i,ch in enumerate(characters):
#         if i < ch_len-1:
#             dic[(ch,characters[i+1])]=dic.get((ch,characters[i+1]),0)+1
#     for i,ch1 in enumerate(characters_unique):
#         for j,ch2 in enumerate(characters_unique):
#             d1[i,j]=float(dic[(ch1,ch2)])/characters.count(ch1)
#     #可观察状态发射矩阵
#     d2=np.zeros((ch_len,ph_len),float)
#     for i,ch in enumerate(characters_unique):
#         for j,ph in enumerate(phrase_unique):
#             d2[i,j]=float(text.count(ch+ph))/characters.count(ch)
#     fr.close()
#     return dic_ch_poss,d1,d2
#
# def Viterbi():
#     pass
#
# def main():
#     characters_unique = list(set(characters))
#     phrase_unique = list(set(phrase))
#     N=len(characters_unique)
#
# pre_process('dict.txt')