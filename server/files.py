import string
import time
file_info="file\\file_info.txt"
file_dir="file\\"

def curTime():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

def recordFileInfo(sno,rno,fname):
    fw = open(file_info,"a")
    cont = u"%s\t%s\t%s\t%s\n" %(sno,rno,curTime(),fname)
    fw.write(cont)
    fw.close()

def write2file(fname,cont):
    fw = open(file_dir+fname,"ab")
    fw.write(cont)
    fw.close()

def getFileLists(sno, rno):
    ret = ""
    fr = open(file_info,"r")
    line = fr.readline()
    while len(line)>2:
        #print line
        fields = line.split('\t')
        if (fields[0]==sno and fields[1]==rno) or (fields[1]==sno and fields[0]==rno):
            ret = ret +"|" + fields[3]
        line = fr.readline()
    fr.close()
    if len(ret)==0:
        ret = "NONE"
    return ret

def getFileContent(fname, recvd_bytes, read_bytes):
    fr = open(file_dir+fname,"rb")
    fr.seek(recvd_bytes)
    rdata = fr.read(read_bytes)
    fr.close()
    return rdata
    
