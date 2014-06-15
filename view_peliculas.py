# -*- coding: utf-8 -*-
import sys
import controller
from PySide import QtGui, QtCore
from interfaz import Ui_MainWindow
import os


class Peliculas(QtGui.QMainWindow):

	tabla_columnas = (
		(u"Título",200),
		(u"Año",50),
		(u"Director",150),
		(u"País",50),
		(u"Rank",40),
		)

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.load_data_tabla()
		self.show()
		self.setFixedSize(576,348)
		self.conectar_acciones()
		self.ui.info.setVisible(False)

	def conectar_acciones(self):
		self.ui.btn_subir.clicked.connect(self.action_btn_subir)
		self.ui.btn_bajar.clicked.connect(self.action_btn_bajar)
		#self.ui.tabla.pressed.connect(self.tabla_cell_selected)
		#self.ui.tabla.activated.connect(self.tabla_cell_selected)

	def load_data_tabla(self):
		'''Método para mostrar los datos de la tabla, muestra todos los elementos de la tabla "movies" de la base de datos'''
		datos = controller.getDatos()
		rows = len(datos)
		model = QtGui.QStandardItemModel(rows,len(self.tabla_columnas))
		self.ui.tabla.setModel(model)

		for col,h in enumerate(self.tabla_columnas):
			model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
			self.ui.tabla.setColumnWidth(col, h[1])

		for i,data in enumerate(datos):
			row = [data[1],data[3],data[4],data[5],data[8]]
			for j, field in enumerate(row):
				index = model.index(i, j, QtCore.QModelIndex())
				model.setData(index,field)
			model.item(i).mov = data

		
		modelSel = self.ui.tabla.selectionModel()
		modelSel.currentChanged.connect(self.tabla_cell_selected)

	def tabla_cell_selected(self,index,indexp):
		self.mostrar_datos(index)

	def action_btn_subir(self):
		self.action_rank("subir")

	def action_btn_bajar(self):
		self.action_rank("bajar")

	def mostrar_datos(self,index):
		self.ui.info.setVisible(True)
		self.ui.lbl_title_reparto.setText("Reparto:")
		self.ui.lbl_title_descripcion.setText("Descripcion:")

		model = self.ui.tabla.model()
		rank = model.index(index.row(), 4, QtCore.QModelIndex()).data()
		movie = controller.getDatoRank(rank)
		pmap = QtGui.QPixmap(str(os.getcwd())+"/db_movies/"+str(movie[0]['poster']))

		self.ui.lbl_image.setPixmap(pmap)
		self.ui.lbl_reparto.setText(str(movie[0]['stars']))
		self.ui.lbl_descripcion.setText(str(movie[0]['description']))

		self.setFixedSize(805,650)

	def action_rank(self,accion):
		model = self.ui.tabla.model()
		index = self.ui.tabla.currentIndex()
		if index.row()==-1:
			self.messageDialog = QtGui.QMessageBox(self)
			self.messageDialog.setWindowTitle("Error")
			self.messageDialog.setText(u"Debe seleccionar una película.")
			self.messageDialog.exec_()

		else:
			rank = model.index(index.row(), 4, QtCore.QModelIndex()).data()
			movie = controller.getDatoRank(rank)
			old_rank = int(movie[0]['ranking'])
			if(accion == "subir"):
				new_rank = old_rank-1
			elif(accion == "bajar"):
				new_rank = old_rank+1
			if(new_rank == 0):
				#self.errorMessageDialog = QtGui.QErrorMessage(self)
				self.messageDialog.setText(u"No se puede subir más el rank.")
				self.messageDialog.exec_()
			else:
				movie_a = controller.getDatoRank(new_rank)
				controller.updateDatoRank(movie[0]['title'],new_rank)
				if(movie_a):
					controller.updateDatoRank(movie_a[0]['title'],old_rank)
				self.load_data_tabla()

def run():
	app = QtGui.QApplication(sys.argv)
	main = Peliculas()
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()