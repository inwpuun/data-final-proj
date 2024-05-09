import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from spark import get_year_count_filter_by_subject , get_all_affil , get_filter_by_affilname ,get_affil_count_filter_by_year , get_all_year, get_all_subject_count, get_chula_thai_collaboration_country_by_subject_year_count, get_chula_thai_collaboration_by_subject_year_count, get_all_country

subjects = ["GENE","AGRI","ARTS","BIOC","BUSI","CENG","CHEM","COMP","DECI","EART","ECON","ENER","ENGI","ENVI","IMMU","MATE","MATH","MEDI","NEUR","NURS","PHAR","PHYS","PSYC","SOCI","VETE","DENT","HEAL"] #27 subjects

st.set_page_config(layout="wide")

# st.title('Research')

@st.cache_data
def loadData():
    df = pd.read_csv('scopusData.csv')
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    return df

# data_load_state = st.text('Loading data...')
# df = loadData()
# data_load_state.text('Loading data...done!')



col1_affi, col2_country,col3_research = st.columns(3)
with col1_affi:
    all_affi = len(get_all_affil())
    st.markdown("<h6 style='text-align: left; color: black;'>จำนวนสถาบันที่จุฬาฯทำงานวิจัยร่วม</h6>", unsafe_allow_html=True)
    st.subheader(all_affi)
    st.subheader(' ')
    st.subheader(' ')
    st.subheader(' ')

with col2_country:
    all_country = len(get_all_country())
    st.markdown("<h6 style='text-align: left; color: black;'>จำนวนประเทศที่จุฬาทำงานวิจัยร่วม</h6>", unsafe_allow_html=True)
    st.subheader(all_country)

with col3_research:
    dff = get_all_subject_count()
    dff = dff.toPandas()
    n = dff['count'].sum()
    st.markdown("<h6 style='text-align: left; color: black;'>จำนวนงานวิจัยทั้งหมด</h6>", unsafe_allow_html=True)
    st.subheader(n)



col1_first_row, col2_first_row = st.columns([5,3])
with col1_first_row :
    col1_2018_2023, col2_each_year,col3 = st.columns([2,1,3])
    with col1_2018_2023:
        st.markdown("<h6 style='text-align: center; color: black;'>Subject ที่จุฬาฯทำในปี 2018-2023</h6>", unsafe_allow_html=True)
        all_subject_count_df = get_all_subject_count()

        fig = px.pie(all_subject_count_df, values='count', names='subject', title='',
                    hover_data=['subject'], hole=0.3)

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20),height=250, width=250)
        st.plotly_chart(fig)
        st.markdown("<div style='margin-right: 40px'></div>", unsafe_allow_html=True)

    with col2_each_year:
        subject_map = {subject: True for subject in subjects}
        with st.container(border=True,height=300):
            for i in subject_map:
                # st.markdown(f"<style> .checkbox-size input {{ width: 20px; height: 20px; }}</style>", unsafe_allow_html=True)
                subject_map[i] = st.checkbox(i,value=True)
        st.markdown("<div style='margin-left: 40px'></div>", unsafe_allow_html=True)

    with col3:
            selected_subjects = [subject for subject, selected in subject_map.items() if selected]
            filtered_df = get_year_count_filter_by_subject(selected_subjects)
            filtered_df= filtered_df.toPandas()
            fig = px.line(filtered_df, x="year", y="count", color="subject")
            fig.update_layout(
                title="จำนวนงานวิจัยในแต่ละ Subject ที่ทำในปี 2018-2023",
                xaxis_title="Year",
                yaxis_title="Number of Research",
                showlegend=False
                )
            fig.update_layout(height=300, width=600)
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("<div style='margin-left: 40px'></div>", unsafe_allow_html=True)

with col2_first_row:
    col1_pie_chart, col2_pie_chart = st.columns([10,10])
    with col1_pie_chart:
        st.markdown("<h6 style='text-align: center; color: black;'>มหาวิทยาลัยในไทยที่มีความร่วมมือกับจุฬา</h6>", unsafe_allow_html=True)
        chula_collab_affi_df = get_chula_thai_collaboration_by_subject_year_count()

        fig = px.pie(chula_collab_affi_df, values='count', names='affilname', title='',
                    hover_data=['affilname'], hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20),height=250, width=250)
        st.plotly_chart(fig)

    with col2_pie_chart:
        st.markdown("<h6 style='text-align: center; color: black;'>ประเทศที่มีงานวิจัยร่วมกับจุฬา</h6>", unsafe_allow_html=True)
        chula_collab_country_df = get_chula_thai_collaboration_country_by_subject_year_count()

        fig = px.pie(chula_collab_country_df, values='count', names='affiliation_country', title='',
                    hover_data=['affiliation_country'], hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20),height=250, width=250)
        st.plotly_chart(fig)



with st.container(height=1100):
    col1, col2 = st.columns([2,3])
    with col1:
        with st.container():

            col1_affi_in_each_year, col2_dropdown_affi = st.columns([3,2])
            affis = get_all_affil()
            with col2_dropdown_affi:
                optionA = st.selectbox(
                    "Which Affiliation?",
                    affis,
                    index=1,
                    placeholder="Select Affiliation...",
                )

            with col1_affi_in_each_year:
                # st.subheader('ในแต่ละสถาบันเราทำการวิจัยด้วยจำนวนเท่าไหร่ในแต่ละปี')
                st.markdown("<h6 style='text-align: center; color: white;'>จำนวนวิจัยในแต่ละปีจุฬาฯทำกับแต่ละสถาบัน</h6>", unsafe_allow_html=True)
                filtered_df2 = get_filter_by_affilname(optionA)
                st.bar_chart(filtered_df2, x="year", y="count", color="year",height=500) 


    with col2:
        col1_affi_in_subj, col2_dropdown_year = st.columns([8,2])
        years = get_all_year()
        with col2_dropdown_year:
            optionY = st.selectbox(
                "Which Year?",
                years,
                index=1,
                placeholder="Select Year...",
            )
        with col1_affi_in_subj:
            # st.subheader('จุฬาร่วมกับสถาบันไหนใน subject นี้เยอะที่สุด')
            st.markdown("<h6 style='text-align: center; color: white;'>จำนวนงานวิจัยที่จุฬาฯร่วมกับแต่ละสถาบันในแต่ละ subject</h6>", unsafe_allow_html=True)
            filtered_df3 = get_affil_count_filter_by_year(optionY)
            filtered_df3 = filtered_df3.toPandas()
            st.scatter_chart(
                filtered_df3,
                x='affilname',
                y='count',
                color='subject',
                height=1000
            )


