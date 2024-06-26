# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
#st.write("""Name on Smoothie:""")
name_on_order=st.text_input('Name on Smoothie:')
if name_on_order:
    name_on_order = ' '.join(elem.capitalize() for elem in name_on_order.split())
st.write ('The name on your Smoothie will be:',name_on_order)
st.write(
    """Choose the **Fruits**:lemon::banana::apple::cherries: you want in your custom smoothie!
    """)
from snowflake.snowpark.functions import col
#session = get_active_session()
session=st.connection("snowflake").session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
ingredients_list = st.multiselect('choose up to **5** ingredients:', my_dataframe, max_selections=5)

if ingredients_list and name_on_order:
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == x, 'SEARCH_ON'].iloc[0]
        st.subheader(x + ' Nnutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+x)
        st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        #st.text(fruityvice_response)
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(ingredients_string)
    time_to_insert = st.button('Submit')
    
    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothies is ordered,'+name_on_order+':'+ingredients_string+'!' ,icon="✅")
        my_insert_stmt = ''
        #st.multiselect = []

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
#st.dataframe(data=fruityvice_response.json(),use_container_width=True)
