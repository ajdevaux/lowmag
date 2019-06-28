import os
import shutil


def main():
    
    py_files = search_for_pyc_files()
    for fn in  py_files:
        print fn
        os.remove(fn)
    if (os.path.isfile('..\IRIS.zip')):
        os.remove('..\IRIS.zip')

def search_for_pyc_files():
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.') for f in filenames if os.path.splitext(f)[1] == '.pyc']
    return result

if __name__ == '__main__':
    main()  
