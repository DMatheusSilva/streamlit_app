import streamlit as st
import pandas as pd

def summary_stats(df:pd.DataFrame):
    df_data = df.groupby('Data')[['Valor']].sum()
    df_data['Diferença mensal'] = df_data['Valor'].diff()
    df_data['Avg 6M diferença'] = df_data['Diferença mensal'].rolling(6).mean().round(2)
    df_data['Avg 12M diferença'] = df_data['Diferença mensal'].rolling(12).mean().round(2)
    df_data['Avg 24M diferença'] = df_data['Diferença mensal'].rolling(24).mean().round(2)
    df_data['Diferença relativa mensal'] = df_data['Valor'] / df_data['Valor'].shift() - 1
    return df_data

st.set_page_config(page_title='Finanças', page_icon='🏦', layout='wide')
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

    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

    instituicoes = df.pivot_table(index='Data', columns='Instituição', values='Valor', aggfunc='sum')
    exp2 = st.expander('Instituições')

    # Abas para diferentes visualizações
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

    exp3 = st.expander('Estatísticas Gerais')
    tab_stats, tab_abs, tab_rel = exp3.tabs(['Dados', 'Histórico de evolução', 'Crescimento Relativo'])
    columns_config = {
        'Diferença mensal': st.column_config.NumberColumn('Diferença mensal', format='R$ %.2f'),
        'Avg 6M diferença': st.column_config.NumberColumn('Avg 6M diferença', format='R$ %.2f'),
        'Avg 12M diferença': st.column_config.NumberColumn('Avg 12M diferença', format='R$ %.2f'),
        'Avg 24M diferença': st.column_config.NumberColumn('Avg 24M diferença', format='R$ %.2f'),
        'Diferença relativa mensal': st.column_config.NumberColumn('Diferença relativa mensal', format='percent')
    }
    df_stats = summary_stats(df)
    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config)
    with tab_abs:
        abs_cols = [
            'Diferença mensal',
            'Avg 6M diferença',
            'Avg 12M diferença',
            'Avg 24M diferença'
        ]
        st.line_chart(df_stats[abs_cols])
    with tab_rel:
        st.line_chart(df_stats['Diferença relativa mensal'])

    with st.expander('Metas'):
        col1, col2 = st.columns(2)
        data_inicio_meta = col1.date_input('Inicio da meta', max_value = df_stats.index.max())
        data_filtrada = df_stats.index[df_stats.index <= data_inicio_meta][-1]
        # valor_inicio = df_stats.loc[data_filtrada]['Valor']
        # col2.markdown(f'**Valor no inicio da Meta**:R$ {valor_inicio:.2f}')

        salario_bruto = col1.number_input('Salário Bruto', min_value=0., format='%.2f')
        salario_liquido = col2.number_input('Salário Líquido', min_value=0., format='%.2f')
        custos_fixos = col2.number_input('Custos Fixos', min_value=0., format='%.2f')

        valor_inicio = df_stats.loc[data_filtrada]['Valor']
        col1.markdown(f'**Valor no inicio da Meta**: R$ {valor_inicio:.2f}')
        mensal = salario_liquido - custos_fixos
        anual = mensal*12
        col1.markdown(f'**Potencial arrecadação Mês**: R$ {mensal:.2f}')
        col1.markdown(f'**Potencial arrecadação Ano**: R$ {anual:.2f}')



