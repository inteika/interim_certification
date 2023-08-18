import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
#import statsmodels.api as sm
from scipy import stats

if "model1_computed" not in st.session_state:
    st.session_state.model1_computed = False

test_flag = False
test=[]
file=None

def violinStrip_plot():
    global file
    file = st.file_uploader(label='Выберите файл расширения .csv', type='csv')
    if file is not None:
        df=pd.read_csv(file)
        st.dataframe(df)
        columns=list(df)
        
        x = st.selectbox("Выберите числовой столбец",columns, on_change=change)
        cat_x=st.checkbox('X является категориальными данными', on_change=change)
        y = st.selectbox("Выберите категориальный или числовой столбец",columns, on_change=change)
        cat_y=st.checkbox('Y является категориальными данными', on_change=change)


        btn_plot = st.button('Построить распределение')
        if btn_plot or st.session_state.model1_computed:
            st.session_state.model1_computed = True
            df_to_plot = df[[x,y]].dropna().copy()
            if cat_x and cat_y:
                test_flag = True
                test=['chi-square']
                fig1 = px.pie(df_to_plot, values=np.ones_like(df[x]), names=x)
                fig2 = px.pie(df_to_plot, values=np.ones_like(df[y]), names=y)
                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
            elif not cat_y and not cat_x:
                test_flag = True
                test=['t-test','u-test']
                fig1 = px.histogram(df[x].dropna())
                fig2 = px.histogram(df[y].dropna())
                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
            elif cat_x and not cat_y:
                test_flag = False
                fig = px.pie(df_to_plot, values=y, names=df_to_plot[x])
                st.plotly_chart(fig)
            else:
                test_flag = False
                fig = px.pie(df_to_plot, values=x, names=df_to_plot[y])
                st.plotly_chart(fig)

            if test_flag:
                t = st.selectbox("Выберите алгоритм теста гипотез",test)
                btn_calc = st.button('Расчитать')
                if btn_calc:
                    if t == 't-test':
                        res = stats.ttest_ind(df[x], df[y], equal_var=False)
                        st.write(f'Значение критерия t: {res.statistic:.4f}')
                        st.write(f'Значение p-value: {res.pvalue:.4f}')
                    elif t == 'u-test':
                        res = stats.mannwhitneyu(df_to_plot[x], df_to_plot[y])
                        st.write(f'Значение критерия Манна-Уитни U: {res.statistic / 2:.4f}')
                        st.write(f'Значение p-value: {res.pvalue:.4f}')
                    elif t == 'chi-square':
                        res = stats.chi2_contingency(observed = pd.DataFrame(df[y],df[x]))
                        st.write(f'Значение критерия chi square: {res.statistic/ 2:.4f}')
                        st.write(f'Значение p-value: {res.pvalue:.4f}')
                    st.write(f'При значениях p-value меньше 0,05 "0" гипотезу следует отклонить, при значениях больше следует отклонить альтернативную гипотезу')
            else:
                st.write(f'{x} и {y} являются данными различного рода, для проведения статистического теста выберите данные одного рода "числовую и числовую" или "категориальную и категориальную"')

def change():
    st.session_state.model1_computed = False

def run():
    st.title("demo")
    html_temp="""
    
    """
    
    violinStrip_plot()
    
    
    
if __name__=='__main__':
    run()