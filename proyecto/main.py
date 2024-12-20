
"""
Proyecto Big Data Clima
Plataforma de Big Data para la Visualización y Análisis del Clima Global  
Integrantes:
Christopher Briceño Arias,
Tiffany Arroyo Arias
Jose Ignacio Ramirez Solano
Garrett Jackson Gomez 
Zuñiga Redondo Mauricio 
"""
from tkinter import Tk, Button, Label, filedialog, Toplevel, Text, Scrollbar, VERTICAL, Y, END
from tkinter.ttk import Style, Frame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# cargar csv
def cargar_csv():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        label_info["text"] = f"Archivo cargado: {filepath.split('/')[-1]}"
        btn_estadisticas["state"] = "normal"
        btn_clasificacion["state"] = "normal"
        btn_graficos["state"] = "normal"
        btn_limpieza["state"] = "normal"
        btn_eliminar["state"] = "normal"
       
# eliminar csv
def eliminar_csv():
    global df
    df = None
    label_info["text"] = "Cargue un archivo CSV para comenzar."
    btn_estadisticas["state"] = "disabled"
    btn_clasificacion["state"] = "disabled"
    btn_graficos["state"] = "disabled"
    btn_limpieza["state"] = "disabled"
    btn_eliminar["state"] = "disabled"

# Estadisticas descriptivas
def mostrar_estadisticas():
    if df is not None:
        top = Toplevel(root)
        top.title("Estadísticas Descriptivas")
        top.configure(bg="#f4f4f4")

        estadisticas = df.describe().transpose()
        metricas_descripcion = {
            "count": "Cantidad de valores",
            "mean": "Promedio de los valores",
            "std": "Desviación estándar (dispersión)",
            "min": "Valor más bajo registrado",
            "25%": "Percentil 25 (valor bajo típico)",
            "50%": "Mediana (valor central)",
            "75%": "Percentil 75 (valor alto típico)",
            "max": "Valor más alto registrado",
        }

        text = Text(top, wrap="word", font=("Arial", 10), bg="#ffffff", fg="#333333", bd=0, relief="flat")
        scrollbar = Scrollbar(top, orient=VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        for columna in estadisticas.index:
            text.insert(END, f"\n\n--- {columna} ---\n")
            for metric, value in estadisticas.loc[columna].items():
                descripcion = metricas_descripcion.get(metric, "Sin descripción")
                text.insert(END, f"{metric}: {value} ({descripcion})\n")

        text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill=Y)

# Clasificar por pais
def clasificar_por_pais():
    if df is not None:
        top = Toplevel(root)
        top.title("Datos Clasificados por País")
        top.configure(bg="#f4f4f4")

        text = Text(top, wrap="word", font=("Arial", 10), bg="#ffffff", fg="#333333", bd=0, relief="flat")
        scrollbar = Scrollbar(top, orient=VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        clasificados = df.sort_values(by=["País", "Año"])
        text.insert(END, clasificados.to_string())

        text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill=Y)


#  Submenu para los graficos
def submenu_graficos():
    if df is not None:
        top = Toplevel(root)
        top.title("Seleccionar Gráfico")
        top.geometry("300x300")
        top.configure(bg="#f4f4f4")
        
        label = Label(top, text="Seleccione el gráfico a generar:", font=("Arial", 12), bg="#f4f4f4", fg="#333333")
        label.pack(pady=10)

        btn_boxplot = Button(top, text="Temperatura Promedio", command=lambda: generar_boxplot(top), font=("Arial", 12), bg="#007bff", fg="white", activebackground="#0056b3")
        btn_boxplot.pack(pady=5)

        btn_barplot = Button(top, text="Frecuencia de Eventos Climáticos Extremos", command=lambda: generar_barplot(top), font=("Arial", 12), bg="#28a745", fg="white", activebackground="#1e7e34")
        btn_barplot.pack(pady=5)

        btn_precip = Button(top, text="Precipitación Promedio", command=lambda: generar_precipitacion(top), font=("Arial", 12), bg="#ffc107", fg="black", activebackground="#e0a800")
        btn_precip.pack(pady=5)

        btn_humedad = Button(top, text="Humedad Promedio", command=lambda: generar_humedad(top), font=("Arial", 12), bg="#6f42c1", fg="white", activebackground="#5a3791")
        btn_humedad.pack(pady=5)

        btn_close = Button(top, text="Cerrar", command=top.destroy, font=("Arial", 12), bg="#dc3545", fg="white", activebackground="#c82333")
        btn_close.pack(pady=10)

# Temperatura Promedio
def generar_boxplot(window):
    window.destroy()  
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x="País", y="Temperatura Promedio (°C)", palette="Set2")
        plt.title("Distribución de Temperaturas Promedio por País")
        plt.xticks(rotation=45)
        plt.show()


# Eventos Climaticos Extremos Frecuencia
def generar_barplot(window):
    window.destroy() 
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="País", y="Eventos Climáticos Extremos (Frecuencia)", ci=None, palette="Set3")
        plt.title("Frecuencia de Eventos Climáticos Extremos por País")
        plt.xticks(rotation=45)
        plt.show()

# Precipitacion % por pais
def generar_precipitacion(window):
    window.destroy() 
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="País", y="Precipitación Promedio (mm)", ci=None, palette="Blues")
        plt.title("Precipitación Promedio por País")
        plt.xticks(rotation=45)
        plt.show()

# Humedad % por pais
def generar_humedad(window):
    window.destroy()  
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="País", y="Humedad Promedio (%)", ci=None, palette="Greens")
        plt.title("Humedad Promedio por País")
        plt.xticks(rotation=45)
        plt.show()

# Eliminan nulos y se ordenan por pais y años
def limpiar_datos():
    global df
    if df is not None:
        
        df_limpio = df.dropna()  
        df_limpio = df_limpio.sort_values(by=["País", "Año"])  

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
        if save_path:
            df_limpio.to_csv(save_path, index=False)
            label_info["text"] = f"Datos limpiados y guardados en: {save_path.split('/')[-1]}"

# Ventana Main 
root = Tk()
root.title("Análisis Exploratorio de Datos")
root.geometry("600x400")
root.configure(bg="#e9ecef")

style = Style()
style.configure("TButton", font=("Arial", 12), padding=5, relief="flat")
style.configure("TLabel", font=("Arial", 12), background="#e9ecef", foreground="#333333")


frame = Frame(root, style="TFrame", padding=10)
frame.place(relx=0.5, rely=0.5, anchor="center")  


label_info = Label(frame, text="Cargue un archivo CSV para comenzar.", font=("Arial", 14), background="#e9ecef")
label_info.grid(row=0, column=0, columnspan=2, pady=10)

btn_cargar = Button(frame, text="Cargar CSV", command=cargar_csv, font=("Arial", 12), bg="#17a2b8", fg="white", activebackground="#138496")
btn_cargar.grid(row=1, column=0, pady=5, padx=5)

btn_eliminar = Button(frame, text="Eliminar CSV", state="disabled", command=eliminar_csv, font=("Arial", 12), bg="#dc3545", fg="white", activebackground="#c82333")
btn_eliminar.grid(row=1, column=1, pady=5, padx=5)

btn_estadisticas = Button(frame, text="Mostrar Estadísticas", state="disabled", command=mostrar_estadisticas, font=("Arial", 12), bg="#007bff", fg="white", activebackground="#0056b3")
btn_estadisticas.grid(row=2, column=0, pady=5, padx=5)

btn_clasificacion = Button(frame, text="Clasificar por País", state="disabled", command=clasificar_por_pais, font=("Arial", 12), bg="#28a745", fg="white", activebackground="#1e7e34")
btn_clasificacion.grid(row=2, column=1, pady=5, padx=5)

btn_graficos = Button(frame, text="Generar Gráficos", state="disabled", command=submenu_graficos, font=("Arial", 12), bg="#ffc107", fg="black", activebackground="#e0a800")
btn_graficos.grid(row=3, column=0, pady=5, padx=5)

btn_limpieza = Button(frame, text="Limpieza de Datos", state="disabled", command=limpiar_datos, font=("Arial", 12), bg="#6f42c1", fg="white", activebackground="#5a3791")
btn_limpieza.grid(row=3, column=1, pady=5, padx=5)

root.mainloop()