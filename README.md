# An-lisis_produccion_petrolera

#  Informe de Tarea Interna – Análisis de Producción Petrolera en Colombia

**Empresa:** Ecopetrol S.A.  
**Departamento:** Dirección Técnica de Producción  
**Área Responsable:** Inteligencia Operativa – Análisis de Datos  
**Archivo Base:** petroleum_colombia_500.csv  
**Fecha:** 4 de julio de 2025

---

## Objetivo del Proyecto

Realizar un análisis integral del comportamiento diario de producción de petróleo, gas y condiciones de yacimiento en cuatro campos colombianos para:

- Comparar la eficiencia productiva entre campos
- Detectar presencia de agua de formación
- Identificar relaciones entre presión, profundidad y producción
- Validar un modelo predictivo de producción en función de la presión

---

## 1. Preparación de los Datos y EDA

- Se creó una clase `eda()` para revisar estructura, tipos, estadísticos descriptivos, valores nulos, outliers e incluso limpieza con IQR.
- Se detectaron y filtraron outliers en variables numéricas clave.
- La columna `date` se convirtió al tipo datetime correctamente.
- Se identificaron 452 registros limpios tras la limpieza (de los 500 originales).

---

## 2. Exploración de Variables

### Producción de Petróleo

![Histograma Oil](fig/histograma_oil.png)  
La mayoría de los pozos producen entre 30.000 y 70.000 barriles diarios. Se detectaron algunos valores atípicos por encima de 100.000.

### Producción de Gas por Campo

![Boxplot Gas](fig/boxplot_gas.png)  
La dispersión en la producción de gas es significativa. El campo **Cupiagua** muestra gran variabilidad.

📁 [frecuencia_por_campo.csv](fig/frecuencia_por_campo.csv) confirma una distribución de registros relativamente balanceada entre campos.

---

##  3. Análisis de Agua de Formación

Se generó la variable `alta_agua` (True si corte de agua ≥ 30%) y se analizaron sus frecuencias por campo.

📁 [tabla_alta_agua.csv](fig/tabla_alta_agua.csv)  
📁 [porcentaje_alta_agua.csv](fig/porcentaje_alta_agua.csv)

| Campo       | % Días con Alta Agua |
|-------------|-----------------------|
| Cusiana     | 37.96%                |
| Cupiagua    | 32.00%                |
| Chichimene  | 29.20%                |
| Rubiales    | 27.20%                |

**Conclusión:** Cusiana y Cupiagua muestran signos de envejecimiento o intrusión de agua.

---

## 4. Estadística Básica y Correlación

![Heatmap](fig/heatmap_correlacion.png)

Se evaluaron correlaciones entre variables numéricas.

- Producción (`oil_bbl`) muestra débil correlación positiva con presión del yacimiento.
- Temperatura y profundidad no presentan correlaciones significativas.

---

## 5. Relaciones Visuales

### Presión vs Producción

![Presión vs Producción](fig/Presion_vs_produccion.png)  
Aunque se sugiere una relación directa, hay mucha dispersión. No se observa tendencia clara.

### Pairplot

![Pairplot](fig/pairplot_variables.png)  
Relaciones entre variables clave coloreadas por campo. Destacan patrones distintos entre Rubiales y Cupiagua, especialmente en gas y temperatura.

---

## 6. Regresión Lineal Simple

Se modeló la producción de petróleo (`oil_bbl`) en función de la presión del yacimiento (`reservoir_pressure_psi`).

📁 [metricas_modelo.csv](fig/metricas_modelo.csv)

| Métrica             | Resultado     |
|---------------------|---------------|
| β₁ (coeficiente)    | ≈ 0.44        |
| β₀ (intercepto)     | ≈ 52,339      |
| R²                  | ≈ -0.0397     |
| MSE                 | ≈ 448,165,580 |

 **Conclusión:** La presión no explica bien la variabilidad de producción. El modelo tiene bajo poder predictivo y requiere incorporar más variables.

---

## 7. Conclusiones y Recomendaciones

- **Campos a monitorear:** *Cusiana* y *Cupiagua* debido a mayor proporción de días con alto corte de agua.
- **Modelado:** El modelo lineal simple no es suficiente. Se recomienda un modelo multivariado no lineal.
- **Eficiencia operativa:** Rubiales y Chichimene mantienen valores operativos más estables.

---

 *Análisis desarrollado con Python, pandas, seaborn, scikit-learn y matplotlib*  
 Proyecto: `analisis-produccion-petrolera`  
 Autores: *[Vanessa Morales - Isanevys Urdaneta]*  
 Julio 2025
