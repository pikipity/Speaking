from distutils.core import setup
import py2exe

setup(windows=["main.pyw",{"script":"main.pyw","icon_resources":[(1,"icon//cake.ico")]}],\
      data_files=[\
    ("icon",["icon//cake.ico"]),\
    ("Help",["Help//Help"]),\
    ("history",["history//history"])])
