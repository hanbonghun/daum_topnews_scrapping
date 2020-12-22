from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_similar(title, list_title,list_contents):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(list_contents)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    index = list_title.index(title) # Get the index of a particular article
    sim_scores = list(enumerate(cosine_sim[index])) # enumerate -> To create sequence pairs between article content and words
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True) # Similarities are expressed in sim_scores[1] -> key = lambda x: x[1], reverse=True -> descending order
    sim_scores = sim_scores[1:6] # In order to use only the top 5 articles with similarity.
    indices = [i[0] for i in sim_scores] # Index is expressed in sim_scores[0] -> i[0] for i in sim_scores
    sim_title = [] # To make a list of the titles of articles
    for i in indices:
        sim_title.append(list_title[i])
    return sim_title # Return list of titles for 5 articles with high similarity

