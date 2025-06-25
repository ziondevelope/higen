import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def buscar_no_google(consulta):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    resultados = []
    for item in soup.select("div.g")[:10]:
        titulo = item.select_one("h3")
        link = item.select_one("a")
        snippet = item.select_one("span.aCOpRe")

        if titulo and link:
            resultados.append({
                "Título": titulo.get_text(),
                "Link": link["href"],
                "Resumo": snippet.get_text() if snippet else ""
            })
    return resultados

def gerar_planilha(dados):
    df = pd.DataFrame(dados)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

st.title("Extrator de Leads do Google")
consulta = st.text_input("Digite sua busca no Google (ex: site:instagram.com pizzaria 'niterói' '@gmail.com'):")

if st.button("Extrair Leads"):
    if consulta.strip() == "":
        st.warning("Por favor, digite uma consulta válida.")
    else:
        with st.spinner("Buscando no Google..."):
            dados = buscar_no_google(consulta)
            if dados:
                planilha = gerar_planilha(dados)
                st.success("Leads extraídos com sucesso!")
                st.download_button(
                    label="📥 Baixar planilha (.xlsx)",
                    data=planilha,
                    file_name="leads_extraidos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("Nenhum resultado encontrado.")
