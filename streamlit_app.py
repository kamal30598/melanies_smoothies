# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw:  Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom **Smoothie**!
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)


cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_list = st.multiselect(
    "Choose upto 5 Ingredients",
     my_dataframe, max_selections=5)

if Ingredients_list:
    
    ingredients_string=''

    for fruit_chosen in Ingredients_list:
        ingredients_string +=fruit_chosen +' '

    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS , NAME_ON_ORDER)
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
   #st.stop()

    time_to_insert =st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


        
