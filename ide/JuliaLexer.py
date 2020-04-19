from PyQt5.QtGui import QColor, QFont
from PyQt5.Qsci import QsciLexerCustom
import re
from CheckNum import checkNum
class JuliaLexer(QsciLexerCustom):
	def __init__(self,parent):
		super().__init__(parent)
		self.editor=parent
		
		#Default Text Settings
		self.setDefaultColor(QColor("#000000"))
		self.setDefaultPaper(QColor("#ffffff"))
		self.setDefaultFont(QFont("Times New Roman",14))
		
		#Lexer color settings
		self.setColor(QColor("#000000"),0) #Base text
		self.setColor(QColor("#e0a51b"),1) #Keywords
		self.setColor(QColor("#00c4c4"),2) #Operators and keywords
		self.setColor(QColor("#ff0080"),3) #Numbers
		self.setColor(QColor("#800080"),4) #Characters
		self.setColor(QColor("#00ff00"),5) #Strings
		self.setColor(QColor("#ff0000"),6) #Comments
		self.setColor(QColor("#000064"),7) #Data Types
		
		#Set Paper color
		self.setPaper(QColor("#ffffff"),0) #Base text
		self.setPaper(QColor("#ffffff"),1) #Keywords
		self.setPaper(QColor("#ffffff"),2) #Operators and keywords
		self.setPaper(QColor("#ffffff"),3) #Numbers
		self.setPaper(QColor("#ffffff"),4) #Characters
		self.setPaper(QColor("#ffffff"),5) #Strings
		self.setPaper(QColor("#ffffff"),6) #Comments
		self.setPaper(QColor("#ffffff"),7) #Data types
		
		#Set Font
		self.setFont(QFont("Times New Roman", 14),0) #Base text
		self.setFont(QFont("Times New Roman",14),1) #Keywords
		self.setFont(QFont("Times New Roman",14),2) #Operators and braces
		self.setFont(QFont("Times New Roman",14),3) #Numbers
		self.setFont(QFont("Times New Roman",14),4) #Characters
		self.setFont(QFont("Times New Roman",14),5) #Strings
		self.setFont(QFont("Times New Roman",14),6) #Comments
		self.setFont(QFont("Times New Roman",14),7) #Data Types
		
		self.stack_obj=Stack()
	def language(self):
		return "Julia"
	
	def description(self,style_nr):
		if style_nr==0:
			return "baseText"
		elif style_nr==1:
			return "keyWords"
		elif style_nr==2:
			return "operatorKeywords"
		elif style_nr==3:
			return "numbers"
		elif style_nr==4:
			return "characters"
		elif style_nr==5:
			return "strings"
		elif style_nr==6:
			return "comments"
		elif style_nr==7:
			return "DataTypes"
		else:
			return ""
	
	def styleText(self,start,end):
		self.startStyling(start)
		text=self.editor.text()[start:end]
		keyword_list=("baremodule", "begin", "break", "catch", "const", "continue", "do", "else", "elseif", "end", "export", "false", "finally", "for", "function", "global", "if", "import", "let", "local",
		"macro", "module", "quote", "return", "struct", "true", "try", "using", "while")
		operator_braces_list=("+","-","*","/","\\","^","%", "!","~","&","|",">","<","=","(",")","[","]","{","}")
		data_type_list=("Complex","Real","BigInt","BigFloat","Bool","Char","String","Rational","Int8","Int16","Int32","Int64","Int128","UInt8","UInt16","UInt32","UInt64","UInt128","Float16","Float32","Float64")
		valueList=("NaN","Inf","nothing")
		pattern=re.compile(r"\s+|\w+|\W")
		tokens=pattern.findall(text)
		comment_index=-1
		for i in tokens:
			if i=="#":
				comment_index=tokens.index(i)
				break
		comment_end_index=-1
		for i in tokens[comment_index:]:
			if i=="\n":
				comment_end_index=tokens.index(i)
				break
		comment_string=""
		for i in tokens[comment_index:comment_end_index+1]:
			comment_string+=i
		tokens=tokens[:comment_index]+[comment_string]+tokens[comment_end_index:]
		token_list=[(token,len(bytearray(token,"utf-8"))) for token in tokens]
		print(token_list)
		char_flag=False
		string_flag=False
		if start>0:
			previous_style_nr=self.editor.SendScintilla(self.editor.SCI_GETSTYLEAT,start-1)
			if previous_style_nr==4:
				char_flag=True
			elif previous_style_nr==5:
				string_flag=True
		for i,token in enumerate(token_list):
			print(token[0])
			if char_flag:
				self.setStyling(token[1],4)
				if token[0] =="'":
					char_flag=False
			elif string_flag:
				self.setStyling(token[1],5)
				if token[0]=="\"":
					string_flag=False
			else:
				if token[0] in keyword_list:
					self.setStyling(token[1], 1)
				elif token[0] in operator_braces_list:
					self.setStyling(token[1], 2)
				elif ((checkNum(token[0])) or (token[0] in valueList)):
					self.setStyling(token[1], 3)
				elif token[0]=="'":
					self.setStyling(token[1], 4)
					char_flag=True
				elif token[0]=="\"":
					self.setStyling(token[1], 5)
					string_flag=True
				elif token[0].startswith("#"):
					self.setStyling(token[1], 6)
				elif token[0] in data_type_list:
					self.setStyling(token[1], 7)
				else:
					self.setStyling(token[1], 0)
	def setLexerFont(self,font):
		self.setFont(font,0) #Base text
		self.setFont(font,1) #Keywords
		self.setFont(font,2) #Operators and braces
		self.setFont(font,3) #Numbers
		self.setFont(font,4) #Characters
		self.setFont(font,5) #Strings
		self.setFont(font,6) #Comments
		self.setFont(font,7) #Data Types