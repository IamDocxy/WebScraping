
# coding: utf-8

# In[31]:


import requests
from bs4 import BeautifulSoup

url = "http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS"
r = requests.get(url)

c = r.content

soup = BeautifulSoup(c,"html.parser")
# print(soup.prettify())

page_nr = soup.find_all("a",{"class":"Page"})[-1].text

l = []
base_url = url+"/t=0&s="
for page in range(0,int(page_nr)*10,10):
    r=requests.get(base_url+str(page)+".html")
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d = {}

        d["Address"] = item.find_all("span",{"class":{"propAddressCollapse"}})[0].text # Address Line 1
        try:
            d["Locality"] = item.find_all("span",{"class":{"propAddressCollapse"}})[1].text # Address Line 2
        except:
            d["Locality"] = None
            
        d["Price"] = item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","") # price

        try:
            d["Beds"] = item.find("span",{"class":"infoBed"}).find("b").text # No. of bedrooms
        except:
            d["Beds"] = None

        try:
            d["Area"] = item.find("span",{"class":"infoSqFt"}).find("b").text # SqFt
        except:
            d["Area"] = None

        try:
            d["Full Baths"] = item.find("span",{"class":"infoValueFullBath"}).find("b").text # No. of bathrooms
        except:
            d["Full Baths"] = None

        try:
            d["Full Baths"] = item.find("span",{"class":"infoValueHalfBath"}).find("b").text # No. of Half bathrooms
        except:
            d["Full Baths"] = None

        # Retrieving the "Lot Size"
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),                                                   column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)


# In[32]:


import pandas
df = pandas.DataFrame(l)


# In[33]:


df


# In[36]:


df.to_csv("OutPut.csv")

