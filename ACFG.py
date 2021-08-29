import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pymongo
import os

import re


def regexmatch(y):
  pair = re.compile(r"[^\(]*(\(.*\))[^\)]*")
  match=pair.match(y)
  if match is None:
    return False
  else:
    return True

def createJavaCode(code):
    s=""
    s+="public class Main{\n\n"
    s+="public static void main(args String){\n\n"
    s+=code
    s+="}\n\n"
    s+="}"
    return s

def createPyCode(code):
    s=""
    s+="def main():\n\t"
    s+=code
    s+='\n'
    s+='\n'
    s+="""if __name__=="__main__":"""
    s+='\n\t'
    s+="main()"
    return s

# wcResult=[]
def perfromWordCount(data):
        refurl="https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/"
        code=createPyCode("len(data.split())")
        output =len(data.split())
        wcResult=[refurl,code,output]
        return wcResult



def scrapData(query,langs,inputFileData):
    
    # query = 'read text file using python'
    results =set()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ACFG"]
    collection = db["ACFGCollection"]
    query = query + " " +langs
    print("query ====>  "+query)
    if(query.find("word count") >= 0) and (inputFileData) and (inputFileData.strip()):
        wcResult=perfromWordCount(inputFileData)
        return [query,wcResult]
    else:
        # make sure you search for genuine sites
        for i in search(query,lang='en',num_results=10):
            results.add(i)
        print(results)
        

        for val in results:
            data=[]
            print("link ==>" + val)
            r=requests.get(val)
            htmlContent = r.content
            soup = BeautifulSoup(htmlContent,'html.parser')
            title=soup.title.text
            data = soup.find_all('code')
            fdata=[]
        
            
            dictionary= {'query' :query}
            for i, x in enumerate(data):
                if(len(str(x.text)) > 20) and (str(x.text).find("#") == -1) and  (str(x.text).endswith(".") == False) and regexmatch(str(x.text)):
                    print("length is {} text is == > {}".format(len(str(x.text).strip()),x.text))
                    fdata.append(x.text)
            s = ""
            for d in fdata:
                s += d     
            
            code =str(s)
            if(langs.lower()== "python"):
                code=createPyCode(s)
            elif(langs.lower()== "java"):
                code=createJavaCode(s)

            print("=================Code starts==================")
            print(code)
            print("=================Code Ends==================")
            dictionary['code'] =code
            dictionary['link'] =val
            dictionary['title']=title
            print("--------------------------------")
            collection.insert_one(dictionary)
        print("Search Result Saved in MongoDB")
        wcResult=[]
        return [query,wcResult]



# if __name__=="__main__":
#     scrapData()
#     sm.similiarity_measure(str_param="")