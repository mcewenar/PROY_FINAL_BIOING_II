from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDialog,QDialog ,QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import  QPixmap
from PyQt5.uic import loadUi

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import cv2
import numpy as np
 
########################################MENÚ PRINCIPAL##############################################
regex = QRegExp("[a-z A-Z]+")
validator = QRegExpValidator(regex) #The QRegExpValidator class is used to check a 
#string against a regular expression.

class VentanaPrincipal(QMainWindow):
    def __init__(self,ppal=None):
        super(VentanaPrincipal,self).__init__(ppal)
        loadUi('menu_principal.ui',self)
        self.setup()
    
    def setup(self): 
        self.BotonIngresoPac.clicked.connect(self.AbrirIngresoPac)
        self.BotonIngresoDon.clicked.connect(self.AbrirIngresoDon)
        self.BotonConteoCelular.clicked.connect(self.AbrirConteoCelular)
        self.BotonGraficos.clicked.connect(self.AbrirVentanaDatosGraficos)
        self.BotonSalir.clicked.connect(self.Salir)
        
    def asignarControlador(self,c):
        self.__mi_controlador = c
    
    def AbrirIngresoPac(self):
        ventanaingreso = VentanaPaciente(self)
        ventanaingreso.asignarControlador(self.__mi_controlador)
        ventanaingreso.show()
        self.hide()    
    
    def AbrirIngresoDon(self):
        ventanaingreso = VentanaDonante(self)
        ventanaingreso.asignarControlador(self.__mi_controlador)
        ventanaingreso.show()
        self.hide() 
    
    def AbrirConteoCelular(self):
        ventanaingreso = VentanaConteoCelular(self)
        ventanaingreso.asignarControlador(self.__mi_controlador)
        ventanaingreso.show()
        self.hide() 
    
    def AbrirVentanaDatosGraficos(self):
        ventanaingreso = VentanaDatosEstadisticos(self)
        ventanaingreso.asignarControlador(self.__mi_controlador)
        ventanaingreso.show()
        self.hide() 

    def Salir(self):
        self.hide()
        
############################OPCIÓN 1 MENÚ PRINCIPAL (INGRESAR UN DONANTE DE SANGRE) #######################################################
class VentanaDonante(QDialog):
    def __init__(self,ppal=None):
        super(VentanaDonante,self).__init__(ppal)
        loadUi('menu_donante.ui',self)        
        self.setup()

    def setup(self):
        self.BotonNuevoDon.clicked.connect(self.abrirNuevoDon)
        self.BotonVerDon.clicked.connect(self.verDonante)
        self.BotonEditarDon.clicked.connect(self.editarDonante)
        self.BotonEliminarDon.clicked.connect(self.eliminarDonante)
        self.BotonVolver.clicked.connect(self.volver)
    def asignarControlador(self,c):
        self.__mi_controlador = c       
    
    def abrirNuevoDon(self):
        VentanaNuevoDon = AbrirNuevoDonante(self)
        VentanaNuevoDon.asignarControlador(self.__mi_controlador)
        VentanaNuevoDon.show()        
        self.hide()

    def verDonante(self):
        ventanaVerDonante = VerificacionVerDonante(self)
        ventanaVerDonante.asignarControlador(self.__mi_controlador)
        ventanaVerDonante.show()
        
        self.hide()

    def editarDonante(self):
        editarDonante = VerificarEditarDonante(self)
        editarDonante.asignarControlador(self.__mi_controlador)
        editarDonante.show()        
        self.hide()
    
    def eliminarDonante(self):
        eliminarDonante = EliminarDonante(self)
        eliminarDonante.asignarControlador(self.__mi_controlador)
        eliminarDonante.show()        
        self.hide()
    
    def volver(self):
        ventanaGeneral = VentanaPrincipal(self)
        ventanaGeneral.asignarControlador(self.__mi_controlador)
        ventanaGeneral.show()      
        self.hide()
    

class AbrirNuevoDonante(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('ingreso_donante.ui',self)
        self.setup()

        self.__HTLV = False
        self.__HepatitisB = False
        self.__HepatitisC= False
        self.__Sida= False
        self.__OtrasEnfermedades= False
        self.__TextOtrasEnfermedades = "N/A"
        self.__Chagas= False
        self.__Anemia = False
        self.__Sifilis = False

    def setup(self):
        self.Boton_Confirmar.clicked.connect(self.ConfirmarIngreso)
        self.Boton_Volver.clicked.connect(self.Volver)
        self.lineEdit_Nombres.setValidator(validator)
        self.lineEdit_Apellidos.setValidator(validator)
        self.lineEdit_Cedula.setValidator(QIntValidator())
        self.lineEdit_Tel.setValidator(QIntValidator())
        self.lineEdit_Edad.setValidator(QIntValidator(1,150))
        self.lineEdit_Correo.text()
        self.lineEdit_Peso.setValidator(QIntValidator(1,1000))
        self.lineEdit_Ciudad.setValidator(validator)
        self.lineEdit_Otras_Enf.setValidator(validator)        
        self.lineEdit_HierroS.setValidator(QIntValidator())
        self.lineEdit_Hemoglob.setValidator(QIntValidator())        
        #genero
        self.radioButton_Masculino.toggled.connect(self.GuardarGenero)
        self.radioButton_Femenino.toggled.connect(self.GuardarGenero)        
        #Sangre
        self.radioButton_APos.toggled.connect(self.GuardarSangre)
        self.radioButton_ANeg.toggled.connect(self.GuardarSangre)
        self.radioButton_BPos.toggled.connect(self.GuardarSangre)
        self.radioButton_BNeg.toggled.connect(self.GuardarSangre)
        self.radioButton_ABPos.toggled.connect(self.GuardarSangre)
        self.radioButton_ABNeg.toggled.connect(self.GuardarSangre)
        self.radioButton_OPos.toggled.connect(self.GuardarSangre)
        self.radioButton_ONeg.toggled.connect(self.GuardarSangre)               
        #Enfermedades
        self.radioButton_Hepat_B.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_Hepat_C.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_SIDA.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_Sifilis.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_HTLV.toggled.connect(self.GuardarEnfermedad)       
        self.radioButton_Chagas.toggled.connect(self.GuardarEnfermedad)       
        self.radioButton_Otras_Enf.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_Anemia.toggled.connect(self.GuardarEnfermedad)    
    
    def GuardarEnfermedad(self):
        if self.radioButton_Hepat_C.isChecked():
            self.__HepatitisC = True         

        if self.radioButton_HTLV.isChecked():
            self.__HTLV = True
            
        if self.radioButton_Hepat_B.isChecked():
            self.__HepatitisB = True           
        
        if self.radioButton_SIDA.isChecked():
            self.__Sida = True
            
        if self.radioButton_Sifilis.isChecked():
            self.__Sifilis = True            
        
        if self.radioButton_Chagas.isChecked():
            self.__Chagas = True

        if self.radioButton_Otras_Enf.isChecked():
            self.__OtrasEnfermedades = True    
            self.__TextOtrasEnfermedades = self.lineEdit_Otras_Enf.text()                   
            
        if self.radioButton_Anemia.isChecked():
            self.__Anemia = True

        
    def GuardarSangre(self):  
        if self.radioButton_APos.isChecked():
            self.__tipoSangre = "A+"
            return self.__tipoSangre
        if self.radioButton_ANeg.isChecked():
            self.__tipoSangre = "A-"
            return self.__tipoSangre
        if self.radioButton_BPos.isChecked():
            self.__tipoSangre = "B+"
            return self.__tipoSangre
        if self.radioButton_BNeg.isChecked():
            self.__tipoSangre = "B-"
            return self.__tipoSangre
        if self.radioButton_ABPos.isChecked():
            self.__tipoSangre = "AB+"
            return self.__tipoSangre
        if self.radioButton_ABNeg.isChecked():
            self.__tipoSangre = "AB-"
            return self.__tipoSangre
        if self.radioButton_OPos.isChecked():
            self.__tipoSangre = "O+"
            return self.__tipoSangre
        if self.radioButton_ONeg.isChecked():
            self.__tipoSangre = "O-"
            return self.__tipoSangre
    
    def GuardarGenero(self):
        if self.radioButton_Masculino.isChecked():
            self.__genero = "Masculino"
            return self.__genero
        if self.radioButton_Femenino.isChecked():
            self.__genero = "Femenino"
            return self.__genero
    
    
    def ConfirmarIngreso(self):
        Hemoglobina = ""
        try:
            Hemoglobina = float(self.lineEdit_Hemoglob.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo de ingreso de Hemoglobina Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        hierroS = ""
        try:
            hierroS = float(self.lineEdit_HierroS.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo de ingreso de Hierro Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        nueva_ident =""
        try:
            nueva_ident = int(self.lineEdit_Cedula.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Identificación de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        tel_don=""
        try:
            
            tel_don = int(self.lineEdit_Tel.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Teléfono de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        edad_don = ""
        try:
            edad_don = int(self.lineEdit_Edad.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Edad de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        peso_don= ""
        try:
            peso_don = int(self.lineEdit_Peso.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Peso de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        self.__TextOtrasEnfermedades   = self.lineEdit_Otras_Enf.text()    
        nom_don=self.lineEdit_Nombres.text()
        apellido_don=self.lineEdit_Apellidos.text()
        correo=self.lineEdit_Correo.text()
        ciudad=self.lineEdit_Ciudad.text()
               
        
        verif_nombre=nom_don.strip()
        verif_apellido=apellido_don.strip()
        verif_correo=correo.strip()
        verif_ciudad=ciudad.strip()        
        verif_gen_mas=self.GuardarGenero()
        verif_tipo=self.GuardarSangre()
    
        msgBox = QMessageBox(self)
        if verif_nombre=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('Debe ingresar campo Nombre de Donante')
            msgBox.show()
        elif verif_gen_mas == None:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('Debe oprimir género de donante')
            msgBox.show()
        
        elif verif_tipo == None:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('Debe oprimir tipo de sangre de donante')
            msgBox.show()
        elif verif_apellido=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('Debe ingresar campo Apellido de Donante')
            msgBox.show()
        elif verif_ciudad=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setWindowTitle("Debe ingresar campo Ciudad de Donante")
            msgBox.show()
        elif nueva_ident <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Cédula de Donante no puede estar vacío ni ser letra')
            msgBox.show()
        elif tel_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Teléfono de Donante no puede estar vacío ni ser cero')
            msgBox.show()
        elif edad_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta")
            msgBox.setText('El campo edad de donante no puede estar vacío')
            msgBox.show()
        elif peso_don <= 0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCION")
            msgBox.setText('Debe seleccionar un Peso')
            msgBox.show()
        elif verif_correo=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta")
            msgBox.setText('Llenar correo de Donante')
            msgBox.show()
        elif Hemoglobina <= 0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCION")
            msgBox.setText('Debe llenar completo el campo Hemoglobina de Donante')
            msgBox.show()
        elif hierroS <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCION")
            msgBox.setText('Debe llenar completo el campo Hierro de Donante')
            msgBox.show()
            
        else:
            sangre=self.GuardarSangre()            
            genero=self.GuardarGenero()
            htlv=self.__HTLV
            hepaB=self.__HepatitisB 
            hepaC=self.__HepatitisC
            sida=self.__Sida
            otrasEnf=self.__OtrasEnfermedades
            TextoOtrasEnf = self.__TextOtrasEnfermedades            
            chagas=self.__Chagas
            anemia=self.__Anemia
            sifilis = self.__Sifilis

            ingreso_donante=self.__mi_controlador.recibirDonante(nom_don,apellido_don,nueva_ident,tel_don,edad_don,peso_don,sangre,genero,ciudad,correo,Hemoglobina,hierroS,anemia,hepaC,hepaB,sida,htlv,otrasEnf,chagas,sifilis,TextoOtrasEnf)
            if ingreso_donante==True:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText('Donante ingresado con éxito')     
                msgBox.show()
                                        
            else:
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('El donante con identificación '+str(nueva_ident)+' ya existe.\n\n           Inténtalo de nuevo.')
                msgBox.show()                

            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)            
            ventanaMenDon.show()
            self.hide()            

    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()
    
    def asignarControlador(self,c):
        self.__mi_controlador = c
class VerificacionVerDonante(QDialog):
    def __init__(self,ppal=None):
        super(VerificacionVerDonante,self).__init__(ppal)
        loadUi('verificacionCC_VerDon.ui',self)
        self.__ventana_principal=ppal
        self.setup()
    def setup(self):
        self.BotonOkCancel.accepted.connect(self.confirmarVerDonante)
        self.BotonOkCancel.rejected.connect(self.Volver)        

    def asignarControlador(self,c):
        self.__mi_controlador = c
        
    def confirmarVerDonante(self):
        
        cedula = int(self.InputCedula.text())
        verificacion = self.__mi_controlador.verificarIdDon(cedula)
        if verificacion == True:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Ver Donante')
            mensaje=("INFORMACIÓN DE DONANTE con identificación "+str(cedula))
            msgBox.setText(mensaje)
            msgBox.show()
            
            VerDon = VentanaVerDonante(self)
            VerDon.asignarControlador(self.__mi_controlador)
            VerDon.Tabular_Información(cedula)
            VerDon.show()
            self.hide() 
                            
        elif verificacion == False:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Ver Donante')
            msgBox.setText('El donante con identificación '+str(cedula)+' no existe.\n\n           Inténtelo de nuevo.')
            msgBox.show()
            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)
            ventanaMenDon.show()
            self.hide()
    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()        
class VentanaVerDonante(QDialog):
    def __init__(self,ppal=None):
        super(VentanaVerDonante,self).__init__(ppal)
        loadUi('ver_info_donante.ui',self)
        self.__ventana_principal=ppal
        self.setup()        
        
    def setup(self):
        self.Boton_Volver.clicked.connect(self.Volver)

    def asignarControlador(self,c):
        self.__mi_controlador = c    

    def Tabular_Información(self,cc): #llamamos el donante correspondiente
        Donante = self.__mi_controlador.RegresarDonante(cc)
        if Donante == False:
            
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(" ATENCIÓN")
            msgBox.setText('La cédula ingresada NO se encuentra registrada.')
            msgBox.show()
        
        else : 

            #llamamos toda la informacion del donante
            Nom = Donante.verNombre()
            Ape = Donante.verApellido()
            Ident = Donante.verIdent()
            Tel = Donante.verTel()
            Edad = Donante.verEdad()
            Gen = Donante.verGenero()
            Correo =Donante.verCorreo()
            Ciud = Donante.verCiudad()
            TipoSang = Donante.verTipoSangre()
            Peso = Donante.verPeso()
            
            Examenes = Donante.verExamenes()

            HierroS = Examenes.verHierro()
            Anemia = Examenes.verAnemia()
            Hemoglo = Examenes.verHemoglobina()
            Sifilis = Examenes.verValorSifilis()
            HepatB = Examenes.verValorHepatitisB()
            HepatC = Examenes.verValorHepatitisC()
            SIDA = Examenes.verValorSIDA()
            Chagas = Examenes.verValorChagas()
            HTLV = Examenes.verValorHTLV()
            OtrasEnf =  Examenes.verOtrasEnfer()
            TextoOtrasEnf = Examenes.verTextoOtrasEnfer()
            TotalOtrasEnf = (str(OtrasEnf) + " : " +str(TextoOtrasEnf))

            celdaNomb = QTableWidgetItem(str(Nom))
            celdaApe = QTableWidgetItem(str(Ape))
            celdaIdent = QTableWidgetItem(str(Ident))
            celdaTel = QTableWidgetItem(str(Tel))
            celdaEdad = QTableWidgetItem(str(Edad))
            celdaGen = QTableWidgetItem(str(Gen))
            celdaCorreo = QTableWidgetItem(str(Correo))
            celdaCiud = QTableWidgetItem(str(Ciud))
            celdaTipoSang = QTableWidgetItem(str(TipoSang))
            celdaPeso = QTableWidgetItem(str(Peso))
            
            celdaHierroS = QTableWidgetItem(str(HierroS))
            celdaAnemia = QTableWidgetItem(str(Anemia))
            celdaHemoglo = QTableWidgetItem(str(Hemoglo))
            celdaSifilis = QTableWidgetItem(str(Sifilis))
            celdaHepatB = QTableWidgetItem(str(HepatB))
            celdaHepatC = QTableWidgetItem(str(HepatC))
            celdaSIDA = QTableWidgetItem(str(SIDA))
            celdaChagas = QTableWidgetItem(str(Chagas))
            celdaHTLV = QTableWidgetItem(str(HTLV))
            celdaOtrasEnf = QTableWidgetItem(str(TotalOtrasEnf))

            self.Tabla_DatosDon.setItem(-1,1,celdaNomb)
            self.Tabla_DatosDon.setItem(0,1,celdaApe) 
            self.Tabla_DatosDon.setItem(1,1,celdaGen) 
            self.Tabla_DatosDon.setItem(2,1,celdaIdent) 
            self.Tabla_DatosDon.setItem(3,1,celdaTel) 
            self.Tabla_DatosDon.setItem(4,1,celdaPeso) 
            self.Tabla_DatosDon.setItem(5,1,celdaTipoSang) 
            self.Tabla_DatosDon.setItem(6,1,celdaEdad) 
            self.Tabla_DatosDon.setItem(7,1,celdaCorreo) 
            self.Tabla_DatosDon.setItem(8,1,celdaCiud) 

            self.Tabla_DatosDon2.setItem(-1,1,celdaHierroS)
            self.Tabla_DatosDon2.setItem(0,1,celdaAnemia) 
            self.Tabla_DatosDon2.setItem(1,1,celdaHemoglo) 
            self.Tabla_DatosDon2.setItem(2,1,celdaHepatB) 
            self.Tabla_DatosDon2.setItem(3,1,celdaHepatC) 
            self.Tabla_DatosDon2.setItem(4,1,celdaSIDA) 
            self.Tabla_DatosDon2.setItem(5,1,celdaSifilis) 
            self.Tabla_DatosDon2.setItem(6,1,celdaHTLV) 
            self.Tabla_DatosDon2.setItem(7,1,celdaChagas) 
            self.Tabla_DatosDon2.setItem(8,1,celdaOtrasEnf)  
        
    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()

class VerificarEditarDonante(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('verificacionCC_ActualizarDon.ui',self)
        self.__ventana_principal=ppal
        self.setup()
        
    def setup(self):        
        self.BotonOkCancel.accepted.connect(self.ConfirmarActualizarDon)
        self.BotonOkCancel.rejected.connect(self.Volver)
    def asignarControlador(self,c):
        self.__mi_controlador = c
    def ConfirmarActualizarDon(self):
        
        ident = int(self.InputCedula.text())
        verificar=self.__mi_controlador.verificarIdDon(ident)
        if verificar==True:
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('Editar Donante')
                mensaje=("Donante con identificación "+str(ident))
                msgBox.setText(mensaje)
                msgBox.show()                
                ActualDon = EditarDonante(self)
                ActualDon.AsignarCedula_Verificacion(ident)
                ActualDon.asignarControlador(self.__mi_controlador)
                ActualDon.show()
                self.hide()
                
        else:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Editar Donante')
            msgBox.setText('El donante con identificación '+str(ident)+' no existe.\n\n           Inténtelo de nuevo.')
            msgBox.show()
            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)
            ventanaMenDon.show()
            self.hide()             

    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()

class EditarDonante(QDialog):
    def __init__(self,ppal=None):
        super(EditarDonante,self).__init__(ppal) #Hereda la clase VerificarEdiciónPaciente para tomar el Ident
        loadUi('editar_donante2.ui',self)
        self.__ventana_principal=ppal
        self.setup()
        self.__HTLV = False
        self.__HepatitisB = False
        self.__HepatitisC= False
        self.__Sida= False
        self.__OtrasEnfermedades= False
        self.__TextOtrasEnfermedades = "N/A"
        self.__Chagas= False
        self.__Anemia = False
        self.__Sifilis = False

        self.__Cedula_verificación = 0
    def setup(self):
        self.Boton_Confirmar.clicked.connect(self.ConfirmarIngreso)
        self.Boton_Volver.clicked.connect(self.Volver)
        self.lineEdit_nombre.setValidator(validator)
        self.cedulaDonante.setValidator(QIntValidator())
        self.lineEdit_apellido.setValidator(validator)
        self.lineEdit_edad.setValidator(QIntValidator(1,150))
        self.lineEdit_ciudad.setValidator(validator)
        self.lineEdit_telefono.setValidator(QIntValidator())
        self.lineEdit_correo.text()
        self.lineEdit_peso.setValidator(QIntValidator(1,1000))
        self.lineEdit_OtraEnfer.setValidator(validator)        
        self.lineEdit_Hierro.setValidator(QIntValidator())
        self.lineEdit_hemoGlo.setValidator(QIntValidator())        
        #genero
        self.radiomascu.toggled.connect(self.GuardarGenero)
        self.radiofeme.toggled.connect(self.GuardarGenero)        
        #Sangre
        self.radioButtonAPOS.toggled.connect(self.GuardarSangre)
        self.radioButtonANEG.toggled.connect(self.GuardarSangre)
        self.radioButtonBPOS.toggled.connect(self.GuardarSangre)
        self.radioButtonBNEG.toggled.connect(self.GuardarSangre)
        self.radioButtonABPOS.toggled.connect(self.GuardarSangre)
        self.radioButtonABNEG.toggled.connect(self.GuardarSangre)
        self.radioButtonOPOS.toggled.connect(self.GuardarSangre)
        self.radioButtonONEG.toggled.connect(self.GuardarSangre)
        #Enfermedades
        self.radioButton_Hepat_B.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_Hepat_C.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_SIDA.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_Sifilis.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_HTLV.toggled.connect(self.GuardarEnfermedad)       
        self.radioButton_Chagas.toggled.connect(self.GuardarEnfermedad)       
        self.radioButton_Otras_Enf.toggled.connect(self.GuardarEnfermedad)
        self.radioButton_anemia.toggled.connect(self.GuardarEnfermedad)
        
    
    def AsignarCedula_Verificacion(self,id):
        self.__Cedula_verificación = id
       
    def GuardarSangre(self):  #En esta opción se guardará cual de las opciones presionó el usuario y se retornara la respectiva
        if self.radioButtonAPOS.isChecked():
            self.__tipoSangre = "A+"
            return self.__tipoSangre
        elif self.radioButtonANEG.isChecked():
            self.__tipoSangre = "A-"
            return self.__tipoSangre
        elif self.radioButtonBPOS.isChecked():
            self.__tipoSangre = "B+"
            return self.__tipoSangre
        elif self.radioButtonBNEG.isChecked():
            self.__tipoSangre = "B-"
            return self.__tipoSangre
        elif self.radioButtonABPOS.isChecked():
            self.__tipoSangre = "AB+"
            return self.__tipoSangre
        elif self.radioButtonABNEG.isChecked():
            self.__tipoSangre = "AB-"
            return self.__tipoSangre
        elif self.radioButtonOPOS.isChecked():
            self.__tipoSangre = "O+"
            return self.__tipoSangre
        elif self.radioButtonONEG.isChecked():
            self.__tipoSangre = "O-"
            return self.__tipoSangre

    def GuardarEnfermedad(self):
        if self.radioButton_Hepat_C.isChecked():
            self.__HepatitisC = True            
            
        if self.radioButton_HTLV.isChecked():
            self.__HTLV = True
            
        if self.radioButton_Hepat_B.isChecked():
            self.__HepatitisB = True           
        
        if self.radioButton_SIDA.isChecked():
            self.__Sida = True
            
        if self.radioButton_Sifilis.isChecked():
            self.__Sifilis = True            
        
        if self.radioButton_Chagas.isChecked():
            self.__Chagas = True
            
        if self.radioButton_Otras_Enf.isChecked():
            self.__OtrasEnfermedades = True
            self.__TextOtrasEnfermedades = self.lineEdit_OtraEnfer.text()
            
        if self.radioButton_anemia.isChecked():
            self.__Anemia = True
        
    def GuardarGenero(self):
        if self.radiomascu.isChecked():
            self.__genero = "Masculino"
            return self.__genero
        elif self.radiofeme.isChecked():
            self.__genero = "Femenino"
            return self.__genero    
    
    def ConfirmarIngreso(self):
        Hemoglobina = ""
        try:
            Hemoglobina = float(self.lineEdit_hemoGlo.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo de ingreso de Hemoglobina Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        hierroS = ""
        try:
            hierroS = float(self.lineEdit_Hierro.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo de ingreso de Hierro Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        nueva_ident =""
        try:
            nueva_ident = int(self.cedulaDonante.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Identificación de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        tel_don=""
        try:
            
            tel_don = int(self.lineEdit_telefono.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Teléfono de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        edad_don = ""
        try:
            edad_don = int(self.lineEdit_edad.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Edad de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        peso_don= ""
        try:
            peso_don = int(self.lineEdit_peso.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Peso de Donante no puede estar vacío ni ser cero')
            msgBox.show()
            return
        self.__TextOtrasEnfermedades=self.lineEdit_OtraEnfer.text()    
        nom_don=self.lineEdit_nombre.text()
        apellido_don=self.lineEdit_apellido.text()
        correo=self.lineEdit_correo.text()
        ciudad=self.lineEdit_ciudad.text()
        
        verif_nombre=nom_don.strip()
        verif_apellido=apellido_don.strip()
        verif_correo=correo.strip()
        verif_ciudad=ciudad.strip()
    
        msgBox = QMessageBox(self)
        if verif_nombre=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('Debe ingresar campo Nombre de Donante')
            msgBox.show()
        elif verif_apellido=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('Debe ingresar campo Apellido de Donante')
            msgBox.show()
        elif verif_ciudad=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setWindowTitle("Debe ingresar campo Ciudad de Donante")
            msgBox.show()
        elif verif_correo=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta Edición")
            msgBox.setText('Llenar correo de Donante')
            msgBox.show()           
        elif nueva_ident <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo Cédula de Donante no puede estar vacío ni ser letra')
            msgBox.show()
        elif tel_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo Teléfono de Donante no puede estar vacío ni ser cero')
            msgBox.show()
        elif edad_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta Edición")
            msgBox.setText('El campo Edad de Donante no puede estar vacío')
            msgBox.show()
        elif peso_don <= 0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCIÓN")
            msgBox.setText('Debe seleccionar un Peso mayor o igual a 0')
            msgBox.show()
        elif Hemoglobina <= 0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCIÓN")
            msgBox.setText('Debe llenar completo el campo Hemoglobina de Donante')
            msgBox.show()
        elif hierroS <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCIÓN")
            msgBox.setText('Debe llenar completo el campo Hierro de Donante')
            msgBox.show()
            
        else:
            sangre=self.GuardarSangre()
            genero=self.GuardarGenero()
            htlv=self.__HTLV
            hepaB=self.__HepatitisB 
            hepaC=self.__HepatitisC
            sida=self.__Sida
            sifilis = self.__Sifilis
            otrasEnf=self.__OtrasEnfermedades
            TextOtrasEnf = self.__TextOtrasEnfermedades
            chagas=self.__Chagas
            anemia=self.__Anemia            
            ident = self.__Cedula_verificación

            edicion = self.__mi_controlador.ingresoEditarDonante(nom_don,apellido_don,genero,ident,nueva_ident,edad_don,peso_don,tel_don,sangre,correo,ciudad,hierroS,anemia,Hemoglobina,sifilis,hepaB,hepaC,sida,htlv,chagas,otrasEnf,TextOtrasEnf )

            if edicion == True:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText('Donante editado con éxito')     
                msgBox.show()  
            elif edicion == False:                                                
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText('Ha Habido un ERROR')     
                msgBox.show()  
            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)            
            ventanaMenDon.show()
            self.hide()
    def asignarControlador(self,c):
        self.__mi_controlador = c
    
    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()   
        
class EliminarDonante(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('verificacionCC_ElimDon.ui',self)
        self.__ventana_principal=ppal
        self.setup()
    def setup(self):
        self.BotonOkCancel.accepted.connect(self.ConfirmarEliminarDon)
        self.BotonOkCancel.rejected.connect(self.Volver)
    
    def ConfirmarEliminarDon(self):
        nueva_ident = int(self.InputCedula.text())
        verificar=self.__mi_controlador.verificarIdDon(nueva_ident)
        if verificar==True:
            self.__mi_controlador.eliminarMiDonante(nueva_ident)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Eliminar Donante')
            mensaje=("Donante con identificación "+str(nueva_ident)+" \n se ha eliminado satisfactoriamente")
            msgBox.setText(mensaje)
            msgBox.show()
            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)
            ventanaMenDon.show()
            self.hide()
                
        else:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Eliminar Donante')
            msgBox.setText('El donante a eliminar con identificación '+str(nueva_ident)+' no existe.\n\n           Inténtalo de nuevo.')
            msgBox.show()
            ventanaMenDon = VentanaDonante(self)
            ventanaMenDon.asignarControlador(self.__mi_controlador)
            ventanaMenDon.show()
            self.hide()
        
    def asignarControlador(self,c):
        self.__mi_controlador = c
        
        
    def Volver(self):
        ventanaMenDon = VentanaDonante(self)
        ventanaMenDon.asignarControlador(self.__mi_controlador)
        ventanaMenDon.show()
        self.hide()
 ################################### MENÚ 2 (INGRESAR UN PACIENTE) ####################################################       
class VentanaPaciente(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('menu_paciente.ui',self)
        self.__ventana_principal=ppal
        self.setup()

    def setup(self):
        self.BotonNuevoPac.clicked.connect(self.IngresoPac)
        self.BotonVerPac.clicked.connect(self.VerificarPac_Ver)
        self.BotonEditarPac.clicked.connect(self.VerificarPac_Editar)
        self.BotonEliminarPac.clicked.connect(self.eliminarPaciente)
        self.BotonBuscarDonante.clicked.connect(self.buscarDonante)
        self.BotonVolver.clicked.connect(self.Volver)
        
    def asignarControlador(self,c):
        self.__mi_controlador = c
    
    def IngresoPac(self):
        ventanaIngresoPac = VentanaIngresoPac(self)
        ventanaIngresoPac.asignarControlador(self.__mi_controlador)
        ventanaIngresoPac.show()
        self.hide()
    
    def VerificarPac_Ver(self):
        ventanaVerif = VerificarPaciente_Ver(self)
        ventanaVerif.asignarControlador(self.__mi_controlador)
        ventanaVerif.show()
        self.hide()

    def VerificarPac_Editar(self):
        ventanaVerif = VerificarPaciente_Editar(self)
        ventanaVerif.asignarControlador(self.__mi_controlador)
        ventanaVerif.show()
        self.hide()
    
    def eliminarPaciente(self):
        ventanaEliminar = EliminarPaciente(self)
        ventanaEliminar.asignarControlador(self.__mi_controlador)
        ventanaEliminar.show()
        self.hide()

    def buscarDonante(self):
        buscarDonante = BuscarUnDonante(self)
        buscarDonante.asignarControlador(self.__mi_controlador)
        buscarDonante.show()
        self.hide()
        
    def Volver(self):
        ventanaPrinc = VentanaPrincipal(self)
        ventanaPrinc.asignarControlador(self.__mi_controlador)
        ventanaPrinc.show()
        self.hide()
    
class VentanaIngresoPac(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('ingreso_paciente.ui',self)
        self.__mi_ventana_principal  = ppal     
        self.setup()

    def setup(self):
        self.Boton_Volver.clicked.connect(self.Volver)
        self.Boton_Confirmar.clicked.connect(self.opcion_aceptar)
        
        #INFORMACION PACIENTE
        self.lineEdit_Nom.setValidator(validator)
        self.lineEdit_Apell.setValidator(validator)
        self.lineEdit_Cedula.setValidator(QIntValidator())
        self.lineEdit_Edad.setValidator(QIntValidator(1,150))
        self.lineEdit_Correo.text()
        self.lineEdit_Peso.setValidator(QIntValidator(1,1000))
        self.lineEdit_Ciudad.setValidator(validator)
        self.lineEdit_Tel.setValidator(QIntValidator())        
        #TIPOS DE SANGRE
        self.radioButton_APos.toggled.connect(self.GuardarSangre)
        self.radioButton_ANeg.toggled.connect(self.GuardarSangre)
        self.radioButton_BPos.toggled.connect(self.GuardarSangre)
        self.radioButton_BNeg.toggled.connect(self.GuardarSangre)
        self.radioButton_ABPos.toggled.connect(self.GuardarSangre)
        self.radioButton_ABNeg.toggled.connect(self.GuardarSangre)
        self.radioButton_OPos.toggled.connect(self.GuardarSangre)
        self.radioButton_ONeg.toggled.connect(self.GuardarSangre)
        #GENERO        
        self.radioButton_Masculino.toggled.connect(self.IngresarGenero)        
        self.radioButton_Femenino.toggled.connect(self.IngresarGenero)  
        
    def IngresarGenero(self):
        if self.radioButton_Masculino.isChecked():
            self.__genero = "Masculino"
            return self.__genero
        elif self.radioButton_Femenino.isChecked():
            self.__genero = "Femenino"
            return self.__genero
                    
    def GuardarSangre(self):  #En esta opción se guardará cual de las opciones presionó el usuario y se retornara la respectiva
        if self.radioButton_APos.isChecked():
            self.__tipoSangre = "A+"
            return self.__tipoSangre
        elif self.radioButton_ANeg.isChecked():
            self.__tipoSangre = "A-"
            return self.__tipoSangre
        elif self.radioButton_BPos.isChecked():
            self.__tipoSangre = "B+"
            return self.__tipoSangre
        elif self.radioButton_BNeg.isChecked():
            self.__tipoSangre = "B-"
            return self.__tipoSangre
        elif self.radioButton_ABPos.isChecked():
            self.__tipoSangre = "AB+"
            return self.__tipoSangre
        elif self.radioButton_ABNeg.isChecked():
            self.__tipoSangre = "AB-"
            return self.__tipoSangre
        elif self.radioButton_OPos.isChecked():
            self.__tipoSangre = "O+"
            return self.__tipoSangre
        elif self.radioButton_ONeg.isChecked():
            self.__tipoSangre = "O-"
            return self.__tipoSangre
        
    def opcion_aceptar(self):
        NomPac=self.lineEdit_Nom.text()
        ApePac=self.lineEdit_Apell.text()
        CiuPac=self.lineEdit_Ciudad.text()
        tipoSangre=self.GuardarSangre()
        #enfermedad=self.opcion_enfermedad()
        CedulaPac = ""
        EdadPac = ""
        TelPac = ""
        PesoPac = ""
        CorreoPac=self.lineEdit_Correo.text()
        generoPac=self.IngresarGenero()
        msgBox = QMessageBox(self)
       
        try:#Se validará que en el solo se acepten valores numéricos en los campos que así lo requieran
           CedulaPac = int(self.lineEdit_Cedula.text())
           EdadPac = int(self.lineEdit_Edad.text())
           TelPac= int(self.lineEdit_Tel.text())
           PesoPac = int(self.lineEdit_Peso.text())
        except:
           
           msgBox.setIcon(QMessageBox.Warning)
           msgBox.setWindowTitle("VALIDACIÓN")
           msgBox.setText("En campos cédula, edad, teléfono y peso solo podrá ingresar datos númericos, por favor verifique.")
           msgBox.show()
           return
       
        campo_nombre = NomPac.strip()
        campo_apellido = ApePac.strip()
        campo_ciudad = CiuPac.strip()
        campo_correo=CorreoPac.strip()      
       
        if campo_nombre == "" or campo_ciudad == "" or CorreoPac == "" or campo_apellido =="" or campo_correo ==" " or TelPac == "" or EdadPac == "" or CedulaPac == "" or PesoPac == "" or generoPac == None or tipoSangre == None:
           #Mostrar mensaje de alerta           
           msgBox.setIcon(QMessageBox.Warning)
           msgBox.setWindowTitle("Ingresar Paciente")
           msgBox.setText("No puede haber ningun campo en blanco, por favor ingrese toda la información")
           msgBox.show()           
           
        else:    #Guardará los datos
            ingreso_paciente= self.__mi_controlador.recibirPaciente(NomPac,ApePac,CiuPac,generoPac,EdadPac,PesoPac,tipoSangre ,TelPac,CedulaPac,CorreoPac)
            if ingreso_paciente==True:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText("Paciente con identifación "+str(CedulaPac)+ " ingresado con éxito")     
                msgBox.show()
                                        
            else:
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('El paciente con identificación '+str(CedulaPac)+' ya existe.\n\n           Inténtalo de nuevo.')
                msgBox.show()                
                
            self.Volver_Menu()
            self.hide()     
    
    def Volver_Menu(self):
        self.__mi_ventana_principal.show()
        self.hide()
                
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()   
        self.hide()   

    def asignarControlador(self,c):
        self.__mi_controlador = c
        
class VerificarPaciente_Ver(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('verificacionCC_VerPac.ui',self)
        self.__ventana_principal=ppal
        self.setup()

    def setup(self):
        self.BotonOkCancel.accepted.connect(self.Ingresar_VerPac)
        self.BotonOkCancel.rejected.connect(self.Volver)
        
    def Ingresar_VerPac(self):
        
        cc = int(self.InputCedula.text())
        verificacion = self.__mi_controlador.verificarIdPac(cc)
        if verificacion == True:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Ver Paciente')
            mensaje=("INFORMACIÓN DE PACIENTE con identificación "+str(cc))
            msgBox.setText(mensaje)
            msgBox.show()
            
            
            VerPac = VentanaVerInfoPac(self)
            VerPac.asignarControlador(self.__mi_controlador)
            VerPac.Tabular_Informacion(cc)        
            VerPac.show()
            self.hide()
            
                
        elif verificacion == False:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Ver PACIENTE')
            msgBox.setText('El PACIENTE con identificación '+str(cc)+' no existe.\n\n           Inténtelo de nuevo.')
            msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)
            ventanaPac.show()
            self.hide()
        
    
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()  
        self.hide()   
        
    def asignarControlador(self,c):
        self.__mi_controlador = c

class VentanaVerInfoPac(QDialog):
    def __init__(self,ppal=None):
        super(VentanaVerInfoPac,self).__init__(ppal)
        loadUi('ver_info_paciente.ui',self)
        self.__ventana_principal=ppal
        self.setup()
    
    def Tabular_Informacion(self,cc):        
        Paciente = self.__mi_controlador.Regresar_Paciente(cc)
        if Paciente == False :
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(" ATENCION")
            msgBox.setText('La cédula ingresada NO se encuentra registrada.')
            msgBox.show()
            self.hide()
        
        else: 
            #llamamos toda la informacion del donante
            Nom = Paciente.verNombre()
            Ape = Paciente.verApellido()
            Ident = Paciente.verIdent()
            Tel = Paciente.verTel()
            Edad = Paciente.verEdad()
            Gen = Paciente.verGenero()
            Correo =Paciente.verCorreo()
            Ciud = Paciente.verCiudad()
            TipoSang = Paciente.verTipoSangre()
            Peso = Paciente.verPeso()

            celdaNomb = QTableWidgetItem(str(Nom))
            celdaApe = QTableWidgetItem(str(Ape))
            celdaIdent = QTableWidgetItem(str(Ident))
            celdaTel = QTableWidgetItem(str(Tel))
            celdaEdad = QTableWidgetItem(str(Edad))
            celdaGen = QTableWidgetItem(str(Gen))
            celdaCorreo = QTableWidgetItem(str(Correo))
            celdaCiud = QTableWidgetItem(str(Ciud))
            celdaTipoSang = QTableWidgetItem(str(TipoSang))
            celdaPeso = QTableWidgetItem(str(Peso))

            self.Tabla_DatosPac.setItem(-1,1,celdaNomb)
            self.Tabla_DatosPac.setItem(0,1,celdaApe) 
            self.Tabla_DatosPac.setItem(1,1,celdaGen) 
            self.Tabla_DatosPac.setItem(2,1,celdaIdent) 
            self.Tabla_DatosPac.setItem(3,1,celdaTel) 
            self.Tabla_DatosPac.setItem(4,1,celdaPeso) 
            self.Tabla_DatosPac.setItem(5,1,celdaTipoSang) 
            self.Tabla_DatosPac.setItem(6,1,celdaEdad) 
            self.Tabla_DatosPac.setItem(7,1,celdaCorreo) 
            self.Tabla_DatosPac.setItem(8,1,celdaCiud) 

    def setup(self):
        self.Boton_Volver.clicked.connect(self.Volver)

    def asignarControlador(self,c):
        self.__mi_controlador = c        
        
    def Volver(self):
        MenuPac = VentanaPaciente(self)
        MenuPac.asignarControlador(self.__mi_controlador)
        MenuPac.show()
        self.hide()

class VerificarPaciente_Editar(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('verificacionCC_ActualizarPac.ui',self)
        self.__ventana_principal=ppal
        self.setup()

    def setup(self):
        self.BotonOkCancel.accepted.connect(self.ConfirmarEditarPac)
        self.BotonOkCancel.rejected.connect(self.Volver)

    def ConfirmarEditarPac(self):
        ident = int(self.InputCedula.text())
        verificar=self.__mi_controlador.verificarIdPac(ident)
        if verificar==True:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Editar Paciente')
            mensaje=("Paciente con identificación "+str(ident))
            msgBox.setText(mensaje)
            msgBox.show()                
            VentEdit = EditarPaciente(self)
            VentEdit.AsignarCedula_Verificacion(ident)
            VentEdit.asignarControlador(self.__mi_controlador)
            VentEdit.show()
            self.hide()
                
        else:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Editar Paciente')
            msgBox.setText('El Paciente con identificación '+str(ident)+' no existe.\n\n           Inténtelo de nuevo.')
            msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)
            ventanaPac.show()
            self.hide()   
        
    
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()    
        self.hide()   
        
    def asignarControlador(self,c):
        self.__mi_controlador = c

class EditarPaciente(QDialog):
    def __init__(self,ppal=None):
        super(EditarPaciente,self).__init__(ppal) #Hereda la clase VerificarEdiciónPaciente para tomar el Ident
        loadUi('editar_paciente2.ui',self)
        self.__ventana_principal=ppal
        self.setup()

        self.__Cedula_verificación = 0
    def setup(self):
        self.Boton_Aceptar.clicked.connect(self.ConfirmarIngreso)
        self.volver_paciente.clicked.connect(self.Volver)
        self.Boton_NombrePac.setValidator(validator)
        self.Boton_Apell.setValidator(validator)
        self.Boton_Edad.setValidator(QIntValidator(1,150))
        self.Boton_Ciudad.setValidator(validator)
        self.Boton_Tel.setValidator(QIntValidator())
        self.Boton_Correo.text()
        self.Boton_NuevaCed.setValidator(QIntValidator())
        self.Boton_Peso.setValidator(QIntValidator(1,1000))
        #genero
        self.masculino.toggled.connect(self.GuardarGenero)
        self.femenino.toggled.connect(self.GuardarGenero)        
        #Sangre
        self.APOS.toggled.connect(self.GuardarSangre)
        self.ANEG.toggled.connect(self.GuardarSangre)
        self.BPOS.toggled.connect(self.GuardarSangre)
        self.BNEG.toggled.connect(self.GuardarSangre)
        self.ABPOS.toggled.connect(self.GuardarSangre)
        self.ABNEG.toggled.connect(self.GuardarSangre)
        self.OPOS.toggled.connect(self.GuardarSangre)
        self.ONEG.toggled.connect(self.GuardarSangre)
        
    
    def AsignarCedula_Verificacion(self,id):
        self.__Cedula_verificación = id
       
    def GuardarSangre(self):  #En esta opción se guardará cual de las opciones presionó el usuario y se retornara la respectiva
        if self.APOS.isChecked():
            self.__tipoSangre = "A+"
            return self.__tipoSangre
        elif self.ANEG.isChecked():
            self.__tipoSangre = "A-"
            return self.__tipoSangre
        elif self.BPOS.isChecked():
            self.__tipoSangre = "B+"
            return self.__tipoSangre
        elif self.BNEG.isChecked():
            self.__tipoSangre = "B-"
            return self.__tipoSangre
        elif self.ABPOS.isChecked():
            self.__tipoSangre = "AB+"
            return self.__tipoSangre
        elif self.ABNEG.isChecked():
            self.__tipoSangre = "AB-"
            return self.__tipoSangre
        elif self.OPOS.isChecked():
            self.__tipoSangre = "O+"
            return self.__tipoSangre
        elif self.ONEG.isChecked():
            self.__tipoSangre = "O-"
            return self.__tipoSangre
  
    def GuardarGenero(self):
        if self.masculino.isChecked():
            self.__genero = "Masculino"
            return self.__genero
        elif self.femenino.isChecked():
            self.__genero = "Femenino"
            return self.__genero    
    
    def ConfirmarIngreso(self):
        
        nueva_ident =""
        try:
            nueva_ident = int(self.Boton_NuevaCed.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Identificación de Paciente no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        tel_don=""
        try:
            
            tel_don = int(self.Boton_Tel.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo Teléfono de Paciente no puede estar vacío ni ser cero')
            msgBox.show()
            return
        
        edad_don = ""
        try:
            edad_don = int(self.Boton_Edad.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta!")
            msgBox.setText('El campo Edad de Paciente no puede estar vacio ni ser cero')
            msgBox.show()
            return
        
        peso_don= ""
        try:
            peso_don = int(self.Boton_Peso.text())
        except:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo Peso de Paciente no puede estar vacío ni ser cero')
            msgBox.show()
            return
            
        nom_don=self.Boton_NombrePac.text()
        apellido_don=self.Boton_Apell.text()
        correo=self.Boton_Correo.text()
        ciudad=self.Boton_Ciudad.text()
        
        verif_nombre=nom_don.strip()
        verif_apellido=apellido_don.strip()
        verif_correo=correo.strip()
        verif_ciudad=ciudad.strip()
    
        msgBox = QMessageBox(self)
        if verif_nombre=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('Debe ingresar campo Nombre de Paciente')
            msgBox.show()
        elif verif_apellido=='': 
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('Debe ingresar campo Apellido de Paciente')
            msgBox.show()
        elif verif_ciudad=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setWindowTitle("Debe ingresar campo Ciudad de Paciente")
            msgBox.show()
        elif verif_correo=='':
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta Edición")
            msgBox.setText('Llenar correo de Paciente')
            msgBox.show()           
        elif nueva_ident <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo "Cédula" de Paciente no puede estar vacío ni ser letra')
            msgBox.show()
        elif tel_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("¡Alerta Edición!")
            msgBox.setText('El campo Teléfono de Paciente no puede estar vacío ni ser cero')
            msgBox.show()
        elif edad_don <=0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Alerta Edición")
            msgBox.setText('El campo edad de Paciente no puede estar vacío')
            msgBox.show()
        elif peso_don <= 0:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Ingreso de datos - ATENCIÓN")
            msgBox.setText('Debe seleccionar un Peso mayor o igual a 0')
            msgBox.show()
           
        else:
            sangre=self.GuardarSangre()
            genero=self.GuardarGenero()
            ident = self.__Cedula_verificación

            edicion = self.__mi_controlador.ingresoEditarPaciente(nom_don,apellido_don,genero,ident,nueva_ident,edad_don,peso_don,tel_don,sangre,correo,ciudad)                                                        
            if edicion == True:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText('Paciente editado con éxito')     
                msgBox.show()  
                
            elif edicion == False:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('¡Alerta!')
                msgBox.setText('Ha Habido un ERROR')     
                msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)            
            ventanaPac.show()
            self.hide()    

            
    def asignarControlador(self,c):
        self.__mi_controlador = c
        
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()  
        self.hide() 
                
class EliminarPaciente(QDialog):
    def __init__(self,ppal=None):
        super(EliminarPaciente,self).__init__(ppal)
        loadUi('verificacionCC_ElimPac.ui',self)
        self.__ventana_principal=ppal
        self.setup()
        
    def setup(self):
        self.BotonOkCancel.accepted.connect(self.confirmarEliminarPaciente)
        self.BotonOkCancel.rejected.connect(self.Volver)
    def asignarControlador(self,c):
        self.__mi_controlador = c
    
    def confirmarEliminarPaciente(self):
        nueva_ident = int(self.InputCedula.text())
        verificar=self.__mi_controlador.verificarIdPac(nueva_ident)
        if verificar==True:
            self.__mi_controlador.eliminarMiPaciente(nueva_ident)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Eliminar Paciente')
            mensaje=("Paciente con identificación "+str(nueva_ident)+" \n se ha eliminado correctamente")
            msgBox.setText(mensaje)
            msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)
            ventanaPac.show()
            self.hide()
        else:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Eliminar Donante')
            msgBox.setText('El paciente que se desea eliminar con identificación '+str(nueva_ident)+' no existe.\n\n           Inténtelo de nuevo.')
            msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)
            ventanaPac.show()
            self.hide()
    
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()   
        self.hide() 
        
class BuscarUnDonante(QDialog):
    def __init__(self,ppal=None):
        super(BuscarUnDonante,self).__init__(ppal)
        loadUi('Buscar_Donante.ui',self)
        self.__ventana_principal=ppal
        self.setup()
    def setup(self):
        self.BotonOkCancel.accepted.connect(self.confirmarBuscarDonante)
        self.BotonOkCancel.rejected.connect(self.Volver)

    def asignarControlador(self,c):
        self.__mi_controlador = c
    
    def confirmarBuscarDonante(self):
        ident = int(self.InputCedula.text())
        verificar=self.__mi_controlador.verificarIdPac(ident)
        if verificar==True:
            NDon=self.__mi_controlador.filtroDonante(ident)
            if NDon > 0:
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('Buscar Donante')
                mensaje=("Hay "+str(NDon)+ " donante(s) disponible(s) para transfusión de sangre")
                msgBox.setText(mensaje)
                msgBox.show()
                ventanaPac = VentanaPaciente(self)
                ventanaPac.asignarControlador(self.__mi_controlador)
                ventanaPac.show()
                self.hide()
            elif NDon == 0:
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle('Buscar Donante')
                mensaje=("Lo sentimos, en estos momentos no hay donantes disponibles")
                msgBox.setText(mensaje)
                msgBox.show()
                ventanaPac = VentanaPaciente(self)
                ventanaPac.asignarControlador(self.__mi_controlador)
                ventanaPac.show()
                self.hide()
        else:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Buscar Donante')
            msgBox.setText("La identifiación de paciente "+ str(ident)+" que ingresó no existe.\n\n           Inténtalo de nuevo.")
            msgBox.show()
            ventanaPac = VentanaPaciente(self)
            ventanaPac.asignarControlador(self.__mi_controlador)
            ventanaPac.show()
            self.hide()
    
    def Volver(self):
        ventanaPac = VentanaPaciente(self)
        ventanaPac.asignarControlador(self.__mi_controlador)
        ventanaPac.show()   
        self.hide() 
############################MENÚ PRINCIPAL 3 (VISUALIZAR GRÁFICAS DE LOS DATOS ACTUALES DEL SISTEMA)############################################################
class VentanaDatosEstadisticos(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('datos_estadisticos.ui',self)
        self.__ventana_principal=ppal
        self.setup()
        
    def setup(self):
        self.Boton_Volver.clicked.connect(self.Volver)        
        self.Boton_TiposS.clicked.connect(self.GraficarTiposSangre)
        self.Boton_EnfermedadV.clicked.connect(self.GraficarEnferVener)  
    
    def Volver(self):
        ventanaGeneral = VentanaPrincipal(self)
        ventanaGeneral.asignarControlador(self.__mi_controlador)
        ventanaGeneral.show()    
        self.hide()
 
    def GraficarTiposSangre(self,L):       
        self.figure=Figure()
        self.canvas=FigureCanvas(self.figure)         
        self.Histogramas.addWidget(self.canvas)        
        grafico = self.figure.add_subplot(111)

        grafico.clear()               
        grafico.hist(L)
        grafico.set_xlabel('Tipos de sangre')
        grafico.set_ylabel('Número pacientes')
        grafico.set_title("Tipos de sangre Pacientes")
        grafico.grid()
        grafico.plot()
 
    def GraficarEnferVener(self,L_Enfermedad):
        self.figure=Figure()
        self.canvas=FigureCanvas(self.figure)         
        self.Histogramas.addWidget(self.canvas) 

        grafico = self.figure.add_subplot(111)        
        grafico.clear() 
        grafico.hist(L_Enfermedad)
        grafico.set_xlabel('Enfermedades de los Pacientes')
        grafico.set_ylabel('Número pacientes')
        grafico.set_title("Enfermedades Venéreas")
        grafico.grid()
        grafico.plot()
    
    def asignarControlador(self,c):
        self.__mi_controlador = c
########################MENÚ PRINCIPAL #4 (GENERAR UN CONTEO CELULAR (IMAGEN PNG))####################################################

class VentanaConteoCelular(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Interfaz_Conteo.ui",self)
        self.setup()
        self.getValueHorizontal()
        self.getValueVertical()
        self.show()
    def setup(self):  

        pixmap = QPixmap('Captura.png')
        self.label_imagen.setPixmap(pixmap)
        self.archivo_cargado = " "
        #Horizontal slider
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(1000)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(100)
        self.horizontalSlider.valueChanged.connect(self.getValueHorizontal)        
        #Vertical slider
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(1000)
        self.verticalSlider.setSingleStep(10)
        self.verticalSlider.setValue(400)
        self.verticalSlider.valueChanged.connect(self.getValueVertical)

        self.Boton_Img_Original.clicked.connect(self.Ver_Original) 
        self.Boton_Img_Original.setEnabled(False)       
        self.Boton_Cargar.clicked.connect(self.IngresarImagen)  
        
        self.Boton_Volver.clicked.connect(self.Volver)   
        self.Boton_Conteo.clicked.connect(self.Graficar_Conteo)
        self.Boton_Conteo.setEnabled(False) 
        self.Boton_Confirmar_Cambio.clicked.connect(self.Graficar_Conteo)
        self.Boton_Confirmar_Cambio.setEnabled(False)
        
    def Volver(self):
        ventanaGeneral = VentanaPrincipal(self)
        ventanaGeneral.asignarControlador(self.__mi_controlador)
        ventanaGeneral.show() 
        self.hide()
    def asignarControlador(self,c):
            self.__mi_controlador = c
        
    def getValueHorizontal(self):
        value = self.horizontalSlider.value()
        self.labelHorizontal.setText(str(value))

    def getValueVertical(self):
        value = self.verticalSlider.value()
        self.labelVertical.setText(str(value))

    def cv_imread(self,file_path):
        self.cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return self.cv_img

    def IngresarImagen(self):

        self.archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Abrir señal","","Todos los archivos (*)")
        # file_path = 'eri.jpg'
        self.Boton_Img_Original.setEnabled(True)  
        self.Boton_Conteo.setEnabled(True) 
        self.Boton_Confirmar_Cambio.setEnabled(True)
        
        if self.archivo_cargado == "":          
          R = QMessageBox(self)
          R.setText("NO SE HA CARGADO NINGUNA IMAGEN")
          R.show()
        else:
          A = str(self.archivo_cargado)
          R = QMessageBox(self)
          R.setText("SE HA CARGADO LA IMAGEN : " + A)
          R.setWindowTitle("Ingreso Correcto")
          R.show()
          self.label_3.setText("LA IMAGEN CARGADA ES : " + A)
      
    def Graficar_Conteo(self):
        plt.close()
        imagen = self.cv_imread(self.archivo_cargado)
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)          
        Num_Max = self.verticalSlider.value()
        Num_Min = self.horizontalSlider.value()
        bordes = cv2.Canny(grises, Num_Min, Num_Max)
        ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        print('Número de contornos encontrados: ', len(ctns))   
        a = str(len(ctns))
        
        plt.imshow(bordes, cmap='gray')   
        plt.title('\n-\nNúmero de contornos encontrados: '+ a + " \nValores UMBRAL: Mín - "+ str(Num_Min) + " Máx - " + str(Num_Max))        
        plt.show()    
        
    def Ver_Original(self):
            imagen = self.cv_imread(self.archivo_cargado)
            cv2.imshow("Imagen",imagen)            
            cv2.waitKey(0)        
            cv2.destroyAllWindows() 
            