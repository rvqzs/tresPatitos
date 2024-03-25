from PyQt5.QtCore import Qt
import sys

# Import Widgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

# Import Classes

# Login
from src.Ui_Login import Ui_Login

# MDI
from src.Ui_mdi import Ui_mdiWindow

# Usuarios
from src.Ui_Usuarios import Ui_Usuarios

# TODO Empleados

# Departamentos
from src.Ui_Departamentos  import Ui_Departamentos
from model import Departamentos

# Bienes
from model import Bienes
from src.Ui_Bienes import Ui_Bienes
from src.Ui_Asignacion_Bienes import Ui_Asignacion_Bienes
from src.Ui_Desligar_Bienes import Ui_Desligar_Bienes

class mdiApp(QMainWindow):

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
        self.uiMdi.mnuLogin.triggered.connect(self.openWinLogin)
        # TODO self.uiMdi.mnuUsuarios.triggered.connect(self.openWinUsuarios)
        # TODO self.uiMdi.mnuEmpleados.triggered.connect(self.openWinEmpleados)
        self.uiMdi.mnuDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mniAsignar.triggered.connect(self.openWinAsignacion)
        self.uiMdi.mniDesligar.triggered.connect(self.openWinDesligar)

    def openWinLogin(self):
        self.winLogin=winLogin()
        #agregar ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winLogin)
        self.winLogin.show()
        # TODO events/ Esconder password cuando se escribe/ Robert
        # TODO events/ Crear btn de salir/cancelar/ Robert
    
    # TODO openWinUsers/ Kevin
    # TODO openWinEmpleados/ Kevin
    
    def openWinDepartamentos(self):
        self.winDepartamentos=winDepartamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.winDepartamentos.show()
        # TODO events/ Agregar funciones de registrar, actualizar y eliminar

    def openWinBienes(self):
        self.winBienes=winBienes()
        self.uiMdi.mdiArea.addSubWindow(self.winBienes)
        self.winBienes.uiBienes.btnGuardar.clicked.connect(self.guardarBienes)
        self.winBienes.uiBienes.btnModificar.clicked.connect(self.modificarBienes)
        self.winBienes.uiBienes.btnEliminar.clicked.connect(self.eliminarBien)
        self.winBienes.show()

    def openWinAsignacion(self):
        self.winAsignacion=winAsignacion()
        self.uiMdi.mdiArea.addSubWindow(self.winAsignacion)
        self.winAsignacion.show()

    def openWinDesligar(self):
        self.winDesligar=winDesligar()
        self.uiMdi.mdiArea.addSubWindow(self.winDesligar)
        #events
        self.winDesligar.show()

    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()

    # TODO save/edit/delete/search users /Kevin
    # TODO save/edit/delete empleados/ Kevin
        
    def registrarDepartamento(self):
        departamento=Departamentos(self.winDepartamentos.uiDepartamentos.txt_codigo.text(),
                        self.winDepartamentos.uiDepartamentos.txt_nombre.text(),
                        self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentIndex(),
                        )
        if departamento.registrar()==1:
            self.msgBox("Datos guardados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al guardar los datos",QMessageBox.Warning)
    
    def actualizarDepartamento(self):
        departamento=Departamentos(self.winDepartamentos.uiDepartamentos.txt_codigo.text(),
                        self.winDepartamentos.uiDepartamentos.txt_nombre.text(),
                        self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentIndex(),
                        )
        if departamento.actualizar()==1:
            self.msgBox("Departamento actualizado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al actualizar el departamento",QMessageBox.Warning)
    
    def eliminarDepartamento(self):
        departamento=Departamentos(self.winDepartamentos.uiDepartamentos.txt_codigo.text(),
                        self.winDepartamentos.uiDepartamentos.txt_nombre.text(),
                        self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentIndex(),
                        )
        if departamento.eliminar()==1:
            self.msgBox("Departamento eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar departamento",QMessageBox.Warning)

    def guardarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.guardar()==1:
            self.msgBox("Datos guardados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al guardar los datos",QMessageBox.Warning)
    
    def modificarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.actualizar()==1:
            self.msgBox("Bienes actualizados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al actualizar los bienes",QMessageBox.Warning)
    
    def eliminarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.checkEstado.text()
                        )
        if bien.eliminar()==1:
            self.msgBox("Bienes eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los bienes",QMessageBox.Warning)
            

class winLogin(QWidget):
    def initPainter(self):
        super().__init__()
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)
        #manejo de eventos

# TODO class winUsuarios
# TODO class winEmpleados        

class winDepartamentos(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDepartamentos=Ui_Departamentos()
        self.uiDepartamentos.setupUi(self)
        # TODO Manejo de eventos

class winBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiBienes=Ui_Bienes()
        self.uiBienes.setupUi(self)
        # TODO Manejo de eventos

class winAsignacion(QWidget):
    def __init__(self):
        super().__init__()
        self.uiAsignacion=Ui_Asignacion_Bienes()
        self.uiAsignacion.setupUi(self)
        # TODO Manejo de eventos

class winDesligar(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDesligar=Ui_Desligar_Bienes()
        self.uiDesligar.setupUi(self)
        # TODO Manejo de eventos


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=mdiApp()
    win.showMaximized()
    sys.exit(app.exec())
