from PyQt5.QtWidgets import QMessageBox
class Dialogs():
	def __init__(self,parent):
		self.parent=parent
	def Message(self,message,title):
		retval=QMessageBox.information(self.parent,title,message)
		if retval==QMessageBox.Ok:
			pass
	def Question(self,message,title):
		retval=QMessageBox.question(self.parent,title,message,defaultButton=QMessageBox.Yes)
		if retval==QMessageBox.Yes:
			return accept
		else:
			return reject
	def Error(self,message,title):
		retval=QMessagebox.critical(self.parent,title,message)
		if retval==QMessageBox.Ok:
			pass
