# -*- coding:utf-8 -*-
import codecs
import re
import sys
import math
import numpy as np
import pickle
import os
reload(sys)
sys.setdefaultencoding('utf-8')

#state={S,B,M,E}
#text[] 存储
def pre_process(corpusPath='dict.txt'):
    fr=codecs.open('dict.txt','r','utf-8')
    fw=codecs.open('state.txt','w','utf-8')
    text = []
    output = open('text.pkl', 'wb')

    output_21=open('words.pkl','wb')
    output_22=open('words_attr.pkl','wb')
    words=[]
    words_attr=[]
    for word in fr.read().strip().split(u' '):
        if re.findall(r'/',word):
            words.append((word.strip().split(u'/'))[-2])
            words_attr.append((word.strip().split(u'/'))[-1])
    pickle.dump(words,output_21,-1)
    pickle.dump(words_attr, output_22, -1)
    output_21.close()
    output_22.close()
    fr.seek(0,0)
    for line in fr.readlines():
        wordOfline = [(w.split(u'/'))[0] for w in line.strip().split(u' ') if re.findall(r'/', w)]
        wordOfline_State=[]
        for w in wordOfline:
            if w:
                if len(w) == 1:
                    wordOfline_State.append(w+'/S')
                    text.append(w+'/S')
                else:
                    tmpW=''
                    tmpW+=(w[0]+'/B')
                    text.append(w[0] + '/B')
                    for i in range(0,len(w)-2,1):
                        tmpW+=(w[i+1]+'/M')
                        text.append(w[i+1] + '/M')
                    tmpW+=(w[-1]+'/E')
                    text.append(w[-1]+'/E')
                    wordOfline_State.append(tmpW)
        fw.writelines('  '.join(wordOfline_State)+'\n')
    pickle.dump(text, output, -1)
    print u'----------完成-------------'
    fr.close()
    fw.close()
    output.close()

#S->B B->M S->S B->E M->M M->E E->S E->B
def HMM(inputStr):
    fr=codecs.open('state.txt','r','utf-8')
    content=fr.read()
    pklfile1=open('text.pkl','rb')
    text=pickle.load(pklfile1)
    pklfile1.close()

    pklfile2=open('words.pkl','rb')
    words=pickle.load(pklfile2)
    pklfile2.close()

    pklfile3= open('words_attr.pkl', 'rb')
    words_attr = pickle.load(pklfile3)
    pklfile3.close()

    states=[]
    if os.path.exists('states.pkl'):
        pkl_file=open('states.pkl','rb')
        states=pickle.load(pkl_file)
    else:
        states=re.findall('/([SBME])',content)
        output=open('states.pkl','wb')
        pickle.dump(states,output,-1)

    # states_num=len(list(set(states)))
    # states_str=''.join(states)

    #初始选择某个状态的概率
    pi={}
    for st in ['S','B','M','E']:
        pi[st]=math.log(states.count(st)/float(len(states))) if states.count(st)/float(len(states)) <> 0 else float('-inf')
    #状态转移概率矩阵
    dic={}
    for i,st in enumerate(states):
        if i < len(states) - 1:
            dic[(st, states[i+1])]=dic.get((st, states[i+1]),0)+1

    dicA={}
    #先初始化
    for x in ['S','B','M','E']:
        for y in ['S','B','M','E']:
            dicA[(x,y)]=float('-inf')
    for x in [('S','B'),('B','M'),('S','S'),('B','E'),('M','M'),('M','E'),('E','S'),('E','B')]:
        dicA[x]=math.log(dic.get(x,0)/float(states.count(x[0]))) if dic.get(x,0)/float(states.count(x[0])) <> 0 else float('-inf')

    #状态发射矩阵
    dicB={}
    for st in ['S','B','M','E']:
        for i in range(len(inputStr)):
            dicB[(st,inputStr[i])]=math.log(text.count(inputStr[i]+'/'+st)/float(states.count(st))) if text.count(inputStr[i]+'/'+st)/float(states.count(st)) <> 0 else float('-inf')

    str_len=len(inputStr)
    location={}
    juli={}

    for i in ['S','B']:
        juli[(i,inputStr[0])]=pi[i]+dicB[(i,inputStr[0])]
    for i in ['M','E']:
        juli[(i, inputStr[0])]=float('-inf')

    for i in range(1,str_len):
        for j in ['S','B','M','E']:
            juli[(j, inputStr[i])] = float('-inf')
            location[(j,inputStr[i])] = -1
            for k in ['S','B','M','E']:
                tmp = juli[(k,inputStr[i-1])]+dicB[(j,inputStr[i])]+dicA[(k,j)]
                if  tmp > juli[(j,inputStr[i])]:
                    juli[(j, inputStr[i])] = tmp
                    location[(j,inputStr[i])]= k
    jer='S'
    maxp=float('-inf')
    for st in ['S','E']:
        if juli[st,inputStr[str_len-1]] > maxp:
            maxp=juli[st,inputStr[str_len-1]]
            jer=st

    sptr=jer
    for ch in range(str_len-1,0,-1):
        js=location[(jer,inputStr[ch])]
        sptr=js+sptr
        jer=js

    print inputStr
    print sptr
    # word=''
    # for i in range(len(sptr)):
    #     if sptr[i] == 'E' or sptr[i] == 'S':
    #         word+=inputStr[i]
    #         print word+'/'+words_attr[words.index(word)],'  ',
    #         word=''
    #     else:
    #         word+=inputStr[i]

# pre_process()
#HMM(u'19980101-01-001-001') 有问题
HMM(u'合肥工业大学翡翠湖校区')
# print u'\u8fc8'
