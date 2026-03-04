import streamlit as st

import json
from pathlib import Path

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = [] 

next_order_id_number = 6

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

with tab1:
    st.subheader("Place Order")
    with st.container(border = True):

        col1, col2 = st.columns([2,1])
        # col1, col2 = st.columns(2) this will give you 50/50 
        # col1, col2, col3 = st.columns([1,6,1]) # changes spacing 

        with col1:
            with st.container(border = True):
                st.markdown("##### Order Details")
                title = st.text_input("Item Name", placeholder = "Expresso", help = "Enter the item name.")
                price = st.number_input("Price")
                stock = st.number_input("Stock")
                
                #assignment_type = st.text_input("Assignment Type") # wrong bc we know the tyoes
                assignment_type = st.radio("Type", ["Homework", "Lab"], horizontal=True)
                st.caption("Homework Type")
                assignment_type2 = st.selectbox("Type", ["Select an option","Homework", "Lab", "Other"])
                if assignment_type2 == "Other":
                    assignment_type2 = st.text_input("Type", placeholder = "Enter the assignment Type")


        with col2:
            st.markdown("**Due Date Selection**")
            due_date = st.date_input("Due Date")
        
        btn_save = st.button("Save", use_container_width = True, disabled = False) # width = "content"(len of content), width = "stretch" 
        
        if btn_save:
            if not title:
                st.warning("Title needs to be provided!")
            else:
                with st.spinner("Assignment is being recorded..."):
                    time.sleep(5)

                    new_assignment_id = "HW" + str(next_order_id_number)
                    next_order_id_number += 1

                    assignments.append(
                        {
                            "id" : new_assignment_id,
                            "title" : title,
                            "description" : description,
                            "points" : points,
                            "type" : assignment_type

                        }
                    )

                    # record into json file 
                    with json_path.open("w", encoding = "utf-8") as f:
                        json.dump(assignments, f)



                    st.success("New Assignment is recorded!")
                    st.info("This is a new assignment")
                    st.dataframe(assignments)
