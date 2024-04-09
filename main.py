import sys
import pymongo

# Widgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *   
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

#Model
from model.usuarios import Usuarios
from model.empleados import Empleados
from model.departamentos import Departamentos
from model.bienes import Bienes
from model.asignacion import AsignarBienes
from model.desligar import DesligarBienes
from model.reporteBienesAsignados import ReporteBienesAsignados
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

class Login(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiLogin=Ui_Login()
        self.uiLogin.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initComponents()

    def initComponents(self):
        self.uiLogin.btn_login.clicked.connect(self.validarAdmin)
        self.uiLogin.txt_username.setFocus()

    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()

    def login(self):
        mdi = mdiApp()
        mdi.show()
        self.close()

    def startLoading(self):
        # Mostrar la pantalla de carga
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

    def validarAdmin(self):
        username = self.uiLogin.txt_username.text()
        password = self.uiLogin.txt_password.text()

        if not username or not password:
            self.msgBox("Por favor, ingrese un nombre de usuario y una contraseña.", QMessageBox.Warning)
            return
        
        self.startLoading()
        #TODO: Hacer que la validación del usuario administrador se haga desde
            #model/usuarios y hacer una validación para usuarios no admin
        client = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        db = client["TresPatitos"]
        collection = db["admin"]
        user = collection.find_one({"username": username, "password": password})
        if user:
            self.loading_dialog.close()
            mdi = mdiApp()
            mdi.showMaximized()
            self.close()
            self.accept()
        else:
            self.loading_dialog.close()
            QMessageBox.warning(self, "Invalid credentials", QMessageBox.Warning)
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
        self.uiMdi.mniUsuarios.triggered.connect(self.openWinUsuarios)
        self.uiMdi.mniEmpleados.triggered.connect(self.openWinEmpleados)
        self.uiMdi.mniDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniRegistrarBienes.triggered.connect(self.openWinBienes)
        self.uiMdi.mnuAsignar.triggered.connect(self.openWinAsignacionBienes)
        self.uiMdi.mnuDesligar.triggered.connect(self.openWinDesligarBienes)
        self.uiMdi.submnuBienesAsignados.triggered.connect(self.openWinReporteBienesAsignados)

    def msgBox(self,mensaje,icono,tipo=0):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación del Sistema")
        retval=msg.exec_()

    def exitApp(self):
        self.hide()
        login_dialog = Login()
        login_dialog.accepted.connect(self.show)
        login_dialog.exec_()

    #Usuarios

    def openWinUsuarios(self):
        usuarios=Usuarios()
        self.winUsuarios=winUsuarios()
        self.uiMdi.mdiArea.addSubWindow(self.winUsuarios)

        txtusername = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        txtname = self.winUsuarios.uiUsuarios.txtName.text().title()
        txtpassword = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        txtconfirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()
        
        #Eventos
        self.winUsuarios.uiUsuarios.btnCrearUsuario.clicked.connect(self.guardarUsuario)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.clicked.connect(self.modificarUsuario)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.clicked.connect(self.eliminarUsuario)
        self.winUsuarios.uiUsuarios.btnLimpiar.clicked.connect(self.limpiarUsuarios)
        self.winUsuarios.uiUsuarios.isPassowordVisible.toggled.connect(self.btn_ShowPassword)

        if not txtusername or not txtname or not txtpassword or not txtconfirm_password or not is_admin:
            self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(False)
            self.btnEditSaveAreEnabled(False)
        else:
            self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(True)
            self.btnEditSaveAreEnabled(True)

        self.winUsuarios.uiUsuarios.tblUsuarios.clicked.connect(self.cargarDatosUsuarios)
        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.btnEditSaveAreEnabled(True)
        self.winUsuarios.show()

        #Focus order
        self.winUsuarios.uiUsuarios.txtUsername.setFocus()
        self.winUsuarios.uiUsuarios.txtUsername.returnPressed.connect(self.winUsuarios.uiUsuarios.txtName.setFocus)
        self.winUsuarios.uiUsuarios.txtName.returnPressed.connect(self.winUsuarios.uiUsuarios.txtPassword.setFocus)
        self.winUsuarios.uiUsuarios.txtPassword.returnPressed.connect(self.winUsuarios.uiUsuarios.txtConfirmPassword.setFocus)

    def guardarUsuario(self):
        self.loading_dialog = winLoadingDialog(self)
        self.loading_dialog.update_message("Guardando usuario...")
        self.loading_dialog.update_progress(0)
        self.loading_dialog.show()

        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()
        
        if not username or not name or not password or not confirm_password:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            self.loading_dialog.close()
            return

        self.loading_dialog.update_progress(20)

        if password != confirm_password:
            self.msgBox("Las contraseñas no coinciden", QMessageBox.Warning)
            self.loading_dialog.close()
            return
        
        self.loading_dialog.update_progress(50)

        user = Usuarios(username, name, password, is_admin)
        if user.guardar()==0:
            self.loading_dialog.update_progress(100)
            message="Nuevo usuario " + username + " creado con éxito!"
            self.loading_dialog.close()
            self.msgBox(message,QMessageBox.Information)

        elif user.guardar()==1:
            self.loading_dialog.close()
            self.msgBox("Error de registro, el usuario ya está registrado",QMessageBox.Information)
        else:
            self.loading_dialog.close()
            self.msgBox("Error al registrar nuevo usuario",QMessageBox.Information)

        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.limpiarUsuarios()
        self.btnEditSaveAreEnabled(False)

    def modificarUsuario(self):
        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().strip().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()

        if not username or not name or not password or not confirm_password:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return

        if password != confirm_password:
            self.msgBox("Las contraseñas no coinciden", QMessageBox.Warning)
            return
        
        user = Usuarios(username, name, password, is_admin)
        if user.actualizar()==1:
            message="Usuario " + username + " modificado correctamente"
            self.msgBox(message,QMessageBox.Information)
        else:
            message="Error al modificar usuario " + username
            self.msgBox(message, QMessageBox.Information)

        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.limpiarUsuarios()
        self.btnEditSaveAreEnabled(False)

    def eliminarUsuario(self):
        usuarios=Usuarios()
        username = self.winUsuarios.uiUsuarios.txtUsername.text().strip().upper()
        name = self.winUsuarios.uiUsuarios.txtName.text().strip().title()
        password = self.winUsuarios.uiUsuarios.txtPassword.text().strip()
        # confirm_password = self.winUsuarios.uiUsuarios.txtConfirmPassword.text().strip()
        is_admin = self.winUsuarios.uiUsuarios.chkBoxAdmin.isChecked()

        user = Usuarios(username, name, password, is_admin)
        if user.eliminar()==1:
            message="Usuario " + username + " ha sido eliminado correctamente!"
            self.msgBox(message,QMessageBox.Information)
        else:
            message="Error al eliminar usuario " + username
            self.msgBox(message, QMessageBox.Information)

        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.limpiarUsuarios()
        self.btnEditSaveAreEnabled(False)

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
        self.btnEditSaveAreEnabled(True)
        self.winUsuarios.uiUsuarios.btnLimpiar.setEnabled(True)
        numFilas = self.winUsuarios.uiUsuarios.tblUsuarios.currentRow()
        self.winUsuarios.uiUsuarios.txtUsername.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 0).text())
        self.winUsuarios.uiUsuarios.txtName.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 1).text())
        self.winUsuarios.uiUsuarios.txtPassword.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 2).text())
        self.winUsuarios.uiUsuarios.txtConfirmPassword.setText("")
        admin_value = self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas, 3).text()

        if admin_value.lower() in ['true', '1']: 
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
        self.btnEditSaveAreEnabled(False)

    def btnEditSaveAreEnabled(self, isAble):
        # self.winUsuarios.uiUsuarios.btnCrearUsuario.setEnabled(isAble)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.setEnabled(isAble)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.setEnabled(isAble)

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

    #Empleados

    def openWinEmpleados(self):
        creacionEmpleado=Empleados()
        self.winEmpleados=winEmpleados()
        self.uiMdi.mdiArea.addSubWindow(self.winEmpleados)
        
        #Eventos
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.clicked.connect(self.guardarEmpleado)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.clicked.connect(self.actualizarEmpleado)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.clicked.connect(self.eliminarEmpleado)
        self.winEmpleados.uiEmpleados.bttLimpiarEmpleado.clicked.connect(self.limpiarEmpleados)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.clicked.connect(self.cargarDatosEmpleados)
        self.cargarTablaEmpleados(creacionEmpleado.getRegistrosEmpleados(),creacionEmpleado.getEmpleados())
        self.habilitarGuardarEmpleados
        self.winEmpleados.show()

    def guardarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.toPlainText()
                                
        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso, direccion)

        if empleado.guardarEmpleados()==1:
            self.msgBox("Empleado creado correctamente",QMessageBox.Information)
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
        else:
            self.msgBox("Error al crear Empleado",QMessageBox.Information)

    def actualizarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.toPlainText()
                                
        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso, direccion)

        if empleado.actualizarEmpleados()==1:
            self.msgBox("Empleado actualizado correctamente",QMessageBox.Information)
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
        else:
            self.msgBox("Error al actualizar Empleado",QMessageBox.Information)

    def eliminarEmpleado(self):
        usuario=str(self.winEmpleados.uiEmpleados.cmbBoxUsuarios.currentText())
        departamento=str(self.winEmpleados.uiEmpleados.cmbBoxDepartamento.currentText())
        cedula=self.winEmpleados.uiEmpleados.txtCedula.text()
        nombre=self.winEmpleados.uiEmpleados.txtNombre.text()
        telefono=self.winEmpleados.uiEmpleados.txtTelefono.text()
        fechIngreso=self.winEmpleados.uiEmpleados.txtDate.text()
        direccion=self.winEmpleados.uiEmpleados.txtDireccion.toPlainText()
                                
        empleado=Empleados(usuario, departamento, cedula, nombre, telefono, fechIngreso, direccion)

        if empleado.eliminarEmpleados()==1:
            self.msgBox("Empleado eliminado correctamente",QMessageBox.Information)
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(empleado.getRegistrosEmpleados(),empleado.getEmpleados())
        else:
            self.msgBox("Error al eliminar Empleado",QMessageBox.Information)

    def cargarDatosEmpleados(self):

        self.habilitarEliminarModificarEmpleados()
        row=self.winEmpleados.uiEmpleados.tblWidgetEmpleados.currentRow()

        fecha_texto = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 0).text()
        fecha = QDateTime.fromString(fecha_texto, "yyyy-MM-dd")  # Convertir el texto de la fecha a QDateTime
        self.winEmpleados.uiEmpleados.txtDate.setDate(fecha.date())  # Establecer la fecha en el QDateEdit

        valor_usuario = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 1).text()
        index = self.winEmpleados.uiEmpleados.cmbBoxUsuarios.findText(valor_usuario)
        if index != -1:
            self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setCurrentIndex(index)

        self.winEmpleados.uiEmpleados.txtCedula.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,2).text())
        
        self.winEmpleados.uiEmpleados.txtNombre.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,3).text())

        valor_departamento = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 4).text()
        index = self.winEmpleados.uiEmpleados.cmbBoxDepartamento.findText(valor_departamento)
        if index != -1:
            self.winEmpleados.uiEmpleados.cmbBoxDepartamento.setCurrentIndex(index)

        self.winEmpleados.uiEmpleados.txtTelefono.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,5).text())

        self.winEmpleados.uiEmpleados.txtDireccion.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row,6).text())

        puesto = self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(row, 7).text()

        if puesto.lower() in ['true', '1']: 
            self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.setChecked(True)
        else:
            self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.setChecked(False)

    def limpiarEmpleados(self):

        self.winEmpleados.uiEmpleados.txtCedula.setText("")
        self.winEmpleados.uiEmpleados.txtNombre.setText("")
        self.winEmpleados.uiEmpleados.txtTelefono.setText("")
        self.winEmpleados.uiEmpleados.txtDireccion.setText("")
        self.winEmpleados.uiEmpleados.cmbBoxDepartamento.setCurrentIndex(0)
        self.winEmpleados.uiEmpleados.cmbBoxUsuarios.setCurrentIndex(0)
        self.winEmpleados.uiEmpleados.txtDate.setDate(QDateEdit.currentDate())
        self.winEmpleados.uiEmpleados.chckBoxIsSupervisor.isChecked(False)
        self.habilitarGuardarEmpleados()

    def habilitarGuardarEmpleados(self):
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.setEnabled(True)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.setEnabled(False)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.setEnabled(False)

    def habilitarEliminarModificarEmpleados(self):
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.setEnabled(False)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.setEnabled(True)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.setEnabled(True)

    def cargarTablaEmpleados(self,row,data):
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setRowCount(row)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setColumnCount(6)
        i=0
        for b in data:
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,0,QTableWidgetItem(b["fechaIngreso"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,1,QTableWidgetItem(b["_id"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,2,QTableWidgetItem(b["cedula"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,3,QTableWidgetItem(b["nombre"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,4,QTableWidgetItem(b["departamento"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,5,QTableWidgetItem(b["telefono"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,6,QTableWidgetItem(b["direccion"]))
            
            puesto = "Supervisor" if b["puesto"] else "Empleado"
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i, 7, QTableWidgetItem(puesto))
            i+=1

    #Departamentos
    
    def openWinDepartamentos(self):
        self.winDepartamentos=winDepartamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.refresh()
        self.winDepartamentos.show()
        
        #Eventos
        self.winDepartamentos.uiDepartamentos.btn_registrar.clicked.connect(self.registrarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_editar.clicked.connect(self.actualizarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_eliminar.clicked.connect(self.eliminarDepartamento)
        self.winDepartamentos.uiDepartamentos.btnNewCode.clicked.connect(self.generarNuevoCodigo)
        self.winDepartamentos.uiDepartamentos.btnLimpiar.clicked.connect(self.limpiarDepartamentos)
        self.winDepartamentos.uiDepartamentos.btnRefresh.clicked.connect(self.refresh)
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.clicked.connect(self.cargarDatosDepartamentos)

    def registrarDepartamento(self):
        departamento=Departamentos()
        codigo=self.winDepartamentos.uiDepartamentos.txt_codigo.text().strip().upper()
        nombre=self.winDepartamentos.uiDepartamentos.txt_nombre.text().strip().title()
        jefatura= str(self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentText())

        if not codigo or not nombre or not jefatura:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return
        
        if departamento.existeDepartamento():
            self.msgBox("Error al registrar departamento, no pueden existir dos departamentos con el mismo nombre",QMessageBox.Warning)
        else:
            departamento = Departamentos(codigo, nombre, jefatura)

        if departamento.registrar()==1:
            message="Departamento " + nombre + " registrado correctamente"
            self.msgBox(message,QMessageBox.Information)
        else:
            self.msgBox("Error al registrar departamento",QMessageBox.Warning)

        self.refresh()
        self.btnEditDeleteEnabled(False)

    def actualizarDepartamento(self):
        departamento=Departamentos()
        codigo=self.winDepartamentos.uiDepartamentos.txt_codigo.text().strip().upper()
        nombre=self.winDepartamentos.uiDepartamentos.txt_nombre.text().strip().title()
        jefatura=str(self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentText())

        if not codigo or not nombre or not jefatura:
            self.msgBox("Todos los campos deben ser completados", QMessageBox.Warning)
            return

        if departamento.existeDepartamento():
            self.msgBox("Error al actualizar departamento, no pueden existir dos departamentos con el mismo nombre",QMessageBox.Warning)
        else:
            departamento = Departamentos(codigo, nombre, jefatura)

        if departamento.actualizar()==1:
            self.msgBox("Departamento actualizado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al actualizar el departamento",QMessageBox.Warning)

        self.refresh()
        self.btnEditDeleteEnabled(False)

    def eliminarDepartamento(self):
        codigo=self.winDepartamentos.uiDepartamentos.txt_codigo.text().strip().upper()
        nombre=self.winDepartamentos.uiDepartamentos.txt_nombre.text().strip().title()
        jefatura=str(self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentText())

        departamento = Departamentos(codigo, nombre, jefatura)
        if departamento.eliminar()==1:
            message="Departamento "+ nombre + " eliminado con éxito!"
            self.msgBox(message,QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar departamento",QMessageBox.Warning)

        self.refresh()
        self.btnEditDeleteEnabled(False)

    def cargarTablaDepartamentos(self, numFilas, datos):
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setRowCount(numFilas)
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setColumnCount(3)
        i = 0
        for d in datos:
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 0, QTableWidgetItem(d["_id"]))
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 1, QTableWidgetItem(d["nombre"]))
            jefatura_texto = d["jefatura"]
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i, 2, QTableWidgetItem(jefatura_texto))
            i += 1

    def cargarDatosDepartamentos(self):
        self.winDepartamentos.uiDepartamentos.btn_registrar.setEnabled(False)
        numFilas = self.winDepartamentos.uiDepartamentos.tblDepartamentos.currentRow()

        self.winDepartamentos.uiDepartamentos.txt_codigo.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 0).text())
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 1).text())
        valor_jefatura = self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 2).text()
        index = self.winDepartamentos.uiDepartamentos.cmb_jefatura.findText(valor_jefatura)
        if index != -1:
            self.winDepartamentos.uiDepartamentos.cmb_jefatura.setCurrentIndex(index)

        self.btnEditDeleteEnabled(True)

    def comboBoxDepartamentos(self, datos):
        self.winDepartamentos.uiDepartamentos.cmb_jefatura.clear()
        self.winDepartamentos.uiDepartamentos.cmb_jefatura.addItem("Elegir")
        
        for d in datos:
            nombre = d["nombre"]
            apellido = d["apellidos"]
            if nombre and apellido:
                nombre_completo = f"{nombre} {apellido}"
                self.winDepartamentos.uiDepartamentos.cmb_jefatura.addItem(nombre_completo)

    def limpiarDepartamentos(self):
        self.winDepartamentos.uiDepartamentos.txt_codigo.setText("")
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText("")
        self.winDepartamentos.uiDepartamentos.cmb_jefatura.setCurrentIndex(0)

    def generarNuevoCodigo(self):
        self.winDepartamentos.uiDepartamentos.txt_codigo.setText("")
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText("")
        self.winDepartamentos.uiDepartamentos.btn_registrar.setEnabled(True)
        departamento = Departamentos()
        last_code = departamento.getLastCode()

        if last_code is not None:
            nuevo_numero = last_code + 1
        else:
            nuevo_numero = 1

        nuevo_codigo = f"DPT{nuevo_numero:03}"
        self.winDepartamentos.uiDepartamentos.txt_codigo.setText(nuevo_codigo)
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText("Departamento " + str(nuevo_numero))

    def btnEditDeleteEnabled(self, enabled):
        # self.winDepartamentos.uiDepartamentos.btn_registrar.setEnabled(enabled)
        self.winDepartamentos.uiDepartamentos.btn_editar.setEnabled(enabled)
        self.winDepartamentos.uiDepartamentos.btn_eliminar.setEnabled(enabled)
        self.winDepartamentos.uiDepartamentos.btnLimpiar.setEnabled(enabled)

    def refresh(self):
        departamento=Departamentos()
        self.limpiarDepartamentos()
        self.cargarTablaDepartamentos(departamento.getCountDepartamentos(),departamento.getDepartamentos())
        self.comboBoxDepartamentos(departamento.getJefaturas())
        self.winDepartamentos.uiDepartamentos.btn_registrar.setEnabled(True)

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
        self.winBienes.uiBienes.tblRegistro.clicked.connect(self.cargarDatosBienes)
        self.cargarTablaBienes(bien.getNumeroRegistros(),bien.getBienes())
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
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(), self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(), self.winBienes.uiBienes.txtDescripcion.text(),
                        self.winBienes.uiBienes.cbxEstado.currentText()
                        )
        if bien.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)

    def eliminarBienes(self):
        bien=Bienes(self.winBienes.uiBienes.txtPlaca.text(), self.winBienes.uiBienes.txtNombreBien.text(),
                        self.winBienes.uiBienes.txtCategoria.text(), self.winBienes.uiBienes.txtDescripcion.text(),
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

    #Asignacion Bienes

    def openWinAsignacionBienes(self):
        asignado=AsignarBienes()
        self.winAsignacion=winAsignacionBienes()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winAsignacion)
        #eventos
        self.comboBoxAsignarEmpeladosCedula(asignado.getEmpleados())
        self.comboBoxBienes(asignado.getBienes())
        self.winAsignacion.uiAsignacion.btnGuardar.clicked.connect(self.guardarBienAsignado)
        self.winAsignacion.uiAsignacion.btnModificar.clicked.connect(self.modificarBienAsignado)
        self.winAsignacion.uiAsignacion.btnEliminar.clicked.connect(self.eliminarBienAsignado)
        self.winAsignacion.uiAsignacion.tblAsignados.clicked.connect(self.cargarDatosAsignacion)
        self.cargarTablaBienesAsignado(asignado.getNumeroAsignados(),asignado.getAsignados())
        self.winAsignacion.show()

    def guardarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentText(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                    self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
                    self.winAsignacion.uiAsignacion.cbxBienes.currentText()
                    )
        if bienesAsignados.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)

    def modificarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentText(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.cbxBienes.currentText()
                        )
        if bienesAsignados.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)

    def eliminarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.currentText(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.cbxBienes.currentText()
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
            self.winAsignacion.uiAsignacion.tblAsignados.setItem(i,4,QTableWidgetItem(d["bien_asignado"]))
            i+=1
    
    def cargarDatosAsignacion(self):
        numFila=self.winAsignacion.uiAsignacion.tblAsignados.currentRow()
        self.winAsignacion.uiAsignacion.cbxCedulaEmpleados.setCurrentText(self.winAsignacion.uiAsignacion.tblAsignados.item(numFila,0).text())
        self.winAsignacion.uiAsignacion.txtNombre.setText(self.winAsignacion.uiAsignacion.tblAsignados.item(numFila,1).text())
        self.winAsignacion.uiAsignacion.txtApellidos.setText(self.winAsignacion.uiAsignacion.tblAsignados.item(numFila,2).text())
        self.winAsignacion.uiAsignacion.txtTelefono.setText(self.winAsignacion.uiAsignacion.tblAsignados.item(numFila,3).text())
        self.winAsignacion.uiAsignacion.cbxBienes.setCurrentText(self.winAsignacion.uiAsignacion.tblAsignados.item(numFila,4).text())

    def comboBoxAsignarEmpeladosCedula(self, datos):
        for d in datos:
            cedula=d["_id"]
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
        self.winDesligar.uiDesligar.btnDesligar.clicked.connect(self.modificarDesligar)
        self.cargarTablaDesligar(desligar.getNumeroDesligar(),desligar.getAsignados())
        self.winDesligar.uiDesligar.tblDesligar.clicked.connect(self.cargarDatosDesligar)
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
            self.winDesligar.uiDesligar.tblDesligar2.setItem(i,1,QTableWidgetItem(d["bien_asignado"]))
            i+=1
    def cargarMetodoTablaDesligar(self):
        desligar=DesligarBienes()
        self.tablaBienDesligar(desligar.getNumeroDesligar(), desligar.getAsignados())

    def tablaBienDesligar(self, numFilas, datos):

        self.winDesligar.uiDesligar.tblDesligar2.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winDesligar.uiDesligar.tblDesligar2.setColumnCount(2)

        nombreArchivo=self.winDesligar.uiDesligar.cbxEmpleados.currentText()
        i=0
        for d in datos:
            nombre=d["nombre"]
            #bien=["bien_asignado"]
            if nombre==nombreArchivo:
                self.winDesligar.uiDesligar.tblDesligar2.setItem(i,0,QTableWidgetItem(d["nombre"]))
                self.winDesligar.uiDesligar.tblDesligar2.setItem(i,1,QTableWidgetItem(d["bien_asignado"]))
                i+=1

    def espaciosDesligar(self):
        nombre=self.winDesligar.uiDesligar.cbxEmpleados.currentText()
        self.winDesligar.uiDesligar.txtNombre.setText(nombre)
        #self.winDesligar.uiDesligar.txtBienAsignado.setText()
    
    def modificarDesligar(self):
        desligar=DesligarBienes(self.winDesligar.uiDesligar.txtCedula.text(),
                        self.winDesligar.uiDesligar.txtNombre.text()
                        )
        if desligar.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)
    
    def eliminarDesligar(self):
        desligar=DesligarBienes(self.winDesligar.uiDesligar.txtCedula.text(),
                        self.winDesligar.uiDesligar.txtNombre.text()
                        )
        if desligar.eliminar()==1:
            self.msgBox("Bien desligado Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al desligar los datos",QMessageBox.Warning)

    def cargarTablaDesligar(self, numFilas, datos):
        #determinar el numero de filas de la tabla
        self.winDesligar.uiDesligar.tblDesligar.setRowCount(numFilas)
        #determinar el numero de columnas de la tabla
        self.winDesligar.uiDesligar.tblDesligar.setColumnCount(3)
        i=0
        for d in datos:
            print(d)
            self.winDesligar.uiDesligar.tblDesligar.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winDesligar.uiDesligar.tblDesligar.setItem(i,1,QTableWidgetItem(d["nombre"]))
            self.winDesligar.uiDesligar.tblDesligar.setItem(i,2,QTableWidgetItem(d["bien_asignado"]))
            i+=1
    
    def comboBoxBienesAsignado(self, datos):
        for d in datos:
            nombre=d["nombre"]
            if nombre:
                self.winDesligar.uiDesligar.cbxEmpleados.addItem(nombre)

    def cargarDatosDesligar(self):
        numFila=self.winDesligar.uiDesligar.tblDesligar.currentRow()
        #self.winDesligar.uiDesligar.cbxEmpleados.setCurrentText(self.winDesligar.uiDesligar.tblDesligar.item(numFila,0).text())
        self.winDesligar.uiDesligar.txtCedula.setText(self.winDesligar.uiDesligar.tblDesligar.item(numFila,0).text())
        self.winDesligar.uiDesligar.txtNombre.setText(self.winDesligar.uiDesligar.tblDesligar.item(numFila,1).text())
        self.winDesligar.uiDesligar.txtBienAsignado.setText(self.winDesligar.uiDesligar.tblDesligar.item(numFila,2).text())

    def openWinReporteBienesAsignados(self):
        reporteBienesAsignados=ReporteBienesAsignados()
        self.winReporteBienesAsig=winReporteBienesAsignados()
        #agregar ventana
        self.uiMdi.mdiArea.addSubWindow(self.winReporteBienesAsig)
        #eventos
    
        self.winReporteBienesAsig.show()
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

class winReporteBienesAsignados(QWidget):
    def __init__(self):
        super().__init__()
        self.uiReporteBienesAsignados=Ui_ReporteBienesAsignados()
        self.uiReporteBienesAsignados.setupUi(self)
        # TODO Manejo de eventos

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
    app=QApplication(sys.argv)
    win=Login()
    if win.exec_() == QDialog.Accepted:
        mdi=mdiApp()
        mdi.showMaximized()
    sys.exit(app.exec())