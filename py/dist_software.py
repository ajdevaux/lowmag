from IRIS import IRIS
import os
import shutil

import distutils.dir_util
import distutils.file_util 

import zipfile




dist_folder = 'IRIS/'
full_dist = '../' + dist_folder

py_dist = full_dist + 'py/'

def main():
    
    if (os.path.isdir(full_dist)):
        shutil.rmtree(full_dist)
    distutils.dir_util.mkpath(full_dist)
    distutils.dir_util.mkpath(py_dist)
    distutils.dir_util.copy_tree('.', py_dist)
    py_files = search_for_py_files()
    for fn in  py_files:
        print fn
        os.remove(fn)
    fld = 'bin/'
    distutils.dir_util.copy_tree('../' + fld, full_dist + fld)
    fld = 'config/'
    distutils.dir_util.copy_tree('../' + fld, full_dist + fld)
    fld = 'resources/'
    distutils.dir_util.copy_tree('../' + fld, full_dist + fld)
    distutils.dir_util.mkpath(full_dist + 'data/')
    file = open(full_dist + 'data/' + "dummy.txt", "w")
    file.write("Dummy file for Data Directory")
    file.close()
    
    fld = 'Run_IRIS.bat'
    distutils.file_util.copy_file('../' + fld, full_dist + fld)

    zipf = '../IRIS'
    zip(full_dist, zipf)
    shutil.rmtree(full_dist)

def search_for_py_files():
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(full_dist) for f in filenames if os.path.splitext(f)[1] == '.py']
    return result

def search_for_pyc_files():
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.') for f in filenames if os.path.splitext(f)[1] == '.pyc']
    return result

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()


if __name__ == '__main__':
    main()  
