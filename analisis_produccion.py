
#Informe de Tarea Interna – Análisis de Producción Petrolera en Colombia
#importar librerias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
 
#1. Prepación de los datos y EDA
"""• Leer el archivo petroleum_colombia_500.csv.
• Convertir la columna date a tipo datetime.
• Revisar estructura, tipos y datos faltantes."""
class eda:
    def __init__(self,df,columnas,col_cat):
        self.df = df
        self.columnas = columnas
        self.col_cat = col_cat
 
    def info_general(self):
        print("----- Estructura del dataframe -----")
        print(self.df.head())
        print("----- Información general -----")
        print(self.df.info())
        print("\n----- Análisis descriptivo -----")
        print(self.df.describe())
        print("----- Valores nulos -----")
        print(self.df.isnull().sum())
   
    def _calcular_limites_iqr(self, col): #privado, uso interno
        q1 = self.df[col].quantile(0.25)
        q3 = self.df[col].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        return q1, q3, limite_inferior, limite_superior
 
    def frecuencia(self):
        print("\n----- FRECUENCIA -----")
        for col in self.col_cat:
            print(f"\n--- {col} ---")
            print(f"Frecuencia {col}: {self.df[col].value_counts()}")
 
    def analizar_tendencia_central(self):
        print("\n----- ESTADÍSTICAS -----")
        for col in self.columnas:
            print(f"\n--- {col} ---")
            print(f"Media: {self.df[col].mean():.2f}")
            print(f"Mediana: {self.df[col].median():.2f}")
            print(f"Moda: {self.df[col].mode().iloc[0]:.2f}")
            print(f"STD (sin corrección): {self.df[col].std(ddof=0):.2f}")
            print(f"Varianza (sin corrección): {df[col].var(ddof=0):.2f}")
            print(f"STD (corregida): {self.df[col].std(ddof=1):.2f}")
            print(f"Varianza (corregida): {df[col].var(ddof=1):.2f}")
            print(f"P25 (Q1): {df[col].quantile(0.25):.2f}")
            print(f"P50 (Q2): {df[col].quantile(0.50):.2f}")
            print(f"P75 (Q3): {df[col].quantile(0.75):.2f}")
 
    def analizar_outliers(self):
        print("\n----- OUTLIERS -----")
        for col in self.columnas:
            q1, q3, lim_inf, lim_sup = self._calcular_limites_iqr(col)
            outliers = self.df[(self.df[col] < lim_inf) | (self.df[col] > lim_sup)]
            print(f"\n--- {col} ---")
            print(f"Q1: {q1:.2f} | Q3: {q3:.2f}")
            print(f"Límite inferior: {lim_inf:.2f} | superior: {lim_sup:.2f}")
            print(f"Número de outliers: {outliers.shape[0]}")
   
    def limpieza_datos(self, columna=None):
        print("\n----- DATAFRAME LIMPIO -----")
        df_limpio = self.df.copy()
        if columna:
            columnas_a_limpiar = [columna]
        else:
            columnas_a_limpiar = self.columnas
        for col in columnas_a_limpiar:
            q1, q3, lim_inf, lim_sup = self._calcular_limites_iqr(col)
            df_limpio = df_limpio[(df_limpio[col] >= lim_inf) & (df_limpio[col] <= lim_sup)]
            print(f"Columna: {col}")
            print(f"   Limite inferior: {lim_inf:.2f}, superior: {lim_sup:.2f}")
            print(f"   Filas restantes: {df_limpio.shape[0]}")
        print(f"\nDatos originales: {len(self.df)} | Datos después de limpieza: {len(df_limpio)}")
        return df_limpio
 
df = pd.read_csv('data/petroleum_colombia_500.csv')
columnas_a_analizar = ['oil_bbl','gas_mscf', 'water_cut_pct','reservoir_pressure_psi','reservoir_temperature_c','well_depth_m']
columnas_categoricas = ['field']
explorador = eda(df, columnas_a_analizar, columnas_categoricas)
explorador.info_general()
explorador.frecuencia()
explorador.analizar_tendencia_central()
explorador.analizar_outliers()
explorador.limpieza_datos()
"""Outliers en todas las columnas numéricas"""
#Convertir la columna date a tipo datetime
df['date'] = pd.to_datetime(df['date'])
print("Columna fecha en formatoo datetime:\n", df.dtypes)
 
#🔹 2. Análisis exploratorio
"""• Histograma de oil_bbl (producción) con curva KDE.
• Boxplot de gas_mscf por campo (field).
• Tabla de frecuencia de registros por campo"""
# Histograma + KDE
plt.figure(figsize=(8, 5))
sns.histplot(df['oil_bbl'], kde=True, color='green')
plt.title('Distribución de Producción de Petróleo (oil_bbl)')
plt.savefig('fig/histograma_oil.png')
plt.close()
# Boxplot por campo
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='field', y='gas_mscf', palette='Set2')
plt.title('Distribución de Gas por Campo')
plt.savefig('fig/boxplot_gas.png')
plt.close()
# Frecuencia por campo
conteo_campo = df['field'].value_counts()
conteo_campo.to_csv('fig/frecuencia_por_campo.csv')
 
#3. Análisis de agua de formación
"""• Crear columna alta_agua = True si water_cut_pct ≥ 30.
• Generar tabla de contingencia: campo vs alta_agua"""
#columna alta_agua = True si water_cut_pct ≥ 30
df['alta_agua'] = df['water_cut_pct'] >= 30
tabla_agua = pd.crosstab(df['field'], df['alta_agua'])
tabla_agua.to_csv('fig/tabla_alta_agua.csv')
#• Calcular porcentaje de días con agua elevada por campo.
#tabla de contingencia: campo vs alta_agua
porc_agua = (tabla_agua[True] / tabla_agua.sum(axis=1) * 100).round(2)
porc_agua.to_csv('fig/porcentaje_alta_agua.csv')
 
#4. Estadística básica y correlación
"""• Calcular media, varianza (con y sin corrección de Bessel).
• Obtener matriz de correlaciones numéricas.
• Visualizar correlaciones con un heatmap."""
# Calcular la matriz de correlación
corr = df.corr(numeric_only=True)
#Visualizar correlaciones con un heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación')
plt.savefig('fig/heatmap_correlacion.png')
plt.close()
 
#5. Análisis gráfico de correlación
"""• Gráfico de dispersión: presión vs producción.
• Línea de regresión ajustada con Seaborn.
• Pairplot entre 4 variables clave coloreado por campo.
Objetivo: Observar visualmente la relación presión-producción y otras combinaciones."""
#Gráfico de dispersión: presión vs producción
plt.figure(figsize=(8, 5))
plt.scatter(df['reservoir_pressure_psi'], df['oil_bbl'],cmap='viridis', alpha=0.7)
plt.xlabel('Presión del yacimiento (psi)')
plt.ylabel('Producción de Petróleo (barriles)')
plt.title('Producción de Petróleo vs Presión en el yacimiento')
plt.grid()
plt.savefig('fig/Presion_vs_produccion.png', dpi=300, bbox_inches='tight')
plt.close()
#Línea de regresión ajustada con Seaborn
 
#Pairplot entre 4 variables clave coloreado por campo
sns.pairplot(df[['oil_bbl', 'gas_mscf', 'reservoir_pressure_psi', 'reservoir_temperature_c', 'field']], hue='field')
plt.savefig('fig/pairplot_variables.png')
plt.close()
 
#6. Modelo de regresión lineal simple
"""• Modelo de predicción: oil_bbl = f(reservoir_pressure_psi).
• Usar train_test_split (80/20).
• Ajustar LinearRegression de sklearn.
• Reportar:
o Coeficiente β₁
o Intercepto β₀
o R²
o MSE
Objetivo: Evaluar si la presión del yacimiento puede predecir la producción."""
X = df[['reservoir_pressure_psi']]
y = df['oil_bbl']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
modelo = LinearRegression()
modelo.fit(X_train, y_train) 
y_pred = modelo.predict(X_test)
metricas = { 
    'coeficiente_beta1': modelo.coef_[0],
    'intercepto_beta0': modelo.intercept_,
    'R2_score': r2_score(y_test, y_pred),
    'MSE': mean_squared_error(y_test, y_pred)
}
pd.DataFrame.from_dict(metricas, orient='index').to_csv('fig/metricas_modelo.csv')

#7. Informe final y recomendaciones
