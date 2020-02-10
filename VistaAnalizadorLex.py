from tkinter import *
from LogicaAnalizadoLex import *

class VistaAnalizadorLex():

    def __init__(self):

        """
            Colores:

                1. #004445
                2. #2c7873
                3. #6fb98f
                4. #ffd800

        """

        self._logica = LogicaAnalizadorLex(self)

        root=Tk()
        root.title("Analizador Lexico")
        root.resizable(width=False, height=False)
        root.geometry("800x530")

        #Frame utilizado para las opciones de los botones
        self._frameOpciones = Frame(root)
        self._frameOpciones.config(bg="#6fb98f")
        self._frameOpciones.pack(fill='x')

        #Frame principal para las opciones de las operaciones
        self._framePrincipal = Frame(root)
        self._framePrincipal.config(bg="#004445", height='400')
        self._framePrincipal.pack(fill='x')

        #Frame utilizado para los autómatas guardados
        self._frameGuardado = Frame(root)
        self._frameGuardado.config(bg="#2c7873", height='200')
        self._frameGuardado.pack(fill='x')

        #Variables de interes para la opción ER
        self._ERBotonesGuardado = []
        self._ERGuardadoSeleccionado = -1

        #Variables de interes para la opción de AFN's
        self._AFNSimbolo1 = None
        self._AFNSimbolo2 = None
        self._AFNGuardadoCargado1 = None
        self._AFNGuardadoCargado2 = None
        self._AFNguardadoSeleccionado = -1
        self._AFNBotonesGuardado = []

        #Variables de interes para la opción de Graficar
        self._GraficarSeleccionado = None

        self._framesOperaciones = [self._crearFrameER(), self._crearFrameAFN(), self._crearFrameAFD(), self._crearFrameGraficar(), self._crearFrameGuardados()]

        self._botonOpcionesActual = None
        self._operacionActual = None

        self._crearBotonesOpciones()

        root.mainloop()

    def _crearFrameER(self):
        frame1=Frame(self._framePrincipal)
        frame1.config(bg="#004445")
        
        label2=Label(frame1 , text="Ingreso de una Expresión Regular:", font=("Helvetica",16,"bold"))
        label2.grid(row=0,column=0,sticky="e",padx=10, pady=10, columnspan=2) 
        label2.config(bg="#004445", fg='white')
        
        CT1=Entry(frame1)
        CT1.config(fg='#434e52', width=45)
        CT1.grid(row=1,column=0,sticky="w",padx=10, pady=10, columnspan=2)    

        label3=Label(frame1 , text="Generar:")
        label3.grid(row=2,column=0,sticky="w",padx=10, pady=10) 
        label3.config(bg="#004445", fg='white')
        
        Boton1= Button(frame1, text="AFN", command="")
        Boton1.grid(row=3,column=0,sticky="n",padx=10, pady=10)
        Boton1.config(command=lambda: self._logica.opcionGenerarDeER('AFN', CT1.get(), self._ERGuardadoSeleccionado))
        Boton1.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')
        
        Boton2=Button(frame1, text="AFD", command="")
        Boton2.grid(row=3,column=1,sticky="n",padx=10, pady=10)
        Boton2.config(state='disable', activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')
                      
        label4=Label(frame1 , text="Guardar en:")
        label4.grid(row=2,column=2,sticky="n",padx=10, pady=10) 
        label4.config(bg="#004445", fg='white')
                     
        Boton3= Button(frame1, text="Automata 1", command=lambda: self.opcionGuardadoSeleccionada(0,'ER'))
        Boton3.grid(row=3,column=2,sticky="n",padx=10, pady=10)
        Boton3.config(bg="#004445", fg='white', activeforeground='#004445')
        
        Boton4=Button(frame1, text="Automata 2", command=lambda: self.opcionGuardadoSeleccionada(1,'ER'))
        Boton4.grid(row=3,column=3,sticky="n",padx=10, pady=10)
        Boton4.config(bg="#004445", fg='white', activeforeground='#004445')
        
        Boton5= Button(frame1, text="Automata 3", command=lambda: self.opcionGuardadoSeleccionada(2,'ER'))
        Boton5.grid(row=3,column=4,sticky="n",padx=10, pady=10)
        Boton5.config(bg="#004445", fg='white', activeforeground='#004445')

        self._ERBotonesGuardado = [Boton3, Boton4, Boton5]
        
        return frame1  

    def _crearFrameAFN(self):

        opcionesGuardado = ['', 'Automata 1', 'Automata 2', 'Automata 3']

        self._AFNGuardadoCargado1 = StringVar()
        self._AFNGuardadoCargado1.set(opcionesGuardado[0])

        self._AFNGuardadoCargado2 = StringVar()
        self._AFNGuardadoCargado2.set(opcionesGuardado[0])

        frame2=Frame(self._framePrincipal)
        frame2.config(bg="#004445", height=400)
        
        label6=Label(frame2 , text="Generador Basico de AFN's")
        label6.grid(row=0,column=0,padx=10, pady=10, columnspan=2, sticky='w') 
        label6.config(bg="#004445", font=("Helvetica",16,"bold"), fg='white')
        
        label7=Label(frame2 , text="Ingresa: (simbolos)")
        label7.grid(row=1,column=0,padx=10, pady=10, sticky='w') 
        label7.config(bg="#004445", fg='white')
        
        self._AFNSimbolo1= Entry(frame2)
        self._AFNSimbolo1.grid(row=2,column=0,sticky="e",padx=10, pady=10)  
        
        self._AFNSimbolo2=Entry(frame2)
        self._AFNSimbolo2.grid(row=2,column=1,sticky="e",padx=10, pady=10)  
        
        label7=Label(frame2 , text="Cargar: (autómatas)")
        label7.grid(row=1,column=2,sticky="e",padx=10, pady=10) 
        label7.config(bg="#004445", fg='white')
                      
        cargar1 = OptionMenu(frame2, self._AFNGuardadoCargado1 , *opcionesGuardado)
        cargar1.grid(row=2,column=2,sticky="w",padx=10, pady=10)
        cargar1.config(activebackground="#004445", relief='flat', activeforeground='white', width=10, bg='#6fb98f', fg='white')
        
        cargar2 = OptionMenu(frame2, self._AFNGuardadoCargado2 , *opcionesGuardado)
        cargar2.grid(row=2,column=3,sticky="w",padx=10, pady=10)
        cargar2.config(activebackground="#004445", relief='flat', activeforeground='white', width=10, bg='#6fb98f', fg='white')

        Boton8= Button(frame2, text="AFN Basico")
        Boton8.grid(row=3,column=0,sticky="n",padx=10, pady=10)
        Boton8.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
        Boton8.config(command=lambda:self._logica.operacionAFN('α'))
        
        Boton9= Button(frame2, text="Cerradura positiva")
        Boton9.grid(row=4,column=0,sticky="n",padx=10, pady=10)
        Boton9.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')  
        Boton9.config(command=lambda:self._logica.operacionAFN('⁺'))
        
        Boton10= Button(frame2, text="Cerradura de Kleene")
        Boton10.grid(row=5,column=0,sticky="n",padx=10, pady=10)
        Boton10.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
        Boton10.config(command=lambda:self._logica.operacionAFN('*'))

        Boton11= Button(frame2, text="Opcional")
        Boton11.grid(row=3,column=1,sticky="n",padx=10, pady=10)
        Boton11.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
        Boton11.config(command=lambda:self._logica.operacionAFN('?'))
        
        Boton12= Button(frame2, text="Union")
        Boton12.grid(row=4,column=1,sticky="n",padx=10, pady=10)
        Boton12.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
        Boton12.config(command=lambda:self._logica.operacionAFN('|'))
        
        Boton13= Button(frame2, text="Concatenacion")
        Boton13.grid(row=5,column=1,sticky="n",padx=10, pady=10)
        Boton13.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
        Boton13.config(command=lambda:self._logica.operacionAFN('°'))
                       
        label7=Label(frame2 , text="Guardar en:")
        label7.grid(row=3,column=2,sticky="w",padx=10, pady=10) 
        label7.config(bg="#004445", fg='white')
                     
        Boton14= Button(frame2, text="Automata 1", command=lambda: self.opcionGuardadoSeleccionada(0,'AFN'))
        Boton14.grid(row=4,column=2,sticky="n",padx=10, pady=10)
        Boton14.config(bg="#004445", fg='white', activeforeground='#004445')
        
        Boton15=Button(frame2, text="Automata 2", command=lambda: self.opcionGuardadoSeleccionada(1,'AFN'))
        Boton15.grid(row=4,column=3,sticky="w",padx=10, pady=10)
        Boton15.config(bg="#004445", fg='white', activeforeground='#004445')
        
        Boton16= Button(frame2, text="Automata 3", command=lambda: self.opcionGuardadoSeleccionada(2,'AFN'))
        Boton16.grid(row=4,column=4,sticky="n",padx=10, pady=10)
        Boton16.config(bg="#004445", fg='white', activeforeground='#004445')

        self._AFNBotonesGuardado = [Boton14, Boton15, Boton16]

        return frame2

    def _crearFrameAFD(self):
        frame3=Frame(self._framePrincipal)
        frame3.config(bg="#0F9D58")

    def _crearFrameGraficar(self):

        opcionesGuardado = ['Automata 1', 'Automata 2', 'Automata 3']

        self._GraficarSeleccionado = StringVar()
        self._GraficarSeleccionado.set(opcionesGuardado[0])

        frame4=Frame(self._framePrincipal)
        frame4.config(bg="#004445")
        
        label21=Label(frame4 , text="Graficador de Automatas")
        label21.grid(row=0,column=0,sticky="w",padx=10, pady=10, columnspan=2) 
        label21.config(bg="#004445", fg='white', font=("Helvetica",16,"bold"))    
                       
        label20=Label(frame4 , text="Seleccionar:")
        label20.grid(row=1,column=0,sticky="w",padx=10, pady=10) 
        label20.config(bg="#004445", fg='white')
        
        cargar1 = OptionMenu(frame4, self._GraficarSeleccionado, *opcionesGuardado)
        cargar1.grid(row=2,column=0,sticky="w",padx=10, pady=10)
        cargar1.config(activebackground="#004445", relief='flat', activeforeground='white', width=10, bg='#6fb98f', fg='white')
        
        Boton7= Button(frame4, text="Graficar")
        Boton7.config(command=lambda:self._logica.opcionGraficar(int(self._GraficarSeleccionado.get()[len(self._GraficarSeleccionado.get())-1])-1))
        Boton7.grid(row=2,column=1,sticky="n",padx=10, pady=10)
        Boton7.config(bg="#004445", fg='white', activeforeground='#004445', width=30)

        return frame4

    def _crearFrameGuardados(self):

        frame1=Frame(self._frameGuardado)
        frame1.config(bg="#2c7873", height=200)
        frame1.pack(fill='both')

        label4=Label(frame1 , text="Guardados:")
        label4.grid(row=4,column=0,sticky="n",padx=10, pady=10,) 
        label4.config(bg="#2c7873", fg='white', font=("Helvetica",16,"bold"))
        
        CT2=Entry(frame1)
        CT2.insert(0, 'Autómata 1')
        CT2.grid(row=5,column=0,sticky="e",padx=10, pady=10)    

        CT3=Entry(frame1)
        CT3.insert(0, 'Autómata 2')
        CT3.grid(row=5,column=1,sticky="e",padx=10, pady=10)    

        CT4=Entry(frame1)
        CT4.insert(0, 'Autómata 3')
        CT4.grid(row=5,column=2,sticky="e",padx=10, pady=10)  

        CT5=Entry(frame1)
        CT5.grid(row=4,column=4,sticky="e",padx=10, pady=10)  

        Boton5= Button(frame1, text="Borrar", command="")
        Boton5.grid(row=5,column=4,sticky="n",padx=10, pady=10)
        Boton5.config(activebackground="#2c7873", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')

        return frame1

    def _crearBotonesOpciones(self):

        botonER= Button(self._frameOpciones, text="Expresion Regular", width=22, pady=5, justify='center')
        botonER.config(command=lambda: self.opcionPresionada(botonER,"ER"))
        botonER.config(bg="#6fb98f", fg='white', relief='raised', bd=0)
        botonER.config(activebackground="#2c7873", activeforeground='white')
        botonER.grid(row=0, column=0)

        botonAFN= Button(self._frameOpciones, text="AFN", width=22, pady=5, justify='center')
        botonAFN.config(command=lambda: self.opcionPresionada(botonAFN,"AFN"))
        botonAFN.config(bg="#6fb98f", fg='white', relief='flat', bd=0)
        botonAFN.config(activebackground="#2c7873", activeforeground='white')
        botonAFN.grid(row=0, column=1)

        botonAFD= Button(self._frameOpciones, text="AFD", width=22, pady=5, justify='center')
        botonAFD.config(command=lambda:self.opcionPresionada(botonAFD,"AFD"))
        botonAFD.config(bg="#6fb98f", fg='white', relief='flat', bd=0, state='disable')
        botonAFD.config(activebackground="#2c7873", activeforeground='white')
        botonAFD.grid(row=0, column=2)

        botonGraficar= Button(self._frameOpciones, text="Graficar",width=22, pady=5, justify='center')
        botonGraficar.config(command=lambda: self.opcionPresionada(botonGraficar,"G"))
        botonGraficar.config(bg="#6fb98f", fg='white', relief='flat', bd=0)
        botonGraficar.config(activebackground="#2c7873", activeforeground='white')
        botonGraficar.grid(row=0, column=3)

    # Getters

    def getFramesOperaciones(self):
        return self._framesOperaciones

    def getAFNSimbolo1(self):
        return self._AFNSimbolo1.get()

    def getAFNSimbolo2(self):
        return self._AFNSimbolo2.get()

    def getAFNGuardadoCargado1(self):
        if self._AFNGuardadoCargado1.get() == '':
            return -1
        else:
            return int(self._AFNGuardadoCargado1.get()[len(self._AFNGuardadoCargado1.get())-1]) - 1

    def getAFNGuardadoCargado2(self):
        if self._AFNGuardadoCargado2.get() == '':
            return -1
        else:
            return int(self._AFNGuardadoCargado2.get()[len(self._AFNGuardadoCargado2.get())-1]) - 1

    def getAFNguardadoSeleccionado(self):
        return self._AFNguardadoSeleccionado

    # Setters

    def setAFNGuardadoSeleccionado(self, seleccion):
        self._AFNguardadoSeleccionado = seleccion

    # Manejo Eventos

    def opcionPresionada(self, opcion, nombre):

            opciones = {'ER':0, 'AFN':1, 'AFD':2, 'G':3}
            padDic = {'ER':109, 'AFN':56, 'G':129.5}

            if self._botonOpcionesActual != None:
                self._botonOpcionesActual.config(bg="#6fb98f", fg='white', activebackground="#2c7873", activeforeground='white')
            
            opcion.config(bg='#ffd800', fg='#434e52',activebackground="#ffd800", activeforeground='#434e52')
            self._botonOpcionesActual = opcion

            if self._operacionActual != None:
                self._operacionActual.pack_forget()

            self._operacionActual = self._framesOperaciones[opciones[nombre]]
            self._operacionActual.pack(fill='both', pady=padDic[nombre])

    def opcionGuardadoSeleccionada(self, seleccion, seccion):

        if seccion == 'AFN':
            if self._AFNguardadoSeleccionado >= 0:
                self._AFNBotonesGuardado[self._AFNguardadoSeleccionado].config(bg="#004445", fg='white', activeforeground='#004445', activebackground='white')

            self._AFNBotonesGuardado[seleccion].config(bg="#2c7873", fg='white', activebackground='#2c7873', activeforeground='white')
            self._AFNguardadoSeleccionado = seleccion

        if seccion == 'ER':
            if self._ERGuardadoSeleccionado >= 0:
                self._ERBotonesGuardado[self._ERGuardadoSeleccionado].config(bg="#004445", fg='white', activeforeground='#004445', activebackground='white')

            self._ERBotonesGuardado[seleccion].config(bg="#2c7873", fg='white', activebackground='#2c7873', activeforeground='white')
            self._ERGuardadoSeleccionado = seleccion