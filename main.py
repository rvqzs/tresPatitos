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
from model.Usuarios import Usuarios

# Empleados
from src.Ui_creacionEmpleados import Ui_CrearEmpleados
from model.Empleados import crearEmpleados

# Departamentos
from src.Ui_Departamentos  import Ui_Departamentos
from model.Departamentos import Departamentos

# Bienes
from model.Bienes import Bienes
from src.Ui_Bienes import Ui_Bienes
from src.Ui_Asignacion_Bienes import Ui_Asignacion_Bienes
from model.Asignacion import Asignar
from src.Ui_Desligar_Bienes import Ui_Desligar_Bienes


class Login(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)
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
        self.uiMdi.mniEmpleados.triggered.connect(self.openWinCrearEmpleado)
        self.uiMdi.mniDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mniAsignar.triggered.connect(self.openWinAsignacion)
        self.uiMdi.mniDesligar.triggered.connect(self.openWinDesligar)

    # def openWinLogin(self):
    #     self.winLogin=winLogin()
    #     #agregar ventana al mdi
    #     self.uiMdi.mdiArea.addSubWindow(self.winLogin)
    #     self.winLogin.show()
    #     # TODO events/ Esconder password cuando se escribe/ Robert
    #     # TODO events/ Crear btn de salir/cancelar/ Robert
    
    def openWinUsuarios(self):
        self.winUsuarios=winUsuarios()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winUsuarios)
        #eventos
        self.winUsuarios.uiUsuarios.bttCrearUsuario.clicked.connect(self.guardarUsuario)
        self.winUsuarios.uiUsuarios.bttModificarUsuario.clicked.connect(self.modificarUsuario)
        self.winUsuarios.uiUsuarios.bttEliminarUsuario.clicked.connect(self.eliminarUsuario)
        self.winUsuarios.show()

    def openWinCrearEmpleado(self):
        self.wincrearEmpleados=wincrearEmpleados()
        #agregar ventana
        self.uiMdi.mdiArea.addSubWindow(self.wincrearEmpleados)
        #eventos
        self.wincrearEmpleados.uicreacionEmpleado.bttCrearEmpleado.clicked.connect(self.guardarEmpleado)
        self.wincrearEmpleados.show()
    
    def openWinDepartamentos(self):
        self.winDepartamentos=winDepartamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.winDepartamentos.show()
        self.winDepartamentos.uiDepartamentos.btn_registrar.clicked.connect(self.registrarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_editar.clicked.connect(self.actualizarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_eliminar.clicked.connect(self.eliminarDepartamento)

    def openWinBienes(self):
        self.winBienes=winBienes()
        self.uiMdi.mdiArea.addSubWindow(self.winBienes)
        self.winBienes.uiBienes.btnGuardar.clicked.connect(self.guardarBienes)
        self.winBienes.uiBienes.btnModificar.clicked.connect(self.modificarBienes)
        self.winBienes.uiBienes.btnEliminar.clicked.connect(self.eliminarBienes)
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

    def guardarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombreUsuario.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.guardar()==1:
            self.msgBox("Usuario creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear usuario",QMessageBox.Information)

    def modificarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombreUsuario.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.actualizar()==1:
            self.msgBox("Datos moidificados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al modificar datos",QMessageBox.Information)

    def eliminarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtNombreUsuario.text(),self.winUsuarios.uiUsuarios.txtEmail.text())
        if usuarios.eliminar()==1:
            self.msgBox("Datos eliminados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar datos",QMessageBox.Information)
    
    # TODO edit/delete empleados/ Kevin
            
    def guardarEmpleado(self):
        creacionEmpleado=crearEmpleados(self.wincrearEmpleados.uicreacionEmpleado.txtCedula.text(),self.wincrearEmpleados.uicreacionEmpleado.txtNombre.text(),self.wincrearEmpleados.uicreacionEmpleado.txtApellidos.text(),self.wincrearEmpleados.uicreacionEmpleado.txtTelefono.text(),self.wincrearEmpleados.uicreacionEmpleado.txtDireccion.text(),self.wincrearEmpleados.uicreacionEmpleado.txtPuesto.text(),self.wincrearEmpleados.uicreacionEmpleado.txtIngreso.text(),self.wincrearEmpleados.uicreacionEmpleado.txtJefatura.text())
        if creacionEmpleado.guardarEmpleados()==1:
            self.msgBox("Empleado creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear Empleado",QMessageBox.Information)
        
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
    
    def guardarBienAsignado(self):
        bienesAsignados=Asignar(self.winAsignacion.uiAsignacion.txtCedula.text(),
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
        bienesAsignados=Asignar(self.winAsignacion.uiAsignacion.txtCedula.text(),
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
        bienesAsignados=Asignar(self.winAsignacion.uiAsignacion.txtCedula.text(),
                        self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(),
                        self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                        )
        if bienesAsignados.eliminar()==1:
            self.msgBox("Datos Eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los datos",QMessageBox.Warning)

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
    win=Login()
    if win.exec_() == QDialog.Accepted:
        mdi=mdiApp()
        mdi.showMaximized()
    sys.exit(app.exec())
