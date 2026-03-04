import streamlit as st

import json
from pathlib import Path

json_file1 = Path("inventory.json")

json_file2 = Path("orders.json")


next_order_id_number = 3

# For saving after changing information
#with open(json_file, "w") as f:
    #json.dump(inventory, f, indent=4)

st.set_page_config(page_title = "Inventory Management", 
                   page_icon = "",
                   layout = "centered",
                   initial_sidebar_state = "collapsed")

st.title("Inventory Management App")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Place Order", "View Inventory", "Restock", "Manage Orders"])

if json_file1.exists():
    with open(json_file1, "r") as f:
        inventory = json.load(f)

if json_file2.exists():
    with open(json_file2, "r") as f:
        orders = json.load(f)
with tab1:
    st.subheader("Place Order")
    with st.container(border = True):

        col1, col2 = st.columns([2,1])
        # col1, col2 = st.columns(2) this will give you 50/50 
        # col1, col2, col3 = st.columns([1,6,1]) # changes spacing 

    with col1:
        with st.container(border = True):
            st.markdown("##### Order Details")
            place_order = []

            selected_item = st.selectbox("Select Item", options = inventory,
                                           format_func = lambda x: f"{x['name']}")
            if selected_item:
                with st.expander("Order Details", expanded = True):
                    st.markdown(f"### Item: {selected_item["name"]}")
                    st.markdown(f"Unit Price: {selected_item["price"]}")
                    quantity_orederd = int(st.number_input("Enter the order quantity", 
                                                           min_value = 0, 
                                                           key = f"quantity_ordered_{selected_item["id"]}"))
                
                    total_price = quantity_orederd * selected_item["price"]

                    st.markdown(f"Total Price: {total_price}")
        

            
            
    
            #enter_quantity =
             
            #show_total_price =  

            #edit_name = st.text_input("Item Name", key = f"edit_name_{place_order_edit["id"]}", value = place_order_edit["name"])

        
        # btn_save = st.button("Save", use_container_width = True, disabled = False) # width = "content"(len of content), width = "stretch" 
        
        # if btn_save:
        #     if not title:
        #         st.warning("Title needs to be provided!")
        #     else:
        #         with st.spinner("Assignment is being recorded..."):
        #             time.sleep(5)

        #             new_assignment_id = "HW" + str(next_order_id_number)
        #             next_order_id_number += 1

        #             assignments.append(
        #                 {
        #                     "id" : new_assignment_id,
        #                     "title" : title,
        #                     "description" : description,
        #                     "points" : points,
        #                     "type" : assignment_type

        #                 }
        #             )

        #             # record into json file 
        #             with json_path.open("w", encoding = "utf-8") as f:
        #                 json.dump(assignments, f)



        #             st.success("New Assignment is recorded!")
        #             st.info("This is a new assignment")
        #             st.dataframe(assignments)
