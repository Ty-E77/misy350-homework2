import streamlit as st
import time
import json
from pathlib import Path

json_file1 = Path("inventory.json")

json_file2 = Path("orders.json")


next_order_id_number = 0

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

        col1, col2 = st.columns([5,4])
        # col1, col2 = st.columns(2) this will give you 50/50 
        # col1, col2, col3 = st.columns([1,6,1]) # changes spacing 

    with col1:
        with st.container(border = True):
            st.markdown("##### Order Details")
            customer_name = st.text_input("Enter item name:", placeholder = "Ex: John Doe")

            selected_item = st.selectbox("Select Item:", options = inventory,
                                           format_func = lambda x: f"{x['name']}")
            if selected_item:
                with st.expander("Order Details", expanded = True):
                    st.markdown(f"### Item: {selected_item['name']}")
                    st.markdown(f"Unit Price: ${selected_item['price']}")
                    quantity_ordered = int(st.number_input("Enter the order quantity", 
                                                           min_value = 0, 
                                                           key = f"quantity_ordered_{selected_item['id']}"))
                
                    total_price = quantity_ordered * selected_item['price']

                    st.markdown(f"Total Price: ${total_price:.2f}")
        
                    btn_order = st.button("Place Order", use_container_width = True, type = "primary", disabled = False) # width = "content"(len of content), width = "stretch" 
        
        if btn_order:
            if (not customer_name) or (quantity_ordered == 0):
                st.error("Missing required information")
                st.stop()

            else:
                found_item = None 
                for item in inventory:
                    if item['id'] == selected_item['id']:
                        found_item = item
                        break
                
                if found_item['stock'] < quantity_ordered:
                    st.warning(f"Not enough stock. Available: {found_item['stock']}")
                    st.stop()

                else:
                    with st.spinner("Order is being placed..."):
            
                    # Reduce stock
                        found_item['stock'] -= quantity_ordered
                        with json_file1.open("w", encoding="utf-8") as f:
                            json.dump(inventory, f, indent=4)
                        
                        new_order_id = "Order_" + str(next_order_id_number)
                        next_order_id_number += 1
                    
                    order_status = "Placed"

                    orders.append(
                        {
                            "order_id" : new_order_id,
                            "customer" : customer_name,
                            "item" : selected_item,
                            "quantity" : quantity_ordered,
                            "total" : total_price,
                            "Status" : order_status

                        }
                    )

                    # record into json file 
                    with json_file2.open("w", encoding = "utf-8") as f:
                        json.dump(orders, f)



                    st.success("Order was placed")
                    with col2: 
                        with st.container(border = True):
                            st.markdown("##### Reciept")
                            st.markdown(f"**Order_ID:** {new_order_id}")
                            st.markdown(f"**Customer Name:** {customer_name}")
                            st.markdown(f"**Item Name:** {selected_item['name']}")
                            st.markdown(f"**Quantity Ordered:** {quantity_ordered}")
                            st.markdown(f"**Total:** ${total_price:.2f}")
                            st.markdown(f"**Status:** {order_status}")
                    
