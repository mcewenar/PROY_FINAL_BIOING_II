
class Receptor(): #OJO: PACIENTE == RECEPTOR
    def __init__(self):
        self.__nombre= " "
        self.__apellido=" "
        self.__Cedula= 0
        self.__telefono= 0
        self.__edad = 0
        self.__genero= " "
        self.__correo= " "
        self.__ciudad= " "
        self.__peso = 0
        self.__tipoSangre = " "
    
    def asignarNombre(self,n):
        self.__nombre=n
    def asignarApellido(self,a):
        self.__apellido=a
    def asignarCedula(self,f):
        self.__Cedula=f
    def asignarTel(self,t):
        self.__telefono=t
    def asignarEdad(self,u):
        self.__edad=u
    def asignarGenero(self,g):
        self.__genero=g
    def asignarCorreo(self,c):
        self.__correo=c
    def asignarCiudad(self,r):
        self.__ciudad=r
    def asignarTipoSangre(self,s):
        self.__tipoSangre = s    
    def asignarPeso(self,p):
        self.__peso = p
    
    def verNombre(self):
        return self.__nombre
    def verApellido(self):
        return self.__apellido
    def verIdent(self):
        return self.__Cedula
    def verTel(self):
        return self.__telefono
    def verEdad(self):
        return self.__edad
    def verGenero(self):
        return self.__genero
    def verCorreo(self):
        return self.__correo
    def verCiudad(self):
        return self.__ciudad
    def verTipoSangre(self):            
        return self.__tipoSangre
    def verPeso(self):
        return self.__peso
    
    
class Donante(Receptor):
    def __init__(self):
        Receptor.__init__(self)
        self.__examenes=""
    
    def asignarExamenes(self,e):
        self.__examenes=e
    def verExamenes(self):
        return self.__examenes
    

         
class Examenes():
    def __init__(self):
        self.__hierro_sangre=0
        self.__hemoglobina=0
        self.__Anemia=" "
        self.__Sifilis = False
        self.__HepatitisB = False #(Antígeno de Superficie y Core)
        self.__HepatitisC = False
        self.__Sida = False       #(HIV 1,2)
        self.__HTLV = False       #I-II
        self.__Chagas = False
        self.__OtrasEnfermedades = "N/A"
        self.__TextoOtrasEnfermedades = "N/A"


    def asignarHierro(self,h):
        self.__hierro_sangre=h
    def asignarAnemia(self,a):
        self.__Anemia = a
    def asignarHemoglobina(self,l):
        self.__hemoglobina=l

    def asignarValorSifilis(self,vs):
        self.__Sifilis = vs
    def asignarValorHepatitisB(self,vhb):
        self.__HepatitisB = vhb
    def asignarValorHepatitisC(self,vhc):
        self.__HepatitisC = vhc
    def asignarValorSIDA(self,vsd):
        self.__Sida = vsd
    def asignarValorHTLV(self,vht):
        self.__HTLV = vht
    def asignarValorChagas(self,vch):
        self.__Chagas = vch
    def asignarOtrasEnfermedades(self , oe):
        self.__OtrasEnfermedades = oe
    def asignarTextoOtrasEnfermedades(self , oe):
        self.__TextoOtrasEnfermedades = oe
    



    def verHierro(self):
        return self.__hierro_sangre
    def verAnemia(self):
        return self.__Anemia
    def verHemoglobina(self):
        return self.__hemoglobina 

    def verValorSifilis(self):
        return self.__Sifilis
    def verValorHepatitisB(self):
        return self.__HepatitisB
    def verValorHepatitisC(self):
        return self.__HepatitisC
    def verValorSIDA(self):
        return self.__Sida
    def verValorChagas(self):
        return self.__Chagas
    def verValorHTLV(self):
        return self.__HTLV
    def verOtrasEnfer(self):
        return self.__OtrasEnfermedades
    def verTextoOtrasEnfer(self):
        return self.__TextoOtrasEnfermedades
          
class Sistema():
    def __init__(self):

        self.__dicc_receptores = {}
        self.__dicc_Donantes= {}

##############################DONANTES########################################   

    def ingresarDonante(self,nom_don,apellido_don,ident,tel_don,edad_don,peso_don,sangre,genero,ciudad,correo,Hemoglobina,hierroS,anemia,hepaC,hepaB,sida,htlv,otrasEnf,chagas,sifilis,TextoOtrasEnf):
        
        resultado=self.verificarIdDonante(ident)        
        if resultado==True:
            return False
        else:            
            Don=Donante()            
            Don.asignarNombre(nom_don)
            Don.asignarApellido(apellido_don)
            Don.asignarCedula(ident)
            Don.asignarTel(tel_don)
            Don.asignarEdad(edad_don)
            Don.asignarGenero(genero)
            Don.asignarCorreo(correo)
            Don.asignarCiudad(ciudad)
            Don.asignarTipoSangre(sangre)
            Don.asignarPeso(peso_don)                
            ex=Examenes()        
            ex.asignarHierro(hierroS)
            ex.asignarAnemia(anemia)
            ex.asignarHemoglobina(Hemoglobina)
            ex.asignarValorSifilis(sifilis)
            ex.asignarValorHepatitisB(hepaB)
            ex.asignarValorHepatitisC(hepaC)
            ex.asignarValorSIDA(sida)
            ex.asignarValorHTLV(htlv)
            ex.asignarValorChagas(chagas)
            ex.asignarOtrasEnfermedades(otrasEnf)
            ex.asignarValorSifilis(sifilis)
            ex.asignarTextoOtrasEnfermedades(TextoOtrasEnf)
            
            Don.asignarExamenes(ex)
            self.__dicc_Donantes[ident]=Don
        
            return True

    def editadoDonante(self,nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad,hierro,Anemia,hemoglo,sifilis,hepatitisB,hepatitisC,sida,htlv,chagas,otrasEnfer,TextoOtrasEnf):
        resultado=self.verificarIdDonante(ident)
        
        if resultado==False:
            return False

        else:
            self.CambiarCedulDon(ident,nueva_ident)

            don = Donante()
            
            don.asignarCedula(nueva_ident)
            don.asignarNombre(nom)
            don.asignarApellido(apellido)
            don.asignarGenero(genero)
            don.asignarEdad(edad)
            don.asignarPeso(peso)
            don.asignarTipoSangre(tipo_sangre)
            don.asignarTel(tel)
            don.asignarCorreo(mail)
            don.asignarCiudad(ciudad)
            
            ex=Examenes()
            ex.asignarHierro(hierro)
            ex.asignarAnemia(Anemia)
            ex.asignarHemoglobina(hemoglo)
            ex.asignarValorSifilis(sifilis)
            ex.asignarValorHepatitisB(hepatitisB)
            ex.asignarValorHepatitisC(hepatitisC)
            ex.asignarValorSIDA(sida)
            ex.asignarValorHTLV(htlv)
            ex.asignarValorChagas(chagas)
            ex.asignarOtrasEnfermedades(otrasEnfer)
            ex.asignarTextoOtrasEnfermedades(TextoOtrasEnf)
            
            
            don.asignarExamenes(ex)            
            self.__dicc_Donantes[nueva_ident] = don            
          
            return True

    def verificarIdDonante(self,CC):
        resultado=CC in self.__dicc_Donantes.keys()
        return resultado

    def CambiarCedulDon(self,cc,ncc):
        self.__dicc_Donantes[ncc] = self.__dicc_Donantes.pop(cc)
    
    def eliminarDonante(self,id):
        del self.__dicc_Donantes[id]  
        print("Donante eliminado")
        
    def verNumDonantes(self):
        return len(self.__dicc_Donantes)

    def Regresar_Donante(self,cc):
        if cc in self.__dicc_Donantes.keys():
            Donante = self.__dicc_Donantes[cc]
            return Donante
        else: 
            return False
        

####################PACIENTES#################################################
    def ingresarReceptor(self,nom_pac,apell,ciudad,genero,edad_pac,peso_pac,grupo_sang,tel_pac,cc,correo):
        
        resultado=self.verificarIdReceptor(cc)

        if resultado==True:
            return False
        else:    
            Pac=Receptor()
            
            Pac.asignarNombre(nom_pac)
            Pac.asignarApellido(apell)
            Pac.asignarCiudad(ciudad) 
            Pac.asignarGenero(genero)
            Pac.asignarEdad(edad_pac)
            Pac.asignarPeso(peso_pac)
            Pac.asignarTipoSangre(grupo_sang)
            Pac.asignarTel(tel_pac)
            Pac.asignarCedula(cc) 
            Pac.asignarCorreo(correo)
                                          
            self.__dicc_receptores[cc]=Pac             
            return True         
    def editadoPaciente(self,nom,apellido,genero,ident,nueva_ident,edad,peso,tel,tipo_sangre,mail,ciudad):
        resultado=self.verificarIdReceptor(ident)
        
        if resultado==False:
            return False

        else:
            self.CambiarCedulaPac(ident,nueva_ident)

            Pac = Receptor()
            Pac.asignarCedula(nueva_ident)
            Pac.asignarNombre(nom)
            Pac.asignarApellido(apellido)
            Pac.asignarGenero(genero)
            Pac.asignarEdad(edad)
            Pac.asignarPeso(peso)
            Pac.asignarTipoSangre(tipo_sangre)
            Pac.asignarTel(tel)
            Pac.asignarCorreo(mail)
            Pac.asignarCiudad(ciudad)                        
                       
            self.__dicc_receptores[nueva_ident] = Pac
            return True
    def CambiarCedulaPac(self,cc,ncc):
        self.__dicc_receptores[ncc] = self.__dicc_receptores.pop(cc)

    def eliminarPaciente(self,id):
            del self.__dicc_receptores[id]
        
    def verNumPacientes(self):
        return len(self.__dicc_receptores)
    
    def Regresar_Paciente(self,cc):
        if cc in self.__dicc_receptores.keys():
            Paciente_Receptor = self.__dicc_receptores[cc]
            return Paciente_Receptor
        else : 
            return False
    
    
    def verificarIdReceptor(self,CCpaciente):
        resultado=CCpaciente in self.__dicc_receptores.keys()
        return resultado
     
    
    
    def filtroDonante(self):
            p=Examenes()
            d=Donante()
            c=0
            if (p.verHemoglobina() >= 13.3 or p.verHemoglobina() <= 16.6) and p.verValorHepatitisB() !=True and p.verValorHepatitisC() != True and p.verAnemia() != True and p.verValorHTLV() != True and p.verValorSIDA() != True and p.asignarOtrasEnfermedades() !=True (d.verEdad() >= 18 or d.verEdad() <= 65):
                c=c+1
                return c
                                   
            else:
                return False
        
        
    
    def NumAptoDonante(self,CCdonante):
        for CCdonante in self.__dicc_Donantes:
            if CCdonante.verificarIdDonante() == True:
                hemoglo=self.filtroDonante()
                return hemoglo
            else:
                return False