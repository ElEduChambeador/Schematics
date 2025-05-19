import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Parámetros
deposito = 2*2059.15  # 2000 propios + 2000 empresa
n_periodos = 26  # Catorcenas por año
tasa_fondo = 0.04  # 4% anual
tasa_externa = 0.12  # 12% anual

# Función para calcular el saldo del fondo en la catorcena k
def calcular_saldo_fondo(hasta_periodo, desde_periodo=1):
    saldo = 0
    tasa_por_periodo = tasa_fondo / n_periodos
    for i in range(desde_periodo, hasta_periodo + 1):
        periodos_interes = hasta_periodo - i + 1
        saldo += deposito * (1 + tasa_por_periodo) ** periodos_interes
    return saldo

# Función para calcular el valor total al final del año
def calcular_valor_total(k):
    # Saldo antes del retiro en catorcena k
    saldo_antes = calcular_saldo_fondo(k)
    
    # Valor futuro del dinero retirado en el instrumento externo
    tiempo_restante = (n_periodos - k) / n_periodos
    valor_externo = saldo_antes * (1 + tasa_externa) ** tiempo_restante
    
    # Saldo del fondo después del retiro (depósitos de k+1 a 26)
    if k < n_periodos:
        saldo_despues = calcular_saldo_fondo(n_periodos, k + 1)
    else:
        saldo_despues = 0
    
    # Valor total
    return valor_externo + saldo_despues

# Calcular valores totales para cada catorcena
catorcenas = np.arange(1, n_periodos + 1)
valores_totales = [calcular_valor_total(k) for k in catorcenas]

# Crear DataFrame para exportar a Excel
df = pd.DataFrame({
    'Catorcena': catorcenas,
    'Valor Total (MXN)': [round(valor, 2) for valor in valores_totales]
})

# Exportar a Excel
df.to_excel('valores_por_catorcena.xlsx', index=False)

# Encontrar la catorcena óptima
k_optimo = catorcenas[np.argmax(valores_totales)]
valor_optimo = max(valores_totales)

# Crear la gráfica
plt.figure(figsize=(12, 8))
plt.plot(catorcenas, valores_totales, 'b-', label='Valor total al final del año')
plt.scatter([k_optimo], [valor_optimo], color='red', s=100, label=f'Óptimo: Catorcena {k_optimo}')
plt.title('Valor Total según Catorcena de Retiro (Depósitos Continúan)')
plt.xlabel('Catorcena de Retiro')
plt.ylabel('Valor Total (MXN)')
plt.grid(True)
plt.legend()

# Añadir etiquetas con el valor en cada catorcena
for i, valor in enumerate(valores_totales):
    plt.text(catorcenas[i], valor + 100, f'{valor:.2f}', 
             ha='center', va='bottom', fontsize=8, rotation=45)

# Mostrar la gráfica en vivo
plt.show()