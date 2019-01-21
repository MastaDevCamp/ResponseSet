#-*- coding:utf-8 -*-
import json, sys, os

class_header = "public class #className {\n"
variable_format = '\tpublic static final #type #varName = "#data"; #desc\n'
class_footer = "}"

def readJson():
	# open json
	with open(sys.argv[1], encoding="utf-8-sig") as data_file:
		data = json.load(data_file)
	return data

class Json2Class():
	def __init__(self, dic):
		self.dic = dic
		self.content = ""
		self.variable_format = variable_format.replace("#type", self.dic['type'])
		if self.dic['type'] == "int":
			self.variable_format = self.variable_format.replace('"', "")

	def makeClass(self):
		self.content += class_header.replace("#className", self.dic['name'])
		data = ""
		for val in self.dic['data']:
			if self.dic['name'] == "StatusCode":
				data += self.variable_format.replace("#varName", val['variable']).replace("#data", str(val['value'])).replace("#desc","// "+ val['desc'])
			else:
				data += self.variable_format.replace("#varName", val['variable']).replace("#data", str(val['value'])).replace("#desc", "")				
		self.content += data
		self.content += class_footer
		return data

	def saveClass(self):
		if not os.path.exists("output"):
		    os.makedirs("output")
		f = open("output/" + self.dic['name'] + ".java", "w", encoding="utf-8")
		f.write(self.content)
		f.close()


# main start
if sys.argv[1] == "":
	print("Give parameter as a json file.")

jsonData = readJson()	# read json
for dic in jsonData['ResponseSet']:
	json2Class = Json2Class(dic)
	json2Class.makeClass()	
	json2Class.saveClass()	# save output/{className}.class files
