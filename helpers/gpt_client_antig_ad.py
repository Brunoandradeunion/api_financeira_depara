import openai
import streamlit as st
import pandas as pd
import numpy as np
import re

import helpers.dadoscontabeis as data_contabil


# Inicialização da API 
openai.api_key = 'sk-proj-2G9Z6JlCa8iZKgeU0O1RT3BlbkFJkg2EENY6YcWSf3KbVaIu'

def generate_analysis_dashboard(df):
    # Extração dos índices
    indices = {
        "Liq_corrente": df.loc[df["ÍNDICES"] == "Liq_corrente", "VALOR"].values[0],
        "Div_liq_ebit": df.loc[df["ÍNDICES"] == "Div_liq_ebit", "VALOR"].values[0],
        "Div_liq_pl": df.loc[df["ÍNDICES"] == "Div_liq_pl", "VALOR"].values[0],
        "PL_ativos": df.loc[df["ÍNDICES"] == "PL_ativos", "VALOR"].values[0],
        "Passivos_ativos": df.loc[df["ÍNDICES"] == "Passivos_ativos", "VALOR"].values[0],
        "Margem_Bruta": df.loc[df["ÍNDICES"] == "Margem_Bruta", "VALOR"].values[0],
        "Div_liq_ebitda": df.loc[df["ÍNDICES"] == "Div_liq_ebitda", "VALOR"].values[0],
        "Ebitda_rec_liq": df.loc[df["ÍNDICES"] == "Ebitda_rec_liq", "VALOR"].values[0],
        "Ebit_rec_liq": df.loc[df["ÍNDICES"] == "Ebit_rec_liq", "VALOR"].values[0],
        "ROIC": df.loc[df["ÍNDICES"] == "ROIC", "VALOR"].values[0],
        "GA": df.loc[df["ÍNDICES"] == "GA", "VALOR"].values[0],
        "CAGR RECEITAS": df.loc[df["ÍNDICES"] == "CAGR RECEITAS", "VALOR"].values[0],
        "CAGR LUCROS": df.loc[df["ÍNDICES"] == "CAGR LUCROS", "VALOR"].values[0],
        "Margem_liquida": df.loc[df["ÍNDICES"] == "Margem_liquida", "VALOR"].values[0],
        "ROE": df.loc[df["ÍNDICES"] == "ROE", "VALOR"].values[0],
        "ROA": df.loc[df["ÍNDICES"] == "ROA", "VALOR"].values[0]
    }
    
    # Texto de entrada para o modelo
    input_text = f"Com base nos seguintes índices financeiros: {indices}, forneça uma análise explícita período a período sobre os índices apresentados e possíveis diagnósticos financeiros. Aqui está o que cada sigla signifca: Liq_corrente = liquidez corrente, Div_liq_ebit = divida liquida da empresa dividido pelo ebit atual, Div_liq_pl = divida liquida dividido pelo patrimônio liquido, PL_ativos = patrimonio liquido dividido pelos ativos, Passivos_ativos = passivos divididos pelos ativos, Margem_Bruta = margem bruta, Margem_liquida = margem líquida, Div_liq_ebitda = divida líquida dividida pelo ebitda, Ebit_rec_liq = receita liquida Ebit, Ebitda_rec_liq = receita liquida Ebitda, ROIC = retorno no capital investido, GA = giros ativos, CAGR RECEITAS = receitas da Taxa composta de crescimento anual, CAGR LUCROS = lucro da Taxa composta de crescimento anual, Margem_liquida = margem líquida, ROE = Retorno sobre patrimônio líquido, ROA = Retorno sobre ativos. Não mencionar as siglas no texto da análise, apenas seus significados. Os dados apresentados se referem ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Faça a análise dos indicadores em relação a dados históricos setoriais como a Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo."
    
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
             "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas." 
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        max_tokens=1600
    )
    
    return response.choices[0].message.content

def generate_analysis_dashboard_agressiva(df):
    # Extração dos índices
    indices = {
        "Liq_corrente": df.loc[df["ÍNDICES"] == "Liq_corrente", "VALOR"].values[0],
        "Div_liq_ebit": df.loc[df["ÍNDICES"] == "Div_liq_ebit", "VALOR"].values[0],
        "Div_liq_pl": df.loc[df["ÍNDICES"] == "Div_liq_pl", "VALOR"].values[0],
        "PL_ativos": df.loc[df["ÍNDICES"] == "PL_ativos", "VALOR"].values[0],
        "Passivos_ativos": df.loc[df["ÍNDICES"] == "Passivos_ativos", "VALOR"].values[0],
        "Margem_Bruta": df.loc[df["ÍNDICES"] == "Margem_Bruta", "VALOR"].values[0],
        "Div_liq_ebitda": df.loc[df["ÍNDICES"] == "Div_liq_ebitda", "VALOR"].values[0],
        "Ebitda_rec_liq": df.loc[df["ÍNDICES"] == "Ebitda_rec_liq", "VALOR"].values[0],
        "Ebit_rec_liq": df.loc[df["ÍNDICES"] == "Ebit_rec_liq", "VALOR"].values[0],
        "ROIC": df.loc[df["ÍNDICES"] == "ROIC", "VALOR"].values[0],
        "GA": df.loc[df["ÍNDICES"] == "GA", "VALOR"].values[0],
        "CAGR RECEITAS": df.loc[df["ÍNDICES"] == "CAGR RECEITAS", "VALOR"].values[0],
        "CAGR LUCROS": df.loc[df["ÍNDICES"] == "CAGR LUCROS", "VALOR"].values[0],
        "Margem_liquida": df.loc[df["ÍNDICES"] == "Margem_liquida", "VALOR"].values[0],
        "ROE": df.loc[df["ÍNDICES"] == "ROE", "VALOR"].values[0],
        "ROA": df.loc[df["ÍNDICES"] == "ROA", "VALOR"].values[0]
    }
    
    # Gerar a análise com o gpt-3.5-turbo
    input_text = f"Com base nos seguintes índices financeiros: {indices}, forneça uma sugestão de ações administrativas agressivas para melhorar o desempenho da empresa. Você pode se basear nos dados apresentados e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais) e na IBRI (Instituto Brasileiro de Relação com Investidores). Aqui está o que cada sigla signifca apresentada no dataframe: Liq_corrente = liquidez corrente, Div_liq_ebit = divida liquida da empresa dividido pelo ebit atual, Div_liq_pl = divida liquida dividido pelo patrimônio liquido, PL_ativos = patrimonio liquido dividido pelos ativos, Passivos_ativos = passivos divididos pelos ativos, Margem_Bruta = margem bruta, Margem_liquida = margem líquida, Div_liq_ebitda = divida líquida dividida pelo ebitda, Ebit_rec_liq = receita liquida Ebit, Ebitda_rec_liq = receita liquida Ebitda, ROIC = retorno no capital investido, GA = giros ativos, CAGR RECEITAS = receitas da Taxa composta de crescimento anual, CAGR LUCROS = lucro da Taxa composta de crescimento anual, Margem_liquida = margem líquida, ROE = Retorno sobre patrimônio líquido, ROA = Retorno sobre ativos. Não mencionar as siglas no texto da análise, apenas seus significados. Os dados apresentados se referem ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Para a sugestão de ações administrativas agressivas, leve em consideração também os dados históricos setoriais como os dados da Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo."
    
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analysis_dashboard_conservadora(df):
    # Extração dos índices
    indices = {
        "Liq_corrente": df.loc[df["ÍNDICES"] == "Liq_corrente", "VALOR"].values[0],
        "Div_liq_ebit": df.loc[df["ÍNDICES"] == "Div_liq_ebit", "VALOR"].values[0],
        "Div_liq_pl": df.loc[df["ÍNDICES"] == "Div_liq_pl", "VALOR"].values[0],
        "PL_ativos": df.loc[df["ÍNDICES"] == "PL_ativos", "VALOR"].values[0],
        "Passivos_ativos": df.loc[df["ÍNDICES"] == "Passivos_ativos", "VALOR"].values[0],
        "Margem_Bruta": df.loc[df["ÍNDICES"] == "Margem_Bruta", "VALOR"].values[0],
        "Div_liq_ebitda": df.loc[df["ÍNDICES"] == "Div_liq_ebitda", "VALOR"].values[0],
        "Ebitda_rec_liq": df.loc[df["ÍNDICES"] == "Ebitda_rec_liq", "VALOR"].values[0],
        "Ebit_rec_liq": df.loc[df["ÍNDICES"] == "Ebit_rec_liq", "VALOR"].values[0],
        "ROIC": df.loc[df["ÍNDICES"] == "ROIC", "VALOR"].values[0],
        "GA": df.loc[df["ÍNDICES"] == "GA", "VALOR"].values[0],
        "CAGR RECEITAS": df.loc[df["ÍNDICES"] == "CAGR RECEITAS", "VALOR"].values[0],
        "CAGR LUCROS": df.loc[df["ÍNDICES"] == "CAGR LUCROS", "VALOR"].values[0],
        "Margem_liquida": df.loc[df["ÍNDICES"] == "Margem_liquida", "VALOR"].values[0],
        "ROE": df.loc[df["ÍNDICES"] == "ROE", "VALOR"].values[0],
        "ROA": df.loc[df["ÍNDICES"] == "ROA", "VALOR"].values[0]
    }
    
    # Gerar a análise com o gpt-3.5-turbo
    input_text = f"Com base nos seguintes índices financeiros: {indices}, forneça uma sugestão de ações administrativas conservadoras para melhorar o desempenho da empresa. Você pode se basear nos dados apresentados e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais) e na IBRI (Instituto Brasileiro de Relação com Investidores). Aqui está o que cada sigla signifca apresentada no dataframe: Liq_corrente = liquidez corrente, Div_liq_ebit = divida liquida da empresa dividido pelo ebit atual, Div_liq_pl = divida liquida dividido pelo patrimônio liquido, PL_ativos = patrimonio liquido dividido pelos ativos, Passivos_ativos = passivos divididos pelos ativos, Margem_Bruta = margem bruta, Margem_liquida = margem líquida, Div_liq_ebitda = divida líquida dividida pelo ebitda, Ebit_rec_liq = receita liquida Ebit, Ebitda_rec_liq = receita liquida Ebitda, ROIC = retorno no capital investido, GA = giros ativos, CAGR RECEITAS = receitas da Taxa composta de crescimento anual, CAGR LUCROS = lucro da Taxa composta de crescimento anual, Margem_liquida = margem líquida, ROE = Retorno sobre patrimônio líquido, ROA = Retorno sobre ativos. Não mencionar as siglas no texto da análise, apenas seus significados. Os dados apresentados se referem ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Para a sugestão de ações administrativas conservadoras, leve em consideração também os dados históricos setoriais como os dados da Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo."
    
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )    
    return response.choices[0].message.content

def generate_analises_indicadores(df):

    input_text = (
        f"Por favor, forneça uma análise detalhada baseada nas seguintes métricas: {df}. Os dados são referentes ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Faça a análise explícita período a período dos indicadores em relação a dados históricos setoriais como a Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo."
    )
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_indicadores_agressiva(df):
    
    input_text = (
        f"Com base nas seguintes métricas: {df}, forneça uma sugestão de ações administrativas agressivas para melhorar o desempenho da empresa. Os dados são referentes ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas agressivas."
    )

    # Realizar chamada ao GPT-3
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_indicadores_conservadora(df):
   
    input_text = (
        f"Com base nas seguintes métricas: {df}, forneça uma sugestão de ações administrativas conservadoras para melhorar o desempenho da empresa. Os dados são referentes ao grupo brasileiro Arezzo que atua no ramo de calçados e roupas. Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas conservadoras."
    )

    # Realizar chamada ao GPT-3
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_dre(df, tipo_analise):

    analysis_type_description = {
        "AH": "análise horizontal do DRE",
        "AV": "análise vertical do DRE",
        "DATA": "dados básicos do DRE"  
    }.get(tipo_analise, "dados do DRE")  
    
    print(analysis_type_description)

    input_text = (
        f"Por favor, forneça uma análise detalhada baseada nas seguintes métricas para {analysis_type_description} referente ao dataframe:\n"
        f"{df}. \n\n"        
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao DRE (Demonstração do Resultado de Exercício) do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Faça a análise explícita período a período dos dados do DRE em relação a dados históricos setoriais, "
        "como os da Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo."
    )

    # Realizar chamada ao GPT (use sua chamada de API conforme sua implementação)
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_dre_agressiva(df, tipo_analise):   
    
    analysis_type_description = {
        "AH": "análise horizontal do DRE",
        "AV": "análise vertical do DRE",
        "DATA": "dados básicos do DRE"  
    }.get(tipo_analise, "dados do DRE")  
    
    print(analysis_type_description) 

    input_text = (
        f"Por favor, forneça uma sugestão de ações administrativas agressivas para melhorar o desempenho da empresa baseado nas métricas para {analysis_type_description} do dataframe: \n"
        f"{df}. \n\n"        
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao DRE (Demonstração do Resultado de Exercício) do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Forneça uma sugestão de ações administrativas agressivas baseadas nos dados fornecidos do DRE. Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas agressivas."
        )

    # Realizar chamada ao GPT (use sua chamada de API conforme sua implementação)
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_dre_conservadora(df, tipo_analise):
        
    analysis_type_description = {
        "AH": "análise horizontal do DRE",
        "AV": "análise vertical do DRE",
        "DATA": "dados básicos do DRE"  
    }.get(tipo_analise, "dados do DRE")  
    
    print(analysis_type_description) 
    input_text = (
        f"Por favor, forneça uma sugestão de ações administrativas conservadoras para melhorar o desempenho da empresa baseado nas métricas para {analysis_type_description} do dataframe: \n"
        f"{df}. \n\n"        
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao DRE (Demonstração do Resultado de Exercício) do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Forneça uma sugestão de ações administrativas conservadoras baseadas nos dados fornecidos do DRE. Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas conservadoras."
    )
    
    # Realizar chamada ao GPT (use sua chamada de API conforme sua implementação)
    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_bp(df, tipo_analise):
   
    analysis_type_description = {
        "AH": "análise horizontal do Balanço Patrimonial",
        "AV": "análise vertical do Balanço Patrimonial",
        "DATA": "dados básicos do Balanço Patrimonial"  
    }.get(tipo_analise, "dados do Balanço Patrimonial")  
    
    input_text = (
        f"Por favor, forneça uma análise detalhada baseada nas seguintes métricas para a {analysis_type_description} referente ao dataframe:\n"
        f"{df}.\n\n"
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao Balanço Patrimonial do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Faça a análise explícita período a período dos dados do Balanço Patrimonial em relação a dados históricos setoriais, "
        "como os da Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo. Quando o período selecionado for maior que 5 anos, resumir a análise."
    )

    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_bp_agressiva(df, tipo_analise):

    analysis_type_description = {
        "AH": "análise horizontal do Balanço Patrimonial",
        "AV": "análise vertical do Balanço Patrimonial",
        "DATA": "dados básicos do Balanço Patrimonial"  
    }.get(tipo_analise, "dados do Balanço Patrimonial")  
        
    input_text = (
        f"Por favor, forneça uma sugestão de ações administrativas agressivas para melhorar o desempenho da empresa baseado em {analysis_type_description} referente ao dataframe:\n"
        f"{df}.\n\n"
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao Balanço Patrimonial do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Forneça uma sugestão de ações administrativas agressivas baseadas nos dados fornecidos do Balanço Patrimonial. "
        "Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas agressivas."
    )

    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content

def generate_analises_bp_conservadora(df, tipo_analise):
  
    analysis_type_description = {
        "AH": "análise horizontal do Balanço Patrimonial",
        "AV": "análise vertical do Balanço Patrimonial",
        "DATA": "dados básicos do Balanço Patrimonial"  
    }.get(tipo_analise, "dados do Balanço Patrimonial")  
        
    input_text = (
        f"Por favor, forneça uma sugestão de ações administrativas conservadoras para melhorar o desempenho da empresa baseado em {analysis_type_description} referente ao dataframe:\n"
        f"{df}.\n\n"
        "Favor observar os nomes das linhas no texto acima. "
        "Estes dados são referentes ao Balanço Patrimonial do grupo brasileiro Arezzo, "
        "que atua no ramo de calçados e roupas. "
        "Forneça uma sugestão de ações administrativas conservadoras baseadas nos dados fornecidos do Balanço Patrimonial. "
        "Você pode se basear nos dados apresentados neste dataframe e também em análises da APIMEC (Associação dos Analistas e profissionais de investimento do mercado de capitais), na IBRI (Instituto Brasileiro de Relação com Investidores), Abicalçados e Relatórios de Relações com Investidores (RI) da própria Arezzo para a sugestão de ações administrativas conservadoras."
    )

    # Solicitar uma resposta do modelo gpt-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro que fornece análises detalhadas e explicativas."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content
