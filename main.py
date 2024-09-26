import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu
from streamlit_option_menu import option_menu

import paginas.Resultados as dre
import paginas.Indicadores as indicadores
import paginas.BalancoPatrimonial as bp
import paginas.Dashboard as dashboard
import paginas.configuracao as config


# Configuração da página
st.set_page_config(
    page_title='Aplicativo',
    layout='wide',
    page_icon=":bar_chart:",
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
    #header, footer {visibility: hidden;}

    /* This code gets the first element on the sidebar,
    and overrides its default styling */
    section[data-testid="stSidebar"] div:first-child {
        top: 0;
        height: 100vh;
    }
    .st-emotion-cache-1jicfl2 {
    width: 100%;
    padding: 1rem 4rem 2rem;
    min-width: auto;
    max-width: initial;
}
    .st-emotion-cache-12fmjuu {
    padding: 0rem 2rem 2rem;
    background-color: transparent;            
}
            
    .st-emotion-cache-h4xjwg {
    padding: 0rem 2rem 2rem;
    background-color: transparent;            
}
    .st-emotion-cache-1xarl3l {
    font-size: 1.80rem;
    padding-bottom: 0.25rem;
}
            
</style>
""",unsafe_allow_html=True)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: gray;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by UNION IT</p>
</div>
"""


@st.dialog("Aviso")
def aviso(texto, tipo):
    if tipo == "sucesso":
        st.success('Esta é uma mensagem de sucesso!', icon="✅")
    elif tipo == "erro":
        st.warning(texto, icon="⚠️")

# Funçao para verificar se existe o arquivo dados.csv
def verifica_dados():
    # Defina o caminho da pasta e o nome do arquivo
    path_pasta = 'data'
    arquivo = 'dados.csv'
    
#EQUATORIAL_ENERGIA
    # Inicialize a flag como False
    arquivo_existe = False

    # Verifique se o arquivo existe na pasta
    caminho_completo = os.path.join(path_pasta, arquivo)
    if os.path.isfile(caminho_completo):
        arquivo_existe = True

    return arquivo_existe

# Verifica se existe dados armazenados 
if 'conta' not in st.session_state:
    st.session_state['arquivo_existe'] = verifica_dados()

# Altera a exibição caso o arquivo exista ou não
if st.session_state['arquivo_existe']:      
    # Inicializa o session state e armazena o dataset
    if 'data_anual' not in st.session_state:
        #aqui onde le os dados         
        st.session_state['data'] = pd.read_csv("./data/EQUATORIAL_ENERGIA.csv")
        #st.session_state['data'] = pd.read_csv("./data/dados.csv")
        pd.to_numeric(st.session_state['data']["VALOR"])   
        pd.to_datetime(st.session_state['data']["ANO"]) 

    selected2 = option_menu(None, ['Dashboard', 'Indicadores', 'Balanço Patrimonial', 'Resultado', 'Configuração'  ], 
        icons=['house', 'activity', "list-task",'list-task'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    
    # selected2 = option_menu(None, ['Dashboard','Configuração' ], 
    #     icons=['house', 'activity', "list-task",'list-task'], 
    #     menu_icon="cast", default_index=0, orientation="horizontal")
    
    

    try:
        if selected2 == "Dashboard":
            dashboard.dashboard()

        elif selected2 == "Indicadores":
            indicadores.pagina_indicadores()

        elif selected2 == "Balanço Patrimonial":
            bp.pagina_bp()

        elif selected2 == "Resultado":
            dre.pagina_dre()

        elif selected2 == "Configuração":
            config.pagina_configuracao()
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a página {selected2}: {e}")

    st.markdown(footer, unsafe_allow_html=True)

else:
    selected2 = option_menu(None, ['Dashboard', 'Indicadores', 'Balanço Patrimonial', 'Resultado', 'Configuração'  ], 
        icons=['house', 'activity', "list-task",'list-task'], 
        menu_icon="cast", default_index=4, orientation="horizontal")

    if selected2 == "Dashboard":
        st.error('Ausência de dados', icon="🚨")
        st.write("Vá para a aba de configuração para inserir dados")    
        aviso("Não existem dados, vá até a página de configuração e insira.", "erro")

    if selected2 == "Indicadores":
        st.error('Ausência de dados', icon="🚨")
        st.write("Vá para a aba de configuração para inserir dados")
        aviso("Não existem dados, vá até a página de configuração e insira.", "erro")


    if selected2 == "Balanço Patrimonial":
        st.error('Ausência de dados', icon="🚨")
        st.write("Vá para a aba de configuração para inserir dados")
        aviso("Não existem dados, vá até a página de configuração e insira.", "erro")

    if selected2 == "Resultado":
        st.error('Ausência de dados', icon="🚨")
        st.write("Vá para a aba de configuração para inserir dados")
        aviso("Não existem dados, vá até a página de configuração e insira.", "erro")

    if selected2 == "Configuração":
        config.pagina_configuracao()

    st.markdown(footer,unsafe_allow_html=True)
