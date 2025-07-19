#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import requests
import datetime
import pandas as pd
import json
from newsapi import NewsApiClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.corpus import stopwords
import re
try:
    nltk.data.find('corpora/stopwords')
except LookupError: # This is the correct exception to catch when a resource is not found
    nltk.download('stopwords')
    print("NLTK 'stopwords' downloaded successfully.")
except Exception as e:
    print(f"An unexpected error occurred during NLTK stopwords check/download: {e}")

fields = "name,cca2" 
response = requests.get(f"https://restcountries.com/v3.1/all?fields={fields}")
st.set_page_config(page_title="streamlit News App", page_icon=":newspaper:", layout="wide")
st.title("📰 news app")


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) # Remove non-alphabetic characters
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return " ".join(words)
def get_news(country,category, from_date, to_date, api_key,country_name):
    
    API_KEY = "YOUR API KEY" 

    if category == 'headlines':
       url= "https://gnews.io/api/v4/top-headlines"
       params = {
           "token": API_KEY,
           "q":f"{category} AND {country_name}",
           "category": category,
           "country": country,
           
           "lang": "en",  
           "max": 3   
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
           "lang": "en",  
           "max": 3  
       } 
    response = requests.get(url, params=params)
    data = response.json()
    all_data=[]    
  
    if 'articles' in data:
       
        items=data['articles']
       
        for item in items:
           
           news_info={'link':item['url'],
                      'headline':item['title'],
                      'country':country_name,
                      'category':category,
                      'short_description':item['description'],
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


    selected_question = st.sidebar.selectbox( "**_:rainbow[Select a Question to View Analysis]_**", ['Search News','Cluster','Report'],index=None)
    if selected_question == 'Search News':
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
                               
                               dff=pd.DataFrame(get_news(country_code.lower(),selected_category.lower(),from_date,to_date,"yourapikey",selected_country))
                              
                               if  not dff.empty:
                                    dff['links'] = dff['link']
                                    dff['links'] = dff.apply(lambda row: f"<a href='{row['link']}' target='_blank'>{row['headline']}</a>", axis=1)
                                   
                                    df_display = dff[['links','headline', 'country', 'category','short_description','date']]

                                    html_table = df_display.to_html(escape=False)
                                    st.markdown(html_table, unsafe_allow_html=True)

                                    st.write("---")

                               else:
                                    st.write(dff)
                             
                           

              else:
                      st.error(f"Error fetching data: {response.status_code}")
                      st.write("Response content:", response.text)  # Print the error message if any
    elif selected_question == 'Cluster':    
              dfvec=pd.read_csv(r'c:\users\91904\combined.csv')
              vect=TfidfVectorizer(stop_words='english',max_features=5000)
              dfvec['headline'] = dfvec['headline'].fillna('')
              dfvec['short_description'] = dfvec['short_description'].fillna('')
              dfvec['text_content'] = dfvec['headline'] + " " + dfvec['short_description']
              x=vect.fit_transform(dfvec['text_content'])
              num_cluster=7
              kmean=KMeans(n_clusters=7,random_state=42,init='k-means++')
              dfvec['cluster']=kmean.fit_predict(x)
              cluster_name_mapping = {
                                    0: "US Presidential Campaigns (Clinton-Sanders Era)",
                                    1: "Regional US News & Local Stories",
                                    2: "Presidential & Judicial Affairs (Obama Era Focus)",
                                    3: "US Congressional & White House Politics",
                                    4: "Broad & General News Coverage",
                                    5: "Healthcare Policy & Debates",
                                    6: "Donald Trump & Related Politics"}
              unique_clusters = sorted(dfvec['cluster'].unique())
              n_clusters = len(unique_clusters)
              n_cols = min(3, n_clusters) 
              n_rows = (n_clusters + n_cols - 1) // n_cols
              #fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4)) 
              fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
              if n_rows * n_cols == 1: # Only one subplot
                                axes = np.array([axes]) # Wrap the single Axes object in an array
              else:
                                axes = axes.flatten() 
             # plt.figure(figsize=(n_cols * 5, n_rows * 4))
             
              for i, cluster_id in enumerate(unique_clusters):
    # Filter text content for the current cluster
                     cluster_text = " ".join(dfvec[dfvec['cluster'] == cluster_id]['text_content'].dropna())
                  
    # Generate word cloud
                     wordcloud = WordCloud(width=800, height=400, background_color='white',
                     max_words=50, collocations=False).generate(cluster_text)
                    
    # Get the meaningful title for the current cluster
                     cluster_title = cluster_name_mapping.get(cluster_id, f"Cluster {cluster_id} (No Title)")
    # Plotting
                     
                     

                    # plt.subplot(n_rows, n_cols, i + 1)
                     ax = axes[i] 
                     ax.imshow(wordcloud, interpolation='bilinear')
                     ax.set_title(cluster_title, fontsize=12, wrap=True)
                     ax.axis('off')
             
                    # plt.subplot(n_rows, n_cols, i + 1) # Create subplot
                    # plt.imshow(wordcloud, interpolation='bilinear')
                    # plt.title(cluster_title, fontsize=12, wrap=True) # Use the meaningful title
                    # plt.axis('off')
              for j in range(n_clusters, n_rows * n_cols):
                                axes[j].set_visible(False)
              plt.tight_layout() # Adjust layout to prevent titles/plots from overlapping
              plt.suptitle("Word Clouds for News Article Clusters", y=1.02, fontsize=16) # Overall title
              st.pyplot(fig)
              plt.close(fig)
              custom_query = st.sidebar.text_input(
                ":rainbow[Enter custom search keywords:]")
              if custom_query !="": 
                     pre_text=preprocess_text(custom_query)  

                     vect_text=vect.transform([pre_text])
                     predict=(kmean.predict(vect_text))
                     cluster = cluster_name_mapping.get(predict[0], f"Cluster {predict[0]} (No Title)")
                     st.sidebar.write(f"**_:rainbow[{cluster}]_**")
       
        










