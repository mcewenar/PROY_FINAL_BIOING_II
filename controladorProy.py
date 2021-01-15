from PyQt5.QtWidgets import QApplication
import sys
from vistaProy import VentanaPrincipal
from modeloProy import Sistema

class Coordinador:
    def __init__(self, vistaProy,modeloProy):
        self.__vista = vistaProy
        self.__modelo = modeloProy
        
        
##################MÉTODOS OPCIÓN 1 MENÚ PRINCIPAL (DONANTES) ######################################################
    def recibirDonante(self,nom_don,apellido_don,ident,tel_don,edad_don,peso_don,sangre,genero,ciudad,correo,Hemoglobina,hierroS,anemia,hepaC,hepaB,sida,htlv,otrasEnf,chagas,sifilis,TextoOtrasEnf):
        return self.__modelo.ingresarDonante(nom_don,apellido_don,ident,tel_don,edad_don,peso_don,sangre,genero,ciudad,correo,Hemoglobina,hierroS,anemia,hepaC,hepaB,sida,htlv,otrasEnf,chagas,sifilis,TextoOtrasEnf)
    
    def ingresoEditarDonante(self,nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad,hierro,Anemia,hemoglo,sifilis,hepatitisB,hepatitisC,sida,htlv,chagas,otrasEnfer,TextoOtrasEnf):
        ingreso_d=self.__modelo.editadoDonante(nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad,hierro,Anemia,hemoglo,sifilis,hepatitisB,hepatitisC,sida,htlv,chagas,otrasEnfer,TextoOtrasEnf)
        return ingreso_d
    
    def verificarIdDon(self,id):
        return self.__modelo.verificarIdDonante(id)
    
    def eliminarMiDonante(self,i):
        Eliminar = self.__modelo.eliminarDonante(i)
        return Eliminar
    
    def RegresarDonante(self,cc):
        Donante = self.__modelo.Regresar_Donante(cc)
        return Donante
    
    

########################MÉTODOS OPCIÓN 2 MENÚ PRINCIPAL (PACIENTES) #############################################
    def recibirPaciente(self,n,a,c,g,e,p,gs,tel,ce,cr):
        DatosPaciente=self.__modelo.ingresarReceptor(n,a,c,g,e,p,gs,tel,ce,cr)
        return DatosPaciente

    def ingresoEditarPaciente(self,nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad):
        ingreso_d=self.__modelo.editadoPaciente(nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad)
        return ingreso_d
    
    def verificarIdPac(self,id):
        return self.__modelo.verificarIdReceptor(id)
    
    def eliminarMiPaciente(self,i):
        Eliminar = self.__modelo.eliminarPaciente(i)
        return Eliminar
        
    def Regresar_Paciente(self,cc):
        Paciente_Receptor = self.__modelo.Regresar_Paciente(cc)
        return Paciente_Receptor
    def filtradoDonante(self,num):
        return self.__modelo.NumAptoDonante(num)
        

def main():
    app = QApplication(sys.argv)
    mi_vista = VentanaPrincipal()
    mi_sistema = Sistema()
    mi_controlador = Coordinador(mi_vista, mi_sistema)
    mi_vista.asignarControlador(mi_controlador)
    
    mi_vista.show()
    sys.exit(app.exec_())



main()