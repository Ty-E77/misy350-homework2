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

# got lines 35 from 44 from chatgpt becuase I tried the method we 
# we used in class but it would't update

max_order_num = 0
for o in orders:
    oid = str(o.get("order_id", ""))
    if oid.startswith("Order_"):
        try:
            max_order_num = max(max_order_num, int(oid.split("_")[1]))
        except ValueError:
            pass

next_order_id_number = max_order_num 

if "show_receipt" not in st.session_state:
    st.session_state.show_receipt = False

if "receipt_data" not in st.session_state:
    st.session_state.receipt_data = None


with tab1:
    st.subheader("Place Order")
    if st.session_state.show_receipt:
        col1, col2 = st.columns([5, 4])
    else:
        col1, = st.columns([10])
    with st.container(border = True):
        with col1:
            with st.container(border = True):
                st.markdown("#### **Order Details**")
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
                    receipt_col = True
                    with st.spinner("Order is being placed..."):
                        time.sleep(5)
            
                    # Reduce stock
                        found_item['stock'] -= quantity_ordered
                        with json_file1.open("w", encoding="utf-8") as f:
                            json.dump(inventory, f, indent=4)
                        
                        next_order_id_number = next_order_id_number + 1
                        new_order_id = "Order_" + str(next_order_id_number)
                        
                    
                    order_status = "Placed"

                    orders.append(
                        {
                            "order_id" : new_order_id,
                            "customer" : customer_name,
                            "item" : selected_item["name"],
                            "quantity" : quantity_ordered,
                            "total" : round(total_price, 2),
                            "status" : order_status

                        }
                    )

                    # record into json file 
                    with json_file2.open("w", encoding = "utf-8") as f:
                        json.dump(orders, f, indent = 6)
                    st.session_state.show_receipt = True
                    st.session_state.receipt_data = {
                         "order_id" : new_order_id,
                         "customer" : customer_name,
                         "item" : selected_item["name"],
                         "quantity" : quantity_ordered,
                         "total" : round(total_price, 2),
                         "status" : order_status
                    }
                    st.rerun()


                    
        if st.session_state.show_receipt and st.session_state.receipt_data:
            with col2:
                with st.container(border=True):
                    receipt = st.session_state.receipt_data
                    st.markdown("#### **Order Receipt**")
                    with st.container(border=True):
                        st.markdown(f"**Order_ID:** {receipt['order_id']}")
                        st.markdown(f"**Customer Name:** {receipt['customer']}")
                        st.markdown(f"**Item Name:** {receipt['item']}")
                        st.markdown(f"**Quantity Ordered:** {receipt['quantity']}")
                        st.markdown(f"**Total:** ${receipt['total']:.2f}")
                        st.markdown(f"**Status:** {receipt['status']}")
            st.success("Order was placed")
                    
with tab2:
    
    tab_option = st.radio("View/Search", ["View", "Search"], horizontal = True)
    
    st.divider()

    with st.container(border = True):
        if tab_option == "View":
            st.markdown("## **Inventory View**")
            st.dataframe(inventory)

            total_stock = 0
            low_stock = 10

            for item in inventory:
                total_stock += item["stock"]
                if item["stock"] < low_stock:
                    st.warning(f"LOW STOCK: {item['name']} has {item['stock']} left in stock.")

            with st.container(border = True):
                st.markdown(f"### **Total Stock:** {total_stock}")        
            

        else:
            with st.container(border = True):
                st.markdown("## Inventory Search")
                selected_item = st.selectbox("Select Item:", options = inventory,
                                            format_func = lambda x: f"{x['name']}",
                                            key = f"view_item{selected_item['id']}")
                if selected_item:
                    with st.expander("**Inventory**", expanded = True):
                        st.markdown(f"**Item ID:** {selected_item['id']}")
                        st.markdown(f"**Item Name:** {selected_item['name']}")
                        st.markdown(f"**Stock Count:** {selected_item['stock']}")

with tab3:
    with st.container(border = True):
        st.markdown("## Restock Inventory")
        with st.container(border = True):
            selected_item = st.selectbox("Select Item:", options = inventory,
                                        format_func = lambda x: f"{x['name']}",
                                        key = f"restock_item{selected_item['id']}")
                
            restock_ordered = int(st.number_input("Enter the restock quantity", 
                                                    min_value = 0, 
                                                    key = f"restock_ordered_{selected_item['id']}"))
            
            btn_restock = st.button("Restock", use_container_width = True, type = "primary", disabled = False) # width = "content"(len of content), width = "stretch" 
            
            if btn_restock:
                if restock_ordered == 0:
                    st.error("Missing required information")
                    st.stop()
                else:
                    found_item = None 
                    for item in inventory:
                        if item['id'] == selected_item['id']:
                            found_item = item
                            break
                    with st.spinner("Restock is being placed..."):
                        time.sleep(5)

                        found_item['stock'] += restock_ordered
                        with json_file1.open("w", encoding="utf-8") as f:
                            json.dump(inventory, f, indent=4)
                        st.success("Restock Placed")

with tab4:
    st.markdown("## Mange Orders")

    tab_option = st.radio("View/Delete or Cancel", ["View", "Delete or Cancel"], horizontal = True)
    
    st.divider()
    with st.container(border = True):
        if tab_option == "View":
            st.markdown("## **Order View**")
            if not orders:
                st.info("No orders have been placed yet.")
                st.stop()
            else:
                st.dataframe(orders)
        else:
            with st.container(border = True):
                st.markdown("### Cancel Order")
                if not orders:
                    st.info("No orders have been placed yet.")
                    st.stop()
                selected_item = st.selectbox("Select order to cancel:", options = orders,
                                        format_func = lambda x: f"{x['order_id']}",
                                        key = f"manage_item_{selected_item['id']}")
            if not orders:
                    st.info("No orders have been placed yet.")
                    st.stop()
            else:
                with st.expander("Order Details", expanded = True):
                    st.markdown(f"### Customer: {selected_item['customer']}")
                    st.markdown(f"**Item:** {selected_item['item']}")
                    st.markdown(f"**Quantity:** {selected_item['quantity']}")
                    st.markdown(f"**Total:** ${selected_item['total']:.2f}")
                    st.markdown(f"**Status:** {selected_item['status']}")
                
            btn_cancel = st.button("Cancel Order", use_container_width = True, type = "primary", disabled = False)

            if btn_cancel:

                found_item = None 
                for item in inventory:
                    if item['name'] == selected_item['item']:
                        found_item = item
                        break

            
                found_item['stock'] = selected_item['quantity'] + found_item['stock']
                with json_file1.open("w", encoding="utf-8") as f:
                    json.dump(inventory, f, indent=4)
                        
                cancel_order = selected_item['order_id']
                orders = [order for order in orders if order['order_id'] != selected_item['order_id']]
                    
                with st.spinner("Order is being cancelled..."):
                    time.sleep(5)
  
                    # record into json file 
                with json_file2.open("w", encoding = "utf-8") as f:
                    json.dump(orders, f, indent = 6)



                st.success("Order Cancelled and Stock Refunded")    