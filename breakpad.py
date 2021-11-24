# -*- coding: utf-8 -*-
import os 
import sys
import subprocess
import shutil
import traceback

ENVPATH = "/usr/local/bin"
def track_error():
    error_message=""
    (type,value,trace)=sys.exc_info()
    print("**************************************************************")
    print("Error_Type:\t%s\n"%type)
    print("Error_Value:\t%s\n"%value)
    print("%-40s %-20s %-20s %-20s\n"%("Filename", "Function","Linenum", "Source"))
    for filename, linenum, funcname, source in traceback.extract_tb(trace):
        print("%-40s %-20s %-20s%-20s" % (os.path.basename(filename),funcname,linenum, source))
    print("**************************************************************")

class RunDump(object):
    def __init__(self,m_app):
        self.current = os.path.abspath(os.path.dirname(m_app))
        self.appname = os.path.basename(m_app)
        self.app = os.path.abspath(m_app)
        self.symbols = os.path.join(self.current,"symbols")
        self.dump = None
        self.symfile = "%s.sym"%(self.app)
        self.mkdirpath = None
       

        self.Run()

    def __del__(self):
        if  os.path.exists(self.symbols):
            shutil.rmtree(self.symbols)
        if self.dump:
            os.remove(self.dump)
    def Get_Dump(self):
        dmp = list(filter(lambda file:  os.path.splitext(file)[-1] == ".dmp",os.listdir(self.current)))
        if dmp == list():
            print("dmp file not exist...")
            exit(1)
        self.dump = os.path.join(self.current,dmp[-1])
        
      
    def RunCmd(self,cmd):
        new_env = os.environ.copy()
        new_env["PATH"] = ENVPATH
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,env = new_env)
        for i in pid.communicate():
            if len(i)>0:
                print(i)
        return pid.wait()
    
    def readlline(self):
        line = ""
        with open(self.symfile) as fd:
            for line in fd:
                break
        linemd5 = line.split()[-2]
        self.mkdirpath = os.path.join(self.symbols,self.appname,linemd5)
        os.makedirs(self.mkdirpath,exist_ok = True)   
        shutil.move(self.symfile,self.mkdirpath)
        print("symbols目录生成：%s"%self.mkdirpath )

    def Run(self):
        self.Get_Dump()
        self.CreatSym()
        self.readlline()
        self.CreatDump()

    def CreatSym(self):
        cmd = "dump_syms %s>%s"%(self.app,self.symfile)
        if self.RunCmd(cmd):
            print("%s 运行出错"%cmd)
            exit(1)
        else:
            print("生成sym文件:%s"%self.symfile)
         
    def CreatDump(self):
        sysmbols = os.path.join(os.path.join(self.current,"symbols"))
        creashlog = os.path.join(os.path.join(self.current,"crash.log"))
        errorlog = os.path.join(os.path.join(self.current,"error.log"))
        cmd = "minidump_stackwalk %s %s >%s 2>%s"%(self.dump,sysmbols,creashlog,errorlog)
        if self.RunCmd(cmd):
            print("%s 运行出错"%cmd)
        else:
            print("crash.log生成成功:%s"%creashlog)
    

if __name__ == "__main__":
    if len(sys.argv[:])<2:
        print("""输入命令：./Breakpad.py  AppPath 
            AppPath：程序app 所在路径
        """)
        exit(1)
    try:
        app = sys.argv[1]
        RunDump(app)
    except BaseException:
            track_error()
