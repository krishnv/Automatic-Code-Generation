
import sys
from io import StringIO
import contextlib

def execPythonFile():

    inputfilepath = r"C:\Users\Nivetha.S\Documents\Python Scripts\outputfiles\main.py"


    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    with stdoutIO() as s:
        try:
            with open(inputfilepath) as fin:
                code = compile(fin.read(), inputfilepath, 'exec')
                exec(code)
        except:
            return "Something wrong with the code"
    return (s.getvalue())


if __name__ == "__main__":
    print(execPythonFile())