import sys
import pymongo

# Widgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

# Login
from src.Ui_001_login import Ui_Login

# MDI
from src.Ui_000_mdi import Ui_mdiWindow

# Usuarios
from src.Ui_002_usuarios import Ui_Usuarios
from model.usuarios import Usuarios

# Empleados
from src.Ui_003_empleados import Ui_Empleados
from model.empleados import Empleados

# Departamentos
from src.Ui_004_departamentos  import Ui_Departamentos
from model.departamentos import Departamentos

# Bienes
from model.bienes import Bienes
from src.Ui_005_bienes import Ui_Bienes
from src.Ui_051_asignacion_bienes import Ui_Asignacion
from model.asignacion import AsignarBienes
from src.Ui_052_desligar_bienes import Ui_Desligar
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
        self.uiLogin.btn_login.clicked.connect(self.validarAdmin)

    def login(self):
        mdi = mdiApp()
        mdi.show()
        self.close()

    def validarAdmin(self):
        username = self.uiLogin.txt_username.text()
        password = self.uiLogin.txt_password.text()

        # Conectarse a la base de datos
        client = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        db = client["TresPatitos"]
        collection = db["admin"]
        user = collection.find_one({"username": username, "password": password})
        if user:
            mdi = mdiApp()
            mdi.showMaximized()
            self.close()
            self.accept()
        else:
            # Si no se encuentra el usuario, mostrar un mensaje de advertencia
            QMessageBox.warning(self, "Invalid credentials", "Invalid username or password")

    # TODO hacer exit para la pagina de login
    def exitLogin(self):
        pass

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
        self.uiMdi.mniUsuarios.triggered.connect(self.openWinUsuarios)
        self.uiMdi.mniEmpleados.triggered.connect(self.openWinEmpleados)
        self.uiMdi.mniDepartamentos.triggered.connect(self.openWinDepartamentos)
        self.uiMdi.mniRegistrarBienes.triggered.connect(self.openWinBienes)
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
        usuarios=Usuarios()
        self.winUsuarios=winUsuarios()
        #agregar la ventana al mdi
        self.uiMdi.mdiArea.addSubWindow(self.winUsuarios)
        #eventos
        self.winUsuarios.uiUsuarios.btnCrearUsuario.clicked.connect(self.guardarUsuario)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.clicked.connect(self.modificarUsuario)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.clicked.connect(self.eliminarUsuario)
        self.winUsuarios.uiUsuarios.btnLimpiar.clicked.connect(self.limpiarUsuarios)
        self.winUsuarios.uiUsuarios.tblUsuarios.clicked.connect(self.cargarDatosUsuarios)
        self.cargarTablaUsuarios(usuarios.getRegistrosUsuarios(),usuarios.getUsuarios())
        self.habilitarGuardarUsuarios
        self.winUsuarios.show()

    def guardarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtUsername.text(),
                        self.winUsuarios.uiUsuarios.txtEmail.text()
                        )
        if usuarios.guardar()==1:
            self.msgBox("Usuario creado correctamente",QMessageBox.Information)
            self.cargarTablaUsuarios()
        else:
            self.msgBox("Error al crear usuario",QMessageBox.Information)

    def modificarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtUsername.text(),
                        self.winUsuarios.uiUsuarios.txtEmail.text()
                        )
        if usuarios.actualizar()==1:
            self.msgBox("Datos moidificados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al modificar datos",QMessageBox.Information)

    def eliminarUsuario(self):
        usuarios=Usuarios(self.winUsuarios.uiUsuarios.txtID.text(),self.winUsuarios.uiUsuarios.txtUsername.text(),
                        self.winUsuarios.uiUsuarios.txtEmail.text()
                        )
        if usuarios.eliminar()==1:
            self.msgBox("Datos eliminados correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al eliminar datos",QMessageBox.Information)

    def cargarTablaUsuarios(self,numFilas,datos):
        self.winUsuarios.uiUsuarios.tblUsuarios.setRowCount(numFilas)
        self.winUsuarios.uiUsuarios.tblUsuarios.setColumnCount(3)
        i=0
        for d in datos:
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i,1,QTableWidgetItem(d["Usuario"]))
            self.winUsuarios.uiUsuarios.tblUsuarios.setItem(i,2,QTableWidgetItem(d["email"]))
            i+=1

    def habilitarGuardarUsuarios(self):
        self.winUsuarios.uiUsuarios.btnCrearUsuario.setEnabled(True)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.setEnabled(False)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.setEnabled(False)

    def limpiarUsuarios(self):
        self.winUsuarios.uiUsuarios.txtID.setText("")
        self.winUsuarios.uiUsuarios.txtUsername.setText("")
        self.winUsuarios.uiUsuarios.txtEmail.setText("")
        self.habilitarGuardarUsuarios()
    
    def habilitarEliminarModificarusuario(self):
        self.winUsuarios.uiUsuarios.btnCrearUsuario.setEnabled(False)
        self.winUsuarios.uiUsuarios.btnModificarUsuario.setEnabled(True)
        self.winUsuarios.uiUsuarios.btnEliminarUsuario.setEnabled(True)

    def cargarDatosUsuarios(self):
        self.habilitarEliminarModificarusuario()
        numFilas=self.winUsuarios.uiUsuarios.tblUsuarios.currentRow()
        self.winUsuarios.uiUsuarios.txtID.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas,0).text())
        self.winUsuarios.uiUsuarios.txtUsername.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas,1).text())
        self.winUsuarios.uiUsuarios.txtEmail.setText(self.winUsuarios.uiUsuarios.tblUsuarios.item(numFilas,2).text())

    #Empleados
            
    def openWinEmpleados(self):
        creacionEmpleado=Empleados()
        self.winEmpleados=winEmpleados()
        #agregar ventana
        self.uiMdi.mdiArea.addSubWindow(self.winEmpleados)
        #eventos
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.clicked.connect(self.guardarEmpleado)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.clicked.connect(self.actualizarEmpleado)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.clicked.connect(self.eliminarEmpleado)
        self.winEmpleados.uiEmpleados.bttLimpiarEmpleado.clicked.connect(self.limpiarEmpleados)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.clicked.connect(self.cargarDatosEmpleados)
        self.cargarTablaEmpleados(creacionEmpleado.getRegistrosEmpleados(),creacionEmpleado.getEmpleados())
        self.habilitarGuardarEmpleados
        self.winEmpleados.show()
    
    def guardarEmpleado(self):
        creacionEmpleado=Empleados(self.winEmpleados.uiEmpleados.txtCedula.text(),self.winEmpleados.uiEmpleados.txtNombre.text(),
                                self.winEmpleados.uiEmpleados.txtApellidos.text(),self.winEmpleados.uiEmpleados.txtTelefono.text(),
                                self.winEmpleados.uiEmpleados.txtDireccion.text(),self.winEmpleados.uiEmpleados.txtPuesto.text(),
                                self.winEmpleados.uiEmpleados.txtIngreso.text(),self.winEmpleados.uiEmpleados.txtJefatura.text()
                                )
        if creacionEmpleado.guardarEmpleados()==1:
            self.msgBox("Empleado creado correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al crear Empleado",QMessageBox.Information)

    def actualizarEmpleado(self):
        creacionEmpleado=Empleados(self.winEmpleados.uiEmpleados.txtCedula.text(),self.winEmpleados.uiEmpleados.txtNombre.text(),
                                        self.winEmpleados.uiEmpleados.txtApellidos.text(),self.winEmpleados.uiEmpleados.txtTelefono.text(),
                                        self.winEmpleados.uiEmpleados.txtDireccion.text(),self.winEmpleados.uiEmpleados.txtPuesto.text(),
                                        self.winEmpleados.uiEmpleados.txtIngreso.text(),self.winEmpleados.uiEmpleados.txtJefatura.text()
                                        )
        if creacionEmpleado.actualizarEmpleados()==1:
            self.msgBox("Empleado actualizado correctamente",QMessageBox.Information)
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(creacionEmpleado.getRegistrosEmpleados(),creacionEmpleado.getEmpleados())
        else:
            self.msgBox("Error al actualizar Empleado",QMessageBox.Information)

    def eliminarEmpleado(self):
        creacionEmpleado=Empleados(self.winEmpleados.uiEmpleados.txtCedula.text(),self.winEmpleados.uiEmpleados.txtNombre.text(),
                                        self.winEmpleados.uiEmpleados.txtApellidos.text(),self.winEmpleados.uiEmpleados.txtTelefono.text(),
                                        self.winEmpleados.uiEmpleados.txtDireccion.text(),self.winEmpleados.uiEmpleados.txtPuesto.text(),
                                        self.winEmpleados.uiEmpleados.txtIngreso.text(),self.winEmpleados.uiEmpleados.txtJefatura.text()
                                        )
        if creacionEmpleado.eliminarEmpleados()==1:
            self.msgBox("Empleado eliminado correctamente",QMessageBox.Information)
            self.limpiarEmpleados()
            self.cargarTablaEmpleados(creacionEmpleado.getRegistrosEmpleados(),creacionEmpleado.getEmpleados())
        else:
            self.msgBox("Error al eliminar Empleado",QMessageBox.Information)

    def cargarDatosEmpleados(self):
        self.habilitarEliminarModificarEmpleados()
        numFilasE=self.winEmpleados.uiEmpleados.tblWidgetEmpleados.currentRow()
        self.winEmpleados.uiEmpleados.txtCedula.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,0).text())
        self.winEmpleados.uiEmpleados.txtNombre.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,1).text())
        self.winEmpleados.uiEmpleados.txtApellidos.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,2).text())
        self.winEmpleados.uiEmpleados.txtTelefono.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,3).text())
        self.winEmpleados.uiEmpleados.txtDireccion.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,4).text())
        self.winEmpleados.uiEmpleados.txtPuesto.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,5).text())
        self.winEmpleados.uiEmpleados.txtIngreso.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,6).text())
        self.winEmpleados.uiEmpleados.txtJefatura.setText(self.winEmpleados.uiEmpleados.tblWidgetEmpleados.item(numFilasE,7).text())

    def limpiarEmpleados(self):
        self.winEmpleados.uiEmpleados.txtCedula.setText("")
        self.winEmpleados.uiEmpleados.txtNombre.setText("")
        self.winEmpleados.uiEmpleados.txtApellidos.setText("")
        self.winEmpleados.uiEmpleados.txtTelefono.setText("")
        self.winEmpleados.uiEmpleados.txtDireccion.setText("")
        self.winEmpleados.uiEmpleados.txtPuesto.setText("")
        self.winEmpleados.uiEmpleados.txtIngreso.setText("")
        self.winEmpleados.uiEmpleados.txtJefatura.setText("")
        self.habilitarGuardarEmpleados()

    def habilitarGuardarEmpleados(self):
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.setEnabled(True)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.setEnabled(False)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.setEnabled(False)
    
    def habilitarEliminarModificarEmpleados(self):
        self.winEmpleados.uiEmpleados.bttCrearEmpleado.setEnabled(False)
        self.winEmpleados.uiEmpleados.bttModificarEmpleado.setEnabled(True)
        self.winEmpleados.uiEmpleados.bttEliminarEmpleado.setEnabled(True)

    def cargarTablaEmpleados(self,numFilasE,datosE):
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setRowCount(numFilasE)
        self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setColumnCount(8)
        i=0
        for b in datosE:
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,0,QTableWidgetItem(b["_id"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,1,QTableWidgetItem(b["Nombre"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,2,QTableWidgetItem(b["Apellidos"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,3,QTableWidgetItem(b["Telefono"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,4,QTableWidgetItem(b["Direccion"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,5,QTableWidgetItem(b["Puesto"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,6,QTableWidgetItem(b["Ingreso"]))
            self.winEmpleados.uiEmpleados.tblWidgetEmpleados.setItem(i,7,QTableWidgetItem(b["Jefatura"]))
            i+=1
            
    #Departamentos
            
    def openWinDepartamentos(self):
        departamentos=Departamentos()
        self.winDepartamentos=winDepartamentos()
        self.uiMdi.mdiArea.addSubWindow(self.winDepartamentos)
        self.winDepartamentos.show()
        
        self.cargarTblDepartamentos(departamentos.getRegistroDepartamentos(),departamentos.getDepartamentos())
        self.winDepartamentos.uiDepartamentos.btn_registrar.clicked.connect(self.registrarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_editar.clicked.connect(self.actualizarDepartamento)
        self.winDepartamentos.uiDepartamentos.btn_eliminar.clicked.connect(self.eliminarDepartamento)
        
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.clicked.connect(self.cargarDatostblDepartamentos)
        

    def registrarDepartamento(self):
        departamento=Departamentos(self.winDepartamentos.uiDepartamentos.txt_codigo.text(), self.winDepartamentos.uiDepartamentos.txt_nombre.text(),
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
        departamento=Departamentos(self.winDepartamentos.uiDepartamentos.txt_codigo.text(), self.winDepartamentos.uiDepartamentos.txt_nombre.text(),
                self.winDepartamentos.uiDepartamentos.cmb_jefatura.currentIndex(),
                )
        if departamento.eliminar()==1:
            self.msgBox("Departamento eliminado",QMessageBox.Information)
            self.cargarTblDepartamentos
        else:
            self.msgBox("Error al eliminar departamento",QMessageBox.Warning)

    def cargarTblDepartamentos(self, numFilas, datos):
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setRowCount(numFilas)
        self.winDepartamentos.uiDepartamentos.tblDepartamentos.setColumnCount(3)
        i=0
        for d in datos:
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i,0,QTableWidgetItem(d["_id"]))
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i,1,QTableWidgetItem(d["nombre"]))
            self.winDepartamentos.uiDepartamentos.tblDepartamentos.setItem(i,2,QTableWidgetItem(d["jefatura"]))
            i+=1
    
    def cargarDatostblDepartamentos(self):
        numFilas = self.winDepartamentos.uiDepartamentos.tblDepartamentos.currentRow()
        self.winDepartamentos.uiDepartamentos.txt_codigo.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 0).text())
        self.winDepartamentos.uiDepartamentos.txt_nombre.setText(self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 1).text())
        valor_jefatura = self.winDepartamentos.uiDepartamentos.tblDepartamentos.item(numFilas, 2).text()
        index = self.winDepartamentos.uiDepartamentos.cmb_jefatura.findText(valor_jefatura)
        if index != -1:
            self.winDepartamentos.uiDepartamentos.cmb_jefatura.setCurrentIndex(index)

        
    def comboBoxDepartamentos(self, datos):
        # Limpiar el combo box antes de agregar nuevos elementos
        self.winDepartamentos.uiDepartamentos.cmb_jefatura.clear()
        
        for d in datos:
            nombre = d["nombre"]
            if nombre:
                self.winDepartamentos.uiDepartamentos.cmb_jefatura.addItem(nombre)

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
        self.cargarTablaBienesAsignado(asignado.getNumeroAsignados(),asignado.getAsignados())
        self.winAsignacion.show()
            
    def guardarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                    self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
                    self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                    )
        if bienesAsignados.guardar()==1:
            self.msgBox("Datos Guardados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Guardar los datos",QMessageBox.Warning)

    def modificarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
                        self.winAsignacion.uiAsignacion.txtBienAsignado.text()
                        )
        if bienesAsignados.actualizar()==1:
            self.msgBox("Datos Modificados Correctamente",QMessageBox.Information)
        else:
            self.msgBox("Error al Modificar los datos",QMessageBox.Warning)

    def eliminarBienAsignado(self):
        bienesAsignados=AsignarBienes(self.winAsignacion.uiAsignacion.txtCedula.text(), self.winAsignacion.uiAsignacion.txtNombre.text(),
                        self.winAsignacion.uiAsignacion.txtApellidos.text(), self.winAsignacion.uiAsignacion.txtTelefono.text(),
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

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=Login()
    if win.exec_() == QDialog.Accepted:
        mdi=mdiApp()
        mdi.showMaximized()
    sys.exit(app.exec())
