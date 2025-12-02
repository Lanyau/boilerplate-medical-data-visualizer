import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1
path='medical_examination.csv'
df=pd.read_csv(path)
# 2
BMI= df['weight']/((df['height']/100)**2)
df['overweight'] = BMI.apply(lambda x: 1 if x>25 else 0)

# 3
df['cholesterol']=df['cholesterol'].apply(lambda x: 0 if x==1 else 1)
df['gluc']=df['gluc'].apply(lambda x: 0 if x==1 else 1)

# 4
def draw_cat_plot():
    # 5
    df_p=pd.melt(df, id_vars=['id','cardio'], value_vars=['active','alco','cholesterol', 'gluc','overweight','smoke'], var_name='variable', value_name='value')
    df_cat = df_p.groupby(['cardio', 'variable', 'value']).size().reset_index()
    # 6
    df_cat = df_cat.rename(columns={0: 'total'})
    # 7
    g = sns.catplot(
    data=df_cat,        
    x='variable',       # Eje X: Las seis categorías ('active', 'alco', etc.)
    y='total',          # Eje Y: El conteo de ese valor
    hue='value',        # Dividir las barras por el VALOR de la variable (0 o 1)
    col='cardio',       # ¡División principal! Crea un gráfico para cardio=0 y otro para cardio=1
    kind='bar',         
    height=5, 
    aspect=1,         # Ajustamos el aspecto para que quepan las 6 barras en X
   
)
# 🏷️ Etiquetas y Título
# Renombramos las etiquetas del eje X para mayor claridad
    g.set_titles("cardio: {col_name}")
    # 8
    fig = g.fig
    # 9
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # 11
    
    # 1. Aplicar los filtros según los requisitos del proyecto:
    df_heat = df[
    (df['ap_lo'] <= df['ap_hi']) &  # Presión Diastólica <= Presión Sistólica
    (df['height'] >= df['height'].quantile(0.025)) & 
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))
     ]
    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(10, 8))

    # 15
    # Trazar la matriz de correlación
    sns.heatmap(
        corr, 
        mask=mask,               # Aplicamos la máscara aquí para ocultar el triángulo superior
        annot=True,              # Mostrar los valores de correlación en las celdas
        fmt=".1f",               # Formato de los números (una cifra decimal)
        cmap='hsv',         # Esquema de color (puedes cambiarlo, ej: 'vlag', 'RdBu')
        center=0,                # Punto central del esquema de color (usualmente 0 para correlación)
        square=True,             # Asegura que las celdas sean cuadradas
        linewidths=.5,           # Líneas entre las celdas
        cbar_kws={"shrink": .5}, # Configuración de la barra de color
        ax=ax                    # Dibujar en el objeto 'ax' de Matplotlib que creamos
    )
    # 16
    fig.savefig('heatmap.png')
    return fig
