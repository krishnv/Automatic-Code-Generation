from flask import Flask,request, render_template,jsonify
import ACFG
import Similarity_measure as sm
import ast
import re
from flask_cors import CORS
import shutil
import os
from datetime import datetime
import json
import execpython as ep

app = Flask(__name__)
CORS(app)
print("start")

@app.route("/", methods=['POST'])
def hello_world():
    data = request.data
    a = data.decode("utf-8")
    print(a)
    x = ast.literal_eval(re.search('({.+})', a).group(0))

    query=x["inputQuery"]
    lang=x["Language"]
    data=x["fileData"]
    

    print(query)
    print(lang)
    print(data)

    if(len(query) > 10) and (query) and (query.strip()):
        moveFiles()
        print("Start Execution")
        retQuery = ACFG.scrapData(query,lang,data)
        print(retQuery)
        
        joutput={}
        if(len(retQuery[1]) == 0):
            output=sm.similiarity_measure(retQuery[0])
            sourceFile=output[0]
            outputFile=output[2]
            ReferenceFile=output[1]
            joutput={"sourceFile": sourceFile, "outputFile":outputFile, "ReferenceFile":ReferenceFile }

        # if(len(retQuery[1]) == 0):
            
        elif(len(retQuery[1]) > 0):
            joutput={"sourceFile": retQuery[1][1], "outputFile":retQuery[1][2], "ReferenceFile":retQuery[1][0] }
               

    return json.dumps(joutput) 


def moveFiles():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H_%M_%S")
    # os.mkdir("C:/archive")
    os.mkdir("C:/archive/"+dt_string)
    source_dir = "C:/outputFiles/"
    target_dir = "C:/archive/"+dt_string+"/"
    
    file_names = os.listdir(source_dir)
    
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)

if __name__ == "__main__":
    app.run(debug=True)
    