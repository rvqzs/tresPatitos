from PyQt5.QtCore import Qt
import sys


#importar los widgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

#Import Classes

#Login
from Ui_Login import Ui_Login

#MDI
from Ui_mdi import Ui_mdiWindow

#Usuarios
from Ui_Usuarios import Ui_Usuarios

#Empleados

#Departamentos
from Ui_Departamentos  import Ui_Departamentos
from model.Departamentos import Departamentos

#Bienes
from model.Bienes import Bienes
from Ui_Bienes import Ui_Bienes
from Ui_Asignacion_Bienes import Ui_Asignacion_Bienes
from Ui_Desligar_Bienes import Ui_Desligar_Bienes

class mdiApp(QMainWindow):
    #init al constructor
    def __init__(self):
        super().__init__()
        #instanciar la ventana
        self.uiMdi=Ui_mdiWindow()
        #generar los componentes
        self.uiMdi.setupUi(self)
        #estilos
        self.uiMdi.mdiArea.setFixedHeight(2000)
        self.uiMdi.mdiArea.setFixedWidth(2000)
        #definir los eventos
        self.initComponents()
        #mostrar la ventana
        self.show()
    
    def initComponents(self):
        self.uiMdi.mniBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mniAsignar.triggered.connect(self.openWinAsignacion)
        self.uiMdi.mniDesligar.triggered.connect(self.openWinDesligar)
    
    def openWinBienes(self):
        self.winBienes=winBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winBienes)
        #eventos
        self.winBienes.uiBienes.btnGuardar.clicked.connect(self.guardarBien)
        self.winBienes.uiBienes.btnModificar.clicked.connect(self.modificarBien)
        self.winBienes.uiBienes.btnEliminar.clicked.connect(self.eliminarBien)
        self.winBienes.show()
    def openWinAsignacion(self):
        self.winAsignacion=winAsignacion()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winAsignacion)
        #eventos
        self.winAsignacion.show()
    def openWinDesligar(self):
        self.winDesligar=winDesligar()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winDesligar)
        #eventos
        self.winDesligar.show()
    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Mensaje")
        retval=msg.exec_()

    def guardarBien(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)
    
    def modificarBien(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)
    
    def eliminarBien(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.eliminar()==1:
            self.msgBox("Datos Eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los datos",QMessageBox.Warning)



class winBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiBienes=Ui_Bienes()
        self.uiBienes.setupUi(self)
        #manejo de eventos

class winAsignacion(QWidget):
    def __init__(self):
        super().__init__()
        self.uiAsignacion=Ui_Asignacion_Bienes()
        self.uiAsignacion.setupUi(self)
        #manejo de eventos

class winDesligar(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDesligar=Ui_Desligar_Bienes()
        self.uiDesligar.setupUi(self)
        #manejo de eventos

if __name__=="__main__":
    app=QApplication(sys.argv)
    #cargar ventana
    win=mdiApp()
    win.showMaximized()
    sys.exit(app.exec())
