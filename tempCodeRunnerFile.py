	def showEvent(self, event):
		if(self.__content):
			self.__content.show()
		return super().showEvent(event)