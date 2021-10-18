import pandas as pd
import numpy as np
import streamlit as st
import PIL


st.title('Relatório Docentes')

st.write('Olá Docente! Este é o seu **relatório do SIMENEM I 2021**.')
st.write("Ele é dividido em **duas seções principais**. A primeira delas, apresenta dados gerais sobre toda a prova, estas informações são padronizadas para todas as disciplinas. A seção 2 apresenta dados **específicos para cada matéria**. Para selecionar qual matéria você deseja analisar os dados, basta selecioná-la na barra lateral esquerda.")
st.write("Façam bom uso!")

# ! dados gerais !

st.header("**1. Dados sobre a Prova Geral**")

st.subheader("**1.1 Dados sobre as Questões Objetivas**")

# media e % das objetivas 
media_acerto_materia = pd.read_pickle('dados-relatorio-docentes/media_acerto_materia.pkl')
media_acertos_obj = media_acerto_materia['Média'].mean()

st.write("A média geral de acertos da prova objetiva foi ", str(round(media_acerto_materia['Total Acertos'].sum() / media_acerto_materia['Total Respostas'].sum() , 3)*100)+'%')


# media geral de acertos por materia

def get_media_a_m():
    path = 'dados-relatorio-docentes/media_acerto_materia.pkl'
    return pd.read_pickle(path)
    

st.markdown("**Média de acertos por matéria (em %)**")

media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
media_acerto_materia.set_index('Matéria',inplace=True)

st.write(pd.DataFrame({
   'Total de Acertos': media_acerto_materia["Total Acertos"],
   'Total de Respostas': media_acerto_materia["Total Respostas"],
   'Média': round(media_acerto_materia['Média'],3)*100,
    "Desvio Padrão": round(media_acerto_materia['Desvio Padrão'],3)*100
}))

st.markdown("**Média de acertos por área de conhecimento (em %)**")

media_area_conhecimento = pd.read_pickle("dados-relatorio-docentes/media_area_conhecimento.pkl")

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
st.write(pd.DataFrame({
   'Total de Acertos': media_area_conhecimento["Total Acertos"],
   'Total de Respostas': media_area_conhecimento[ "Total Respostas"],
   'Média': round(media_area_conhecimento['Média'],3)*100,
    "Desvio Padrão": round(media_area_conhecimento['Desvio Padrão'],3)*100
}))




# gráfico com a média de acerto de cada matéria

# o grafico fica com os rotulos na horizontal com as duas linhas a seguir, mas, quando o codigo é upado no servidor do streamlit ele sai todo desconfigurado. 
# caso queira testar para ver se não dá mais o bug, é so "descomentar" as duas linhas a seguir

# media_acerto_materia = media_acerto_materia.reset_index()
# media_acerto_materia = media_acerto_materia.set_index('Correção')
media_acerto_materia = get_media_a_m()
st.markdown("**Gráfico da porcentagem média de acerto em cada matéria**")


media_acerto_materia['Média'] = media_acerto_materia["Média"]

st.bar_chart(data=media_acerto_materia['Média'])
st.write("Passando o mouse por cima do gráfico você pode identificar qual é a matéria e nota referentes a cada barra.")


# media e % da redação

media_redacao = pd.read_pickle('dados-relatorio-docentes/media_redacao.pkl')

# tabela com os dados coletados acima
st.subheader("**1.2 Dados sobre a Redação**")
st.write(round(media_redacao))


# tabela com a colocação dos alunos

colocacao = pd.read_pickle('dados-relatorio-alunos/colocacao.pkl')
st.subheader("**1.3   Colocação dos alunos do Einstein**")
colocacao.set_index('Colocação',inplace=True)
st.write(pd.DataFrame({
    'Nome': colocacao['Nome'],
    'Pontos': colocacao['Total Acertos'],
    "Porcentagem de Acerto": colocacao['% de acerto']
}))


#  ! dados específicos por matéria  ! 

# questões separadas por materia e por assunto
# # tem o total de acertos, total de alunos que responderam e média de acerto

media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

materia_escolhida = st.sidebar.selectbox("Escolha a matéria", media_acerto_materia['Matéria'])

dados_materia_escolhida = media_acerto_materia[(media_acerto_materia['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dados_materia_escolhida.set_index('Matéria',inplace=True)

st.header("**2. Dados sobre a Matéria Selecionada**")

st.write("Aqui você encontra dados sobre a matéria que foi selecionada na caixa localizada na aba lateral.")
st.write(pd.DataFrame({
    "Média Acertos(em %)": round(dados_materia_escolhida['Média'],3)*100
}))


# todas as questões separadas por matéria
# #  tem o total de acertos, total de alunos que responderam e média de acerto
media_acerto_questao = pd.read_pickle('dados-relatorio-docentes/media_acerto_questao.pkl')

st.subheader("**2.1   Média de acertos por questão**")
media_acerto_questao = media_acerto_questao.reset_index()
questao_materia_escolhida = media_acerto_questao[(media_acerto_questao['Matéria'] == materia_escolhida)]


# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
questao_materia_escolhida.set_index('Questão',inplace=True)

st.write(pd.DataFrame({
    "Assunto": questao_materia_escolhida['Assunto'],
    "Dificuldade": questao_materia_escolhida['Dificuldade'],
    "Média de Acerto": round(questao_materia_escolhida['Média'],3)*100,
    "Desvio Padrão": round(questao_materia_escolhida['Desvio Padrão'],3)*100,
    "Tempo Médio(minutos)": round(questao_materia_escolhida["tempo_no_exercicio(s)"]/60,2)
}))

grafico_questoes = questao_materia_escolhida['Média']
grafico_questoes = grafico_questoes.reset_index()
grafico_questoes['questao'] = grafico_questoes['Questão'].astype(str)
grafico_questoes["media"] = grafico_questoes['Média']
grafico_questoes.set_index('questao',inplace=True)

st.bar_chart(data=grafico_questoes['media'])
st.write("Dependendo das pontuações das questões, pode ser que o gráfico apresente **escalas diferentes para cada matéria**. Lembre de sempre olhar os valores do eixo vertical.")

# questões separadas por materia e por assunto
# #  tem o total de acertos, total de alunos que responderam e média de acerto

def get_media_p_a():
    path = 'dados-relatorio-docentes/media_por_assunto.pkl'
    return pd.read_pickle(path)
media_por_assunto = get_media_p_a()
# print(media_por_assunto)

media_por_assunto = media_por_assunto.reset_index()
assuntos_materia_escolhida = media_por_assunto[(media_por_assunto['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
assuntos_materia_escolhida.set_index('Assunto',inplace=True)

st.subheader("**2.2   Média de acertos por assunto**")

st.write(pd.DataFrame({
    "Total Acertos": assuntos_materia_escolhida['Total Acertos'],
    'Total Respostas': assuntos_materia_escolhida['Total Respostas'],
    'Média (em %)': round(assuntos_materia_escolhida['Média'],2)*100,
    "Desvio Padrão": round(assuntos_materia_escolhida['Desvio Padrão'],3)*100
}))



# analise dos acertos por dificuldade
media_por_dificuldade = pd.read_pickle('dados-relatorio-docentes/media_por_dificuldade.pkl')

st.subheader("**2.3   Média de acertos por dificuldade**")

media_por_dificuldade = media_por_dificuldade.reset_index()
dificuldade_materia_escolhida = media_por_dificuldade[(media_por_dificuldade['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dificuldade_materia_escolhida.set_index('Dificuldade',inplace=True)


st.write(pd.DataFrame({
    "Total Acertos": dificuldade_materia_escolhida['Total Acertos'],
    'Total Respostas': dificuldade_materia_escolhida['Total Respostas'],
    'Média (em %)': round(dificuldade_materia_escolhida['Média'],3)*100,
    "Desvio Padrão": round(dificuldade_materia_escolhida['Desvio Padrão'],3)*100
}))

st.subheader("**2.4   Distribuição das respostas**")

st.write("Esta tabela mostra quantas vezes cada alternativa foi assinalada.")

assinaladas = pd.read_pickle("dados-relatorio-docentes/assinaladas.pkl")
assinaladas_materia = assinaladas[(assinaladas['Matéria'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
assinaladas_materia.set_index("Questão", inplace=True)
st.write(pd.DataFrame({
    "Gabarito": assinaladas_materia['Gabarito'],
    "A":assinaladas_materia['A'],
    "B":assinaladas_materia['B'],
    "C":assinaladas_materia['C'],
    "D":assinaladas_materia['D'],
    "E":assinaladas_materia['E']
}))