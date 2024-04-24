from tkinter import *
import requests
import math
from tkinter import ttk, messagebox
temp=0
wind_speed=0
humidity=0
pressure=0
description="clear"
punto_rocio=0
ciudad=""

descripcion_en_espanol={}
    
#Barra de progreso
ventana2=None
barra_progreso=None
porcentaje_etiqueta=None
progreso_ventana=None
def generar_pdf():
 global humidity
 global temp
 global wind_speed
 global pressure
 global description
 global punto_rocio
 global descripcion_en_espanol
 global ciudad

 n=2 #n es la cantidad de digitó decimales que desea

 print("Guardar en PDF")
 archivo=open("estadísticas.pdf","w+")
 archivo.write("Estadísticas climáticas\n\n")
 archivo.write(f"Descripción: {descripcion_en_espanol}\n")
 archivo.write(f"Humedad: {round(humidity,n)}%\n")
 archivo.write(f"velocidad del viento: {round(wind_speed,n)}m/s\n") # round(número,cantidad de decimales que desea móstrar)
 archivo.write(f"presión: {round(pressure,n)}hPa\n")
 archivo.write(f"punto de rocío: {round(punto_rocio,n)}\n")
 archivo.close()

def generar_csv():
 global humidity
 global temp
 global wind_speed
 global pressure
 global description
 global punto_rocio
 global descripcion_en_espanol

 n=2 #n es la cantidad de digitó decimales que desea

 print("Generar Archivo CSV")
 archivo=open("estadísticas.csv","w+")
 archivo=open("estadísticas.csv","w+")
 archivo.write("Estadísticas climáticas\n\n")
 archivo.write(f"Descripción: {descripcion_en_espanol}\n")
 archivo.write(f"Humedad: {round(humidity,n)}%\n")
 archivo.write(f"velocidad del viento: {round(wind_speed,n)}m/s\n") # round(número,cantidad de decimales que desea móstrar)
 archivo.write(f"presión: {round(pressure,n)}hPa\n")
 archivo.write(f"punto de rocío: {round(punto_rocio,n)}\n")
 archivo.close()

def campo_vacio():
   global ciudad
   global ventana2
   if not ciudad: #si no se llenó el campo de ciudad
       ventana2=Tk()
      # ventana2.overrideredirect(True)
       ventana2.title("Error de busqueda")
       ventana2.geometry("500x100+500+250")
       ventana2.overrideredirect(True) #elimina la barra de titulo
       barra_titul=Frame(ventana2,bg="black")
       barra_titul.pack(fill="x")
       ventana2.resizable(False, False) 
       ventana2.config(bg="black")
       texto2 = Label(ventana2, text="Error. Campo de la ciudad vacío, digite por favor la información", font=("arial", 12, "bold"),fg="#30FD1B",bg="black")
       texto2.place(x=0, y=0)
       texto2 = Label(ventana2, text="para continuar.", font=("arial", 12, "bold"),fg="#30FD1B",bg="black")
       texto2.place(x=0, y=30)
   else:
       ventana2.destroy()
def actualizar_progreso():
        # Obtener el valor actual de la barra de progreso
        global barra_progreso
        global porcentaje_etiqueta
        global progreso_ventana
        valor_actual = barra_progreso["value"]
        
        # auemnto el valor de la barra de progreso
        if valor_actual < 100:

            barra_progreso["value"] = valor_actual + 10
            
            ## calcular y mostrar el porcentaje de progreso
            porcentaje = barra_progreso["value"]
            porcentaje_etiqueta.config(text=f"{porcentaje}%")
            
            progreso_ventana.update_idletasks()
            progreso_ventana.after(60, actualizar_progreso)
        else:
            progreso_ventana.destroy() # para cerar la ventana de progreso
        
def obtener_datos():
      # ventana que muestra el progreso
    global progreso_ventana
    progreso_ventana = Toplevel(ventana)
    progreso_ventana.title("TU PROGRESO")
    progreso_ventana.geometry("400x100+1200+200")

    global barra_progreso
    barra_progreso = ttk.Progressbar(progreso_ventana, orient=HORIZONTAL, length=250, mode='determinate')
    barra_progreso.pack(pady=10)
    
    # para mostrar el porcentaje
    global porcentaje_etiqueta
    porcentaje_etiqueta = Label(progreso_ventana, text="0%", font=("Helvetica", 12))
    porcentaje_etiqueta.pack()
    
    # Inicializar el progreso de la barra
    barra_progreso["maximum"] = 100
    barra_progreso["value"] = 0
    
    ciudad = texto.get()
    if ciudad:
       if ventana2!=None:
         ventana2.destroy()
    else:
       campo_vacio()
    api_key = "2e5a99bb31e2c59e130187ac05fe8675"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"
    res = requests.get(url)
    actualizar_progreso()
    # Verificar el estado de la respuesta
    if res.status_code == 200:
        data = res.json()
        
        b = 17.27
        c = 237.7
        # Extraer datos meteorológicos
        global temp 
        temp=data["main"]["temp"]
        global wind_speed 
        wind_speed= data["wind"]["speed"]
        global humidity
        humidity= data["main"]["humidity"]
        global pressure
        pressure = data["main"]["pressure"]
        global description 
        description= data["weather"][0]["description"]
        global punto_rocio 
        punto_rocio=math.log(humidity/100) + b*(temp)/(c + temp)
        
        
        #diccionario para que la descipcion salga en español
        descripciones_traduccion = {
        "clear sky": "cielo despejado",
        "few clouds": "pocas nubes",
        "scattered clouds": "nubes dispersas",
        "broken clouds": "nubes rotas",
        "shower rain": "lluvia de chubascos",
        "rain": "lluvia",
        "thunderstorm": "tormenta eléctrica",
        "snow": "nieve",
        "mist": "neblina",
        "overcast clouds": "cielo nublado",
        "light rain": "lluvia ligera",
        "moderate rain": "lluvia moderada",
        "heavy intensity rain": "lluvia intensa",
        "very heavy rain": "lluvia muy intensa",
        "extreme rain": "lluvia extrema",
        "freezing rain": "lluvia helada",
        "light snow": "nieve ligera",
        "snow": "nieve",
        "heavy snow": "nieve intensa",
        "sleet": "aguanieve",
        "light shower sleet": "aguanieve ligera",
        "shower sleet": "aguanieve",
        "light rain and snow": "lluvia y nieve ligera",
        "rain and snow": "lluvia y nieve",
        "light shower snow": "nevada ligera",
        "shower snow": "nevada",
        "heavy shower snow": "nevada intensa",
        "smoke": "humo",
        "haze": "calima",
        "sand/dust whirls": "torbellino de arena/polvo",
        "fog": "niebla",
        "sand": "arena",
        "dust": "polvo",
        "volcanic ash": "ceniza volcánica",
        "squalls": "ráfagas",
        "tornado": "tornado",
        "tropical storm": "tormenta tropical",
        "hurricane": "huracán",
        "cold": "frío",
        "hot": "caliente",
        "windy": "ventoso",
        "hail": "granizo"
}       
        descripcion_en_ingles = data["weather"][0]["description"]

        # traducir la descripción del clima al español
        global descripcion_en_espanol
        descripcion_en_espanol = descripciones_traduccion.get(descripcion_en_ingles, descripcion_en_ingles)

        #  asignar la descripción en español a la etiqueta correspondiente
        TEMPERATURA.config(text=f"{temp}°C")
        HUMEDAD.config(text=f"{humidity}%")
        VELOCIDAD_VIENTO.config(text=f"{wind_speed} m/s")
        PRESION.config(text=f"{pressure} hPa")
        DESCRIPCION.config(text=descripcion_en_espanol)
        ROCIO.config(text=f"{punto_rocio:.2f}")
    else:
        # si la respuesta no es exitosa muestra el código de error
        error_message = res.json().get('message', 'Error desconocido')
        print(f"Error: {res.status_code} - {error_message}")
def crear_menu(event):
    # Crear un menú desplegable
    menu = Menu(ventana, tearoff=0)
    menu.add_command(label="Generar Estadísticas", command=lambda: print("Generar Estadísticas"))
    
    menu.add_command(label="Generar Archivo CSV", command=generar_csv)
    
    menu.add_command(label="Guardar en PDF", command= generar_pdf)
    # Mostrar el menú
    menu.post(event.x_root, event.y_root)
    
  
ventana = Tk()
ventana.title("USC Weather App")
ventana.geometry("910x500")
ventana.resizable(False, False)

# imagen de búsqueda en la cajita
buscar_imagen = PhotoImage(file="cajita de texto.png")
mi_imagen = Label(ventana, image=buscar_imagen)
mi_imagen.place(x=20, y=22)

# entrada de texto
texto = Entry(ventana, justify="center", width=17, font=("poppins", 20, "bold"), bg="#404040", border=0, fg="white")
texto.place(x=50, y=40)
texto.focus()

# botón de búsqueda
buscar_icono = PhotoImage(file="icono_buscar.png")
my_imagen = Button(ventana, image=buscar_icono, borderwidth=0, cursor="hand2", bg="#404040", command=obtener_datos)
my_imagen.place(x=400, y=34)

# botón  que genera el menú desplegable
boton_guardar = Button(ventana, text="GENERAR", font=("arial", 12, 'bold'), width=20, height=1, bg="SpringGreen2")
boton_guardar.place(x=540, y=100)
boton_guardar.bind("<Button-1>", crear_menu)

# imagen del tiempo
logo_clima = PhotoImage(file="clima.png")
resized_logo = logo_clima.subsample(2, 2)
my_logo = Label(ventana, image=resized_logo)
my_logo.place(x=90, y=120)

# caja azul
caja_azul = PhotoImage(file="caja azul.png")
caja = Label(ventana, image=caja_azul)
caja.pack(padx=5, pady=5, side=BOTTOM)

# etiquetas para datos meteorológicos
label_temp = Label(ventana, text="HUMEDAD", font=("Helvetica", 12, 'bold'), fg="white", bg="#1ab5ef")
label_temp.place(x=100, y=400)

label_humd = Label(ventana, text="V_VIENTO", font=("Helvetica", 12, 'bold'), fg="white", bg="#1ab5ef")
label_humd.place(x=270, y=400)

label_viento = Label(ventana, text="PRESION ATM", font=("Helvetica", 12, 'bold'), fg="white", bg="#1ab5ef")
label_viento.place(x=450, y=400)

label_presion = Label(ventana, text="ROCIO", font=("Helvetica", 12, 'bold'), fg="white", bg="#1ab5ef")
label_presion.place(x=670, y=400)

# etiquetas para mostrar datos meteorológicos
TEMPERATURA = Label(ventana, font=("arial", 40, "bold"), fg="#ee666d")
TEMPERATURA.place(x=400, y=200)

DESCRIPCION = Label(ventana, font=("arial", 17, 'bold'))
DESCRIPCION.place(x=400, y=350)

HUMEDAD = Label(ventana, text="...", font=("arial", 18, "bold"), bg="#1ab5ef")
HUMEDAD.place(x=100, y=426)

VELOCIDAD_VIENTO = Label(ventana, text="...", font=("arial", 18, "bold"), bg="#1ab5ef")
VELOCIDAD_VIENTO.place(x=270, y=426)

PRESION = Label(ventana, text="...", font=("arial", 18, "bold"), bg="#1ab5ef")
PRESION.place(x=450, y=426)

ROCIO = Label(ventana, text="...", font=("arial", 18, "bold"), bg="#1ab5ef")
ROCIO.place(x=670, y=426)

# título de la aplicación
titulo = Label(ventana, text="METEOROLOGÍA MUNDIAL USC", font=("arial", 12, "bold"))
titulo.place(x=500, y=47)

ventana.mainloop()
