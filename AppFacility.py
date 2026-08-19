import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Ordem de Serviço - Manutenção", page_icon="🛠️", layout="centered")

st.title("🛠️ Abertura de Ordem de Serviço")
st.write("Preencha os dados abaixo para relatar o problema na máquina.")

with st.form("form_os"):
    maquina = st.selectbox("Selecione a Máquina", ["Torno CNC 01", "Injetora 04", "Esteira de Embalagem"])
    tipo_problema = st.selectbox("Tipo de Ocorrência", ["Falha Elétrica", "Problema Mecânico", "Parada de Emergência", "Outros"])
    descricao = st.text_area("Descrição detalhada do problema")
    
    foto_anexada = st.file_uploader("Anexar foto da falha (Opcional)", type=["jpg", "png", "jpeg"])
    
    enviar = st.form_submit_button("Enviar Ordem de Serviço")

if enviar:
    if not descricao:
        st.warning("Por favor, preencha a descrição do problema antes de enviar.")
    else:
        with st.spinner("Enviando chamado para a manutenção..."):
            try:
                fromn = st.secrets["from"]
                key = st.secrets["key"]
                to = st.secrets["to"]
                server = st.secrets["server"]
                port = st.secrets["port"]
               
                msg = EmailMessage()
                msg['Subject'] = f"🚨 Nova OS: {maquina} - {tipo_problema}"
                msg['From'] = fromn
                msg['To'] = to
                
                corpo_email = f"""
                Foi aberta uma nova Ordem de Serviço via QR Code:
                
                - Máquina: {maquina}
                - Tipo de Ocorrência: {tipo_problema}
                - Descrição: {descricao}
                """
                msg.set_content(corpo_email)
                
                if foto_anexada is not None:
                    dados_foto = foto_anexada.getvalue()
                    nome_arquivo = foto_anexada.name
                    msg.add_attachment(dados_foto, maintype='image', subtype='jpeg', filename=nome_arquivo)
                
                with smtplib.SMTP_SSL(server, port) as smtp:
                    smtp.login(fromn, key)
                    smtp.send_message(msg)
                
                st.success("✅ Ordem de Serviço enviada com sucesso para a equipe de Facility !")
                
            except Exception as e:
                st.error(f"Erro ao enviar o e-mail: {e}")
