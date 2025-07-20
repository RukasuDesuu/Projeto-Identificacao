
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 1. Carregar os dados
data = pd.read_csv('./data55.csv')

# 2. Pré-processamento dos dados
# Converter a coluna 'Subtração' para segundos
def time_to_seconds(time_str):
    parts = list(map(int, time_str.split(':')))
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

data['Tempo_segundos'] = data['Subtração'].apply(time_to_seconds)

t = data['Tempo_segundos'].values
y = data['Nível'].values
u = data['Velocidade'].values

# Ajustar o tempo para começar do zero
t = t - t[0]

# Remover os pontos iniciais onde a entrada é zero e a saída é zero
# Encontrar o primeiro índice onde a velocidade ou o nível não são zero
start_index = np.where((u != 0) | (y != 0))[0][0]
t = t[start_index:]
y = y[start_index:]
u = u[start_index:]

# Reajustar o tempo para começar do zero após o corte
t = t - t[0]

# Normalizar os dados (opcional, mas boa prática para alguns modelos)
# Neste caso, como é um degrau, podemos trabalhar com os valores absolutos ou normalizar para 0-1
# Para um modelo de primeira ordem, vamos usar os valores absolutos e ajustar o ganho

# 3. Definir o modelo de primeira ordem
# Modelo: tau * dy/dt + y = K * u(t)
# Para uma entrada em degrau, a resposta é y(t) = K * U * (1 - exp(-t/tau))
# Onde U é o valor do degrau de entrada

def first_order_model(t, K, tau):
    # Assumimos que a entrada 'u' é um degrau constante após o tempo inicial
    # Pegamos o valor final da entrada como o valor do degrau
    U_step = u[-1] # Valor do degrau de velocidade
    return K * U_step * (1 - np.exp(-t / tau))

# 4. Aplicar o método de identificação (Mínimos Quadrados via curve_fit)
# Estimativas iniciais para K e tau
# K_initial = y_final / U_step_final (ganho estático)
# tau_initial = tempo para atingir 63.2% do valor final

# Encontrar o valor do degrau de entrada (Velocidade)
U_step_value = u[-1] # Assume que a velocidade se estabiliza no final

# Encontrar o valor final do Nível
y_final_value = y[-1]

K_initial = y_final_value / U_step_value if U_step_value != 0 else 1.0
tau_initial = t[-1] / 2.0 # Estimativa inicial razoável

# Realizar o ajuste da curva
# Definir limites para os parâmetros para evitar valores não físicos
# K deve ser positivo, tau deve ser positivo
popt, pcov = curve_fit(first_order_model, t, y, p0=[K_initial, tau_initial], bounds=([0, 0], [np.inf, np.inf]))

K_identified, tau_identified = popt

print(f"Parâmetros identificados:")
print(f"K (Ganho): {K_identified:.2f}")
print(f"tau (Constante de Tempo): {tau_identified:.2f} segundos")

# 5. Validar o modelo
y_simulated = first_order_model(t, K_identified, tau_identified)

# Calcular o RMSE (Root Mean Squared Error)
rmse = np.sqrt(np.mean((y - y_simulated)**2))
print(f"RMSE: {rmse:.2f}")

# 6. Plotar os resultados
plt.figure(figsize=(12, 6))
plt.plot(t, y, 'b.', label='Dados Reais (Nível)')
plt.plot(t, y_simulated, 'r-', label='Modelo de Primeira Ordem Simulado')
plt.plot(t, u, 'g--', label='Entrada (Velocidade)')
plt.title('Identificação de Sistema de Primeira Ordem')
plt.xlabel('Tempo (segundos)')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('./first_order_model_identification.png')
plt.show()
