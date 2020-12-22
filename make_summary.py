from readCsv import getTitles, getContents
import csv
import numpy as np
from konlpy.tag import Kkma
from sklearn.feature_extraction.text import TfidfVectorizer

kkma = Kkma()

list_titles = getTitles()
list_contents = getContents()

f = open('summaries.csv', 'w', newline="\n", encoding='utf-8')
writer = csv.writer(f)

for contents in list_contents:
    list_sentences = []
    list_temp = kkma.sentences(contents)
    for i in range(len(list_temp)):
        if len(list_temp[i]) > 10:
            list_sentences.append(list_temp[i])
    tfidf = TfidfVectorizer()
    tfidf_sentence_matrix = tfidf.fit_transform(list_sentences).toarray()
    transpose_tfidf_sentence_matrix = np.transpose(tfidf_sentence_matrix) # 그래프 생성을 위한 전치행렬 만들기
    sentence_graph = np.dot(tfidf_sentence_matrix, transpose_tfidf_sentence_matrix) # 전치행렬과의 곱으로 그래프에서 어느 노드들이 엣지로 연결되었는지 나타내는 정사각 행렬을 구한다.
    d = 0.85 # damping factor , PageRank에서 웹 서핑을 하는 사람이 해당 페이지를 만족하지 못하고 다른페이지로 이동하는 확률로써, TextRank에서도 그 값을 그대로 사용(0.85로 설정)
    A = sentence_graph
    size = sentence_graph.shape[0]
    for i in range(size):
        A[i][i] = 0
        sum_row = np.sum(A[i][:])
        if sum_row != 0:
            A[i][:] /= sum_row # textrank formula에서 한 노드와 연결된 다른 노드들의 가중치값을 나누는 부분 -> 이후 상수에 반영 
        A[i][:] *= -d # TR(Vi) = (1-d) + d * sum(가중치*TR(Vj)) -> TR(Vi) - d(c1TR(Va) + c2TR(Vb) + c3TR(Vc) + c4TR(Vd)) = 1 - d (c1, c2, c3, c4 is constant) ->Ax=B
        A[i][i] = 1
    B = (1 - d) * np.ones((size, 1))
    textrank = np.linalg.solve(A, B) # x = [TR(Va), TR(Vb), TR(Vc), TR(Vd)] -> each textrank
    idx_textrank = enumerate(textrank)
    sorted_textrank = sorted(idx_textrank, key = lambda x: x[1], reverse = True)

    contents = ""
    summaries = []

    for idx in sorted_textrank[:5]:
        contents  = contents + list_sentences[idx[0]]
    summaries.append(contents)
    for summary in summaries:
        writer.writerow([summary])

f.close()