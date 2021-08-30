import pymongo
  
  
client = pymongo.MongoClient("mongodb://localhost:27017/")
 
# Database Name
db = client["ACFG"]
  
# Collection Name
col = db["ACFGCollection"]

# read form MongoDB  
x = col.find({"query": "read text file using python"})
result=[]
for y in x:
    result.append(y)

for f in result:
    print(f['title'])
    print(f['link'])
    print(f['code'])