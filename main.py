import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo dos gráficos
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Leitura dos dados
hospedes = pd.read_csv('Hospedes.csv')
reservas = pd.read_csv('Reservas.csv')

# Verificando os dados
print(hospedes.head())
print(reservas.head())

# Junção das tabelas
df_geral = reservas.merge(hospedes, left_on='DocumentoHospede', right_on='Documento')

# Tratamento das colunas de data
df_geral['DataCheckin'] = pd.to_datetime(df_geral['DataCheckin'])
df_geral['DataCheckout'] = pd.to_datetime(df_geral['DataCheckout'])
df_geral['DataNascimento'] = pd.to_datetime(df_geral['DataNascimento'], errors='coerce')

# Cálculo da idade dos hóspedes
df_geral['Idade'] = (df_geral['DataCheckin'] - df_geral['DataNascimento']).dt.days // 365

# Cálculo dos dias de estadia
df_geral['DiasEstadia'] = (df_geral['DataCheckout'] - df_geral['DataCheckin']).dt.days

# ===============================
# Análises e Gráficos
# ===============================

## 1. Distribuição dos Tipos de Quartos
quartos = df_geral['TipoQuarto'].value_counts()

plt.figure()
sns.barplot(x=quartos.index, y=quartos.values, palette="Blues_d")
plt.title('Distribuição dos Tipos de Quartos Reservados')
plt.xlabel('Tipo de Quarto')
plt.ylabel('Quantidade de Reservas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## 2. Faturamento por Tipo de Quarto
faturamento_quarto = df_geral.groupby('TipoQuarto')['ValorReserva'].sum().sort_values(ascending=False)

plt.figure()
sns.barplot(x=faturamento_quarto.index, y=faturamento_quarto.values, palette="Greens_d")
plt.title('Faturamento por Tipo de Quarto')
plt.xlabel('Tipo de Quarto')
plt.ylabel('Faturamento Total (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## 3. Distribuição de Idade dos Hóspedes
plt.figure()
sns.histplot(df_geral['Idade'].dropna(), bins=10, kde=True, color='purple')
plt.title('Distribuição de Idade dos Hóspedes')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

## 3.1 Distribuição por Gênero
genero = df_geral['Genero'].value_counts()

plt.figure()
sns.barplot(x=genero.index, y=genero.values, palette="pastel")
plt.title('Distribuição por Gênero dos Hóspedes')
plt.xlabel('Gênero')
plt.ylabel('Quantidade de Hóspedes')
plt.tight_layout()
plt.show()

## 4. Tempo Médio de Estadia
tempo_medio = df_geral['DiasEstadia'].mean()
print(f" Tempo médio de estadia: {tempo_medio:.2f} dias")

## 5. Evolução do Faturamento por Ano
df_geral['Ano'] = df_geral['DataCheckin'].dt.year
faturamento_ano = df_geral.groupby('Ano')['ValorReserva'].sum()

plt.figure()
sns.lineplot(x=faturamento_ano.index, y=faturamento_ano.values, marker='o')
plt.title('Evolução do Faturamento por Ano')
plt.xlabel('Ano')
plt.ylabel('Faturamento Total (R$)')
plt.tight_layout()
plt.show()

print(f"\n Faturamento por ano:\n{faturamento_ano}")



