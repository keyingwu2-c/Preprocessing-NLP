import os
import csv
import random
import string
import jieba
import re
import numpy as np

def add_randpuns(path, inpf, outf):
    os.chdir(path)
    str_puns = string.punctuation
    list_puns = list(str_puns)
    # print(list_puns)
    max_pun_indx = len(list_puns) - 1
    with open(inpf, encoding='utf-8') as csvfile:

        reader = csv.reader(csvfile)
        writer = csv.writer(open(outf, 'w', encoding='utf-8'), delimiter=",", lineterminator='\n')
        for line in reader:
            # line[0] += ('。')
            linelist = list(line[0])
            n_puns = random.randint(1, 3)
            max_indx = len(line[0]) - 1

            for i in range(1, n_puns):
                position = random.randint(1, max_indx)
                pun_indx = random.randint(0, max_pun_indx)
                linelist.insert(position, list_puns[pun_indx])
            line[0] = "".join(linelist)
            print(line[0])
            # print(max_indx)
            writer.writerow([line[0]])

    return outf

def remove_puns(path, inpf, outf):
    os.chdir(path)
    with open(inpf, encoding='utf-8') as csvfile:

        reader = csv.reader(csvfile)
        writer = csv.writer(open(outf, 'w', encoding='utf-8'), delimiter=",", lineterminator='\n')
        for line in reader:
            line[0] = line[0].translate(str.maketrans("", "", string.punctuation))
            print(line[0])
            writer.writerow([line[0]])
    return outf

def filter_sents(path, inpf, outf, max_len):
    os.chdir(path)
    with open(inpf, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(open(outf, 'w', encoding='utf-8'), delimiter=",", lineterminator='\n')
        line_indx = 1
        for line in reader:
            str_lineindx = str(line_indx)
            print(str_lineindx)
            len_strlidx = len(str_lineindx)
            print(str(len_strlidx))
            line[0] = line[0][len_strlidx:]
            print(line[0])
            line_indx = line_indx + 1
            if len(line[0])< (max_len+1):
                #print(line[0])
                writer.writerow([line[0]])
    return outf

def tokenize_sents(path, inpf, outf, concatenator):
    os.chdir(path)
    with open(inpf, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(open(outf, 'w', encoding='utf-8'), delimiter=",", lineterminator='\n')

        for line in reader:
            tokenized = jieba.cut(line[0])
            line[0] = concatenator.join(tokenized)
            print(line[0])
            writer.writerow([line[0]])
    return outf

def remove_stopwds(path, inpf, outf, stpwf):
    os.chdir(path)
    file_stpw = open(stpwf, encoding='utf-8')
    text_stpw = file_stpw.read()
    file_stpw.close()
    list_stpw = text_stpw.split('\n')
    print(list_stpw)
    with open(inpf, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(open(outf, 'w', encoding='utf-8'), delimiter=",", lineterminator='\n')

        for line in reader:
            mywordlist = []
            for word in line[0].split('/'):
                if not(word.strip() in list_stpw) and len(word.strip()) > 1:
                    mywordlist.append(word)
            print(mywordlist)
            writer.writerow([' '.join(mywordlist)])

    return outf

def count_words(path, inpf, min_count, max_vocab=-1):
    os.chdir(path)
    with open(inpf, encoding='utf-8') as f:
        text = f.read()
        list_all_words = re.split('\s|\n',text)
        #print(list_all_words[0:100])
        vocabs = set(list_all_words)
        #print(vocabs)
        vocab_count = {}
        for word in vocabs:
            vocab_count[word] = 0
        for word in list_all_words:
            vocab_count[word] += 1
        vocab_count_list = []
        for word in vocab_count:
            if vocab_count[word] > min_count:
                vocab_count_list.append((word, vocab_count[word]))
        vocab_count_list.sort(key=lambda x: x[1], reverse=True)
        if len(vocab_count_list) > max_vocab:
            vocab_count_list = vocab_count_list[:max_vocab]
        #print(vocab_count_list)

    return vocab_count_list

def word2onehot(vocab_count_list):
    onehotveclen = len(vocab_count_list)
    n_words = onehotveclen
    vocab_list = list()
    for tup in vocab_count_list:
        vocab_list.append(tup[0])
    print(vocab_list)
    #创建矩阵变量，或其它方法

    list_onehot = list()
    for value in vocab_list:
        zovl = [0 for _ in range(n_words)]
        indx = vocab_list.index(value)
        zovl[indx] = 1
        list_onehot.append(zovl)
    print(list_onehot[1])
    mat_oh = np.array(list_onehot)
    print(mat_oh.shape)
    return mat_oh

if __name__ == '__main__':
    path = 'C:\元微培训\word2vec'
    input_file = "train5.csv"
    output_file = ""
    concatenator = "/"
    stpwf_file ="stopwords.txt"
    #add_randpuns(path, input_file, output_file)
    #remove_puns(path, input_file, output_file)
    #filter_sents(path, input_file, output_file, max_len=40)
    #tokenize_sents(path, input_file, output_file, concatenator)
    #remove_stopwds(path, input_file, output_file, stpwf_file)
    vocab_count_list = count_words(path, input_file, min_count=10)
    print(vocab_count_list)
    word2onehot(vocab_count_list)



