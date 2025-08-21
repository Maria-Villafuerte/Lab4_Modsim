import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from load_data import load_data

print("ANÁLISIS DE SIMULACIÓN EPIDEMIOLÓGICA - PASO 1")
print("=" * 50)

# 1. CARGAR DATOS
data = load_data()
discrete = data['discrete']
continuous = data['continuous']

print(f"Discrete - Timestamps: {len(discrete['timestamps'])}, Infecciones: {len(discrete['infections'])}")
print(f"Continuous - Timestamps: {len(continuous['timestamps'])}, Infecciones: {len(continuous['infections'])}")

min_len_discrete = min(len(discrete['timestamps']), len(discrete['infections']))
min_len_continuous = min(len(continuous['timestamps']), len(continuous['infections']))

discrete_times = discrete['timestamps'][:min_len_discrete]
discrete_infections = discrete['infections'][:min_len_discrete]
continuous_times = continuous['timestamps'][:min_len_continuous]
continuous_infections = continuous['infections'][:min_len_continuous]

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
plt.savefig("../Imagenes/parte_1.jpg", format="jpg")
plt.show()

