import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from spark import get_year_count_filter_by_subject , get_all_affil , get_filter_by_affilname ,get_affil_count_filter_by_year , get_all_year, get_all_subject_count, get_chula_thai_collaboration_country_by_subject_year_count, get_chula_thai_collaboration_by_subject_year_count, get_all_country

subjects = ["GENE","AGRI","ARTS","BIOC","BUSI","CENG","CHEM","COMP","DECI","EART","ECON","ENER","ENGI","ENVI","IMMU","MATE","MATH","MEDI","NEUR","NURS","PHAR","PHYS","PSYC","SOCI","VETE","DENT","HEAL"] #27 subjects

st.set_page_config(layout="wide")

st.title(':rainbow[Scopus Dashboard]') #มั้ยย

st.subheader(' ')

# Cached functions imported from spark module
get_year_count_filter_by_subject_cached = st.cache_data(get_year_count_filter_by_subject)
get_all_affil_cached = st.cache_data(get_all_affil)
get_filter_by_affilname_cached = st.cache_data(get_filter_by_affilname)
get_affil_count_filter_by_year_cached = st.cache_data(get_affil_count_filter_by_year)
get_all_year_cached = st.cache_data(get_all_year)
get_all_subject_count_cached = st.cache_data(get_all_subject_count)
get_chula_thai_collaboration_country_by_subject_year_count_cached = st.cache_data(get_chula_thai_collaboration_country_by_subject_year_count)
get_chula_thai_collaboration_by_subject_year_count_cached = st.cache_data(get_chula_thai_collaboration_by_subject_year_count)
get_all_country_cached = st.cache_data(get_all_country)

col1_affi, col2_country,col3_research = st.columns(3)
with col1_affi:
    all_affi = len(get_all_affil_cached())
    st.markdown("<h6 style='text-align: left; color: white;'>จำนวนสถาบันที่จุฬาฯทำงานวิจัยร่วมในปี 2018-2023</h6>", unsafe_allow_html=True)
    st.subheader(all_affi)
    st.subheader(' ')
    st.subheader(' ')
    st.subheader(' ')

with col2_country:
    all_country = len(get_all_country_cached())
    st.markdown("<h6 style='text-align: left; color: white;'>จำนวนประเทศที่จุฬาฯทำงานวิจัยร่วมในปี 2018-2023</h6>", unsafe_allow_html=True)
    st.subheader(all_country)

with col3_research:
    dff = get_all_subject_count_cached()
    n = dff['count'].sum()
    st.markdown("<h6 style='text-align: left; color: white;'>จำนวนงานวิจัยของจุฬาฯทั้งหมดในปี 2018-2023</h6>", unsafe_allow_html=True)
    st.subheader(n)



col1_first_row, col2_first_row = st.columns([5,3])
with col1_first_row :
    col2_each_year,col3 = st.columns([1,3])
    with col2_each_year:
        st.write("หัวข้องานวิจัย")
        subject_map = {subject: True for subject in subjects}
        with st.container(border=True,height=256):
            for i in subject_map:
                subject_map[i] = st.checkbox(i,value=True)
        st.markdown("<div style='margin-left: 40px'></div>", unsafe_allow_html=True)

    with col3:
            selected_subjects = [subject for subject, selected in subject_map.items() if selected]
            filtered_df = get_year_count_filter_by_subject_cached(selected_subjects)
            fig = px.line(filtered_df, x="year", y="count", color="subject")
            fig.update_layout(
                title="                                               จำนวนงานวิจัยในแต่ละหัวข้อที่ทำในปี 2018-2023",
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
        st.markdown("<h6 style='text-align: center; color: white;'>สถาบันในไทยที่มีความร่วมมือกับจุฬาฯ</h6>", unsafe_allow_html=True)
        chula_collab_affi_df = get_chula_thai_collaboration_by_subject_year_count_cached()

        fig = px.pie(chula_collab_affi_df, values='count', names='affilname', title='',
                    hover_data=['affilname'], hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20),height=250, width=250)
        st.plotly_chart(fig)

    with col2_pie_chart:
        st.markdown("<h6 style='text-align: center; color: white;'>ประเทศที่มีงานวิจัยร่วมกับจุฬาฯ</h6>", unsafe_allow_html=True)
        chula_collab_country_df = get_chula_thai_collaboration_country_by_subject_year_count_cached()

        fig = px.pie(chula_collab_country_df, values='count', names='affiliation_country', title='',
                    hover_data=['affiliation_country'], hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20),height=250, width=250)
        st.plotly_chart(fig)



with st.container(height=1200):
    col1, col2 = st.columns([2,3])
    with col1:
        with st.container():
            st.subheader(' ')
            st.markdown("<h6 style='text-align: center; color: white;'>หัวข้องานวิจัยที่จุฬาฯทำในปี 2018-2023</h6>", unsafe_allow_html=True)
            all_subject_count_df = get_all_subject_count_cached()

            fig = px.pie(all_subject_count_df, values='count', names='subject', title='',
                        hover_data=['subject'], hole=0.3)

            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=100, r=20),height=400, width=400)
            st.plotly_chart(fig)
            st.markdown("<div style='margin-right: 120px'></div>", unsafe_allow_html=True)
        with st.container():
            affis = get_all_affil_cached()
            with st.container():
                st.subheader(' ')
                st.markdown("<h6 style='text-align: center; color: white;'>จำนวนงานวิจัยในแต่ละปีที่จุฬาฯทำร่วมกับแต่ละสถาบัน</h6>", unsafe_allow_html=True)
                optionA = st.selectbox(
                    "Which Affiliation?",
                    affis,
                    index=1,
                    placeholder="Select Affiliation...",
                )

            with st.container():
                filtered_df2 = get_filter_by_affilname_cached(optionA)
                fig = px.bar(filtered_df2, x="year", y="count", color="year")
                fig.update_layout(
                    autosize=True,
                    height=500,
                    width=480,
                    xaxis=dict(fixedrange=True, tickvals=filtered_df2['year'].unique(), tickmode='linear'),
                    yaxis=dict(fixedrange=True, showticklabels=False,tickvals=list(range(int(filtered_df2['count'].max()) + 1))),
                    xaxis_title="Year",
                    yaxis_title="Number of Research",
                )
                st.plotly_chart(fig)


    with col2:
        col1_affi_in_subj, col2_dropdown_year = st.columns([8,2])
        years = get_all_year_cached()
        with col2_dropdown_year:
            st.subheader(' ')
            optionY = st.selectbox(
                "Which Year?",
                years,
                index=1,
                placeholder="Select Year...",
            )
        with col1_affi_in_subj:
            st.subheader(' ')
            st.markdown("<div style='margin-left: 40px'></div>", unsafe_allow_html=True)
            st.markdown("<h6 style='text-align: center; color: white;'>จำนวนงานวิจัยที่จุฬาฯร่วมกับแต่ละสถาบันในแต่ละหัวข้อ</h6>", unsafe_allow_html=True)
            filtered_df3 = get_affil_count_filter_by_year_cached(optionY)
            # st.scatter_chart(
            #     filtered_df3,
            #     x='affilname',
            #     y='count',
            #     color='subject',
            #     height=1000
            # )
            fig = px.scatter(filtered_df3, x='affilname', y='count', color='subject')

            fig.update_layout(
                title="",
                autosize=False, 
                height=1100,
                xaxis=dict(fixedrange=False,visible=False), 
                yaxis=dict(fixedrange=False),
                xaxis_title="Affiliation Name", 
                yaxis_title="Number of Research",
            )
            st.plotly_chart(fig)
