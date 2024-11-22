import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, filedialog, Toplevel, Text, Scrollbar, VERTICAL, RIGHT, Y, END

# Configurar estilo para gráficos
sns.set(style="whitegrid")

# Función para cargar el archivo CSV
def cargar_csv():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        label_info["text"] = f"Archivo cargado: {filepath.split('/')[-1]}"
        btn_estadisticas["state"] = "normal"
        btn_clasificacion["state"] = "normal"
        btn_graficos["state"] = "normal"

# Mostrar estadísticas descriptivas generales
def mostrar_estadisticas():
    if df is not None:
        top = Toplevel(root)
        top.title("Estadísticas Descriptivas")

        
        estadisticas = df.describe().transpose()  

        # Generar descripciones dinámicas basadas en las columnas del resumen
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

        # Crear ventana con cuadro de texto
        text = Text(top, wrap="word", font=("Arial", 10))
        scrollbar = Scrollbar(top, orient=VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        # Mostrar cada columna con sus estadísticas
        for columna in estadisticas.index:
            text.insert(END, f"\n\n--- {columna} ---\n")
            for metric, value in estadisticas.loc[columna].items():
                descripcion = metricas_descripcion.get(metric, "Sin descripción")
                text.insert(END, f"{metric}: {value} ({descripcion})\n")

        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill=Y)



# Clasificar y mostrar datos por país
def clasificar_por_pais():
    if df is not None:
        top = Toplevel(root)
        top.title("Datos Clasificados por País")
        text = Text(top, wrap="word", font=("Arial", 10))
        scrollbar = Scrollbar(top, orient=VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        clasificados = df.sort_values(by=["País", "Año"])
        text.insert(END, clasificados.to_string())
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill=Y)

# Generar gráficos exploratorios
def generar_graficos():
    if df is not None:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x="País", y="Temperatura Promedio (°C)")
        plt.title("Distribución de Temperaturas Promedio por País")
        plt.xticks(rotation=45)
        plt.show()

       
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="País", y="Eventos Climáticos Extremos (Frecuencia)", ci=None)
        plt.title("Frecuencia de Eventos Climáticos Extremos por País")
        plt.xticks(rotation=45)
        plt.show()

# Configuración de la ventana principal
root = Tk()
root.title("Análisis Exploratorio de Datos")
root.geometry("600x400")

# Etiqueta para mostrar información del archivo cargado
label_info = Label(root, text="Cargue un archivo CSV para comenzar.", font=("Arial", 12))
label_info.pack(pady=10)

# Botón para cargar archivo
btn_cargar = Button(root, text="Cargar CSV", command=cargar_csv, font=("Arial", 12))
btn_cargar.pack(pady=5)

# Botones de análisis (deshabilitados inicialmente)
btn_estadisticas = Button(root, text="Mostrar Estadísticas", state="disabled", command=mostrar_estadisticas, font=("Arial", 12))
btn_estadisticas.pack(pady=5)

btn_clasificacion = Button(root, text="Clasificar por País", state="disabled", command=clasificar_por_pais, font=("Arial", 12))
btn_clasificacion.pack(pady=5)

btn_graficos = Button(root, text="Generar Gráficos", state="disabled", command=generar_graficos, font=("Arial", 12))
btn_graficos.pack(pady=5)

# Ejecutar la interfaz gráfica
root.mainloop()
