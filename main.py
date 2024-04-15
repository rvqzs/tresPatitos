import sys
import time
import pymongo
import webbrowser

#Graphics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#Widgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *   
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime 

#Model
from model.usuarios import Usuarios
from model.empleados import Empleados
from model.departamentos import Departamentos
from model.bienes import Bienes
from model.asignacion import AsignarBienes
from model.desligar import DesligarBienes
from model.reporteBienesAsignados import ReporteBienesAsignados
from model.reporteBienesNoAsignables import ReporteBienesNoAsignables
# from model.login import Login

# UI
from src.Ui_001_login import Ui_Login
from src.Ui_000_mdi import Ui_mdiWindow
from src.Ui_002_usuarios import Ui_Usuarios
from src.Ui_003_empleados import Ui_Empleados
from src.Ui_004_departamentos  import Ui_Departamentos
from src.Ui_005_bienes import Ui_Bienes
from src.Ui_051_asignacion_bienes import Ui_Asignacion
from src.Ui_052_desligar_bienes import Ui_Desligar
from src.Ui_061_reporte_bienes_asignados import Ui_ReporteBienesAsignados
from src.Ui_062_reporte_bienes_no_asignables import Ui_ReportBienesNoAsignables
from src.Ui_070_LoadingBox import Ui_LoadingDialog
from src.Ui_063_ReporteEmpleados import Ui_ReporteEmpleados

class Login(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initComponents()

    def initComponents(self):
        self.uiLogin.txt_username.setText("admin")
        self.uiLogin.txt_password.setText("admin")
        self.uiLogin.btn_login.clicked.connect(self.validarAdmin)
        self.uiLogin.txt_username.setFocus()

    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()

    def startLoading(self):
        self.loading_dialog = winLoadingDialog(self)
        self.loading_dialog.show()
        time.sleep(1)
        self.loading_dialog.update_progress(50)
        self.loading_dialog.update_message("Cargando...")
        time.sleep(1)
        self.loading_dialog.close()

    def validarAdmin(self):
        username = self.uiLogin.txt_username.text().upper().strip()
        password = self.uiLogin.txt_password.text().strip()

        if not username or not password:
            self.msgBox("Por favor, ingrese un nombre de usuario y una contraseña.", QMessageBox.Warning)
            return
        
        self.startLoading()
        #TODO: Hacer que la validación del usuario administrador se haga desde model/usuarios 
        #TODO: Hacer una validación para usuarios no admin
        
        client = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        db = client["TresPatitos"]
        collection = db["usuarios"]
        user = collection.find_one({"_id": username, "password": password})
        if user:
            self.loading_dialog.close()
            # mdi = mdiApp()
            # mdi.showMaximized()
            self.close()
            self.accept()
        else:
            self.loading_dialog.close()
            self.msgBox("Usuario o contraseña incorrecta, por favor intente de nuevo.", QMessageBox.Warning)
            self.__init__()

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
        self.uiMdi.btn_logout.triggered.connect(self.exitApp)
        self.uiMdi.subMnuGraficoEstado.triggered.connect(self.generar_grafico)
        self.uiMdi.mniUsuarios.triggered.connect(self.openWinUsuarios)
        self.uiMdi.mniEmpleados.triggered.connect(self.openWinEmpleados)
        self.uiMdi.mniDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniRegistrarBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mnuAsignar.triggered.connect(self.openWinAsignacionBienes)
        self.uiMdi.mnuDesligar.triggered.connect(self.openWinDesligarBienes)
        self.uiMdi.submnuBienesAsignados.triggered.connect(self.openWinReporteBienesAsignados)
        self.uiMdi.submnuBienes_no_Asignados.triggered.connect(self.openWinReporteBienesNoAsignables)
        self.uiMdi.subMenuReporteEmpleados.triggered.connect(self.openWinReporteEmpleados)
        self.uiMdi.subMenuITSupport.triggered.connect(self.helpdesk)

    def helpdesk(self):
        link = "https://rviquez.notion.site/A-n-no-hay-soporte-b6a0db1da3e14b989af3bdb65da44ce6?pvs=4"
        webbrowser.open(link)

    def msgBox(self,mensaje,icono):
        msg = QMessageBox()
        msg.setText(mensaje)
        msg.setIcon(icono)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()

    def areButtonsEnabled(self, button1=None, button2=None,
                button3=None, button4=None, isEnabled=bool):
        if button1 is not None:
            button1.setEnabled(isEnabled)
        if button2 is not None:
            button2.setEnabled(isEnabled)
        if button3 is not None:
            button3.setEnabled(isEnabled)
        if button4 is not None:
            button4.setEnabled(isEnabled)

    def isTextFilled(self, txt1=None, txt2=None, txt3=None, txt4=None):
        if txt1 is not None:
            if txt1.text() == "":
                return False
        if txt2 is not None:
            if txt2.text() == "":
                return False
        if txt3 is not None:
            if txt3.text() == "":
                return False
        if txt4 is not None:
            if txt4.text() == "":
                return False
            
        return True
    
    def populateComboBox(self, comboBox, datos, get): 
        comboBox.clear()
        comboBox.addItem("Seleccionar")
        for d in datos:
            nombre = d.get(get, "")
            if nombre:
                comboBox.addItem(nombre)

    def clearTextAndComboBox(self, *elementos):
        for elemento in elementos:
            if isinstance(elemento, QLineEdit):
                elemento.setText("")
            elif isinstance(elemento, QComboBox):
                elemento.setCurrentIndex(0)

    def exitApp(self):
        self.hide()
        login_dialog = Login()
        login_dialog.accepted.connect(self.show)
        login_dialog.exec_()

# Usuarios

    def openWinUsuarios(self):
        usuarios=Usuarios()
        self.winUsuarios=winUsuarios()
        self.uiMdi.mdiArea.addSubWindow(self.winUsuarios)
        self.winUsuarios.show()

        self.winUsuarios.uiUsuarios.txtUsername.setEnabled(True)

        # txtusername = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper() #!Delete make in a function
        # txtname = self.winUsuarios.uiUsuarios.txtName.text().title()
        # txtpassword = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        # txtconfirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        # is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()
        
        #Eventos
        self.winUsuarios.uiUsuarios.btnCrearUsuario.clicked.connect(self.guardarUsuario)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.clicked.connect(self.modificarUsuario)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.clicked.connect(self.eliminarUsuario)
        self.winUsuarios.uiUsuarios.btnLimpiar.clicked.connect(self.limpiarUsuarios)
        self.winUsuarios.uiUsuarios.isPassowordVisible.toggled.connect(self.btn_ShowPassword)

        # if not txtusername or not txtname or not txtpassword or not txtconfirm_password or not is_admin: #!Delete make in a function
        #     self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(False)
        #     self.btnEditSaveAreEnabled(False)
        # else:
        #     self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(True)
        #     self.btnEditSaveAreEnabled(True)

        self.winUsuarios.uiUsuarios.tblUsuarios.clicked.connect(self.cargarDatosUsuarios)
        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.areButtonsEnabled(button1=self.winUsuarios.uiUsuarios.btnCrearUsuario, isEnabled=True)
        

        #Focus order
        self.winUsuarios.uiUsuarios.txtUsername.setFocus()
        self.winUsuarios.uiUsuarios.txtUsername.returnPressed.connect(self.winUsuarios.uiUsuarios.txtName.setFocus)
        self.winUsuarios.uiUsuarios.txtName.returnPressed.connect(self.winUsuarios.uiUsuarios.txtPassword.setFocus)
        self.winUsuarios.uiUsuarios.txtPassword.returnPressed.connect(self.winUsuarios.uiUsuarios.txtConfirmPassword.setFocus)

    def guardarUsuario(self):
        #Loading box
        self.loading_dialog = winLoadingDialog(self)
        self.loading_dialog.update_message("Guardando usuario...")
        self.loading_dialog.update_progress(0)
        self.loading_dialog.show()

        #Input data
        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()
        
        #Validate if all fields entered
        if not username or not name or not password or not confirm_password:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            self.loading_dialog.close()
            return
        
        #Confirm password
        if password != confirm_password:
            self.msgBox("Las contraseñas no coinciden", QMessageBox.Warning)
            self.loading_dialog.close()
            return

        #Save new user
        user = Usuarios(username, name, password, is_admin)
        if user.guardar()==1:
            self.loading_dialog.update_progress(100)
            self.limpiarUsuarios()
            self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
            message="Nuevo usuario " + username + " creado con éxito!"
            self.loading_dialog.close()
            self.msgBox(message,QMessageBox.Information)

        elif user.guardar()==0:
            self.loading_dialog.close()
            self.msgBox("Error de registro, el usuario ya está registrado",QMessageBox.Information)
            self.limpiarUsuarios()
        else:
            self.loading_dialog.close()
            self.limpiarUsuarios()
            self.msgBox("Error al registrar nuevo usuario",QMessageBox.Information)

    def modificarUsuario(self):
        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().strip().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()

        if not username or not name or not password:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return

        if not confirm_password:
            self.msgBox("Debe confirmar la contraseña para modificar un usuario", QMessageBox.Warning)
            return

        if password != confirm_password:
            self.msgBox("Las contraseñas no coinciden", QMessageBox.Warning)
            return
        
        user = Usuarios(username, name, password, is_admin)
        if user.actualizar()==1:
            self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
            self.limpiarUsuarios()
            message="Usuario " + username + " modificado correctamente"
            self.msgBox(message,QMessageBox.Information)
        else:
            message="Error al modificar usuario " + username
            self.msgBox(message, QMessageBox.Information)
            self.limpiarUsuarios()

    def eliminarUsuario(self):
        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().strip().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()

        # confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()

        if not confirm_password:
            self.msgBox("Debe confirmar la contraseña para eliminar un usuario", QMessageBox.Warning)
            return

        user = Usuarios(username, name, password, is_admin)
        if user.eliminar()==1:
            self.limpiarUsuarios()
            self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
            message="Usuario " + username + " ha sido eliminado correctamente!"
            self.msgBox(message,QMessageBox.Information)
        else:
            message="Error al eliminar usuario " + username
            self.msgBox(message, QMessageBox.Information)

        self.areButtonsEnabled(button1=self.winUsuarios.uiUsuarios.btnCrearUsuario,
                            button2=self.winUsuarios.uiUsuarios.btnModificarUsuario,
                            button3=self.winUsuarios.uiUsuarios.btnLimpiar, button4=self.winUsuarios.uiUsuarios.btnEliminarUsuario, isEnabled=False)

    def cargarTablaUsuarios(self, numFilas, datos):
        self.winUsuarios.uiUsuarios.tblUsuarios.setRowCount(numFilas)
        self.winUsuarios.uiUsuarios.tblUsuarios.setColumnCount(4)
        i = 0
        for d in datos:
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i, 0, QTableWidgetItem(d["_id"]))
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i, 1, QTableWidgetItem(d["nombre"]))
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i, 2, QTableWidgetItem(d["password"]))
            privilegio = "Administrador" if d["is_admin"] else "Usuario"
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i, 3, QTableWidgetItem(privilegio))
            i += 1

    def cargarDatosUsuarios(self):
        self.winUsuarios.uiUsuarios.txtUsername.setEnabled(False)
        self.areButtonsEnabled(button1=self.winUsuarios.uiUsuarios.btnCrearUsuario, isEnabled=False)
        self.areButtonsEnabled(button1=self.winUsuarios.uiUsuarios.btnModificarUsuario,
                            button2=self.winUsuarios.uiUsuarios.btnLimpiar, button3=self.winUsuarios.uiUsuarios.btnEliminarUsuario, isEnabled=True)
        
        self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(True)
        numFilas = self.winUsuarios.uiUsuarios.tblUsuarios.currentRow()
        self.winUsuarios.uiUsuarios.txtUsername.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 0).text())
        self.winUsuarios.uiUsuarios.txtName.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 1).text())
        self.winUsuarios.uiUsuarios.txtPassword.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 2).text())
        admin_value = self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 3).text()

        admin_value = self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 3).text()

        if admin_value.lower() == 'Administrador':
            self.winUsuarios.uiUsuarios.chkBoxAdmin.setChecked(True)
        else:
            self.winUsuarios.uiUsuarios.chkBoxAdmin.setChecked(False)

    def limpiarUsuarios(self):
        self.winUsuarios.uiUsuarios.txtUsername.setText("")
        self.winUsuarios.uiUsuarios.txtName.setText("")
        self.winUsuarios.uiUsuarios.txtPassword.setText("")
        self.winUsuarios.uiUsuarios.txtConfirmPassword.setText("")
        self.winUsuarios.uiUsuarios.chkBoxAdmin.setChecked(False)
        self.winUsuarios.uiUsuarios.isPassowordVisible.setChecked(False)
        self.winUsuarios.uiUsuarios.txtUsername.setEnabled(True)
        self.areButtonsEnabled(button2=self.winUsuarios.uiUsuarios.btnModificarUsuario,
                    button3=self.winUsuarios.uiUsuarios.btnLimpiar, button4=self.winUsuarios.uiUsuarios.btnEliminarUsuario, isEnabled=False)
        self.areButtonsEnabled(button1=self.winUsuarios.uiUsuarios.btnCrearUsuario, isEnabled=True)

    def togglePasswordVisibility(self, visible):
        if visible:
            self.winUsuarios.uiUsuarios.txtPassword.setEchoMode(QLineEdit.Normal)
            self.winUsuarios.uiUsuarios.txtConfirmPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.winUsuarios.uiUsuarios.txtPassword.setEchoMode(QLineEdit.Password)
            self.winUsuarios.uiUsuarios.txtConfirmPassword.setEchoMode(QLineEdit.Password)

    def btn_ShowPassword(self):
        visibility = self.winUsuarios.uiUsuarios.isPassowordVisible.isChecked()
        self.togglePasswordVisibility(visibility)

# Empleados
    #TODO: If text = "" disable btn limpiar

    def openWinEmpleados(self):
        self.winEmpleados=winEmpleados()
        departamento=Departamentos()
        empleado=Empleados()
        usuarios=Usuarios() # ? Delete? no se esta utilizando
        self.uiMdi.mdiArea.addSubWindow(self.winEmpleados)
        self.winEmpleados.show()

        self.areButtonsEnabled(button1=self.winEmpleados.uiEmpleados.bttModificarEmpleado,
                                button2=self.winEmpleados.uiEmpleados.bttEliminarEmpleado,
                                button3=self.winEmpleados.uiEmpleados.bttLimpiarEmpleado, isEnabled=False)

        #Eventos
        self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
        self.populateComboBox(self.winEmpleados.uiEmpleados.cmbBoxDepartamento, departamento.getDepartamentos(), get="nombre")
        self.populateComboBox(self.winEmpleados.uiEmpleados.cmbBoxUsuarios, self.getUsersWithoutEmpleado(), get="_id")

        # self.comboBoxDepartamentosEmpleados(departamento.getDepartamentos())
        # self.comboBoxUsuarioEmpleados(usuarios.getUsuarios())

        self.winEmpleados.uiEmpleados.bttCrearEmpleado.clicked.connect(self.guardarEmpleado)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.clicked.connect(self.actualizarEmpleado)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.clicked.connect(self.eliminarEmpleado)
        self.winEmpleados.uiEmpleados.bttLimpiarEmpleado.clicked.connect(self.limpiarEmpleados)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.clicked.connect(self.cargarDatosEmpleados)

    def guardarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text().title()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text().strip()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.text()
        isJefatura=self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.isChecked()            

        if (not usuario or not cedula or not
            nombre or not telefono or not fechIngreso or not
            direccion):
            
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return

        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso,
                            direccion, isJefatura)

        if empleado.guardarEmpleados()==1:
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
            self.limpiarEmpleados()
            self.msgBox("Empleado creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear Empleado",QMessageBox.Information)
            self.limpiarEmpleados()
        
    def actualizarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.text()
        isJefatura=self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.isChecked()

        if (not usuario or not cedula or not
            nombre or not telefono or not fechIngreso or not
            direccion):
            
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return
        
        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso, direccion, isJefatura)

        if empleado.actualizarEmpleados()==1:
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
            self.msgBox("Empleado actualizado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al actualizar Empleado",QMessageBox.Information)

    def eliminarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.text()
        is_Supervisor=self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.isChecked()
        
        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso, direccion, is_Supervisor)

        if empleado.eliminarEmpleados()==1:
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
            self.msgBox("Empleado eliminado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar Empleado",QMessageBox.Information)
            self.limpiarEmpleados()

    def limpiarEmpleados(self):
        self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setEnabled(True)
        self.populateComboBox(self.winEmpleados.uiEmpleados.cmbBoxUsuarios, self.getUsersWithoutEmpleado(), "_id")
        self.areButtonsEnabled(button1=self.winEmpleados.uiEmpleados.bttCrearEmpleado, isEnabled=True)
        self.areButtonsEnabled(button1=self.winEmpleados.uiEmpleados.bttModificarEmpleado, 
                                button2=self.winEmpleados.uiEmpleados.bttEliminarEmpleado,
                                button3=self.winEmpleados.uiEmpleados.bttLimpiarEmpleado, isEnabled=False)

        self.winEmpleados.uiEmpleados.txtCedula.setText("")
        self.winEmpleados.uiEmpleados.txtNombre.setText("")
        self.winEmpleados.uiEmpleados.txtTelefono.setText("")
        self.winEmpleados.uiEmpleados.txtDireccion.setText("")
        self.winEmpleados.uiEmpleados.cmbBoxDepartamento.setCurrentIndex(0)
        self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setCurrentIndex(0)
        self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.setChecked(False)

    def cargarTablaEmpleados(self, row, data):
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setRowCount(row)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setColumnCount(8)
        i=0
        for b in data:
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,0,QTableWidgetItem(b["fechaIngreso"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,1,QTableWidgetItem(b["_id"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,2,QTableWidgetItem(b["cedula"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,3,QTableWidgetItem(b["nombre"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,4,QTableWidgetItem(b["departamento"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,5,QTableWidgetItem(b["telefono"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,6,QTableWidgetItem(b["direccion"]))
            
            isJefatura = "Supervisor" if b["isJefatura"] else "Empleado"
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i, 7, QTableWidgetItem(isJefatura))
            i+=1
    
    def cargarDatosEmpleados(self): 
        self.populateComboBox(self.winEmpleados.uiEmpleados.cmbBoxUsuarios, Usuarios().getUsuarios(), "_id")

        row=self.winEmpleados.uiEmpleados.tblWidgetEmpleados.currentRow()

        #Columna Fecha
        fecha_texto = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 0).text()
        fecha = QDateTime.fromString(fecha_texto, "dd-MM-yyyy")  
        self.winEmpleados.uiEmpleados.txtDate.setDate(fecha.date())

        #Columna Usuario
        valor_usuario = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 1).text()
        index = self.winEmpleados.uiEmpleados.cmbBoxUsuarios.findText(valor_usuario)
        if index != -1:
            self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setCurrentIndex(index)

        #Columna Cedula
        self.winEmpleados.uiEmpleados.txtCedula.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,2).text())

        #Columna Nombre
        self.winEmpleados.uiEmpleados.txtNombre.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,3).text())

        #Columna Departamento
        departamento = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 4).text()
        index = self.winEmpleados.uiEmpleados.cmbBoxDepartamento.findText(departamento)
        if index != -1:
            self.winEmpleados.uiEmpleados.cmbBoxDepartamento.setCurrentIndex(index)
        
        #Columna Telefono
        self.winEmpleados.uiEmpleados.txtTelefono.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,5).text())

        #Columna Direccion
        self.winEmpleados.uiEmpleados.txtDireccion.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,6).text())
        
        #Columna Puesto
        isJefatura = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 7).text()
        if isJefatura=="Supervisor":
            self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.setChecked(True)
        else:
            self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.setChecked(False)

        self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setEnabled(False)
        self.areButtonsEnabled(button1=self.winEmpleados.uiEmpleados.bttCrearEmpleado, isEnabled=False)
        self.areButtonsEnabled(button1=self.winEmpleados.uiEmpleados.bttModificarEmpleado,
                                button2=self.winEmpleados.uiEmpleados.bttEliminarEmpleado,
                                button3=self.winEmpleados.uiEmpleados.bttLimpiarEmpleado, isEnabled=True)

    def getUsersWithoutEmpleado(self):
        user = Usuarios()
        empleado = Empleados()
        allUsers = user.getUsuarios()
        allEmpleados = empleado.getEmpleados()

        # Set of _id values for users associated with an employee
        usuarios_with_empleado = {empleado['_id'] for empleado in allEmpleados}

        # Filter out users with associated employees and exclude admin
        usuarios_without_empleado = [
            usuario for usuario in allUsers 
            if usuario['_id'] not in usuarios_with_empleado 
            and usuario['_id'] != 'ADMIN'
        ]

        return usuarios_without_empleado

# Departamentos
    #TODO: Agregar Pantalla de carga para boton Refresh 
    
    def openWinDepartamentos(self):
        self.winDepartamentos=winDepartamentos()
        departamento=Departamentos()
        empleado=Empleados()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.winDepartamentos.show()

        self.cargarTablaDepartamentos(departamento.getCountDepartamentos(),departamento.getDepartamentos())
        self.populateComboBox(self.winDepartamentos.uiDepartamentos.cmb_jefatura ,empleado.getJefaturas(), get="nombre")

        # Butttons
        self.btnRegistrarDepartamento=self.winDepartamentos.uiDepartamentos.btn_registrar
        self.btnEditarDepartamento=self.winDepartamentos.uiDepartamentos.btn_editar
        self.btnEliminarDepartamento=self.winDepartamentos.uiDepartamentos.btn_eliminar
        self.btnNewCodeDepartamento=self.winDepartamentos.uiDepartamentos.btnNewCode
        self.btnLimpiarDepartamento=self.winDepartamentos.uiDepartamentos.btnLimpiar
        self.btnRefreshDepartamento=self.winDepartamentos.uiDepartamentos.btnRefresh
        self.tblDepartamentos=self.winDepartamentos.uiDepartamentos.tblDepartamentos
        
        #Input
        self.txtCodigoDepartamento=self.winDepartamentos.uiDepartamentos.txt_codigo
        self.txtNombreDepartamento=self.winDepartamentos.uiDepartamentos.txt_nombre
        self.cmbJefaturaDepartamento=self.winDepartamentos.uiDepartamentos.cmb_jefatura

        #Eventos
        self.areButtonsEnabled(button1=self.btnEditarDepartamento, button2=self.btnEliminarDepartamento,
                                button3=self.btnLimpiarDepartamento, isEnabled=False)

        self.btnRegistrarDepartamento.clicked.connect(self.registrarDepartamento)
        self.btnEditarDepartamento.clicked.connect(self.actualizarDepartamento)
        self.btnEliminarDepartamento.clicked.connect(self.eliminarDepartamento)
        self.btnNewCodeDepartamento.clicked.connect(self.generarNuevoCodigo)
        self.btnLimpiarDepartamento.clicked.connect(self.limpiarDatos)
        self.btnRefreshDepartamento.clicked.connect(self.limpiarDatosDepartamento)
        self.tblDepartamentos.clicked.connect(self.cargarDatosDepartamentos)

    def registrarDepartamento(self):
        departamento=Departamentos()
        codigo=self.txtCodigoDepartamento.text().strip().upper()
        nombre=self.txtNombreDepartamento.text().strip().title()
        jefatura=str(self.cmbJefaturaDepartamento.currentText())

        if not codigo or not nombre or jefatura=="Seleccionar":
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return
        
        if departamento.existeDepartamento(nombre):
            self.msgBox("Error al registrar departamento, no pueden existir dos departamentos con el mismo nombre", QMessageBox.Warning)
            return
        else:
            departamento = Departamentos(codigo, nombre, jefatura)


        if departamento.registrar()==1:
            self.limpiarDatosDepartamento()
            message="Departamento " + codigo + " registrado correctamente"
            self.msgBox(message,QMessageBox.Information)
        else:
            self.msgBox("Error al registrar departamento",QMessageBox.Warning)
            return

    def actualizarDepartamento(self):
        departamento=Departamentos()
        codigo=self.txtCodigoDepartamento.text().strip().upper()
        nombre=self.txtNombreDepartamento.text().strip().title()
        jefatura=str(self.cmbJefaturaDepartamento.currentText())

        if not codigo or not nombre or jefatura=='Seleccionar':
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return

        if departamento.existeDepartamento():
            self.msgBox("Error al actualizar departamento, no pueden existir dos departamentos con el mismo nombre",QMessageBox.Warning)
        else:
            departamento = Departamentos(codigo, nombre, jefatura)

        if departamento.actualizar()==1:
            self.limpiarDatosDepartamento()
            self.msgBox("Departamento actualizado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al actualizar el departamento",QMessageBox.Warning)
            return

    def eliminarDepartamento(self):
        codigo=self.txtCodigoDepartamento.text().strip().upper()
        nombre=self.txtNombreDepartamento.text().strip().title()
        jefatura=str(self.cmbJefaturaDepartamento.currentText())

        departamento = Departamentos(codigo, nombre, jefatura)
        if departamento.eliminar()==1:
            self.limpiarDatosDepartamento()
            message="Departamento "+ nombre + " eliminado con éxito!"
            self.msgBox(message,QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar departamento",QMessageBox.Warning)

    def cargarTablaDepartamentos(self, rowCount, datos):
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setRowCount(rowCount)
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setColumnCount(3)

        i = 0
        for d in datos:
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 0, QTableWidgetItem(d["_id"]))
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 1, QTableWidgetItem(d["nombre"]))
            texto_jefatura = d["jefatura"]
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 2, QTableWidgetItem(texto_jefatura))
            i += 1

    def cargarDatosDepartamentos(self):
        rowCount = self.winDepartamentos.uiDepartamentos.tblDepartamentos.currentRow()
        self.txtCodigoDepartamento.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(rowCount, 0).text())
        self.txtNombreDepartamento.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(rowCount, 1).text())
        
        text_jefatura = self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(rowCount, 2).text()
        index = self.cmbJefaturaDepartamento.findText(text_jefatura)
        if index !=-1:
            self.cmbJefaturaDepartamento.setCurrentIndex(index)

        self.areButtonsEnabled(button1=self.btnRegistrarDepartamento, isEnabled=False)
        self.areButtonsEnabled(button1=self.btnEditarDepartamento, button2=self.btnEliminarDepartamento, 
                            button3=self.btnLimpiarDepartamento, isEnabled=True)

    def generarNuevoCodigo(self):
        departamento = Departamentos()
        last_code = departamento.getLastCode()
        if last_code is not None:
            nuevo_numero = last_code + 1
        else:
            nuevo_numero = 1
        nuevo_codigo = f"DPT{nuevo_numero:03}"

        self.winDepartamentos.uiDepartamentos.txt_codigo.setText(nuevo_codigo)
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText("DEPTO " + str(nuevo_numero))
        self.winDepartamentos.uiDepartamentos.txt_codigo.setEnabled(False)

        self.areButtonsEnabled(button1=self.winDepartamentos.uiDepartamentos.btnNewCode,
                                button2=self.winDepartamentos.uiDepartamentos.btn_editar,
                                button3=self.winDepartamentos.uiDepartamentos.btn_eliminar, isEnabled=False)

        self.areButtonsEnabled(button1=self.winDepartamentos.uiDepartamentos.btn_registrar,
                                button2=self.winDepartamentos.uiDepartamentos.btnLimpiar, isEnabled=True)

    def limpiarDatosDepartamento(self):
        departamento=Departamentos()
        empleado=Empleados()
        self.clearTextAndComboBox(self.winDepartamentos.uiDepartamentos.txt_codigo, self.winDepartamentos.uiDepartamentos.txt_nombre,
                                    self.winDepartamentos.uiDepartamentos.cmb_jefatura)
        self.cargarTablaDepartamentos(departamento.getCountDepartamentos(),departamento.getDepartamentos())
        self.winDepartamentos.uiDepartamentos.btnNewCode.setEnabled(True)
        self.winDepartamentos.uiDepartamentos.cmb_jefatura.setEnabled(True)
        # self.populateComboBox(self.winDepartamentos.uiDepartamentos.cmb_jefatura ,empleado.getJefaturas(), get="nombre")

    def limpiarDatos(self):
        self.clearTextAndComboBox(self.winDepartamentos.uiDepartamentos.txt_codigo, self.winDepartamentos.uiDepartamentos.txt_nombre,
                                    self.winDepartamentos.uiDepartamentos.cmb_jefatura)
        self.areButtonsEnabled(button1=self.winDepartamentos.uiDepartamentos.btnNewCode, isEnabled=True)

# Registrar Bienes

    def openWinBienes(self):
        bien=Bienes()
        self.winBienes=winBienes()
        self.contador_placa=1
        
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winBienes)
        #eventos
        self.winBienes.uiBienes.btnGuardar.clicked.connect(self.guardarBienes)
        
        self.winBienes.uiBienes.btnModificar.clicked.connect(self.modificarBienes)
        self.winBienes.uiBienes.btnEliminar.clicked.connect(self.eliminarBienes)
        self.winBienes.uiBienes.btnLimpiar.clicked.connect(self.limpiarBienes)
        self.winBienes.uiBienes.tblRegistro.clicked.connect(self.cargarDatosBienes)
        self.cargarTablaBienes(bien.getNumeroRegistros(),bien.getBienes())
        self.inicializar_contador_placa()
        self.generar_placa()
        self.winBienes.show()

    def guardarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text().strip().title(),
                        self.winBienes.uiBienes.txtCategoria.text().strip().title(),
                        self.winBienes.uiBienes.txtDescripcion.text().strip().title(),
                        self.winBienes.uiBienes.cbxEstado.currentText())
        
        if bien.guardar()==1:
            self.limpiarBienes()
            self.cargarTablaBienes(bien.getNumeroRegistros(),bien.getBienes())
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
            self.contador_placa += 1
            self.generar_placa()
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)

    def modificarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(),
                        self.winBienes.uiBienes.txtNombreBien.text().strip().title(),
                        self.winBienes.uiBienes.txtCategoria.text().strip().title(),
                        self.winBienes.uiBienes.txtDescripcion.text().strip().title(),
                        self.winBienes.uiBienes.cbxEstado.currentText())
        
        if bien.actualizar()==1:
            self.limpiarBienes()
            self.cargarTablaBienes(bien.getNumeroRegistros(),bien.getBienes())
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)

    def eliminarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(), self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(), self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.cbxEstado.currentText())
        if bien.eliminar()==1:
            self.limpiarBienes()
            self.cargarTablaBienes(bien.getNumeroRegistros(),bien.getBienes())
            self.msgBox("Datos Eliminados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar los datos",QMessageBox.Warning)

    def limpiarBienes(self):
        self.winBienes.uiBienes.txtPlaca.setText("")
        self.winBienes.uiBienes.txtNombreBien.setText("")
        self.winBienes.uiBienes.txtCategoria.setText("")
        self.winBienes.uiBienes.txtDescripcion.setText("")
        self.winBienes.uiBienes.cbxEstado.setCurrentIndex(0)

    def cargarTablaBienes(self, numFilas, datos):
        #determinar el numero de filas de la tabla
        self.winBienes.uiBienes.tblRegistro.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winBienes.uiBienes.tblRegistro.setColumnCount(5)
        i=0
        for d in datos:
            print(d)
            self.winBienes.uiBienes.tblRegistro.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,1,QTableWidgetItem(d["nombre"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,2,QTableWidgetItem(d["categoria"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,3,QTableWidgetItem(d["descripcion"]))
            self.winBienes.uiBienes.tblRegistro.setItem(i,4,QTableWidgetItem(d["estado"]))
            i+=1
    
    def cargarDatosBienes(self):
        numFila=self.winBienes.uiBienes.tblRegistro.currentRow()
        self.winBienes.uiBienes.txtPlaca.setText(self.winBienes.uiBienes.tblRegistro.item(numFila,0).text())
        self.winBienes.uiBienes.txtNombreBien.setText(self.winBienes.uiBienes.tblRegistro.item(numFila,1).text())
        self.winBienes.uiBienes.txtCategoria.setText(self.winBienes.uiBienes.tblRegistro.item(numFila,2).text())
        self.winBienes.uiBienes.txtDescripcion.setText(self.winBienes.uiBienes.tblRegistro.item(numFila,3).text())
        self.winBienes.uiBienes.cbxEstado.setCurrentText(self.winBienes.uiBienes.tblRegistro.item(numFila,4).text())

    def inicializar_contador_placa(self):
        self.bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        self.bd = self.bien["TresPatitos"]
        self.tbl = self.bd["bienes"]
        # Buscar el último bien con número de placa y obtener el número siguiente
        ultimo_bien = self.tbl.find_one(sort=[("_id", pymongo.DESCENDING)])
        if ultimo_bien and "_id" in ultimo_bien:
            self.contador_placa = int(ultimo_bien["_id"].split("-")[1]) + 1
        else:
            self.contador_placa = 1  # Si no hay ningún bien con número de placa, empezamos desde 1

    def generar_placa(self):
        # Generar la placa en el formato "AB-0001"
        letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letras_placa = letras[self.contador_placa // 1000 % 26] + letras[self.contador_placa // 100 % 26]  # Dos letras
        numeros_placa = '{:04d}'.format(self.contador_placa % 10000)  # Cuatro números con ceros a la izquierda
        placa = letras_placa + '-' + numeros_placa
        self.winBienes.uiBienes.txtPlaca.setText(placa)

    #Asignar Bienes

    def openWinAsignacionBienes(self):
        asignado=AsignarBienes()
        self.winAsignacion=winAsignacionBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winAsignacion)
        #eventos
        self.comboBoxAsignarEmpeladosCedula(asignado.getEmpleados())
        self.comboBoxBienes(asignado.getBienes())
        self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentIndexChanged.connect(self.cargarMetodoEspaciosAsignar)
        self.winAsignacion.uiAsignacion.btnGuardar.clicked.connect(self.guardarBienAsignado)
        self.winAsignacion.uiAsignacion.btnLimpiar.clicked.connect(self.limpiarAsignados)
        #self.winAsignacion.uiAsignacion.tblAsignados.clicked.connect(self.cargarDatosAsignacion)
        self.cargarTablaBienesAsignado(asignado.getNumeroAsignados(),asignado.getAsignados())
        self.winAsignacion.show()

    def guardarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentText(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                    self.winAsignacion.uiAsignacion.txtTelefono.text(),
                    self.winAsignacion.uiAsignacion.cbxBienes.currentText()
                    )
        if bienesAsignados.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
            self.cargarTablaBienesAsignado(bienesAsignados.getNumeroAsignados(),bienesAsignados.getAsignados())
            self.limpiarAsignados()
        else:
            self.msgBox("Error al guardar los datos, el bien ya ha sido asignado a un empleado",QMessageBox.Warning)

    def limpiarAsignados(self):
        self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.setCurrentIndex(0)
        self.winAsignacion.uiAsignacion.txtNombre.setText("")
        self.winAsignacion.uiAsignacion.txtTelefono.setText("")
        self.winAsignacion.uiAsignacion.cbxBienes.setCurrentIndex(0)

    def espaciosAsignar(self, datos):

        cedulaArchivo=self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentText()
        #i=0
        for d in datos:
            cedula=d["cedula"]
            #bien=["bien_asignado"]
            if cedula==cedulaArchivo:
                self.winAsignacion.uiAsignacion.txtNombre.setText(d["nombre"])
                self.winAsignacion.uiAsignacion.txtTelefono.setText(d["telefono"])
                #i+=1

    def cargarMetodoEspaciosAsignar(self):
        asignar=AsignarBienes()
        self.espaciosAsignar(asignar.getEmpleados())

    def cargarTablaBienesAsignado(self, numFilas, datos):
        #determinar el numero de filas de la tabla
        self.winAsignacion.uiAsignacion.tblAsignados.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winAsignacion.uiAsignacion.tblAsignados.setColumnCount(4)
        i=0
        for d in datos:
            print(d)
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,0,QTableWidgetItem(d["cedula"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,1,QTableWidgetItem(d["nombre"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,2,QTableWidgetItem(d["telefono"]))
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,3,QTableWidgetItem(d["_id"]))
            i+=1

    def comboBoxAsignarEmpeladosCedula(self, datos):
        for d in datos:
            cedula=d["cedula"]
            if cedula:
                self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.addItem(cedula)
    
    def comboBoxBienes(self, datos):
        for d in datos:
            nombre=d["nombre"]
            if nombre:
                self.winAsignacion.uiAsignacion.cbxBienes.addItem(nombre)

    #Desligar Bienes

    def openWinDesligarBienes(self):
        desligar=DesligarBienes()
        self.winDesligar=winDesligarBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winDesligar)
        #eventos
        self.comboBoxBienesAsignado(desligar.getAsignados())
        self.winDesligar.uiDesligar.cbxEmpleados.currentIndexChanged.connect(self.espaciosDesligar)
        self.winDesligar.uiDesligar.cbxEmpleados.currentIndexChanged.connect(self.cargarMetodoTablaDesligar)
        self.winDesligar.uiDesligar.btnDesligar.clicked.connect(self.eliminarDesligar)
        self.winDesligar.uiDesligar.btnLimpiar.clicked.connect(self.limpiarDesligados)
        #self.cargarTablaDesligar(desligar.getNumeroDesligar(),desligar.getAsignados())
        self.winDesligar.uiDesligar.tblDesligar2.clicked.connect(self.cargarDatosDesligar)
        #self.cargarEmpleadosAsignados(desligar.getNumeroDesligar(),desligar.getAsignados())
        self.winDesligar.show()

    def cargarEmpleadosAsignados(self, numFilas, datos):
        
        self.winDesligar.uiDesligar.tblDesligar2.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winDesligar.uiDesligar.tblDesligar2.setColumnCount(2)
        i=0
        for d in datos:
            print(d)
            self.winDesligar.uiDesligar.tblDesligar2.setItem(i,0,QTableWidgetItem(d["nombre"]))
            self.winDesligar.uiDesligar.tblDesligar2.setItem(i,1,QTableWidgetItem(d["_id"]))
            i+=1

    def cargarMetodoTablaDesligar(self):
        desligar=DesligarBienes()
        self.tablaBienDesligar(desligar.getNumeroDesligar(), desligar.getAsignados())

    def tablaBienDesligar(self, numFilas, datos):

        self.winDesligar.uiDesligar.tblDesligar2.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winDesligar.uiDesligar.tblDesligar2.setColumnCount(3)

        nombreArchivo=self.winDesligar.uiDesligar.cbxEmpleados.currentText()
        i=0
        for d in datos:
            nombre=d["nombre"]
            #bien=["bien_asignado"]
            if nombre==nombreArchivo:
                self.winDesligar.uiDesligar.tblDesligar2.setItem(i,0,QTableWidgetItem(d["cedula"]))
                self.winDesligar.uiDesligar.tblDesligar2.setItem(i,1,QTableWidgetItem(d["nombre"]))
                self.winDesligar.uiDesligar.tblDesligar2.setItem(i,2,QTableWidgetItem(d["_id"]))
                i+=1

    def espaciosDesligar(self):
        nombre=self.winDesligar.uiDesligar.cbxEmpleados.currentText()
        self.winDesligar.uiDesligar.txtNombre.setText(nombre)
        #self.winDesligar.uiDesligar.txtBienAsignado.setText()
    
    
    def eliminarDesligar(self):
        desligar=DesligarBienes(self.winDesligar.uiDesligar.txtCedula.text(),
                        self.winDesligar.uiDesligar.txtNombre.text(),
                        self.winDesligar.uiDesligar.txtBienAsignado.text()
                        )
        if desligar.eliminar()==1:
            self.msgBox("Bien desligado Correctamente",QMessageBox.Information)
            self.limpiarDesligados()
        else:
            self.msgBox("Error al desligar los datos",QMessageBox.Warning)

    def limpiarDesligados(self):
        self.winDesligar.uiDesligar.cbxEmpleados.setCurrentIndex(0)
        self.winDesligar.uiDesligar.txtCedula.setText("")
        self.winDesligar.uiDesligar.txtNombre.setText("")
        self.winDesligar.uiDesligar.txtBienAsignado.setText("")
        self.winDesligar.uiDesligar.tblDesligar2.clearContents()
    
    def comboBoxBienesAsignado(self, datos):
        for d in datos:
            nombre=d["nombre"]
            if nombre:
                self.winDesligar.uiDesligar.cbxEmpleados.addItem(nombre)

    def cargarDatosDesligar(self):
        numFila=self.winDesligar.uiDesligar.tblDesligar2.currentRow()
        #self.winDesligar.uiDesligar.cbxEmpleados.setCurrentText(self.winDesligar.uiDesligar.tblDesligar.item(numFila,0).text())
        self.winDesligar.uiDesligar.txtCedula.setText(self.winDesligar.uiDesligar.tblDesligar2.item(numFila,0).text())
        self.winDesligar.uiDesligar.txtNombre.setText(self.winDesligar.uiDesligar.tblDesligar2.item(numFila,1).text())
        self.winDesligar.uiDesligar.txtBienAsignado.setText(self.winDesligar.uiDesligar.tblDesligar2.item(numFila,2).text())

    def openWinReporteBienesAsignados(self):
        reporteBienesAsignados=ReporteBienesAsignados()
        self.winReporteBienesAsig=winReporteBienesAsignados()
        #agregar ventana
        self.uiMdi.mdiArea.addSubWindow(self.winReporteBienesAsig)
        #eventos
        self.comboBoxBienesAsignadoReporte(reporteBienesAsignados.getAsignados())
        self.winReporteBienesAsig.uiReporteBienesAsignados.btnLimpiar.clicked.connect(self.limpiarReporte)
        self.winReporteBienesAsig.uiReporteBienesAsignados.cbxSeleccionEmpleado.currentIndexChanged.connect(self.cargarMetodoTablaReporteAsignados)
        self.winReporteBienesAsig.show()

    def comboBoxBienesAsignadoReporte(self, datos):
        for d in datos:
            nombre=d["nombre"]
            if nombre:
                self.winReporteBienesAsig.uiReporteBienesAsignados.cbxSeleccionEmpleado.addItem(nombre)
    
    def cargarMetodoTablaReporteAsignados(self):
        asignadosReporte=ReporteBienesAsignados()
        self.tablaReporteAsignados(asignadosReporte.getNumeroAsignadosReporte(), asignadosReporte.getAsignados())

    def tablaReporteAsignados(self, numFilas, datos):

        self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setColumnCount(4)

        nombreArchivo=self.winReporteBienesAsig.uiReporteBienesAsignados.cbxSeleccionEmpleado.currentText()
        i=0
        for d in datos:
            nombre=d["nombre"]
            if nombre==nombreArchivo:
                self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setItem(i,0,QTableWidgetItem(d["cedula"]))
                self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setItem(i,1,QTableWidgetItem(d["nombre"]))
                self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setItem(i,2,QTableWidgetItem(d["telefono"]))
                self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.setItem(i,3,QTableWidgetItem(d["_id"]))
                i+=1

    def limpiarReporte(self):
        self.winReporteBienesAsig.uiReporteBienesAsignados.cbxSeleccionEmpleado.setCurrentIndex(0)
        self.winReporteBienesAsig.uiReporteBienesAsignados.tblReporteBienesAsignados.clearContents()

    def openWinReporteBienesNoAsignables(self):
        #reporteBienesNoAsignables=ReporteBienesNoAsignables()
        self.winReporteBienesNoAsignables=winReportBienesNoAsignables()
        #ventana
        self.uiMdi.mdiArea.addSubWindow(self.winReporteBienesNoAsignables)
        self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.bttBienesNoAsignables.clicked.connect(self.llamarBienesNoAsignados)
        #self.obtenerBienesNoAsignados(reporteBienesNoAsignables.getNumeroRegistros(),reporteBienesNoAsignables.getBienes())
        #eventos
        self.winReporteBienesNoAsignables.show()

    def llamarBienesNoAsignados(self):
        bien=Bienes()
        self.winBienes=winBienes()
        reporteBienesNoAsignables=ReporteBienesNoAsignables()
        #findestado=self.winBienes.uiBienes.cbxEstado.currentText()
        #if findestado==["Reparacion"]:
        #self.msgBox("Bienes no asignables encontrados",QMessageBox.Information)
        self.obtenerBienesNoAsignados(reporteBienesNoAsignables.getNumeroRegistros(),reporteBienesNoAsignables.getBienes())
        #else:
            #self.msgBox("No hay bienes asignables",QMessageBox.Information)

    def obtenerBienesNoAsignados(self,numFilas,datos):
        self.winBienes=winBienes()
        self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setRowCount(numFilas)
        self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setColumnCount(5)
        i=0
        findestado=self.winBienes.uiBienes.cbxEstado.currentText()
        #self.winBienes.uiBienes.tblRegistro.setItem(i,4,QTableWidgetItem(d["estado"]))
        for d in datos:
            bienestado=d["estado"]
            if findestado!=bienestado:
                #self.msgBox("Bienes no asignables encontrados",QMessageBox.Information)
                self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setItem(i,0,QTableWidgetItem(d["_id"]))
                self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setItem(i,1,QTableWidgetItem(d["nombre"]))
                self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setItem(i,2,QTableWidgetItem(d["categoria"]))
                self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setItem(i,3,QTableWidgetItem(d["descripcion"]))
                self.winReporteBienesNoAsignables.uiReporteBienesNoAsignables.tblWidgetBienesNoAsignados.setItem(i,4,QTableWidgetItem(d["estado"]))
                i+=1

    def generar_grafico(self):
        uri = "mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/"
        base_datos = "TresPatitos"
        coleccion = "bienes"

        client = pymongo.MongoClient(uri)
        bd = client[base_datos]
        bienes = bd[coleccion]

        # Contar la cantidad de bienes en cada estado
        estados = ["Asignable", "Reparacion", "Exclusion"]
        cantidad_por_estado = {}

        for estado in estados:
            cantidad_por_estado[estado] = bienes.count_documents({"estado": estado})

        # Crear el gráfico
        labels = estados
        sizes = [cantidad_por_estado[estado] for estado in estados]
        colors = ['lightblue', 'lightcoral', 'lightgreen']

        plt.bar(labels, sizes, color=colors)
        plt.xlabel('Estado')
        plt.ylabel('Cantidad')
        plt.title('Cantidad de Bienes por Estado')
        plt.show()



    #Reporte Empleados por Departamento
    
    def openWinReporteEmpleados(self):
        self.winReporteEmpleados=winReporteEmpleados()
        departamento=Departamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winReporteEmpleados)
        self.winReporteEmpleados.show()

        self.populateComboBox(self.winReporteEmpleados.uiReporteEmpleados.cmbBoxDepartamento, departamento.getDepartamentos(), get="nombre")  
        self.generarGraficoPastel()

        self.winReporteEmpleados.uiReporteEmpleados.btnSearch.clicked.connect(lambda: self.cargarTablaReporteEmpleados())

    def cargarTablaReporteEmpleados(self):     
        empleado = Empleados()
        row = empleado.getCountEmpleadosByDepartment(self.winReporteEmpleados.uiReporteEmpleados.cmbBoxDepartamento.currentText())
        data = empleado.getEmpleadosByDepartment(self.winReporteEmpleados.uiReporteEmpleados.cmbBoxDepartamento.currentText())

        self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setRowCount(row)
        self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setColumnCount(4)
        i = 0
        for b in data:
            self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setItem(i, 0, QTableWidgetItem(b["fechaIngreso"]))
            self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setItem(i, 1, QTableWidgetItem(b["cedula"]))
            self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setItem(i, 2, QTableWidgetItem(b["nombre"]))
            isJefatura = "Supervisor" if b["isJefatura"] else "Empleado"
            self.winReporteEmpleados.uiReporteEmpleados.tblEmpleadosDepartamento.setItem(i, 3, QTableWidgetItem(isJefatura))
            i+=1

    def generarGraficoPastel(self):
        empleados = Empleados() 
        departamentos = {}
        total_empleados = 0

        # Obtener solo los departamentos con empleados
        departamentos_con_empleados = [departamento["nombre"] for departamento in Departamentos().getDepartamentos()
                                        if empleados.getCountEmpleadosByDepartment(departamento["nombre"]) > 0]

        for nombre_departamento in departamentos_con_empleados:
            count = empleados.getCountEmpleadosByDepartment(nombre_departamento)
            departamentos[nombre_departamento] = count
            total_empleados += count

        labels = [f"{nombre}\nEmpleados: {count}\nPorcentaje: {count / total_empleados * 100:.1f}%"
                    for nombre, count in departamentos.items()]

        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(departamentos.values(), labels=labels, startangle=140, textprops={'fontsize': 'smaller'}, radius=0.5)
        ax.axis('equal')  # Make the chart circular
        plt.subplots_adjust(top=0.8)
        ax.set_title('Empleados por departamento', pad=20)  # Add padding to the title

        # Create a FigureCanvas using the Matplotlib figure
        canvas = FigureCanvas(fig)
        # Create a layout for graphicFrame
        layout = QVBoxLayout(self.winReporteEmpleados.uiReporteEmpleados.graphicFrame)
        # Add the canvas to the layout of graphicFrame
        layout.addWidget(canvas)
        # Set the layout for graphicFrame
        self.winReporteEmpleados.uiReporteEmpleados.graphicFrame.setLayout(layout)

        # plt.show()

#Class Windows

class winLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)

class winUsuarios(QWidget):
    def __init__(self):
        super().__init__()
        self.uiUsuarios=Ui_Usuarios()
        self.uiUsuarios.setupUi(self)

class winEmpleados(QWidget):
    def __init__(self):
        super().__init__()
        self.uiEmpleados=Ui_Empleados()
        self.uiEmpleados.setupUi(self)       

class winDepartamentos(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDepartamentos=Ui_Departamentos()
        self.uiDepartamentos.setupUi(self)

class winBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiBienes=Ui_Bienes()
        self.uiBienes.setupUi(self)

class winAsignacionBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiAsignacion=Ui_Asignacion()
        self.uiAsignacion.setupUi(self)

class winDesligarBienes(QWidget):
    def __init__(self):
        super().__init__()
        self.uiDesligar=Ui_Desligar()
        self.uiDesligar.setupUi(self)

class winReporteBienesAsignados(QWidget):
    def __init__(self):
        super().__init__()
        self.uiReporteBienesAsignados=Ui_ReporteBienesAsignados()
        self.uiReporteBienesAsignados.setupUi(self)

class winReportBienesNoAsignables(QWidget):
    def __init__(self):
        super().__init__()
        self.uiReporteBienesNoAsignables=Ui_ReportBienesNoAsignables()
        self.uiReporteBienesNoAsignables.setupUi(self)

class winReporteEmpleados(QWidget):
    def __init__(self):
        super().__init__()
        self.uiReporteEmpleados=Ui_ReporteEmpleados()
        self.uiReporteEmpleados.setupUi(self)

class winReportes(QWidget):
    def __init__(self):
        super().__init__()

class winLoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiLoadingBox=Ui_LoadingDialog()
        self.uiLoadingBox.setupUi(self)

    def update_progress(self, progress):
        self.uiLoadingBox.progressBar.setValue(progress)

    def update_message(self, message):
        self.uiLoadingBox.messagelabel.setText(message)

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = Login()
    if win.exec_() == QDialog.Accepted:
        mdi = mdiApp()
        mdi.showMaximized()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
