#! /usr/bin/python
import shutil,os
import sys
import msvcrt

try:
 import xml.etree.cElementTree as ET
except ImportError:
 import xml.etree.ElementTree as ET
 
from xml.etree.ElementTree import ElementTree,Element
#为xml插入一行  
def writeinfile(path, cont, line=0):
	lines = [] 
	with open(path, 'r', encoding='utf-8') as r: 
		for l in r:
			lines.append(l) 	
	if line == 0:
		lines.insert(0, '{}\n'.format(cont)) 
	else:
		lines.insert(line-1, '{}\n'.format(cont))
	
	s = ''.join(lines) 
	# print(s) 
	with open(path, 'w') as m:
		m.write(s)
		
#读取element tree
def read_tree(filename):
	return ET.ElementTree(file=filename);

#保存element_tree
def save_tree(tree, filename):
	tree.write(filename, encoding="UTF-8",xml_declaration=True)	
	doctype='<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">'
	writeinfile(filename, doctype, 2)

#读取element_tree
def read_key(tree, key):
	nodes = tree.findall("entry")
	for node in nodes: 
		if node.get("key") == key:
			return node.text
	return ""

#修改elemnt
def change_key(tree, key, txt):
	nodes = tree.findall("entry")
	for node in nodes: 
		if node.get("key") == key:
		   print_s = (node.get("key") + ":" + node.text + "->")
		   node.text = txt
		   print(print_s + node.text)
		   return
	ne = ET.Element('entry', {"key" : key})
	ne.text = txt
	tree.getroot().append(ne)

#删除elment   
def del_key(tree, key):
	nodes = tree.findall("entry")
	for node in nodes: 
		if node.get("key") == key:
		   print("del:" + node.get("key") + "=" + node.text)
		   tree.getroot().remove(node)
		   return
	
def clean_zip(dstpath):
	z_end = ".7z"
	for file in os.listdir(dstpath):
		if file.endswith(z_end):
			print(" del: " + dstpath + file)
			os.remove(dstpath + file)

def cp_file(srcpath, dstpath):
	#清理空数据库文件
	db_end = ".db"
	for file in os.listdir(dstpath):
		if file.endswith(db_end):
			print(" del: " + dstpath + file)
			os.remove(dstpath + file)
			
	#更新lib文件
	dst_dir = dstpath + "lib\\"
	src_dir = srcpath + "dist\\lib"
	try:
		print("del->" + dst_dir);
		shutil.rmtree(dst_dir)
	except Exception as ex:
		print("当前文件夹为空" + str(ex))
		
	print(src_dir + " -> " + str(dst_dir))
	shutil.copytree(src_dir, dst_dir)
	
	#更新.jar文件
	jar_end = ".jar"
	dst_dir = dstpath
	src_dir = srcpath + "dist\\"
	for file in os.listdir(src_dir):
		if file.endswith(jar_end):
			if os.path.exists(dst_dir + file):
				print(" del: " + dst_dir + file)
				os.remove(dst_dir + file)
			print(src_dir + file + " -> " + dst_dir + file)
			shutil.copyfile(src_dir + file ,dst_dir + file)		
			
	#更新help.pdf文件
	src_file = ".//help4.0.pdf"	
	dst_file = dstpath + "help.pdf"
	print(src_file + " -> " + dst_file)
	shutil.copyfile(src_file ,dst_file)

def publish(srcpath, dstpath, config_file):
	#读取配置文件
	config_tree = read_tree(srcpath + config_file)
		
	#获取版本号
	print ("输入版本号:")
	version = sys.stdin.readline()
	version = version.rstrip('\n')
	if version == '':
		print ("使用默认版本号:")
		version = read_key(config_tree, 'VER')	
	print("打包版本" + version)
	
	#更新版本号
	change_key(config_tree, 'VER', version)
	change_key(config_tree, 'IPS', 'Naqing')
	
	#保存配置文件
	save_tree(config_tree, dstpath + config_file)
	#压缩内部版本
	cmd = "\"C:\\Program Files\\7-Zip\\7z.exe\" a " + dstpath.rstrip('\\') + ".B" + version + ".7z  " + dstpath 
	print(cmd)
	os.system(cmd)
	
	#修改配置为外部版本
	del_key(config_tree, 'IPS')
	save_tree(config_tree, dstpath + config_file)
	#压缩外部版本
	cmd = "\"C:\\Program Files\\7-Zip\\7z.exe\" a " + dstpath.rstrip('\\') + ".A" + version + ".7z  " + dstpath 
	print(cmd)
	os.system(cmd)

def up_load(srcpath, server):
	z_end = ".7z"
	for file in os.listdir(srcpath):
		if file.endswith(z_end):
			if os.path.exists(server + file):
				print("clean: " + server + file)
				os.remove(server + file)
				
			print(" copy: " + srcpath + file + " -> " + server + file)
			shutil.copyfile(srcpath + file, server + file)
			print("done!")


def main():
	#源文件
	dst_path = ".\\output\\"
	src_path = "..\\wqa_windows_from_ui\\"
	server_path = "Z:\\胖子\\水质\\"

	#清空旧的打包文件
	clean_zip(dst_path)
	#复制需要的文件信息
	cp_file(src_path, dst_path + "水质探头测试\\")
	#打包发布版本
	publish(src_path, dst_path + "水质探头测试\\", "dev_config")

	#上传服务器
	print ("是否上传服务器:")
	upload = sys.stdin.readline().rstrip('\n')
	if  upload == 'yes' or upload == 'y' or upload == 'Y':
		up_load(dst_path, server_path)

	print ("输入任意字符退出...");
	msvcrt.getch()

main()

