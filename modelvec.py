import re
from gensim.models import Word2Vec
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx


def text_clearing(text):
    hangul = re.compile('[^ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', text)
    return result


f = open("data/return.txt", "r", encoding='utf-8')
token = []
text = f.readlines()
for i in text:
    temp = []
    for j in i.strip().split():
        word = text_clearing(j)
        if word:
            temp.append(word)
    token.append(temp)


# 단어벡터 학습 모델 생성 하는 함수 128차원으로 만들었다.
def modelmaker(token):
    model = Word2Vec(sentences=token, vector_size=100, window=5, min_count=5, workers=4, sg=0)
    model_file = 'word2vec-TeenInstagram.model'
    model.save(model_file)
    print(f"--> Model file <{model_file}> was created!\n")
    return model


def visualization(G, imageFileName, nodecolor='skyblue'):
    plt.figure(figsize=(5, 6), dpi=80)
    matplotlib.rc('font', family="Nanum Gothic")
    mpl.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용시 마이너스 폰트 깨짐 해결

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color=nodecolor)  # default color: '#1f78b4'

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=1.2, edge_color='blue')
    nx.draw_networkx_edges(G, pos, edgelist=esmall,
                           width=1.2, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_family='Nanum Gothic', font_size=8)

    plt.axis('off')
    plt.savefig('%s' % (imageFileName))  # save as png
    # print('It was saved %s' % (imageFileName))
    # plt.show()  # display


def setEdges_simWords(model, word, n1=10, n2=5):
    simWords = model.wv.most_similar(word, topn=n1)

    G = nx.Graph()
    for (w2, wgt) in simWords:
        G.add_edge(word, w2, weight=wgt)

    for (w2, wgt) in simWords:
        simWords2 = model.wv.most_similar(w2, topn=n2)
        for (w3, wgt) in simWords2:
            G.add_edge(w2, w3, weight=wgt)

    return G


def similarity(key, input1, input2, model):
    temp = []
    temp.append(model.wv.similarity(key, input1))
    temp.append(model.wv.similarity(key, input2))
    return temp

# 모델 생성.
model = modelmaker(token)
# visualization(setEdges_simWords(model,"패션"),"newimage")
#
# print(model.wv.similarity("패션","한복"))
# print(model.wv.similarity("패션","정장"))
