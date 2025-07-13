#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import datetime
import pandas as pd
import json
from newsapi import NewsApiClient

fields = "name,cca2" 
response = requests.get(f"https://restcountries.com/v3.1/all?fields={fields}")
st.set_page_config(page_title="streamlit News App", page_icon=":newspaper:", layout="wide")
st.title("📰 news app")



def get_news(country,category, from_date, to_date, api_key,country_name):
    
    API_KEY = "YOUR API KEY" 


    if category == 'headlines':
       url= "https://gnews.io/api/v4/top-headlines"
       params = {
           "token": API_KEY,
           "q":f"{category} AND {country_name}",
           "category": category,
           "country": country,
           
           "lang": "en",  # You can change the language
           "max": 3   # Number of articles to retrieve (max 100 for paid plans)
       } 
    else:    
       url = "https://gnews.io/api/v4/search"
       from_date_iso = from_date.isoformat() + "T00:00:00Z"
       to_date_iso = to_date.isoformat() + "T23:59:59Z"  
   
       params = {
           "token": API_KEY,
           "q":f"{category} AND {country_name}",
           "category": category,
           "country": country,
           "from": from_date_iso,
           "to": to_date_iso,
           "lang": "en",  # You can change the language
           "max": 3   # Number of articles to retrieve (max 100 for paid plans)
       } 
      
       
    
   
    response = requests.get(url, params=params)
 
    data = response.json()


    all_data=[]
  
    if 'articles' in data:
       
        items=data['articles']
       
        for item in items:
           
           news_info={'link':item['url'],
                      'headline':item['title'],
                      'country':country,
                      'category':category,
                     'short_description':item['description'],
                    
                     #'authors':item['author'],
                     'date':item['publishedAt']}
          
           all_data.append(news_info) 
          
           
        return all_data  
    else:
        st.write("Error fetching news:", data)
        return []
  
intro = st.sidebar.radio('Main Menu',["**_:blue[Introduction]_**","**_:blue[Check In for News App]_**"])
if  intro=='Introduction':    
    #main_frame()  
    st.write('Introduction')
elif intro == "**_:blue[Check In for News App]_**":  
    st.title("📖 _:orange[News App]_")

    st.header("📚 :blue[news and sentiment]", divider="rainbow")


    selected_question = st.sidebar.selectbox( "**_:rainbow[Select a Question to View Analysis]_**", ['search','cluster','report'],index=None)
    if selected_question == 'search':
               # Check if the request was successful
              
              if response.status_code == 200:
                      # Successful response, let's proceed
                      data = response.json()
                      

                     # Map country names to their corresponding 2-letter Alpha-2 codes
                      country_codes = {country['name']['common']: country['cca2'] for country in data}
                      sorted_countries = sorted(country_codes.keys())
                      selected_country = st.sidebar.selectbox(':rainbow[Select a country:]', sorted_countries,index=None)
                     # Get the corresponding 2-letter code for the selected country
                      if selected_country is not None:
                             country_code = country_codes[selected_country]
                            
                      categories = ['All','Business', 'Entertainment','HeadLines', 'Health', 'Science', 'Sports', 'Technology']
                      selected_category = st.sidebar.selectbox(':rainbow[Select a category]', categories,index=None)

  
                      max_date = datetime.date.today() 
                      min_date = datetime.date(1800, 1, 1)
                      from_date = st.sidebar.date_input(":rainbow[From date:]", min_value=min_date, max_value=max_date,key="start_date")
                      to_date = st.sidebar.date_input(":rainbow[To date:]", min_value=min_date, max_value=max_date, key="end_date")
                      
                      search=st.sidebar.button("**_:rainbow[SEARCH]_**")
                      if (search):
                          
                          if country_code is not None and selected_category is not None:
                               
                               dff=pd.DataFrame(get_news(country_code.lower(),selected_category.lower(),from_date,to_date,"YOUR  APIKEY",selected_country))
                              
                               if  not dff.empty:
                                    dff['links'] = dff['link']
                                    dff['links'] = dff.apply(lambda row: f"<a href='{row['link']}' target='_blank'>{row['headline']}</a>", axis=1)
                                   
                                    df_display = dff[['links','headline', 'country', 'category','short_description','date']]

                                    html_table = df_display.to_html(escape=False)
                                    st.markdown(html_table, unsafe_allow_html=True)

                                   

                               else:
                                    st.write(dff)
                             
                           

              else:
                      st.error(f"Error fetching data: {response.status_code}")
                      st.write("Response content:", response.text)  # Print the error message if any




