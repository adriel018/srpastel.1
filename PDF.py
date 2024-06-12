import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime


# Função para criar o PDF
def create_pdf(data):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", style="B", size=12)
            self.cell(0, 10, "Relatório de Vendas", ln=True, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", style="I", size=8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(0, 10, "Data: " + data["Data"], ln=True)
    pdf.cell(0, 10, "Valor Total: R$ " + str(data["Valor Total"]), ln=True)
    pdf.cell(0, 10, "Detalhes:", ln=True)

    for index, row in data["Detalhes"].iterrows():
        pdf.cell(0, 10, "Forma de Pagamento: " + row['Forma de Pagamento'], ln=True)
        pdf.cell(0, 10, "Valor: R$ " + str(row['Valor Recebido']), ln=True)

    filename = "relatorio.pdf"
    pdf.output(filename)

    with open(filename, "rb") as f:
        pdf_data = f.read()

    return pdf_data


# Função principal do aplicativo
def main():
    st.title("Relatório de Vendas")

    # Coletando dados do usuário
    nome_cliente = st.text_input("Nome do Cliente:")
    valor_pedido = st.number_input("Valor do Pedido:", step=1.0)
    forma_pagamento = st.selectbox("Forma de Pagamento:", ["Dinheiro", "Pix", "Cartão"])
    valor_recebido = st.number_input("Valor Recebido:", step=1.0)

    # Salvando os dados do usuário
    if st.button("Salvar Pedido"):
        pedido = {"Nome do Cliente": nome_cliente, "Valor do Pedido": valor_pedido,
                  "Forma de Pagamento": forma_pagamento, "Valor Recebido": valor_recebido}
        df = pd.DataFrame([pedido])
        df.to_csv("pedidos.csv", mode='a', index=False, header=not os.path.exists("pedidos.csv"))
        st.success("Pedido Salvo com Sucesso!")

    # Botão para limpar os dados
    if st.button("Limpar Dados"):
        if os.path.exists("pedidos.csv"):
            os.remove("pedidos.csv")
            st.success("Dados Limpos com Sucesso!")
        else:
            st.warning("O arquivo de dados não existe.")

    # Mostrar a tabela em tempo real
    st.subheader("Pedidos Realizados:")
    if os.path.exists("pedidos.csv") and os.path.getsize("pedidos.csv") > 0:
        df = pd.read_csv("pedidos.csv")
        st.write(df)
    else:
        st.warning("Nenhum dado disponível.")

    # Criando o relatório
    if st.button("Gerar Relatório"):
        if os.path.exists("pedidos.csv") and os.path.getsize("pedidos.csv") > 0:
            df = pd.read_csv("pedidos.csv")
            valor_total = df["Valor Recebido"].sum()
            detalhes = df.groupby("Forma de Pagamento")["Valor Recebido"].sum().reset_index()
            data_atual = datetime.now().strftime("%d/%m/%Y")
            relatorio = {"Data": data_atual, "Valor Total": valor_total, "Detalhes": detalhes}
            pdf_data = create_pdf(relatorio)
            st.download_button(label="Baixar PDF", data=pdf_data, file_name="relatorio.pdf", mime="application/pdf")
        else:
            st.warning("Nenhum dado disponível para gerar relatório.")


if __name__ == "__main__":
    main()
