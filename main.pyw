# encoding=utf-8
import Tkinter
import ttk
import threading
import Queue
import tkMessageBox
import time
import sys
import paramiko

usr=Queue.Queue()
ProgramPath=sys.argv[0][0:sys.argv[0].rfind('\\')+1]
Name="Wang Ze"
usr.put("None")
usr.put("None")

ReadQueue=Queue.Queue()
ReadQueue.put("None")

############### Log in Window #################

def login():
    global loginwindow
    loginwindow=Tkinter.Toplevel()

    usrnameLabel=Tkinter.Label(loginwindow,text="Wang Ze Student ID: ",\
                               font="Times 15 bold")
    usrnameLabel.grid(row=0,column=0)
    global usrnameInput
    usrnameInput=Tkinter.Entry(loginwindow,font="Times 15 bold")
    usrnameInput.grid(row=0,column=1)
    usrnameInput.focus()

    passwordLabel=Tkinter.Label(loginwindow,text="Wang Ze password: ",\
                           font="Times 15 bold")
    passwordLabel.grid(row=1,column=0)
    global passwordInput
    passwordInput=Tkinter.Entry(loginwindow,font="Times 15 bold",show="*")
    passwordInput.grid(row=1,column=1)

    EnterButton=Tkinter.Button(loginwindow,text="I know, I know",width=33,\
                               font="Times 15 bold",\
                               command=getnamepass)
    EnterButton.grid(row=2,column=0,columnspan=2)

def getnamepass():
    usrname=usrnameInput.get()
    password=passwordInput.get()
    if usrname == "db02906" and password == "dbghdb650800":
        usr.get()
        usr.get()
        usr.put(usrname)
        usr.put(password)
        loginwindow.destroy()
        global ssh
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("umacux4.wkg1.umac.mo",22,usrname,password)
        ssh.exec_command("echo \"I Love You\" >> ~/speaking/test")
        ReadingProcess=threading.Thread(target=Reading_Process)
        ReadingProcess.start()
        NowSend()
    else:
        tkMessageBox.showwarning("输入错误","你不知道我的学生证号和密码么？")
        usr.get()
        usr.get()
        usr.put(usrname)
        usr.put(password)
        usrnameInput.focus()

################ Reading 副程序 ##########################

def Reading_Process():
    while 1:
        IN,OUT,ADDR=ssh.exec_command("cat ~/speaking/test")
        ReadText=OUT.readlines()
        if len(ReadText)>20:
            ReadText=ReadText[len(ReadText)-20:len(ReadText)]
        ReadTextpast=ReadQueue.get()
        if ReadText <> ReadTextpast:
            ReadQueue.put(ReadText)
            MainText.delete("1.0","end")
            for x in ReadText:
                MainText.insert("end",x)
            time.sleep(1)
        else:
            ReadQueue.put(ReadTextpast)
            time.sleep(1)


############### send to login 副程序 ######################

def Sending():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname <> "db02906" or password <> "dbghdb650800":
        login()
    else:
        NowSend()

############### Send 副程序 ##############################
def NowSend():
    title="\""+Name+" say "+time.strftime("%Y-%m-%d %A %H : %M : %S",time.localtime(time.time()))+"\""
    InputText=""""---> """+InText.get().encode("utf-8")+"""\""""
    ssh.exec_command("echo %s >> ~/speaking/test" % title)
    ssh.exec_command("echo %s >> ~/speaking/test" % InputText)
    InText.delete("0","end")

############### 主程序 #######################
        
root=Tkinter.Tk()

MainText=Tkinter.Text(root,width=60,height=20,border=5,font="Times 15 bold")
MainText.grid(row=0,column=0,columnspan=2)

InText=Tkinter.Entry(root,width=55,border=2,font="Times 15 bold")
InText.grid(row=1,column=0)
InText.focus()

SendButton=Tkinter.Button(root,width=10,height=2,text="Go",font="Times 10 bold",\
                          command=Sending)
SendButton.grid(row=1,column=1)

root.mainloop()
