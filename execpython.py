
import sys
import os.path

outputfilepath = r"C:\Users\Nivetha.S\Documents\Python Scripts\outputfiles"
inputfilepath = r"C:\Users\Nivetha.S\Documents\Python Scripts\outputfiles\main.py"

orig = sys.stdout
with open(os.path.join(outputfilepath, "output.txt"), "w") as fout:
    sys.stdout = fout
    try:
        with open(inputfilepath) as fin:
            code = compile(fin.read(), inputfilepath, 'exec')
            exec(code)
    except:
        print("Error in code!. Code cannot be executed.")        
    else:
        sys.stdout = orig