from tkinter import *

fuenteEncabezados = ("Helvetica",16,"bold")

botonActual = None
operacionActual = None

framePrincipal = None
frameGuardado = None
framesOperaciones = []

def crearFrameER():
    frame1=Frame(framePrincipal)
    frame1.config(bg="#004445")
    
    label2=Label(frame1 , text="Ingreso de una Expresión Regular:", font=fuenteEncabezados)
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
    Boton1.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')
    
    Boton2=Button(frame1, text="AFD", command="")
    Boton2.grid(row=3,column=1,sticky="n",padx=10, pady=10)
    Boton2.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')
                  
    label4=Label(frame1 , text="Guardar en:")
    label4.grid(row=2,column=2,sticky="n",padx=10, pady=10) 
    label4.config(bg="#004445", fg='white')
                 
    Boton3= Button(frame1, text="Automata 1", command="")
    Boton3.grid(row=3,column=2,sticky="n",padx=10, pady=10)
    Boton3.config(bg="#004445", fg='white')
    
    Boton4=Button(frame1, text="Automata 2", command="")
    Boton4.grid(row=3,column=3,sticky="n",padx=10, pady=10)
    Boton4.config(bg="#004445", fg='white')
    
    Boton5= Button(frame1, text="Automata 3", command="")
    Boton5.grid(row=3,column=4,sticky="n",padx=10, pady=10)
    Boton5.config(bg="#004445", fg='white')
    
    return frame1  

def crearFrameAFN():
    frame2=Frame(framePrincipal)
    frame2.config(bg="#004445")
       
    A1="Automata 1"
    A2="Automata 2"
    A3="Automata 3"
    
    label6=Label(frame2 , text="Generador Basico de AFN's")
    label6.grid(row=0,column=0,padx=10, pady=10, columnspan=2) 
    label6.config(bg="#004445", font=fuenteEncabezados, fg='white')
    
    label7=Label(frame2 , text="Ingresa: (simbolos)")
    label7.grid(row=1,column=0,padx=10, pady=10, sticky='w') 
    label7.config(bg="#004445", fg='white')
    
    CT6=Entry(frame2)
    CT6.grid(row=2,column=0,sticky="e",padx=10, pady=10)  
    
    CT7=Entry(frame2)
    CT7.grid(row=2,column=1,sticky="e",padx=10, pady=10)  
    
    label7=Label(frame2 , text="Cargar")
    label7.grid(row=0,column=2,sticky="e",padx=10, pady=10) 
    label7.config(bg="#004445")
                  
    """Cargar= ttk.Combobox(frame2)
    Cargar["values"]=(A1,A2,A3)
    Cargar.grid(row=1,column=3,sticky="e",padx=10, pady=10)
    Cargar.current(0)"""
    
    Boton7= Button(frame2, text="Cargar", command="")
    Boton7.grid(row=1,column=3,sticky="n",padx=10, pady=10, columnspan=2)
    Boton7.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')
    
    Boton8= Button(frame2, text="AFN Basico", command="")
    Boton8.grid(row=3,column=0,sticky="n",padx=10, pady=10)
    Boton8.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
    
    Boton9= Button(frame2, text="Cerradura positiva", command="")
    Boton9.grid(row=4,column=0,sticky="n",padx=10, pady=10)
    Boton9.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
    
    Boton10= Button(frame2, text="Cerradura de Kleene", command="")
    Boton10.grid(row=5,column=0,sticky="n",padx=10, pady=10)
    Boton10.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 

    Boton11= Button(frame2, text="Opcional", command="")
    Boton11.grid(row=3,column=1,sticky="n",padx=10, pady=10)
    Boton11.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
    
    Boton12= Button(frame2, text="Union", command="")
    Boton12.grid(row=4,column=1,sticky="n",padx=10, pady=10)
    Boton12.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
    
    Boton13= Button(frame2, text="Concatenacion", command="")
    Boton13.grid(row=5,column=1,sticky="n",padx=10, pady=10)
    Boton13.config(activebackground="#004445", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white') 
                   
    label7=Label(frame2 , text="Guardar en:")
    label7.grid(row=3,column=2,sticky="n",padx=10, pady=10, columnspan=3) 
    label7.config(bg="#0F9D58")
                 
    Boton14= Button(frame2, text="Automata 1", command="")
    Boton14.grid(row=4,column=2,sticky="n",padx=10, pady=10)
    Boton14.config(bg="#0F9D58")
    
    Boton15=Button(frame2, text="Automata 2", command="")
    Boton15.grid(row=4,column=3,sticky="n",padx=10, pady=10)
    Boton15.config(bg="#0F9D58")
    
    Boton16= Button(frame2, text="Automata 3", command="")
    Boton16.grid(row=4,column=4,sticky="n",padx=10, pady=10)
    Boton16.config(bg="#0F9D58")

    return frame2

def crearFrameAFD():
    frame3=Frame(framePrincipal)
    frame3.config(bg="#0F9D58")

def crearFrameGraficar():
    frame4=Frame(framePrincipal)
    frame4.config(bg="#0F9D58")
   
    A1="Automata 1"
    A2="Automata 2"
    A3="Automata 3"
    
    label21=Label(frame4 , text="Graficador de Automatas")
    label21.grid(row=0,column=0,sticky="n",padx=10, pady=10) 
    label21.config(bg="#0F9D58")    
                   
    label20=Label(frame4 , text="Seleccionar:")
    label20.grid(row=1,column=0,sticky="n",padx=10, pady=10) 
    label20.config(bg="#0F9D58")

    """Cargar= ttk.Combobox(frame4)
    Cargar["values"]=("Automata 1","Automata 2","Automata 3")
    Cargar.grid(row=2,column=0,sticky="e",padx=10, pady=10)
    Cargar.current(0)"""
    
    Boton7= Button(frame4, text="Cargar", command="")
    Boton7.grid(row=2,column=1,sticky="n",padx=10, pady=10)
    Boton7.config(bg="#0F9D58") 

    return frame4

def crearFrameGuardados():

    frame1=Frame(frameGuardado)
    frame1.config(bg="#2c7873", height=200)
    frame1.pack(fill='both')

    label4=Label(frame1 , text="Guardados:")
    label4.grid(row=4,column=0,sticky="n",padx=10, pady=10,) 
    label4.config(bg="#2c7873", fg='white', font=fuenteEncabezados)
                
    A1="Automata 1"
    A2="Automata 2"
    A3="Automata 3"
    
    CT2=Entry(frame1)
    CT2.insert(0, A1)
    CT2.grid(row=5,column=0,sticky="e",padx=10, pady=10)    

    CT3=Entry(frame1)
    CT3.insert(0, A2)
    CT3.grid(row=5,column=1,sticky="e",padx=10, pady=10)    

    CT4=Entry(frame1)
    CT4.insert(0, A3)
    CT4.grid(row=5,column=2,sticky="e",padx=10, pady=10)  

    CT5=Entry(frame1)
    CT5.grid(row=4,column=4,sticky="e",padx=10, pady=10)  

    Boton5= Button(frame1, text="Borrar", command="")
    Boton5.grid(row=5,column=4,sticky="n",padx=10, pady=10)
    Boton5.config(activebackground="#2c7873", relief='flat', activeforeground='white', width=15, bg='#6fb98f', fg='white')

    return frame1


def opcionPresionada(opcion, nombre):

    global botonActual, operacionActual
    opciones = {'ER':0, 'AFN':1, 'AFD':2, 'G':3}

    if botonActual != None:
        botonActual.config(bg="#6fb98f", fg='white', activebackground="#2c7873", activeforeground='white')
    
    opcion.config(bg='#ffd800', fg='#434e52',activebackground="#ffd800", activeforeground='#434e52')
    botonActual = opcion

    if operacionActual != None:
        operacionActual.pack_forget()

    operacionActual = framesOperaciones[opciones[nombre]]
    operacionActual.pack(fill='both')


root=Tk()
root.title("Analizador Lexico")
#root.resizable(width=False, height=False)
root.geometry("800x550")

#Frame utilizado para las opciones de los botones
frameOpciones = Frame(root)
frameOpciones.config(bg="#6fb98f")
frameOpciones.pack(fill='x')

#Frame principal para las opciones de las operaciones
framePrincipal = Frame(root)
framePrincipal.config(bg="#004445", height='400')
framePrincipal.pack(fill='x')

#Frame utilizado para los autómatas guardados
frameGuardado = Frame(root)
frameGuardado.config(bg="#2c7873", height='200')
frameGuardado.pack(fill='x')

framesOperaciones = [crearFrameER(), crearFrameAFN(), crearFrameAFD(), crearFrameGraficar(), crearFrameGuardados()]

"""            
frame0=Frame()
frame0.pack(side="bottom",fill="x")
frame0.config(bg="#4285F4")
frame0.config(width="800",height="275")  
Label(frame0, text="Instituto Politecnico Nacional \n\n Escuela Superior de Computo \n\n Unidad de Aprendizaje: Compiladores \n\n Alumnos: \n\n Oscar Perez \n\n Eduardo Valle",fg="Black",bg="#4285F4",font=("Comic Sans MS",15)).place(x=250,y=50)
"""

"""
    Colores:

        1. #004445
        2. #2c7873
        3. #6fb98f
        4. #ffd800
"""

botonER= Button(frameOpciones, text="Expresion Regular", width=22, pady=5, justify='center')
botonER.config(command=lambda: opcionPresionada(botonER,"ER"))
botonER.config(bg="#6fb98f", fg='white', relief='raised', bd=0)
botonER.config(activebackground="#2c7873", activeforeground='white')
botonER.grid(row=0, column=0)

botonAFN= Button(frameOpciones, text="AFN", width=22, pady=5, justify='center')
botonAFN.config(command=lambda: opcionPresionada(botonAFN,"AFN"))
botonAFN.config(bg="#6fb98f", fg='white', relief='flat', bd=0)
botonAFN.config(activebackground="#2c7873", activeforeground='white')
botonAFN.grid(row=0, column=1)

botonAFD= Button(frameOpciones, text="AFD", width=22, pady=5, justify='center')
botonAFD.config(command=lambda:opcionPresionada(botonAFD,"AFD"))
botonAFD.config(bg="#6fb98f", fg='white', relief='flat', bd=0)
botonAFD.config(activebackground="#2c7873", activeforeground='white')
botonAFD.grid(row=0, column=2)

botonGraficar= Button(frameOpciones, text="Graficar",width=22, pady=5, justify='center')
botonGraficar.config(command=lambda: opcionPresionada(botonGraficar,"G"))
botonGraficar.config(bg="#6fb98f", fg='white', relief='flat', bd=0)
botonGraficar.config(activebackground="#2c7873", activeforeground='white')
botonGraficar.grid(row=0, column=3)

root.mainloop()