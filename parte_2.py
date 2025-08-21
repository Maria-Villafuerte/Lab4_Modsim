# PASO 2: IDENTIFICACIÓN DEL MODELO TEMPORAL
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from load_data import load_data

print("🦠 ANÁLISIS DE SIMULACIÓN EPIDEMIOLÓGICA - PASO 2")
print("🔍 IDENTIFICACIÓN DEL MODELO TEMPORAL")
print("=" * 50)

# 1. CARGAR Y PREPARAR DATOS
data = load_data()
discrete = data['discrete']
continuous = data['continuous']

# Ajustar longitudes
min_len_discrete = min(len(discrete['timestamps']), len(discrete['infections']))
discrete_times = discrete['timestamps'][:min_len_discrete]
discrete_infections = discrete['infections'][:min_len_discrete]

min_len_continuous = min(len(continuous['timestamps']), len(continuous['infections']))
continuous_times = continuous['timestamps'][:min_len_continuous]
continuous_infections = continuous['infections'][:min_len_continuous]

print("📂 Datos cargados y preparados")

# 2. IMPLEMENTAR PSEUDOCÓDIGO DE ANÁLISIS
print("\n🔍 PASO 2.1: Análisis del Pseudocódigo")
print("=" * 40)

# Verificar si timestamps son enteros
def analyze_timestamps(timestamps, name):
    are_integers = all(isinstance(t, (int, np.integer)) or float(t).is_integer() for t in timestamps)
    print(f"\n{name}:")
    print(f"  ¿Timestamps son enteros? {are_integers}")
    
    if are_integers:
        print(f"  → likely_discrete_time = True")
        return "discrete"
    else:
        print(f"  → likely_continuous_time = True")
        return "continuous"

# Analizar ambos datasets
discrete_type = analyze_timestamps(discrete_times, "DATOS DISCRETOS")
continuous_type = analyze_timestamps(continuous_times, "DATOS CONTINUOS")

# 3. ANÁLISIS DE PICOS PERIÓDICOS
print("\n📈 PASO 2.2: Análisis de Picos Periódicos")
print("=" * 40)

def find_peaks(infections, threshold=50):
    """Encuentra picos en las infecciones"""
    peaks = []
    for i, val in enumerate(infections):
        if val > threshold:
            peaks.append(i)
    return peaks

def analyze_periodicity(times, infections, name):
    print(f"\n{name}:")
    
    # Encontrar picos
    peaks = find_peaks(infections)
    peak_times = [times[i] for i in peaks]
    peak_values = [infections[i] for i in peaks]
    
    print(f"  Picos encontrados: {len(peaks)}")
    print(f"  Tiempos de picos: {peak_times}")
    print(f"  Valores de picos: {peak_values}")
    
    # Calcular diferencias entre picos
    if len(peaks) > 1:
        peak_differences = []
        for i in range(1, len(peak_times)):
            diff = peak_times[i] - peak_times[i-1]
            peak_differences.append(diff)
        
        print(f"  Diferencias entre picos: {peak_differences}")
        
        # Verificar periodicidad
        if len(set(peak_differences)) == 1:
            print(f"  → evidence_for_discrete_time += 1 (picos cada {peak_differences[0]} unidades)")
            return "periodic", peak_differences[0]
        else:
            print(f"  → Picos NO son periódicos (intervalos variables)")
            return "non-periodic", None
    else:
        print(f"  → Insuficientes picos para análisis")
        return "insufficient", None

# Analizar periodicidad
discrete_periodicity, discrete_interval = analyze_periodicity(discrete_times, discrete_infections, "DATOS DISCRETOS")
continuous_periodicity, continuous_interval = analyze_periodicity(continuous_times, continuous_infections, "DATOS CONTINUOS")

# 4. ANÁLISIS DE TRANSMISIÓN ENTRE PICOS
print("\n🔄 PASO 2.3: Análisis de Transmisión entre Picos")
print("=" * 40)

def analyze_between_peaks(infections, name):
    print(f"\n{name}:")
    
    # Definir umbral para "pequeñas infecciones"
    threshold_small = 20
    small_infections = [val for val in infections if val < threshold_small]
    
    print(f"  Infecciones pequeñas (< {threshold_small}): {len(small_infections)}/{len(infections)}")
    print(f"  Porcentaje: {len(small_infections)/len(infections)*100:.1f}%")
    
    if len(small_infections) > len(infections) * 0.3:  # Más del 30%
        print(f"  → evidence_for_continuous_time += 1")
        return True
    else:
        print(f"  → Pocas infecciones pequeñas entre picos")
        return False

discrete_small_transmission = analyze_between_peaks(discrete_infections, "DATOS DISCRETOS")
continuous_small_transmission = analyze_between_peaks(continuous_infections, "DATOS CONTINUOS")

# 5. VISUALIZACIÓN DE ANÁLISIS TEMPORAL
print("\n📊 PASO 2.4: Visualización del Análisis")

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Gráfico 1: Datos discretos con análisis de picos
ax1.plot(discrete_times, discrete_infections, 'ro-', linewidth=2, markersize=5)
peaks_discrete = find_peaks(discrete_infections)
for peak in peaks_discrete:
    ax1.axvline(x=discrete_times[peak], color='red', linestyle='--', alpha=0.7)
    ax1.annotate(f'Pico: {discrete_infections[peak]}', 
                xy=(discrete_times[peak], discrete_infections[peak]),
                xytext=(5, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax1.axhline(y=20, color='orange', linestyle=':', label='Umbral bajo (20)')
ax1.set_title('Datos Discretos: Análisis de Picos')
ax1.set_xlabel('Días')
ax1.set_ylabel('Infecciones')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfico 2: Datos continuos con análisis
ax2.plot(continuous_times, continuous_infections, 'b-', linewidth=1)
peaks_continuous = find_peaks(continuous_infections)
for peak in peaks_continuous:
    ax2.axvline(x=continuous_times[peak], color='blue', linestyle='--', alpha=0.7)

ax2.axhline(y=20, color='orange', linestyle=':', label='Umbral bajo (20)')
ax2.set_title('Datos Continuos: Análisis de Picos')
ax2.set_xlabel('Tiempo (días)')
ax2.set_ylabel('Infecciones')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Gráfico 3: Histograma de intervalos entre timestamps
discrete_intervals = np.diff(discrete_times)
ax3.hist(discrete_intervals, bins=10, alpha=0.7, color='red', edgecolor='black')
ax3.set_title('Intervalos entre Timestamps (Discretos)')
ax3.set_xlabel('Intervalo (días)')
ax3.set_ylabel('Frecuencia')

# Gráfico 4: Distribución de valores de infección
ax4.hist(discrete_infections, bins=15, alpha=0.5, color='red', label='Discretos', edgecolor='black')
ax4.hist(continuous_infections, bins=15, alpha=0.5, color='blue', label='Continuos', edgecolor='black')
ax4.axvline(x=20, color='orange', linestyle=':', label='Umbral bajo')
ax4.set_title('Distribución de Valores de Infección')
ax4.set_xlabel('Número de Infecciones')
ax4.set_ylabel('Frecuencia')
ax4.legend()

plt.tight_layout()
plt.savefig("parte_2.jpg")
plt.show()

