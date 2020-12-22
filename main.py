import Cosine_Similarity
import Frequency
import os
from readCsv import getContents,getTitles,getSummaries

import time
def printTitleList(TOTAL,TOTAL_PAGE,page, list_title):
    for i in range(int(TOTAL / TOTAL_PAGE) * (page - 1), int(TOTAL / TOTAL_PAGE) * (page)):
        print(str(i + 1) + ' : ' + list_title[i])

if __name__ == "__main__":
    summaries = getSummaries()
    list_title = getTitles()
    list_contents = getContents()

    TOTAL = len(list_title) # number of articles
    TOTAL_PAGE = TOTAL/20 # number of the printed page
    page = 1
    os.system('cls')
    while True:
        printTitleList(TOTAL,TOTAL_PAGE,page, list_title)
        print("----------------------------------------------------------------------------------------------\n")
        print("                      '>' : Next Page                '<' : Previous Page                      \n")
        print("----------------------------------------------------------------------------------------------\n")

        data = input("Please Input Data : ")
        a = time.time()
        if data == '>':
            if page < TOTAL_PAGE:
                page += 1
            os.system('cls')

        elif data == '<':
            if page > 1:
                page -= 1
            os.system('cls')

        elif data in list_title:    # When an article title is entered in the input value
            index = list_title.index(data)
            os.system('cls')
            print('<Summary>\n')
            print(summaries[index])
            print('\n<Article>\n\n')
            print('<' + list_title[index] + '>' + '\n')
            print(list_contents[index])

            #Find the similarity and output the articles in the order of the highest similarity
            list_sim = Cosine_Similarity.get_similar(list_title[index],list_title,list_contents)
            print("\n\n<Similar Articles>\n")
            for i in range(0, len(list_sim)):
                print(str(i + 1) + ". " + list_sim[i])

            #Prints the words that appear the most in the article in order
            print("\n\n<High Frequency Word>\n")
            rank_word = Frequency.get_FrequencyWord(index)
            for i in range(0, len(rank_word)):
                print(str(i + 1) + ". " + rank_word[i])
            print("\n\n")
            b = time.time()
            print(b-a)
#####################################################################################################

            data = input("Move Main Page or Exit Program? (Enter Yes or Exit) : ")
            if data.lower() == 'yes'.lower():
                page = 1
                os.system('cls')
            elif data.lower() == 'exit'.lower():
                break

        elif ' ' not in data:
            os.system('cls')
            rank_title = Frequency.get_FrequencyTitle(data)
            print("<Articles that '" + data + "' appeared a lot>\n")
            for i in range(0, len(rank_title)):
                print(str(i + 1) + ". " + list_title[i])
            print("\n\n")
            data = input("Move Main Page or Exit Program? (Enter Yes or Exit) : ")
            if data.lower() == 'yes'.lower():
                page = 1
                os.system('cls')
            elif data.lower() == 'exit'.lower():
                break
