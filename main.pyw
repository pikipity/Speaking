# encoding=utf-8
import Tkinter
import ttk
import threading
import Queue
import tkMessageBox
import time
import sys
import paramiko

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

    State.set("Please Login using Wang Ze's count")

def getnamepass():
    usrname=usrnameInput.get()
    password=passwordInput.get()
    usr.get()
    usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname == "db02906" and password == "dbghdb650800":
        loginwindow.destroy()
        LoginThreading=threading.Thread(target=LoginThread)
        LoginThreading.daemon=True
        LoginThreading.start()
    else:
        tkMessageBox.showwarning("输入错误","你不知道我的学生证号和密码么？")
        usrnameInput.focus()

def LoginThread():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    global ssh
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    State.set("开始尝试连接到SSH服务器")
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh.connect("umacux4.wkg1.umac.mo",22,usrname,password,timeout=5)
        except:
            pass
        else:
            break
    global ssh1
    ssh1=paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    State.set("开始尝试连接到SSH服务器")
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh1.connect("umacux4.wkg1.umac.mo",22,usrname,password,timeout=5)
        except:
            pass
        else:
            break
    if (N<10):
        NowSend()
        Rotor=1
        while Rotor:
            try:
                print 1
                State.set("开始接收数据")
                IN,OUT,ADDR=ssh.exec_command("cat ~/speaking/test")
            except:
                State.set("连接错误，没能连接上网络，请重试。")
                usrname=usr.get()
                password=usr.get()
                usr.put("None")
                usr.put("None")
                Rotor=0
            else:
                State.set("接收成功")
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
    else:
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")
    
        
############### send to login 副程序 ######################

def Sending():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname <> "db02906" or password <> "dbghdb650800":
        login()
    else:
        SendingNowThreading=threading.Thread(target=NowSend)
        SendingNowThreading.start()

############### Send 副程序 ##############################
def NowSend():
    title="\""+Name+" say "+time.strftime("%Y-%m-%d %A %H : %M : %S",time.localtime(time.time()))+"\""
    InputText=""""---> """+InText.get().replace("!","\!").encode("utf-8")+"""\""""
    try:
        State.set("开始发送数据")
        ssh1.exec_command("echo %s >> ~/speaking/test;echo %s >> ~/speaking/test" % (title,InputText))
    except:
        InText.delete("0","end")
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")
    else:
        State.set("发送成功")
        InText.delete("0","end")

############### 主程序 #######################

ProgramPath=sys.argv[0][0:sys.argv[0].rfind('\\')+1]
Name="Wang Ze"
global usr
usr=Queue.Queue()
usr.put("None")
usr.put("None")

ReadQueue=Queue.Queue()
ReadQueue.put("None")
        
root=Tkinter.Tk()

MainText=Tkinter.Text(root,width=60,height=20,border=5,font="Times 15 bold")
MainText.grid(row=0,column=0,columnspan=2)

InText=Tkinter.Entry(root,width=55,border=1,font="Times 15 bold")
InText.grid(row=1,column=0)
InText.focus()

SendButton=Tkinter.Button(root,width=6,height=1,text="Go",font="Times 12 bold",\
                          command=Sending)
SendButton.grid(row=1,column=1)

State=Tkinter.StringVar()
StateLabel=Tkinter.Label(root,width=87,textvariable=State,\
                         justify="left",\
                         font="Times 10 bold",\
                         anchor="w")
StateLabel.grid(row=2,column=0,columnspan=2)
State.set("Love You. Enjoy it")

root.mainloop()
