
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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, filedialog, Toplevel, Text, Scrollbar, VERTICAL, Y, END
from tkinter.ttk import Style, Frame

sns.set(style="whitegrid")


def cargar_csv():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        label_info["text"] = f"Archivo cargado: {filepath.split('/')[-1]}"
        btn_estadisticas["state"] = "normal"
        btn_clasificacion["state"] = "normal"
        btn_graficos["state"] = "normal"


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


def generar_graficos():
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x="País", y="Temperatura Promedio (°C)", palette="Set2")
        plt.title("Distribución de Temperaturas Promedio por País")
        plt.xticks(rotation=45)
        plt.show()

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="País", y="Eventos Climáticos Extremos (Frecuencia)", ci=None, palette="Set3")
        plt.title("Frecuencia de Eventos Climáticos Extremos por País")
        plt.xticks(rotation=45)
        plt.show()


# Configuración de la ventana principal
root = Tk()
root.title("Análisis Exploratorio de Datos")
root.geometry("600x400")
root.configure(bg="#e9ecef")

style = Style()
style.configure("TButton", font=("Arial", 12), padding=5, relief="flat")
style.configure("TLabel", font=("Arial", 12), background="#e9ecef", foreground="#333333")

frame = Frame(root, style="TFrame", padding=10)
frame.pack(fill="both", expand=True)

label_info = Label(frame, text="Cargue un archivo CSV para comenzar.", font=("Arial", 14), background="#e9ecef")
label_info.pack(pady=10)

btn_cargar = Button(frame, text="Cargar CSV", command=cargar_csv, font=("Arial", 12), bg="#17a2b8", fg="white", activebackground="#138496")
btn_cargar.pack(pady=5)

btn_estadisticas = Button(frame, text="Mostrar Estadísticas", state="disabled", command=mostrar_estadisticas, font=("Arial", 12), bg="#007bff", fg="white", activebackground="#0056b3")
btn_estadisticas.pack(pady=5)

btn_clasificacion = Button(frame, text="Clasificar por País", state="disabled", command=clasificar_por_pais, font=("Arial", 12), bg="#28a745", fg="white", activebackground="#1e7e34")
btn_clasificacion.pack(pady=5)

btn_graficos = Button(frame, text="Generar Gráficos", state="disabled", command=generar_graficos, font=("Arial", 12), bg="#ffc107", fg="black", activebackground="#e0a800")
btn_graficos.pack(pady=5)

root.mainloop()
