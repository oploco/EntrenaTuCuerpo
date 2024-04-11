import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from datetime import datetime

DATA_FILENAME = "Data/megaGymDataset.csv"
CRYPTOS = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 'Lido Staked Ether', 'USDC', 'Dogecoin', 'Cardano',
           'Avalanche', 'Shiba Inu']


def crear_grafico():
    nombre_archivo_csv = DATA_FILENAME

    df = pd.read_csv(nombre_archivo_csv)

    df.head()
    df.columns = df.columns.str.replace('Unnamed: 0', 'index')

    print(df.info)

    print(df.tail())

    print(df.isnull().sum())

    # Agrupar por ejecicio
    count_exercises = df.groupby(['BodyPart']).count()

    count_exercises = count_exercises.sort_values(by='index', ascending=False)
    print(count_exercises)

    # Crear una figura con un tamaño específico
    plt.figure(figsize=(10, 6))

    plt.barh( count_exercises.index,count_exercises.Title,color='orange')
    plt.xlabel('Ejercicios')
    plt.title('Variedad de ejercicios por parte del cuerpo ')
    plt.gca().invert_yaxis()  # Invertir el eje y para que la criptomoneda con el precio más alto esté arriba
    plt.tight_layout()
    plt.grid()
    plt.show()

    # agrupamos para rellenar los nulos por la media basado en su tipo, parte, equipo,nivel
    grouped_means = df.groupby(['Type', 'BodyPart', 'Equipment', 'Level'])['Rating'].transform('mean')

    # Rellena los valores nulos en la columna con la media
    df['Rating'].fillna(grouped_means, inplace=True)
    print(df['Rating'].unique())
    print(df['RatingDesc'].unique())

    # Función para asignar descripciones basadas en tramos de rating
    def assign_description(rating):
        if rating <= 3:
            return 'Low'
        elif 4 <= rating <= 7:
            return 'Medium'
        else:
            return 'High'

    # Aplica las descripciones al rating
    df['RatingDesc'] = df['Rating'].apply(assign_description)

    df[(df['Equipment'].isna()) & (df['BodyPart'] == 'Abdominals')]

    print(df[df['Equipment'].isna()])

    # Rellenar las desc vacias con el Title
    df['Desc'].fillna(df['Title'], inplace=True)

    """
    df.set_index(df['fecha'])

    # Crear una figura con un tamaño específico
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#eafff3')

    # Graficar los datos
    ax.plot(df['fecha'], df['Precio'], color='orange')
    ax.set_facecolor('#eafff5')

    # Etiquetas de los ejes x e y
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio (USD)')

    # Escala lineal en el eje y
    ax.set_yscale('linear')

    # Título del gráfico
    ax.set_title(f'Precios de {moneda} en USD ({datetime.now().strftime("%H:%M")})')

    # Ajustar el diseño para evitar cortar las etiquetas
    plt.tight_layout()

    # Añadir leyenda
    ax.legend([moneda], loc='upper left', fontsize=10)

    # Añadir una cuadrícula de fondo para hacer más fácil la lectura de los valores exactos
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    # plt.setp(plt.xlabel, rotation=45, horizontalalignment='right')

    # Guardar el gráfico como imagen
    plt.savefig("./crypto/coin/static/graphs/" + moneda + ".png")
"""

if __name__ == "__main__":
    crear_grafico()