##### Author: Jingfeng Yang #####
## Read word embeddings, sentences and sentence embeddings, build training and test dataset ##


import numpy as np

class Sent(object):
    def __init__(self,sent,label,ebd):
        self.label=label
        self.emb=ebd
        self.sent=sent


def read_word_embeds(file='mr_workspace/word.emb'):
    voc=[]
    with open(file,'r') as reader:
        i=0
        for line in reader:
            tokens=line.strip().split()
            if i==0:
                voc_size=int(tokens[0])
                ebd_dim=int(tokens[1])
                ebd = np.zeros((voc_size,ebd_dim), dtype=np.float64)
            else:
                voc.append(tokens[0])
                ebd[i-1]=np.array([float(v) for v in tokens[(-ebd_dim):]],dtype=np.float64)
            i+=1
        assert(i-1==voc_size)
    return voc, ebd

def readData(train_label_file='data/mr/label_train.5.txt',train_text_file='data/mr/text_train.txt',
             test_label_file='data/mr/label_test.txt',test_text_file='data/mr/text_test.txt',
             sent_ebd_file='mr_workspace.5/text.emb',all_text_file='data/mr/text_all.txt'):
    allText=[]
    with open(all_text_file) as reader1, open(sent_ebd_file) as reader2:
        sent_num,sent_dim=[int(n) for n in reader2.readline().strip().split()]
        for line1,line2 in zip(reader1,reader2):
            ebd=line2.strip().split()[1:]
            assert(len(ebd)==sent_dim)
            allText.append((line1.strip().split(),np.array([float(v) for v in ebd],dtype=np.float64)))

    trainCorpus=[]

    with open(train_text_file) as reader1, open(train_label_file) as reader2:
        for line1,line2,text in zip(reader1,reader2,allText):
            assert(line1.strip().split()==text[0])
            sent=Sent(text[0],line2.strip(),text[1])
            trainCorpus.append(sent)

    totolTrainCount=0
    with open(train_text_file) as reader:
        for line in reader:
            totolTrainCount+=1

    testCorpus = []
    with open(test_text_file) as reader1, open(test_label_file) as reader2:
        for line1, line2, text in zip(reader1, reader2, allText[totolTrainCount:]):
            assert (line1.strip().split() == text[0])
            sent = Sent(text[0], line2.strip(), text[1])
            testCorpus.append(sent)


    return trainCorpus,testCorpus


if __name__ == "__main__":
    read_word_embeds()
    readData()
