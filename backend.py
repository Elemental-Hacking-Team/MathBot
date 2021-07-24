# function to transfrom fraction as string to float
def frac2float(string):
    import re
    fraction = re.findall(r'[0-9]{1,}/+[0-9]{1,}', string)
    numbers = re.findall(r'[0-9]{1,}', fraction[0])
    num = int(numbers[0])
    den = int(numbers[1])
    number = num/den

    return num, den, number

# compare two fractions
def maxfraction(float1, float2):

    if (float1 > float2) == True:
        great = float1
        less = float2
    else:
        great = float2
        less = float1

    return great, less


# get information from dataset
def findbestanswer(user, dfconcepts):
    import pandas as pd
    # function for text comparison
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    def sent_comparison(X, Y):
        # tokenization
        X_list = word_tokenize(X)
        Y_list = word_tokenize(Y)

        # sw contains the list of stopwords
        sw = stopwords.words('english')
        l1 =[]
        l2 =[]

        # remove stop words from the string
        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}

        # form a set containing keywords of both strings
        rvector = X_set.union(Y_set)
        for w in rvector:
            if w in X_set: l1.append(1) # create a vector
            else: l1.append(0)
            if w in Y_set: l2.append(1)
            else: l2.append(0)
        c = 0

        # cosine formula
        for i in range(len(rvector)):
                c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)

        return cosine

    rlist = []
    qlist = []

    for index, row in dfconcepts.iterrows():

        r = sent_comparison(user, row['Questions'])
        rlist.append(r)
        qlist.append(row['Questions'])

        maxrlist = max(rlist)

    qindex = rlist.index(maxrlist)
    answer = dfconcepts.iloc[qindex,1]
    qtag = qlist[qindex]

    return answer, qtag

# function for printing circles
def printfraction(num,den):
    import matplotlib.pyplot as plt
    import numpy as np
    
    list = [den] * den
    Color = ["White"] * den

    for i in range(num):
        Color[i] = (0.2, 0.6, 1, 0.9)

    # plt.pie(list, autopct=lambda p:f'1/%d' % (den), colors = Color, wedgeprops={"edgecolor":"0",'linewidth': 1, 'antialiased': True}, startangle = 90)
    plt.pie(list, colors = Color, wedgeprops={"edgecolor":"0",'linewidth': 1, 'antialiased': True}, startangle = 90)
    plt.savefig('fraction{}-{}.png'.format(num, den))
    plt.close("all")
