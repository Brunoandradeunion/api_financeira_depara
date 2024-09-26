import pandas as pd
import streamlit as st
import helpers.criarGraficos as grf
import helpers.analises as anls
import helpers.demonstrativos as demo


def get_valor_anual(df, ano, conta):
    filtro = df.loc[(df['ANO'] == ano) & (df['CONTA'] == conta), "VALOR"]
    if not filtro.empty:
        return filtro.values[0]
    else:
        return 0    
    
def get_valor_anual_mes(df, ano, mes, conta, coluna):
    filtro = df.loc[(df['ANO'] == ano) & (df['CONTA'] == conta), coluna]
    if not filtro.empty:
        return filtro.values[0]
    else:
        return 0    

def ler_contas_anual(df, ano):
    st.session_state['estoque'] = get_valor_anual(df, ano, "1.01.04")
    st.session_state['ativo_total'] = get_valor_anual(df, ano, "1") 

    st.session_state['ativo_circulante'] = get_valor_anual(df, ano, "1.01") 
    st.session_state['caixa_eq'] = get_valor_anual(df, ano, "1.01.01") 

    st.session_state['realizavel_longo_prazo'] = get_valor_anual(df, ano, "1.02.01")                    

    st.session_state['passivo_total'] = get_valor_anual(df, ano, "2")

    st.session_state['passivo_circulante'] = get_valor_anual(df, ano, "2.01")
    st.session_state['passivo_nao_circulante'] = get_valor_anual(df, ano, "2.02")
    st.session_state['patrimonio_liquido'] = get_valor_anual(df, ano, "2.03")
    st.session_state['emprestimo_curto_prazo'] = get_valor_anual(df, ano, "2.01.04")
    st.session_state['emprestimo_longo_prazo_valor'] = get_valor_anual(df, ano, "2.02.01")
    st.session_state['equivalente_caixa'] = get_valor_anual(df, ano, "1.01.01")
    st.session_state['aplicacao_financeira'] = get_valor_anual(df, ano, "1.01.02")


    st.session_state['receita_liquida'] = get_valor_anual(df, ano, "3.01")
    st.session_state['receita_total'] = get_valor_anual(df, ano, "3.03") 
    st.session_state['lucro_bruto'] = get_valor_anual(df, ano, "3.03")
    st.session_state['impostos'] = get_valor_anual(df, ano, "3.08")

    st.session_state['lucro_liquido'] = get_valor_anual(df, ano, "3.11")


    st.session_state['ebit'] = get_valor_anual(df, ano, "3.05") 
    st.session_state['depreciacao_amortizacao'] = get_valor_anual(df, ano, "6.01.01.02") 
    st.session_state['ebitda'] = st.session_state['ebit'] + st.session_state['depreciacao_amortizacao'] # Calculo EBITDA = ebit + depreciação e amortização

    
    

# @st.cache_data
def ordena_dataframe_decrescente(df, inicio, fim):

    # Classifique os trimestres de forma personalizada
    trimestres_ordenados = ["4", "3", "2", "1"]
    anos = [str(ano) for ano in range(fim + 1, inicio - 1, -1)]
    trimestres_ordenados = [f"{tri}T{ano}" for ano in anos for tri in trimestres_ordenados]

    # Ordenar colunas por PERIODO
    df['TRIMESTRE'] = pd.Categorical(df['TRIMESTRE'], categories=trimestres_ordenados, ordered=True)
    bpp = df.sort_values('TRIMESTRE')

    return df

def ordena_tabular_anual(df):
    # Reverte a ordem das colunas (exceto a coluna 'ÍNDICES' que foi resetada como index)
    colunas_ordenadas = ['ÍNDICES'] + df.columns[1:][::-1].tolist()
    # Reindexa o DataFrame para aplicar a nova ordem de colunas
    return df[colunas_ordenadas]

# @st.cache_data
# def ordenar_dataframe_crescente(df, inicio, fim):

#     # Classifique os trimestres de forma personalizada
#     trimestres_ordenados = ["1", "2", "3", "4"]
#     anos = [str(ano) for ano in range(fim + 1, inicio - 1, -1)]
#     trimestres_ordenados = [f"{tri}T{ano}" for ano in anos for tri in trimestres_ordenados]

#     # Ordenar colunas por PERIODO
#     df['PERIODO'] = pd.Categorical(df['PERIODO'], categories=trimestres_ordenados, ordered=True)
#     bpp = df.sort_values('PERIODO')

#     return df

# Função para extrair a receita liquida trimestral
# @st.cache_data
def data_receita_liquida_custos_trimestral(df, inicio, fim):
# Retorna os resultado dos custos, receitas liquidas e lucro liquido.
    # Filtra as contas receita liquida e custos
    df_filtro_contas = (df['CONTA'] == "3.02") | (df['CONTA'] == "3.01") | (df['CONTA'] == "3.11") 
    df = df.loc[df_filtro_contas]            

    df = df[(df["ANO"] >= inicio) & (df["ANO"] <= fim )]


    # Altera a estrutura dos dados para o grafico
    df_pivot = df.pivot_table(index='PERIODO', columns='DESCRIÇÃO', values='VALOR', observed=False).reset_index()   

    # Remove o nome da coluna indice
    df_pivot.columns.name = None

    # Altera os nomes das colunas
    df_pivot.columns = ['PERIODO', 'CUSTOS', 'LUCRO LIQUIDO', 'RECEITA LIQUIDA' ]

    # Cria a coluna trimestre e ano, e ordena os dados
    df_final = anls.cria_coluna_mes_ano(df_pivot)

    return df_final    

# Função para extrair a receita liquida anual
# @st.cache_data
def data_receita_liquida_custos_anual(df, ano_inicio, ano_fim):

    # Filtra os valores para periodo selecionado
    df = df[(df["ANO"] >= ano_inicio) & (df["ANO"] <= ano_fim )]

    # Filtra as contas receita liquida e custos
    df_filtro_contas = (df['CONTA'] == "3.02") | (df['CONTA'] == "3.01") | (df['CONTA'] == "3.11") 
    df = df[df_filtro_contas]            
    
    # Altera a estrutura dos dados para o grafico
    df_pivot = df.pivot_table(index='ANO', columns='DESCRIÇÃO', values='VALOR').reset_index()    

    # Remove o nome da coluna indice
    df_pivot.columns.name = None
   
    # Altera os nomes das colunas
    df_pivot.columns = ['ANO', 'CUSTOS', 'RECEITA LIQUIDA', 'LUCRO LIQUIDO']
    return df_pivot    

# Função para criar os dados anuais para o gráfico
# @st.cache_data
def data_bp_anual(df, inicio, fim):
    # Filtro e ordenação das colunas
    df = df[['CONTA', 'DESCRIÇÃO', 'VALOR','PERIODO', 'ANO', 'MES' ]]

    df = df[(df["ANO"] >= inicio) & (df["ANO"] <= fim )]

    # Contas
    df_ativo = df.loc[df['CONTA'] == '1'].copy()
    df_ativo_circ = df.loc[df['CONTA'] == '1.01'].copy()
    df_ativo_n_circ = df.loc[df['CONTA'] == '1.02'].copy()
    df_passivo_circ = df.loc[df['CONTA'] == '2.01'].copy()
    df_passivo_n_circ = df.loc[df['CONTA'] == '2.02'].copy()
    df_patrimonio_liq = df.loc[df['CONTA'] == '2.03'].copy()

    lista_passivo = []
    meses = df['MES'].unique()
    for ano in range(inicio, fim + 1):
        for m in meses:
            passivo_total = get_valor_anual_mes(df, ano, m, "2", "VALOR")
            patrimonio_liquido = get_valor_anual_mes(df, ano, m, "2.03", 'VALOR')
            periodo = get_valor_anual_mes(df, ano, m, "2.03", 'PERIODO')

            passivo = passivo_total - patrimonio_liquido

            # Cria dataframe com os resultados do calculo do passivo total
            lista_passivo.append({'CONTA': "2", 'DESCRIÇÃO': "Passivo sem patri liq", 'VALOR': round(passivo,2), 'PERIODO': periodo, 'ANO': ano, 'MES': m})                

    # Transforma a lista em dataframe
    df_passivo = pd.DataFrame(lista_passivo)  

    return df_ativo, df_ativo_circ, df_ativo_n_circ, df_passivo_circ, df_passivo_n_circ, df_patrimonio_liq, df_passivo

# Função para criar os dados trimestrais para o gráfico
# @st.cache_data
def data_bp_trimestral(df, inicio, fim):
    # Filtro e ordenação das colunas
    df = df[['CONTA', 'DESCRIÇÃO', 'VALOR','PERIODO', 'ANO', 'MES' ]]
    df = df.dropna()
    df = df.sort_values('PERIODO')
    # Filtro ano
    df = df.loc[(df["ANO"] >= inicio) & (df["ANO"] <= fim )]

    lista = []
    meses = df['MES'].unique()
    for a in range(inicio, fim + 1):
        for m in meses:
            passivo_total = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2"), "VALOR"].values[0]
            patrimonio_liquido = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.03"), "VALOR"].values[0]
            periodo = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2"), "PERIODO"].values[0]           

            # Calculo do passivo 
            passivo = passivo_total - patrimonio_liquido

            lista.append({'CONTA': "2", 'DESCRIÇÃO': "Passivo sem patri liq", 'VALOR': round(passivo,2), 'PERIODO': periodo, 'ANO': a, 'MES': m})
         
    # Transforma a lista em dataframe
    df_passivo_sem_patrimonio = pd.DataFrame(lista) 

    return df, df_passivo_sem_patrimonio

# @st.cache_data
def data_margens_anual(df, inicio, fim):
    # Cria lista dos indices que serão calculados
    indices = [
        "Líquidez Geral", "Líquidez Corrente", "Líquidez Seca",
        "Líquidez Imediata", "Solvência Geral", "Margem de Lucro", 
        "Margem Líquida", "Giro do Ativo" 
        ]

    # Filtra os valores e calcula cada indices e margens listados
    ind_geral = []
    meses = df['MES'].unique()
    for i in indices:   
        for ano in range(inicio, fim + 1):
            for m in meses:  
                ler_contas_anual(df, ano)                                  
                if i == "Líquidez Geral":     
                    try:
                        resultado = (st.session_state['ativo_circulante'] + st.session_state['realizavel_longo_prazo']) / (st.session_state['passivo_circulante'] + st.session_state['passivo_nao_circulante'])                                
                    except ZeroDivisionError:
                        resultado = 0

                elif i == "Líquidez Corrente":
                    try:
                        resultado = st.session_state['ativo_circulante'] / st.session_state['passivo_circulante']
                    except ZeroDivisionError:
                        resultado = 0                        

                elif i == "Líquidez Seca":  
                    try:
                        resultado = (st.session_state['ativo_circulante'] - st.session_state['estoque'])/ st.session_state['passivo_circulante']
                    except ZeroDivisionError:
                        resultado = 0                  
                    
                elif i == "Líquidez Imediata":  
                    try:
                        resultado = st.session_state['caixa_eq'] / st.session_state['passivo_circulante']
                    except ZeroDivisionError:
                        resultado = 0                  

                elif i == "Solvência Geral":
                    try:
                        resultado = st.session_state['ativo_total'] / (st.session_state['passivo_circulante'] + st.session_state['passivo_nao_circulante']) 
                    except ZeroDivisionError:
                        resultado = 0

                elif i == "Margem de Lucro": 
                    try:
                        resultado = (st.session_state['lucro_liquido'] / st.session_state['receita_total'])*100                
                    except ZeroDivisionError:
                        resultado = 0                                  

                elif i == "Margem Líquida":  
                    try:
                        resultado = (st.session_state['lucro_liquido'] / st.session_state['receita_liquida'])*100
                    except ZeroDivisionError:
                        resultado = 0                                       

                elif i == "Giro do Ativo":   
                    try:
                        resultado = st.session_state['lucro_liquido'] / st.session_state['receita_total']
                    except ZeroDivisionError:
                        resultado = 0                                 

                # Insere os dados na lista
                ind_geral.append({'ÍNDICES': i, 'ANO': ano, 'VALOR': round(resultado,2)})  

    # Cria dataframe com os dados dos indices   
    df_indicadores = pd.DataFrame(ind_geral)  

    # Altera a estrutura do dataframe
    df_indicadores_pivot = df_indicadores.pivot_table(index=('ÍNDICES'), columns='ANO', values='VALOR').reset_index()
  
    # Remove o nome da coluna indice
    df_indicadores_pivot.columns.name = None

    # Ordena os dados anuais para as tabelas
    df_indicadores_pivot = ordena_tabular_anual(df_indicadores_pivot)

    # Filtra as margens
    df_margens = df_indicadores[(df_indicadores["ÍNDICES"] == "Margem Líquida") | 
                      (df_indicadores["ÍNDICES"] == "Margem de Lucro") | 
                      (df_indicadores["ÍNDICES"] == "Margem de Lucro")]
    
    # Filtra os indices de liquidez
    df_liquidez = df_indicadores[(df_indicadores["ÍNDICES"] == "Líquidez Geral") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Corrente") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Seca") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Imediata") |
                       (df_indicadores["ÍNDICES"] == "Solvência Geral") |
                       (df_indicadores["ÍNDICES"] == "Giro do Ativo")]

    return df_margens, df_liquidez, df_indicadores_pivot, df_indicadores

# @st.cache_data
def data_margens_trimestral(df, inicio, fim):
    indices = [
        "Líquidez Geral", "Líquidez Corrente", "Líquidez Seca",
        "Líquidez Imediata", "Solvência Geral", "Margem de Lucro", 
        "Margem Líquida", "Giro do Ativo" 
        ]
    
    ind_geral = []
    meses = df['MES'].unique()
    for i in indices:   
        for a in range(inicio, fim + 1):
            for m in meses:                                    
                if i == "Líquidez Geral":                             
                    ativo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01"), "VALOR"].values[0]
                    real_lp = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.02.01"), "VALOR"].values[0]
                    passivo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "VALOR"].values[0]
                    passivo_ncirc = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.02"), "VALOR"].values[0]
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1"), "PERIODO"].values[0]
                    res = (ativo_circ + real_lp) / (passivo_circ + passivo_ncirc)                                

                elif i == "Líquidez Corrente":                        
                    ativo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01"), "VALOR"].values[0]
                    passivo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "VALOR"].values[0]
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01"), "PERIODO"].values[0]
                    res = ativo_circ / passivo_circ

                elif i == "Líquidez Seca":                    
                    ativo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01"), "VALOR"].values[0]
                    passivo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "VALOR"].values[0]
                    estoque = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01.04"), "VALOR"].values[0]
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01"), "PERIODO"].values[0]
                    res = (ativo_circ - estoque)/ passivo_circ
                    
                elif i == "Líquidez Imediata":                    
                    caixa_eq = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1.01.01"), "VALOR"].values[0]
                    passivo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "VALOR"].values[0]      
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "PERIODO"].values[0]    
                    res = caixa_eq / passivo_circ

                elif i == "Solvência Geral":
                    ativo_total = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1"), "VALOR"].values[0]
                    passivo_circ = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "VALOR"].values[0]
                    passivo_ncirc = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.02"), "VALOR"].values[0]
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "2.01"), "PERIODO"].values[0]
                    res = ativo_total / (passivo_circ + passivo_ncirc) 

                elif i == "Margem de Lucro":                                   
                    lucro_liq = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.11"), "VALOR"].values[0]
                    receita_total = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.03"), "VALOR"].values[0] 
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.03"), "PERIODO"].values[0]       
                    res = (lucro_liq / receita_total)*100                

                elif i == "Margem Líquida":                                         
                    lucro_liq = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.11"), "VALOR"].values[0]
                    receita_liq = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.01"), "VALOR"].values[0]   
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.01"), "PERIODO"].values[0]           
                    res = (lucro_liq / receita_liq)*100

                elif i == "Giro do Ativo":                                    
                    ativo_total = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1"), "VALOR"].values[0]
                    receita_total = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "3.03"), "VALOR"].values[0] 
                    trimestre = df.loc[(df['ANO'] == a) & (df['MES'] == m) & (df['CONTA'] == "1"), "PERIODO"].values[0]             
                    res = lucro_liq / receita_total

                ind_geral.append({'ÍNDICES': i, 'TRIMESTRE': trimestre, 'VALOR': round(res,2), 'MES': m, "ANO": a})  

    # Cria, ordenar e pivotar dataframe com dados dos indices   
    df_indicadores = pd.DataFrame(ind_geral)  
    
    # Ordena dados trimestrais para tabelas
    df_indicadores = ordena_dataframe_decrescente(df_indicadores, inicio, fim)

    # Altera estrutura do df
    df_indicadores_pivot = df_indicadores.pivot_table(index=('ÍNDICES'), columns='TRIMESTRE', values='VALOR', observed=False).reset_index()

    # Remove o nome da coluna indice
    df_indicadores_pivot.columns.name = None

    df_margens = df_indicadores[(df_indicadores["ÍNDICES"] == "Margem Líquida") | 
                      (df_indicadores["ÍNDICES"] == "Margem de Lucro") | 
                      (df_indicadores["ÍNDICES"] == "Margem de Lucro")]

    df_liquidez = df_indicadores[(df_indicadores["ÍNDICES"] == "Líquidez Geral") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Corrente") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Seca") |
                       (df_indicadores["ÍNDICES"] == "Líquidez Imediata") |
                       (df_indicadores["ÍNDICES"] == "Solvência Geral") |
                       (df_indicadores["ÍNDICES"] == "Giro do Ativo")]

    return df_margens, df_liquidez, df_indicadores_pivot, df_indicadores

def data_grafico_margens_dashboard(df):
    # Recebe o dataframe do session state 
    # df = st.session_state['data']
    ano_fim = df['ANO'].max()
    ano_inicio = ano_fim - 5    
    df = df[(df["ANO"] >= ano_inicio) & (df["ANO"] <= ano_fim)]
    df = df[(df["PERIODO"] == 'ANUAL') & (df["DEMONSTRATIVO"] == 'Demonstração do Resultado')]

    # df = ordenar_grafico_AH(df,inicio, fim)
    df = df.sort_values('ANO') 

    indices = ["Lucro", "Líquida"]    
    ind_geral = []
    for i in indices:   
        resultado = 0  # Inicializa a variável resultado
        for ano in range(ano_inicio, ano_fim + 1):
            ler_contas_anual(df, ano_fim)

            if i == "Lucro":  
                try:
                    resultado = (st.session_state['lucro_liquido'] / st.session_state['receita_total'])*100
                except ZeroDivisionError:
                    resultado = 0   
                 
            elif i == "Líquida":
                try:
                    resultado = (st.session_state['lucro_liquido'] / st.session_state['receita_liquida'] )*100 
                except ZeroDivisionError:
                    resultado = 0                                                

            ind_geral.append({'MARGENS': i, 'ANO': ano, 'VALOR': round(resultado,2)})                
    
    # Cria, ordenar e pivotar dataframe com dados dos indices   
    df_margens = pd.DataFrame(ind_geral)
    
    return df_margens

# @st.cache_data
def calcula_indicadores_grafico_dashboard(df):

    fim = df['ANO'].max()
    inicio = fim - 5    
    df = df[(df["ANO"] >= inicio) & (df["ANO"] <= fim)]
    df = df[(df["PERIODO"] == 'ANUAL')]

    # df = ordenar_grafico_AH(df,inicio, fim)
    df = df.sort_values('ANO')     
    indices = ["EBITDA", "EBIT", "Bruta"]        
    ind_geral = []
    for i in indices:   
        resultado = 0  # Inicializa a variável resultado
        for ano in range(inicio, fim + 1):
            ler_contas_anual(df, ano)

            if i == "EBITDA":               
                try:
                    resultado =  (st.session_state['ebitda'] / st.session_state['receita_liquida']) * 100
                except ZeroDivisionError:
                    resultado = 0

            elif i == "EBIT": 
                try:
                    resultado =  (st.session_state['ebit'] / st.session_state['receita_liquida']) * 100  
                except ZeroDivisionError:
                    resultado = 0

            elif i == "Bruta":  #REVER  
                try:
                    resultado = (st.session_state['lucro_bruto'] / st.session_state['receita_liquida'])*100             
                except ZeroDivisionError:
                    resultado = 0

            ind_geral.append({'MARGENS': i, 'ANO': ano, 'VALOR': round(resultado,2)})                

    # Cria, ordenar e pivotar dataframe com dados dos indices   
    df_dash = pd.DataFrame(ind_geral)  
    return df_dash


# @st.cache_data
def data_dashboard(df):

    ano_fim = df['ANO'].max()

    # Verifica o número de anos disponíveis no dataframe
    anos_disponiveis = sorted(df['ANO'].unique())

    # Se houver pelo menos 5 anos, utiliza os últimos 5, senão pega o mínimo disponível
    if len(anos_disponiveis) >= 5:
        periodo_5anos = ano_fim - 5
    else:
        periodo_5anos = anos_disponiveis[0]  # Pega o ano mais antigo disponível

    # Filtra os dados do ano mais antigo disponível ou dos últimos 5 anos
    df_5anos = df[(df["PERIODO"] == 'ANUAL') & (df["ANO"] == periodo_5anos)]
    df = df[(df["PERIODO"] == 'ANUAL') & (df["ANO"] == ano_fim)]

    ler_contas_anual(df, ano_fim)

    # Filtra dados no período
    rec_liq_cagr_vi = get_valor_anual(df_5anos, periodo_5anos, "3.01")
    cagr_lucro_liquido_vi = get_valor_anual(df_5anos, periodo_5anos, "3.11")
    # Calcula os indicadores
    # divida bruta = emprestimo curto + emprestimo longo prazo
    divida_bruta =  st.session_state['emprestimo_curto_prazo'] + st.session_state['emprestimo_longo_prazo_valor']   

    # caixa e equivalente de caixa e aplic. finan. curto prazo = caixa equivalente + aplicação financeira
    # caixa_equivalente_aplicacao_financeira = equivalente_caixa + aplicacao_financeira  

    # divida liquida = divida bruta - caixa e equivalente de caixa e aplicações financeiras
    # divida_liquida = divida_bruta - caixa_equivalente_aplicacao_financeira 

    # EBITDA = ebit + depreciação e amortização
    ebitda = st.session_state['ebit'] + st.session_state['depreciacao_amortizacao']  
    ebit_value = st.session_state['ebit']        
    #st.write("O valor de EBIT é:", ebit_value)
    indices = [
         "Div_liq_pl", "Div_liq_ebit", "CAGR RECEITAS", "CAGR LUCROS", "GA", "ROIC", "Ebit_rec_liq", "Ebitda_rec_liq", "Div_liq_ebitda", "Margem_liquida", "PL_ativos", "Passivos_ativos", "Liq_corrente", "Margem_Bruta", "ROE", "ROA"     
            ]
        
    dash_geral = []
    for i in indices:   
                    if i == "PL_ativos":                
                        try:
                            res = (st.session_state['ativo_total'] - st.session_state['passivo_total']) / st.session_state['ativo_total']
                        except ZeroDivisionError:
                            res = 0                                     

                    elif i == "CAGR RECEITAS":  
                        try:
                            if rec_liq_cagr_vi > 0:  # Verifica se o divisor é maior que zero
                                res = ((st.session_state['receita_liquida'] / rec_liq_cagr_vi) ** (1/5) - 1) * 100
                                if res == float('inf'):  # Verifica se o resultado é infinito
                                    res = 0  # Ou outro valor que faça sentido para seu contexto
                            else:
                                #res = 0
                                #res = float('10000')
                                #st.write("Problema identificado: rec_liq_cagr_vi é menor ou igual a zero.")  # Mensagem ao invés de atribuir um valor
                                #st.write("Problema identificado: rec_liq_cagr_vi é menor ou igual a zero.")
                                res = float('nan')
                                #   # Ou outro valor que faça sentido para seu contexto
                        except ZeroDivisionError:
                            res = 0  
                        #st.write(f"O valor de res é: {res}")    

                    elif i == "CAGR LUCROS":
                        try:
                            if cagr_lucro_liquido_vi > 0:  # Verifica se o divisor é maior que zero
                                res = ((st.session_state['lucro_liquido'] / cagr_lucro_liquido_vi) ** (1/5) - 1) * 100
                                if res == float('inf'):  # Verifica se o resultado é infinito
                                    res = 0 #q quando falta conta entra aqui isso acontece pq está faltando as contas
                                    #res = float('nan')
                            else:
                                #st.write("Problema identificado: cagr_lucro_liquido_vi é menor ou igual a zero.")
                                #res = 0 # Ou outro valor específico como -9999 ou float('nan')
                                res = float('nan')
                        except ZeroDivisionError:
                            st.write("Erro de divisão por zero ao calcular CAGR LUCROS.")
                            res = float('nan')  # Ou usar None                     

                    elif i == "ROIC":      
                        try:
                            res = ((st.session_state['ebit'] + st.session_state['impostos']) / (st.session_state['patrimonio_liquido'] + divida_bruta)) * 100
                        except ZeroDivisionError:
                            res = 0

                    elif i == "GA":       
                        try:
                            res =  st.session_state['receita_liquida'] / st.session_state['ativo_total']
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Div_liq_pl":    
                        try:
                            res =  st.session_state['depreciacao_amortizacao'] / st.session_state['patrimonio_liquido']
                        except ZeroDivisionError:
                            res = 0 
                                            

                    elif i == "Div_liq_ebit":  
                        try:
                            # Adiciona prints para verificar os valores antes da divisão
                            #st.write("Depreciação e Amortização:", st.session_state['depreciacao_amortizacao'])
                            #st.write("EBIT:", st.session_state['ebit'])
                            
                            # Realiza a divisão somente se o EBIT não for zero
                            if st.session_state['ebit'] != 0:
                                res = st.session_state['depreciacao_amortizacao'] / st.session_state['ebit']
                            else:
                                #st.warning("EBIT é zero, impossibilitando a divisão.")
                                res = 0  # Ou qualquer valor que faça sentido para o seu caso
                        except ZeroDivisionError:
                            res = 0                         

                    elif i == "Div_liq_ebitda": 
                        try:
                            res =  st.session_state['depreciacao_amortizacao'] / ebitda 
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Ebitda_rec_liq": 
                        try:
                            res =  (ebitda / st.session_state['receita_liquida']) * 100
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Ebit_rec_liq": 
                        try:
                            res =  (st.session_state['ebit'] / st.session_state['receita_liquida']) * 100
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Passivos_ativos":  
                        try:
                            res =  st.session_state['passivo_total'] / st.session_state['ativo_total']
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Liq_corrente":   
                        try:
                            res = st.session_state['ativo_circulante']/ st.session_state['passivo_circulante']
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "ROE":      
                        try:
                            if st.session_state['ativo_total'] == st.session_state['passivo_total']:
                                res = 1
                            else: res = st.session_state['lucro_liquido'] / (st.session_state['ativo_total'] - st.session_state['passivo_total'])
                        except ZeroDivisionError:
                            res = 0                        

                    elif i == "ROA":       
                        try:
                            res = st.session_state['lucro_liquido'] / st.session_state['ativo_total']
                        except ZeroDivisionError:
                            res = 0 
                        
                    elif i == "Margem_Bruta":  #REVER 
                        try:
                            res = (st.session_state['lucro_bruto'] / st.session_state['receita_liquida'])*100
                        except ZeroDivisionError:
                            res = 0 
                            
                    elif i == "Margem_liquida":   
                        try:
                            res = (st.session_state['lucro_liquido'] / st.session_state['receita_liquida'])*100                 
                        except ZeroDivisionError:
                            res = 0 
                            
                    dash_geral.append({'ANO': ano_fim, 'ÍNDICES': i, 'VALOR': round(res,2)})                

    # Cria, ordenar e pivotar dataframe com dados dos indices   
    df_dash = pd.DataFrame(dash_geral)
    return df_dash