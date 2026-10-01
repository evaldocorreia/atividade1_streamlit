import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("Cadastro de Pacientes")

ARQUIVO_CSV = "sl_pacientes.csv"
COLUNAS = [
    "timestamp",
    "nome",
    "endereco",
    "email",
    "idade",
    "genero",
    "contato_emergencia",
    "convenio",
    "prioridade",
    "motivo",
    "historico_medico",
    "alergia",
    "estilo_vida",
    "historico_familiar",
    "hospitalizacao",
]


def salvar_paciente(linha):
    """Salva a nova linha no arquivo CSV de forma persistente."""
    novo = pd.DataFrame([linha])
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)


# Formulário de Cadastro (Usa clear_on_submit para limpar os campos após o envio)
with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente")
    endereco = st.text_input("Endereço do paciente")
    email = st.text_input("Endereço de e-mail")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)

    genero = st.selectbox(
        "Gênero", ["Não declarado", "Masculino", "Feminino"]
    )
    contato_emergencia = st.text_input("Contato de emergência")

    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento", 1, 5, step=1)
    motivo = st.text_area("Motivo da consulta / observações", height=100)

    historico_medico = st.selectbox(
        "Histórico médico",
        [
            "Não Possui",
            "Cardíaco",
            "Hipertenso",
            "Diabético",
            "Câncer",
            "Hepatite",
            "outro",
        ],
    )
    alergia = st.selectbox(
        "Alergias e Reações Adversas",
        ["Não Possui", "Medicamentos", "Alimentos", "Ambiental", "Não sabe"],
    )
    estilo_vida = st.selectbox(
        "Fatores de estilo de vida",
        [
            "Não declarado",
            "Tabagismo",
            "Consumo de álcool",
            "Sedentário",
            "Atividade Física",
        ],
    )
    historico_familiar = st.selectbox(
        "Histórico médico familiar", ["Não declarado", "Sim", "Não", "Não Sabe"]
    )
    hospitalizacao = st.selectbox(
        "Hospitalizações ou tratamentos anteriores",
        [
            "Não declarado",
            "grandes cirurgias",
            "hospitalizações",
            "condições crônicas",
        ],
    )

    enviado = st.form_submit_button("Cadastrar")

# Processamento do formulário após o clique
if enviado:
    if nome.strip() == "":
        st.error("Por favor, preencha pelo tempo menos o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome,
            "endereco": endereco,
            "email": email,
            "idade": idade,
            "genero": genero,
            "contato_emergencia": contato_emergencia,
            "convenio": convenio,
            "prioridade": prioridade,
            "motivo": motivo,
            "historico_medico": historico_medico,
            "alergia": alergia,
            "estilo_vida": estilo_vida,
            "historico_familiar": historico_familiar,
            "hospitalizacao": hospitalizacao,
        }

        salvar_paciente(nova_linha)
        st.success("Paciente cadastrado com sucesso!")

# Seção de visualização dos dados cadastrados
st.subheader("Últimos pacientes cadastrados")
if os.path.exists(ARQUIVO_CSV):
    df_atual = pd.read_csv(ARQUIVO_CSV)
    st.dataframe(df_atual.tail(5), use_container_width=True)

    # Botão de download do arquivo completo
    csv_data = df_atual.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar CSV Completo",
        data=csv_data,
        file_name="pacientes_cadastrados.csv",
        mime="text/csv",
    )
else:
    st.info("Nenhum paciente cadastrado até o momento.")