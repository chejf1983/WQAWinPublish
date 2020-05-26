#! /usr/bin/python
import msvcrt
import shutil,os

#源文件
dst_path = ".\\elements\\"
src_path = "..\\wqa_windows_from\\"

#删除旧文件
try:
	print("删除旧文件" + dst_path + "dist")
	shutil.rmtree(dst_path + "dist")
except Exception as ex:
	print("目标文件夹为空" + str(ex))

print("复制文件夹" + src_path + "dist")
shutil.copytree(src_path+ "dist", dst_path + "dist")
print("复制文件" + ".\\help.pdf")
shutil.copy(".\\help.pdf" ,dst_path + "help.pdf")

print ("输入任意字符退出...");
msvcrt.getch()