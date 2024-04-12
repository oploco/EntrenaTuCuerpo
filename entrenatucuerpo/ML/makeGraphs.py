import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from datetime import datetime
import plotly.express as px
import plotly.io as pio

DATA_FILENAME = "Data/megaGymDataset.csv"
GROUPS = ['BodyPart', 'Level', 'Type', 'Equipment']

#global df,new_df

def normalizarDatos():
    global df,new_df

    nombre_archivo_csv = DATA_FILENAME

    df = pd.read_csv(nombre_archivo_csv)

    df.head()
    df.columns = df.columns.str.replace('Unnamed: 0', 'index')

    # agrupamos para rellenar los nulos por la media basado en su tipo, parte, equipo,nivel
    grouped_means = df.groupby(['Type', 'BodyPart', 'Equipment', 'Level'])['Rating'].transform('mean')

    # Rellena los valores nulos en la columna con la media
    df['Rating'].fillna(grouped_means, inplace=True)
    #print(df['Rating'].unique())
    #print(df['RatingDesc'].unique())

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

    #print('nulos:', df[df['Equipment'].isna()])

    # Rellenar las desc vacias con el Title
    df['Desc'].fillna(df['Title'], inplace=True)

    # Rellena con 'Body' las filas donde 'Equipment' tiene valores NaN y 'BodyPart' es 'Abdominals'
    df.loc[(df['Equipment'].isna()) & (df['BodyPart'] == 'Abdominals'), 'Equipment'] = 'Body'

    # limpio en un neuvo DF
    new_df = df.drop(['index', 'Desc', 'Rating', 'RatingDesc'], axis=1)

def crear_grafico():
    global df, new_df

    df['Level'].unique()

    # Itera sobre cada grupo y crea un gráfico para cada uno
    for group in GROUPS:
        # Agrupar por ejecicio
        group_data = df.groupby(group).count()
        group_data = group_data.sort_values(by='index', ascending=False)

        # Crea un gráfico de barras para el grupo actual
        plt.figure(figsize=(10, 6))

        plt.bar( group_data.index,group_data.Title,color='orange')
        plt.xlabel(group)
        plt.title(f'Variedad de ejercicios por {group} ')
        plt.xticks(rotation=45)  # Rota las etiquetas del eje x para una mejor visualización
        #plt.gca().invert_yaxis()  # Invertir el eje y para que la criptomoneda con el precio más alto esté arriba
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Guardar el gráfico como imagen
        plt.savefig("../cuerpoFit/static/graphs/" + group + ".png")

def crear_grafico_param(vlevel,vequip):

    global df, new_df
    group= ['BodyPart']

    df_for_level = df[df.Level == vlevel]
    df_for_level_for_equipment = df_for_level[df_for_level.Equipment == vequip]

    df_for_level_for_equipment_group = df_for_level_for_equipment.groupby(group).count()
    df_for_level_for_equipment_group = df_for_level_for_equipment_group.sort_values(by='index')

    # Agrupar por ejecicio
    group_data = df.groupby(group).count()
    group_data = group_data.sort_values(by='index', ascending=False)

    # Crea un gráfico de barras para el grupo actual
    plt.figure(figsize=(10, 6))


    fig = px.bar(df_for_level_for_equipment_group, x=df_for_level_for_equipment_group.index, y='index', color='index',title=vlevel)
    # Rota las etiquetas del eje x en 45 grados
    fig.update_xaxes(tickangle=-45)

    # Guardar el gráfico como imagen
    pio.write_image(fig,"../cuerpoFit/static/graphs/" + str(group[0]) + "_" + vlevel + "_" + vequip +".png")

    #fig.show()

if __name__ == "__main__":
    normalizarDatos()
    crear_grafico()
    crear_grafico_param('Beginner','Body Only')
    crear_grafico_param('Intermediate', 'Body Only')
    crear_grafico_param('Expert', 'Body Only')