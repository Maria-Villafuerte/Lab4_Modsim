import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from load_data import load_data

print("🦠 ANÁLISIS DE SIMULACIÓN EPIDEMIOLÓGICA - PASO 1")
print("=" * 50)

# 1. CARGAR DATOS
print("📂 Cargando datos...")
data = load_data()
discrete = data['discrete']
continuous = data['continuous']
print("✅ Datos cargados!")

# 2. VERIFICAR Y CORREGIR LONGITUDES
print("\n🔍 Verificando longitudes de datos...")
print(f"Discrete - Timestamps: {len(discrete['timestamps'])}, Infecciones: {len(discrete['infections'])}")
print(f"Continuous - Timestamps: {len(continuous['timestamps'])}, Infecciones: {len(continuous['infections'])}")

# Ajustar longitudes si es necesario
min_len_discrete = min(len(discrete['timestamps']), len(discrete['infections']))
min_len_continuous = min(len(continuous['timestamps']), len(continuous['infections']))

discrete_times = discrete['timestamps'][:min_len_discrete]
discrete_infections = discrete['infections'][:min_len_discrete]
continuous_times = continuous['timestamps'][:min_len_continuous]
continuous_infections = continuous['infections'][:min_len_continuous]

print(f"✅ Ajustado - Discrete: {len(discrete_times)} puntos, Continuous: {len(continuous_times)} puntos")

# 3. CREAR GRÁFICOS SIMPLES
print("\n📈 Creando gráficos...")

# Figura con 4 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

# Gráfico 1: Datos Discretos
ax1.plot(discrete_times, discrete_infections, 'ro-', linewidth=2, markersize=5)
ax1.set_title('Datos Discretos: Infecciones vs Tiempo')
ax1.set_xlabel('Días')
ax1.set_ylabel('Infecciones')
ax1.grid(True, alpha=0.3)

# Gráfico 2: Datos Continuos
ax2.plot(continuous_times, continuous_infections, 'b-', linewidth=1)
ax2.set_title('Datos Continuos: Infecciones vs Tiempo')
ax2.set_xlabel('Tiempo (días)')
ax2.set_ylabel('Infecciones')
ax2.grid(True, alpha=0.3)

# Gráfico 3: Distribución de Edad
agent_data = discrete['agent_data']
age_counts = agent_data['age'].value_counts()
ax3.bar(age_counts.index, age_counts.values, color=['lightblue', 'lightgreen', 'lightcoral'])
ax3.set_title('Distribución por Edad')
ax3.set_xlabel('Grupo de Edad')
ax3.set_ylabel('Cantidad')

# Gráfico 4: Estado de Vacunación
vaccination_counts = agent_data['vaccinated'].value_counts()
ax4.pie([vaccination_counts[False], vaccination_counts[True]], 
        labels=['No Vacunado', 'Vacunado'], 
        colors=['lightcoral', 'lightgreen'],
        autopct='%1.1f%%')
ax4.set_title('Estado de Vacunación')


plt.tight_layout()
plt.savefig("grafica.jpg", format="jpg")
plt.show()

# 4. ANÁLISIS SIMPLE
print("\n📊 ANÁLISIS DE INTERVALOS:")

# Verificar intervalos regulares
discrete_intervals = np.diff(discrete_times)
print(f"Intervalos en datos discretos: {discrete_intervals[:5]}...")
regular_discrete = len(set(discrete_intervals)) == 1
print(f"¿Intervalos regulares en discretos? {regular_discrete}")

if regular_discrete:
    print(f"Intervalo: {discrete_intervals[0]} día(s)")

# Buscar picos
picos_discretos = [i for i, val in enumerate(discrete_infections) if val > 50]
print(f"\nPicos encontrados en días: {[discrete_times[i] for i in picos_discretos]}")
print(f"Valores de los picos: {[discrete_infections[i] for i in picos_discretos]}")

# Períodos de baja transmisión
bajos_discretos = sum(1 for val in discrete_infections if val < 20)
print(f"Períodos con baja transmisión (< 20 casos): {bajos_discretos}/{len(discrete_infections)}")

