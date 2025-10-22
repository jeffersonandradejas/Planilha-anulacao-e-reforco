import streamlit as st
import pandas as pd
import io

# ==============================
# Configurações da página
# ==============================
st.set_page_config(page_title="Anulações e Reforços", layout="wide")
st.title("📑 Anulações e Reforços - Visualizador")

# Cabeçalho com campo de colagem à esquerda e assinatura à direita
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("### 📋 Cole os dados da planilha abaixo (separados por tabulação):")
with col2:
    st.markdown("<div style='text-align: right; font-size: 14px;'>Desenvolvedor: <b>2S SAD Andrade</b></div>", unsafe_allow_html=True)

# ==============================
# Área de colagem dos dados
# ==============================
dados_colados = st.text_area("Cole aqui os dados", height=600)

if dados_colados:
    try:
        # Leitura dos dados colados (tabulação como separador)
        df = pd.read_csv(io.StringIO(dados_colados), sep="\t", header=None)

        # Define nomes das colunas conforme estrutura esperada
        df.columns = [
            "Solicitação", "Original", "Empenho", "UG Exec", "UG Cred", "LOCAL ATUAL",
            "I/Lotação", "N.D.", "Sb", "Status", "CODEMP", "Fornecedor",
            "Dt Solicitação", "Anulação_Reforço", "Valor", "Cancelar"
        ][:df.shape[1]]

        # Seleciona colunas relevantes
        df_filtrado = df[[
            "Solicitação", "Original", "Empenho", "UG Cred",
            "I/Lotação", "Fornecedor", "Anulação_Reforço", "Valor"
        ]].copy()

        # Insere coluna "Status" em branco após "I/Lotação"
        idx = df_filtrado.columns.get_loc("I/Lotação") + 1
        df_filtrado.insert(idx, "Status", "")

        # Reordena conforme layout desejado
        ordem_final = [
            "Solicitação", "UG Cred", "I/Lotação", "Empenho", "Original",
            "Status", "Fornecedor", "Valor", "Anulação_Reforço"
        ]
        df_filtrado = df_filtrado[ordem_final]

        # ==============================
        # Formatação da coluna "Valor"
        # ==============================
        df_filtrado["Valor"] = (
            df_filtrado["Valor"]
            .astype(str)
            .str.replace(".", "", regex=False)  # remove pontos de milhar
            .str.replace(",", ".", regex=False)  # converte vírgula decimal para ponto
        )

        # Converte para número
        df_filtrado["Valor"] = pd.to_numeric(df_filtrado["Valor"], errors="coerce")

        # ✅ Formata no padrão brasileiro: R$ 1.234,56
        df_filtrado["Valor"] = df_filtrado["Valor"].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            if pd.notnull(x) else ""
        )

        # ==============================
        # Exibição da tabela formatada
        # ==============================
        st.subheader("📊 Tabela formatada:")
        st.dataframe(df_filtrado, use_container_width=True)

        # ==============================
        # Exportação CSV (compatível com Excel BR)
        # ==============================
        csv = df_filtrado.to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button(
            "📥 Baixar como CSV",
            csv,
            "anulacoes_reforcos.csv",
            "text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erro ao processar os dados: {e}")
