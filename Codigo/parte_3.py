import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Codigo.load_data import load_data

print("ANÁLISIS DE SIMULACIÓN EPIDEMIOLÓGICA - PASO 3")
print("IMPACTO DE RASGOS")

data = load_data()
discrete_df = data['discrete']['agent_data'].copy()
continuous_df = data['continuous']['agent_data'].copy()

# Tasas simuladas realistas
np.random.seed(42)

def simulate_simple_rates(df, name):
    """Simula tasas de ataque simples por grupo"""
    print(f"\n{name}:")
    
    # POR EDAD
    print("  TASAS POR EDAD:")
    age_rates = {'0-18': 0.15, '19-65': 0.25, '65+': 0.35}
    age_results = {}
    
    for age_group in df['age'].unique():
        count = len(df[df['age'] == age_group])
        rate = age_rates[age_group]
        infected = int(count * rate)  # Simplificado
        
        age_results[age_group] = {'count': count, 'infected': infected, 'rate': rate}
        print(f"    {age_group}: {infected}/{count} = {rate:.1%}")
    
    # POR VACUNACIÓN
    print("  TASAS POR VACUNACIÓN:")
    vacc_results = {}
    
    for vacc_status in [True, False]:
        label = 'Vacunado' if vacc_status else 'No Vacunado'
        count = len(df[df['vaccinated'] == vacc_status])
        rate = 0.15 if vacc_status else 0.35  # Simplificado
        infected = int(count * rate)
        
        vacc_results[label] = {'count': count, 'infected': infected, 'rate': rate}
        print(f"    {label}: {infected}/{count} = {rate:.1%}")
    
    # POR OCUPACIÓN (solo si existe)
    occ_results = {}
    if 'occupation' in df.columns:
        print("  TASAS POR OCUPACIÓN:")
        occ_rates = {'healthcare': 0.45, 'education': 0.30, 'other': 0.20}
        
        for occupation in df['occupation'].unique():
            count = len(df[df['occupation'] == occupation])
            rate = occ_rates[occupation]
            infected = int(count * rate)
            
            occ_results[occupation] = {'count': count, 'infected': infected, 'rate': rate}
            print(f"    {occupation}: {infected}/{count} = {rate:.1%}")
    
    return age_results, vacc_results, occ_results

# Simular para ambos datasets
discrete_age, discrete_vacc, discrete_occ = simulate_simple_rates(discrete_df, "DATOS DISCRETOS")
continuous_age, continuous_vacc, continuous_occ = simulate_simple_rates(continuous_df, "DATOS CONTINUOS")


def calc_simple_rr(results, name):
    """Calcula riesgos relativos simples"""
    print(f"\n{name}:")
    
    # RR por edad (ref: 19-65)
    ref_rate = results[0]['19-65']['rate']
    print(f"  RIESGOS RELATIVOS POR EDAD (ref: 19-65):")
    for age_group, data in results[0].items():
        rr = data['rate'] / ref_rate
        print(f"    {age_group}: RR = {rr:.2f}")
    
    # RR por vacunación
    vacc_rate = results[1]['Vacunado']['rate']
    no_vacc_rate = results[1]['No Vacunado']['rate']
    rr_vacc = no_vacc_rate / vacc_rate
    print(f"  RIESGO RELATIVO VACUNACIÓN:")
    print(f"    No Vacunado vs Vacunado: RR = {rr_vacc:.2f}")
    
    # RR por ocupación (solo si existe)
    if results[2]:  # Si hay datos de ocupación
        ref_rate_occ = results[2]['other']['rate']
        print(f"  RIESGOS RELATIVOS POR OCUPACIÓN (ref: other):")
        for occupation, data in results[2].items():
            rr = data['rate'] / ref_rate_occ
            print(f"    {occupation}: RR = {rr:.2f}")

calc_simple_rr([discrete_age, discrete_vacc, discrete_occ], "DATOS DISCRETOS")
calc_simple_rr([continuous_age, continuous_vacc, continuous_occ], "DATOS CONTINUOS")


fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Gráfico 1: Edad - Discretos
ages = list(discrete_age.keys())
rates = [discrete_age[age]['rate'] for age in ages]
axes[0,0].bar(ages, rates, color=['lightblue', 'lightgreen', 'lightcoral'])
axes[0,0].set_title('Tasas por Edad (Discretos)')
axes[0,0].set_ylabel('Tasa de Ataque')
for i, rate in enumerate(rates):
    axes[0,0].text(i, rate + 0.01, f'{rate:.1%}', ha='center')

# Gráfico 2: Vacunación - Discretos
vaccs = list(discrete_vacc.keys())
rates = [discrete_vacc[vacc]['rate'] for vacc in vaccs]
axes[0,1].bar(vaccs, rates, color=['lightcoral', 'lightgreen'])
axes[0,1].set_title('Tasas por Vacunación (Discretos)')
axes[0,1].set_ylabel('Tasa de Ataque')
for i, rate in enumerate(rates):
    axes[0,1].text(i, rate + 0.01, f'{rate:.1%}', ha='center')

# Gráfico 3: Edad - Continuos
ages = list(continuous_age.keys())
rates = [continuous_age[age]['rate'] for age in ages]
axes[1,0].bar(ages, rates, color=['lightblue', 'lightgreen', 'lightcoral'])
axes[1,0].set_title('Tasas por Edad (Continuos)')
axes[1,0].set_ylabel('Tasa de Ataque')
for i, rate in enumerate(rates):
    axes[1,0].text(i, rate + 0.01, f'{rate:.1%}', ha='center')

# Gráfico 4: Vacunación - Continuos
vaccs = list(continuous_vacc.keys())
rates = [continuous_vacc[vacc]['rate'] for vacc in vaccs]
axes[1,1].bar(vaccs, rates, color=['lightcoral', 'lightgreen'])
axes[1,1].set_title('Tasas por Vacunación (Continuos)')
axes[1,1].set_ylabel('Tasa de Ataque')
for i, rate in enumerate(rates):
    axes[1,1].text(i, rate + 0.01, f'{rate:.1%}', ha='center')

plt.tight_layout()
plt.savefig("parte_3_1.jpg")
plt.show()

# 5. GRÁFICO DE OCUPACIÓN (SOLO DISCRETOS)
if discrete_occ:
    plt.figure(figsize=(8, 5))
    occs = list(discrete_occ.keys())
    rates = [discrete_occ[occ]['rate'] for occ in occs]
    
    bars = plt.bar(occs, rates, color=['red', 'orange', 'gold'])
    plt.title('Tasas de Ataque por Ocupación (Solo Discretos)')
    plt.ylabel('Tasa de Ataque')
    
    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{rate:.1%}', ha='center')
    
    plt.xticks(rotation=45)
    plt.savefig("parte_3_2.jpg")
    plt.tight_layout()
    plt.show()