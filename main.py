import sys

# Import Widgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

# Import Classes

# Login
from src.Ui_001_login import Ui_Login

# MDI
from src.Ui_000_mdi import Ui_mdiWindow

# Usuarios
from src.Ui_002_usuarios import Ui_Usuarios
from model.usuarios import Usuarios

# Empleados
from src.Ui_003_empleados import Ui_CrearEmpleados
from model.empleados import Empleados

# Departamentos
from src.Ui_004_departamentos  import Ui_Departamentos
from model.departamentos import Departamentos

# Bienes
from model.bienes import Bienes
from src.Ui_005_bienes import Ui_Bienes
from src.Ui_051_asignacion_bienes import Ui_Asignacion
from model.asignacion import AsignarBienes
from Ui_052_desligar_bienes import Ui_Desligar
from model.desligar import DesligarBienes


class Login(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initComponents()

    def initComponents(self):
        self.uiLogin.btn_login.clicked.connect(self.validate_credentials)

    def login(self):
        mdi = mdiApp()
        mdi.show()
        self.close()

    def validate_credentials(self):
        if self.uiLogin.txt_username.text() == "admin" and self.uiLogin.txt_password.text() == "admin":
            # If correct, accept the dialog, allowing it to close
            mdi = mdiApp()
            mdi.showMaximized()
            self.close()
            self.accept()
        else:
            # If incorrect, show a warning message
            QMessageBox.warning(self, "Invalid credentials", "Invalid username or password")

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
        # self.uiMdi.menuLogin.triggered.connect(self.openWinLogin)
        self.uiMdi.mniUsuarios.triggered.connect(self.openWinUsuarios)
        self.uiMdi.mniEmpleados.triggered.connect(self.openWinEmpleados)
        self.uiMdi.mniDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mniAsignar.triggered.connect(self.openWinAsignacionBienes)
        self.uiMdi.mniDesligar.triggered.connect(self.openWinDesligarBienes)

    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()
    
    #Usuarios
        
    def openWinUsuarios(self):
        self.winUsuarios=winUsuarios()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winUsuarios)
        #eventos
        self.winUsuarios.uiUsuarios.btnCrearUsuario.clicked.connect(self.guardarUsuario)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.clicked.connect(self.modificarUsuario)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.clicked.connect(self.eliminarUsuario)
        self.winUsuarios.show()

    def guardarUsuario(self):
        usuarios=usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombre.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.guardar()==1:
            self.msgBox("Usuario creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear usuario",QMessageBox.Information)

    def modificarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombre.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.actualizar()==1:
            self.msgBox("Datos moidificados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al modificar datos",QMessageBox.Information)

    def eliminarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombre.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.eliminar()==1:
            self.msgBox("Datos eliminados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar datos",QMessageBox.Information)

    #Empleados
            
    def openWinEmpleados(self):
        self.wincrearEmpleados=wincrearEmpleados()
        #agregar ventana
        self.uiMdi.mdiArea.addSubWindow(self.wincrearEmpleados)
        #eventos
        self.wincrearEmpleados.uicreacionEmpleado.bttCrearEmpleado.clicked.connect(self.guardarEmpleado)
        self.wincrearEmpleados.show()
    
    def guardarEmpleado(self):
        creacionEmpleado=Empleados(self.wincrearEmpleados.uicreacionEmpleado.txtCedula.text(),self.wincrearEmpleados.uicreacionEmpleado.txtNombre.text(),
                                self.wincrearEmpleados.uicreacionEmpleado.txtApellidos.text(),self.wincrearEmpleados.uicreacionEmpleado.txtTelefono.text(),
                                self.wincrearEmpleados.uicreacionEmpleado.txtDireccion.text(),self.wincrearEmpleados.uicreacionEmpleado.txtPuesto.text(),
                                self.wincrearEmpleados.uicreacionEmpleado.txtIngreso.text(),self.wincrearEmpleados.uicreacionEmpleado.txtJefatura.text()
                                )
        if creacionEmpleado.guardarEmpleados()==1:
            self.msgBox("Empleado creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear Empleado",QMessageBox.Information)

    # TODO add edit/delete empleados/ Kevin
            
    #Departamentos
            
    def openWinDepartamentos(self):
        self.winDepartamentos=winDepartamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.winDepartamentos.show()
        self.winDepartamentos.uiDepartamentos.btn_registrar.clicked.connect(self.registrarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_editar.clicked.connect(self.actualizarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_eliminar.clicked.connect(self.eliminarDepartamento)

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

    #Bienes
            
    def openWinBienes(self):
        bien=Bienes()
        self.winBienes=winBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winBienes)
        #eventos
        self.winBienes.uiBienes.btnGuardar.clicked.connect(self.guardarBienes)
        self.winBienes.uiBienes.btnModificar.clicked.connect(self.modificarBienes)
        self.winBienes.uiBienes.btnEliminar.clicked.connect(self.eliminarBienes)
        self.cargarTabla(bien.getNumeroRegistros(),bien.getBienes())
        self.winBienes.show()

    def guardarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.cbxEstado.currentText()
                        )
        if bien.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)

    def modificarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.cbxEstado.currentText()
                        )
        if bien.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)
    
    def eliminarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(),
                        self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.cbxEstado.currentText()
                        )
        if bien.eliminar()==1:
            self.msgBox("Datos Eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los datos",QMessageBox.Warning)
    
    def cargarTablaBienes(self, numFilas, datos):
        #determinar el numero de filas de la tabla
        self.winBienes.uiBienes.tblRegistro.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winBienes.uiBienes.tblRegistro.setColumnCount(5)
        i=0
        for d in datos:
            print(d)
            self.winBienes.uiBienes.tblRegistro.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,1,QTableWidgetItem(d["nombre bien"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,2,QTableWidgetItem(d["categoria"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,3,QTableWidgetItem(d["descripcion"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,4,QTableWidgetItem(d["estado"]))
            i+=1
    
    #Asignacion Bienes

    def openWinAsignacionBienes(self):
        asignado=AsignarBienes()
        self.winAsignacion=winAsignacionBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winAsignacion)
        #eventos
        self.winAsignacion.uiAsignacion.btnGuardar.clicked.connect(self.guardarBienAsignado)
        self.winAsignacion.uiAsignacion.btnModificar.clicked.connect(self.modificarBienAsignado)
        self.winAsignacion.uiAsignacion.btnEliminar.clicked.connect(self.eliminarBienAsignado)
        self.cargarTablaAsignados(asignado.getNumeroAsignados(),asignado.getAsignados())
        self.winAsignacion.show()
            
    def guardarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(),
                    self.winAsignacion.uiAsignacion.txtNombre.text(),
                    self.winAsignacion.uiAsignacion.txtApellidos.text(),
                    self.winAsignacion.uiAsignacion.txtTelefono.text(),
                    self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                    )
        if bienesAsignados.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)

    def modificarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(),
                        self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(),
                        self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                )
        if bienesAsignados.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)

    def eliminarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(),
                        self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(),
                        self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                        )
        if bienesAsignados.eliminar()==1:
            self.msgBox("Datos Eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los datos",QMessageBox.Warning)
    
    def cargarTablaBienesAsignado(self, numFilas, datos):
        #determinar el numero de filas de la tabla
        self.winAsignacion.uiAsignacion.tblAsignados.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winAsignacion.uiAsignacion.tblAsignados.setColumnCount(5)
        i=0
        for d in datos:
            print(d)
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,1,QTableWidgetItem(d["nombre"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,2,QTableWidgetItem(d["apellidos"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,3,QTableWidgetItem(d["telefono"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,4,QTableWidgetItem(d["bien asignado"]))
            i+=1

    def comboBoxBienesAsignado(self, datos):
        for d in datos:
            nombre=d["nombre"]
            if nombre:
                self.winDesligar.uiDesligar.cbxEmpleados.addItem(nombre)

    #Desligar Bienes
                
    def openWinDesligarBienes(self):
        desligar=DesligarBienes()
        self.winDesligar=winDesligarBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winDesligar)
        #eventos
        self.comboBoxBienesAsignado(desligar.getAsignados())
        self.winDesligar.show()

    #Class Windows
                
class winLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.uiLogin=Ui_Login()
        
        self.uiLogin.setupUi(self)
        #manejo de eventos

class winUsuarios(QWidget):
    def __init__(self):
        super().__init__()
        self.uiUsuarios=Ui_Usuarios()
        self.uiUsuarios.setupUi(self)

class wincrearEmpleados(QWidget):
    def __init__(self):
        super().__init__()
        self.uicreacionEmpleado=Ui_CrearEmpleados()
        self.uicreacionEmpleado.setupUi(self)       

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

class winAsignacionBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiAsignacion=Ui_Asignacion()
        self.uiAsignacion.setupUi(self)
        # TODO Manejo de eventos

class winDesligarBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDesligar=Ui_Desligar()
        self.uiDesligar.setupUi(self)
        # TODO Manejo de eventos

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=Login()
    if win.exec_() == QDialog.Accepted:
        mdi=mdiApp()
        mdi.showMaximized()
    sys.exit(app.exec())
