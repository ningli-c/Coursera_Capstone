
# coding: utf-8

# In[197]:


from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import numpy as np


# In[198]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
page = urllib.request.urlopen(url)


# In[199]:


soup = BeautifulSoup(page, 'html.parser')


# ### scrape postal code from table in wikipedia link and drop the first row.

# In[200]:


data = []
table = soup.find('table', attrs={'class':'wikitable sortable'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
code = pd.DataFrame(data, columns=["PostalCode", "Borough", "Neighborhood"])
code.drop(code.index[0],inplace = True)
code.head(10)


#  ### Drop cells with a borough that is Not assigned.

# In[201]:


code = code[code.Borough != 'Not assigned']
code.shape


# ### merge cells with same Postal Code

# In[202]:


code = code.groupby(['PostalCode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
code.shape


# ### assign borough name to neighborhood where neighborhood is not assigned

# In[203]:


index = code['Neighborhood'] == 'Not assigned'
code.loc[index,'Neighborhood'] = code[index].Borough


# In[191]:


code.shape

