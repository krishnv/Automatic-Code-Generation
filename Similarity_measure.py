# Program to measure the similarity between 
# two sentences using cosine similarity.
import nltk
from nltk.internals import java
import pymongo
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
# nltk.download()
import execpython as ep

def similiarity_measure(str_param):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    # Database Name
    db = client["ACFG"]
    
    # Collection Name
    col = db["ACFGCollection"]

    # reading data from db
    x = col.find({"query":str_param})

    # creating dataframe and writing data into it
    df = pd.DataFrame(x)
    df = df[df['code'].notnull()]
    df = df.drop_duplicates(subset = ['query','title'],keep = 'last').reset_index(drop=True)
    length = len(df['query'])
    df2 = pd.DataFrame(columns=['query', 'title', 'Similarity'])


    for i in range(length):
        X = df['query'][i]
        Y = df['title'][i]
        
        # tokenization
        X_list = word_tokenize(X) 
        Y_list = word_tokenize(Y)

        # Converting data to lower case
        for i in range(len(X_list)):
            X_list[i]=X_list[i].lower()

        for i in range(len(Y_list)):
            Y_list[i]=Y_list[i].lower()

        #sw contains the list of stopwords
        sw = stopwords.words('english') 
        l1 =[];l2 = []
    
        # lemmatizing (removing ing forms from verb)
        lemmatizer = WordNetLemmatizer()
        X_set = {lemmatizer.lemmatize(w) for w in X_list}
        Y_set = {lemmatizer.lemmatize(w) for w in Y_list}

        # Stemming (extracting root word of given word)
        ps = PorterStemmer()
        X_set = {ps.stem(w) for w in X_set}
        Y_set = {ps.stem(w) for w in Y_set} 

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
        
        # writing coisne data to dataframe
        df2 = df2.append({'query': X, 'title': Y, 'Similarity': cosine}, ignore_index=True)

    # Fetching the best Similarity by taking value nearer to 1    
    df2 = df2.iloc[(df2['Similarity']-1).abs().argsort()[:1]]

    # Fetching title related to the best similarity obtained
    final_title = df2['title'].values
    listToStr = ''.join([str(elem) for elem in final_title])

    # Fetching code data from db data related to the title obtained
    final_code = df.loc[df['title'] == listToStr, 'code'].iloc[0]
    final_code = ''.join([str(elem) for elem in final_code])

    # Fetching link data from db data related to the title obtained
    final_url = df.loc[df['title'] == listToStr, 'link'].iloc[0]
    final_url = ''.join([str(elem) for elem in final_url])


    # write to file
    f = open(r"C:\outputFiles\bestlink.txt", "w")
    f.write(final_url)
    f.close()

    # if language is java  main.java
    # if language is python  main.py
    # str_param = "file reac in python"
    l = str_param.split()
    lngth = len(l)
    langs=l[lngth - 1]
    print("language is ====>" + langs)
    if(langs.lower() == "python"):
        f = open(r"C:\outputFiles\main.py", "w")
        f.write(final_code)
        f.close()
        fo = open(r"C:\outputFiles\Pythonoutput.txt", "w")
        fo.write(ep.execPythonFile())
        fo.close()
        return[final_code,final_url,ep.execPythonFile()]
    elif(langs.lower() == "java"):
        f = open(r"C:\outputFiles\main.java", "w")
        f.write(final_code)
        f.close()
        fo = open(r"C:\outputFiles\Javaoutput.txt", "w")
        fo.write("Java output")
        fo.close()
        return[final_code,final_url,"Java output"]
        

    
    