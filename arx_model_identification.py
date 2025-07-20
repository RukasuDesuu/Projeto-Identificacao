
import pandas as pd
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# 1. Carregar os dados
data = pd.read_csv("./data55.csv")

# 2. Pré-processamento dos dados
# Converter a coluna 'Subtração' para segundos
def time_to_seconds(time_str):
    parts = list(map(int, time_str.split(":")))
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

data["Tempo_segundos"] = data["Subtração"].apply(time_to_seconds)

t = data["Tempo_segundos"].values
y = data["Nível"].values
u = data["Velocidade"].values

# Ajustar o tempo para começar do zero
t = t - t[0]

# Remover os pontos iniciais onde a entrada é zero e a saída é zero
start_index = np.where((u != 0) | (y != 0))[0][0]
t = t[start_index:]
y = y[start_index:]
u = u[start_index:]

# Reajustar o tempo para começar do zero após o corte
t = t - t[0]

# Resampling dos dados para um intervalo de tempo fixo
# O modelo ARX requer um tempo de amostragem constante
# Vamos assumir um tempo de amostragem de 1 segundo, que parece razoável pelos dados

dt_resample = 1.0 # 1 segundo

t_resampled = np.arange(0, t[-1], dt_resample)
y_resampled = np.interp(t_resampled, t, y)
u_resampled = np.interp(t_resampled, t, u)

# 3. Definir e aplicar o modelo ARX
# Um modelo ARX (AutoRegressive with eXogenous input) é dado por:
# y(k) + a1*y(k-1) + ... + ana*y(k-na) = b1*u(k-nk) + ... + bnb*u(k-nb-nk+1) + e(k)
# Onde na é a ordem do componente autorregressivo, nb é a ordem do componente de entrada
# e nk é o atraso (dead time) da entrada.

# Para um sistema de primeira ordem, podemos tentar na=1, nb=1, nk=1
na = 1 # Ordem do termo autorregressivo (relacionado à saída anterior)
nb = 1 # Ordem do termo de entrada (relacionado à entrada atual/anterior)
nk = 1 # Atraso (dead time) da entrada

# Construir a matriz de regressores Phi
N = len(y_resampled)
Phi = np.zeros((N - max(na, nb + nk - 1), na + nb))

for k in range(max(na, nb + nk - 1), N):
    # Termos autorregressivos (y(k-i))
    for i in range(na):
        Phi[k - max(na, nb + nk - 1), i] = -y_resampled[k - (i + 1)]
    # Termos de entrada (u(k-nk-j))
    for j in range(nb):
        if (k - nk - j) >= 0:
            Phi[k - max(na, nb + nk - 1), na + j] = u_resampled[k - nk - j]

# Vetor de saída para o ajuste
Y_fit = y_resampled[max(na, nb + nk - 1):]

# Estimar os parâmetros usando Mínimos Quadrados
# theta = (Phi.T @ Phi)^-1 @ Phi.T @ Y_fit
theta = np.linalg.lstsq(Phi, Y_fit, rcond=None)[0]

a_params = theta[0:na]
b_params = theta[na:na+nb]

print(f"Parâmetros do modelo ARX (na={na}, nb={nb}, nk={nk}):")
print(f"a (autorregressivos): {a_params}")
print(f"b (entrada): {b_params}")

# 4. Simular o modelo ARX e validar
# Simular a resposta do modelo com a entrada original
y_arx_simulated = np.zeros_like(y_resampled)

for k in range(N):
    y_pred = 0.0
    # Termos autorregressivos
    for i in range(na):
        if (k - (i + 1)) >= 0:
            y_pred -= a_params[i] * y_arx_simulated[k - (i + 1)]
    # Termos de entrada
    for j in range(nb):
        if (k - nk - j) >= 0:
            y_pred += b_params[j] * u_resampled[k - nk - j]
    y_arx_simulated[k] = y_pred

# Calcular o RMSE para o modelo ARX
rmse_arx = np.sqrt(mean_squared_error(y_resampled, y_arx_simulated))
print(f"RMSE do modelo ARX: {rmse_arx:.2f}")

# 5. Plotar os resultados
plt.figure(figsize=(12, 6))
plt.plot(t_resampled, y_resampled, 'b.', label='Dados Reais (Nível) Resampled')
plt.plot(t_resampled, y_arx_simulated, 'r-', label='Modelo ARX Simulado')
plt.plot(t_resampled, u_resampled, 'g--', label='Entrada (Velocidade) Resampled')
plt.title(f'Identificação de Sistema com Modelo ARX (na={na}, nb={nb}, nk={nk})')
plt.xlabel('Tempo (segundos)')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.savefig('arx_model_identification.png')
plt.show()
