import streamlit as st
import pandas as pd

st.set_page_config(page_title='Finanças', page_icon='🏦')
st.markdown('''
# Boas Vindas!

## Nosso APP financeiro!

Espero que você curta a experiência da nossa solução para organização financeira.
'''
)

# Widget de upload de dados
file_upload = st.file_uploader(label='Faça o upload dos dados aqui', type='csv')
if file_upload: # verificar se tem algum arquivo no upload
    df = pd.read_csv(file_upload)
    exp1 = st.expander('Dados brutos')
    columns_fmt = {"Valor": st.column_config.NumberColumn('Valor', format='R$ %f')}
    exp1.dataframe(df, hide_index = True, column_config=columns_fmt)

    df['Data'] = pd.to_datetime(df['Data']).dt.date

    instituicoes = df.pivot_table(index='Data', columns='Instituição', values='Valor', aggfunc='sum')
    exp2 = st.expander('Instituições')
    tab_data, tab_history, tab_share = exp2.tabs(['Dados', 'Histórico', 'Distribuição'])

    with tab_data:
        st.dataframe(instituicoes)
    with tab_history:
        st.line_chart(instituicoes)
    with tab_share:
        date = st.selectbox('Selecione a data', options=instituicoes.index)
        try:
            st.bar_chart(instituicoes.loc[date])
        except:
            st.warning('Entre com uma data válida!')