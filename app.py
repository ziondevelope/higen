import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def buscar_leads_maps(nicho, regiao):
    headers = {"User-Agent": "Mozilla/5.0"}
    consulta = f'site:maps.google.com {nicho} {regiao}'
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
                "Nome": titulo.get_text(),
                "Link do Google Maps": link["href"],
                "Resumo": snippet.get_text() if snippet else ""
            })
    return resultados

def gerar_planilha(dados):
    df = pd.DataFrame(dados)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# Interface Streamlit
st.set_page_config(page_title="Extrator Google Maps", layout="centered")
st.title("📍 Extrator de Leads do Google Maps")

nicho = st.text_input("🔎 Nicho (ex: pizzaria, dentista, salão de beleza)")
regiao = st.text_input("📍 Região ou Cidade (ex: Copacabana, São Paulo, Barra da Tijuca)")

if st.button("Extrair Leads"):
    if not nicho or not regiao:
        st.warning("Por favor, preencha os dois campos.")
    else:
        with st.spinner("Buscando leads no Google Maps..."):
            dados = buscar_leads_maps(nicho, regiao)
            if dados:
                planilha = gerar_planilha(dados)
                st.success("Leads encontrados com sucesso!")
                st.download_button(
                    label="📥 Baixar Planilha (.xlsx)",
                    data=planilha,
                    file_name="leads_google_maps.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("Nenhum resultado encontrado.")
