# encoding=utf-8
import Tkinter
import ttk
import threading
import Queue
import tkMessageBox
import time
import sys
import paramiko
import base64
import webbrowser
import os

Version="1.0"

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
    usrnameInput.bind("<Return>",getnamepass)

    passwordLabel=Tkinter.Label(loginwindow,text="Wang Ze password: ",\
                           font="Times 15 bold")
    passwordLabel.grid(row=1,column=0)
    global passwordInput
    passwordInput=Tkinter.Entry(loginwindow,font="Times 15 bold",show="*")
    passwordInput.grid(row=1,column=1)
    passwordInput.bind("<Return>",getnamepass)

    EnterButton=Tkinter.Button(loginwindow,text="I know, I know",width=33,\
                               font="Times 15 bold",\
                               command=getnamepass)
    EnterButton.grid(row=2,column=0,columnspan=2)

    State.set("Please Login using Wang Ze's count")

def getnamepass(event=None):
    usrname=usrnameInput.get()
    password=passwordInput.get()
    usr.get()
    usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname == "db02906" and base64.encodestring(password) == 'ZGJnaGRiNjUwODAw\n':
        LoginSource=LoginFrom.get()
        LoginFrom.put(LoginSource)
        if LoginSource=='normal login':
            loginwindow.destroy()
            LoginThreading=threading.Thread(target=LoginThread)
            LoginThreading.daemon=True
            LoginThreading.start()
        else:
            loginwindow.destroy()
            Dowloading()
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
        LoginSource=LoginFrom.get()
        LoginFrom.put(LoginSource)
        if LoginSource=='normal lgoin':
            NowSend()
        Rotor=1
        while Rotor:
            try:
                State.set("开始接收数据")
                FileName=time.strftime("%Y-%m-%d",time.localtime(time.time()))
                IN,OUT,ADDR=ssh.exec_command("cat ~/speaking/"+FileName)
            except:
                State.set("连接错误，没能连接上网络，请重试。")
                usrname=usr.get()
                password=usr.get()
                usr.put("None")
                usr.put("None")
                Rotor=0
            else:
                State.set("接收成功")
                if OUT.readlines==[]:
                    time.sleep(1)
                else:
                    ReadText=OUT.readlines()
                    ReadTextpast=ReadQueue.get()
                    if ReadText <> ReadTextpast:
                        ReadQueue.put(ReadText)
                        MainText.delete("1.0","end")
                        M=0
                        for x in ReadText:
                            M=M+1
                            if(M==len(ReadText)):
                                x=x[0:len(x)-1]
                            MainText.insert("end",x)
                        MainText.yview("moveto",1.0)
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

def Sending(event=None):
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname <> "db02906" or base64.encodestring(password) <> 'ZGJnaGRiNjUwODAw\n':
        LoginFrom.get()
        LoginFrom.put('normal login')
        login()
    else:
        SendingNowThreading=threading.Thread(target=NowSend)
        SendingNowThreading.start()

############### Send 副程序 ##############################
def NowSend():
    TextSend=InText.get()
    title="\""+Name+" say "+time.strftime("%Y-%m-%d %A %H : %M : %S",time.localtime(time.time()))+"\""
    InputText=""""---> """+TextSend.replace("!","\!").encode("utf-8")+"""\""""
    try:
        State.set("开始发送数据")
        FileName=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        ssh1.exec_command("echo %s >> ~/speaking/%s;echo %s >> ~/speaking/%s" % (title,FileName,InputText,FileName))
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

############################################
def QuitFunction():
    root.quit()
    root.destroy()

def AboutFunction():
    AboutWin=Tkinter.Toplevel()
    AboutWin.title("Speaking About")
    TitleLabel=Tkinter.Label(AboutWin,text="Speaking",font="Times 30 bold",fg="#FF1493")
    TitleLabel.pack()
    VersionLabel=Tkinter.Label(AboutWin,text="Version "+Version,\
                               font="Times 15 bold")
    VersionLabel.pack()
    WriteLabel=Tkinter.Label(AboutWin,text="Writed by pikipity",\
                             font="Times 17 bold",fg="#008FFF")
    WriteLabel.pack()
    EmailLabel=Tkinter.Label(AboutWin,text="pikipity's emal: pikipityw@gmail.com",\
                            font="Times 17 bold",fg="#008FFF")
    EmailLabel.pack()
    BlogLabel=Tkinter.Label(AboutWin,text="pikipity's blog: pikipity.github.io",\
                            font="Times 17 bold",fg="#008FFF",cursor="hand2")
    BlogLabel.bind("<Button-1>",OpenBlog)
    BlogLabel.pack()
def OpenBlog(event="None"):
    webbrowser.open("pikipity.github.io")

def HelpFunction():
    #os.system("notepad "+ProgramPath+"Help")
    HelpWin=Tkinter.Toplevel()
    HelpWin.title('Help')
    fp=open(ProgramPath+"Help\\Help")
    HelpMain=fp.readlines()
    fp.close()
    HelpText=Tkinter.Text(HelpWin)
    HelpText.pack()
    for x in HelpMain:
        HelpText.insert('end',x.decode('gb2312'))

################### Download and open history ##########################

def Download():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname <> "db02906" or base64.encodestring(password) <> 'ZGJnaGRiNjUwODAw\n':
        LoginFrom.get()
        LoginFrom.put('download login')
        login()
    else:
        Dowloading()
def Dowloading():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    ssh2=paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    State.set("开始尝试连接到SSH服务器")
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh2.connect("umacux4.wkg1.umac.mo",22,usrname,password,timeout=5)
        except:
            pass
        else:
            break
    if N<10:
        try:
            State.set("开始接收数据")
            IN,OUT,ADDR=ssh2.exec_command("cd ~/speaking;ls")
        except:
            State.set("连接错误，没能连接上网络，请重试。")
            usrname=usr.get()
            password=usr.get()
            usr.put("None")
            usr.put("None")
        else:
            State.set("连接成功")
            DownloadWin=Tkinter.Toplevel()
            DownloadWin.title('Download and open history')
            DownloadLabel=Tkinter.Label(DownloadWin,text="选择你要下载的文件：",\
                                        font="Times 15 bold")
            DownloadLabel.grid(row=0,column=0)
            global DownloadFile
            DownloadFile=Tkinter.StringVar()
            DownloadFile.set("")
            FileChoose=ttk.Combobox(DownloadWin,text=DownloadFile,\
                                    values=OUT.readlines(),\
                                    font="Times 15 bold")
            FileChoose.grid(row=0,column=1)
            DownloadButton=Tkinter.Button(DownloadWin,text="开始下载",\
                                        font="Times 15 bold",\
                                          command=NowDownload)
            DownloadButton.grid(row=0,column=2)
    else:
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")

def NowDownload():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    ssh2=paramiko.Transport(("umacux4.wkg1.umac.mo",22))
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh2.connect(username=usrname,password=password)
            sftp=paramiko.SFTPClient.from_transport(ssh2)
        except:
            pass
        else:
            break
    if N<10:
        remotepath='/home/stud/db02906/speaking/'+DownloadFile.get()
        localpath=ProgramPath+'history\\'+DownloadFile.get()
        try:
            State.set("开始接收数据")
            sftp.get(remotepath,localpath)
        except:
            State.set("连接错误，没能连接上网络，请重试。")
            usrname=usr.get()
            password=usr.get()
            usr.put("None")
            usr.put("None")
        else:
            State.set("连接成功")
            ssh2.close()
            HistoryWin=Tkinter.Toplevel()
            HistoryWin.title(DownloadFile.get())
            fp=open(ProgramPath+'history\\'+DownloadFile.get())
            HistoryMain=fp.readlines()
            fp.close()
            HistoryText=Tkinter.Text(HistoryWin)
            HistoryText.pack()
            for x in HistoryMain:
                HistoryText.insert('end',x)
    else:
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")

############### 主程序 #######################

ProgramPath=sys.argv[0][0:sys.argv[0].rfind('\\')+1]
Name="Wang Ze"
global usr
usr=Queue.Queue()
usr.put("None")
usr.put("None")

ReadQueue=Queue.Queue()
ReadQueue.put("None")

LoginFrom=Queue.Queue()
LoginFrom.put('Normal login')
        
root=Tkinter.Tk()

Menubar=Tkinter.Menu(root)

filemenu=Tkinter.Menu(Menubar,tearoff=0)
filemenu.add_command(label="Download and Open History",command=Download)
filemenu.add_command(label="Quit",command=QuitFunction)
Menubar.add_cascade(label="File",menu=filemenu)

Helpmenu=Tkinter.Menu(Menubar,tearoff=0)
Helpmenu.add_command(label="Help",command=HelpFunction)
Helpmenu.add_command(label="About",command=AboutFunction)
Menubar.add_cascade(label="Help",menu=Helpmenu)

root.config(menu=Menubar)

MainText=Tkinter.Text(root,width=60,height=20,border=5,font="Times 15 bold")
MainText.grid(row=1,column=0,columnspan=2)

InText=Tkinter.Entry(root,width=55,border=1,font="Times 15 bold")
InText.grid(row=2,column=0)
InText.bind("<Return>",Sending)
InText.focus()

SendButton=Tkinter.Button(root,width=6,height=1,text="Go",font="Times 12 bold",\
                          command=Sending)
SendButton.grid(row=2,column=1)

State=Tkinter.StringVar()
StateLabel=Tkinter.Label(root,width=87,textvariable=State,\
                         justify="left",\
                         font="Times 10 bold",\
                         anchor="w")
StateLabel.grid(row=3,column=0,columnspan=2)
State.set("Love You. Enjoy it")

root.mainloop()
