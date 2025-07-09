import streamlit as st
import json
import os

CAKES_FILE = 'cakes.json'
ORDERS_FILE = 'orders.json'
REVIEWS_FILE = 'reviews.json'  # New for reviews

# ---------- Utility Functions ----------

def load_data(file, default):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return default

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- Cake Management ----------

def add_cake():
    st.subheader("🍰 Add New Cake")

    cakes = load_data(CAKES_FILE, {})

    def generate_cake_id():
        if not cakes:
            return '100'
        ids = [int(k) for k in cakes.keys() if k.isdigit()]
        return str(max(ids) + 1) if ids else '100'

    cake_id = generate_cake_id()
    st.text(f"Generated Cake ID: {cake_id}")

    name = st.text_input("Cake Name")
    price = st.number_input("Price", min_value=0.01, format="%.2f")

    if st.button("Add Cake"):
        if not name.strip():
            st.error("Cake name cannot be empty.")
        elif price <= 0:
            st.error("Price must be greater than 0.")
        elif cake_id in cakes:
            st.error("Generated Cake ID already exists. Please try again.")
        else:
            cakes[cake_id] = {'name': name.strip(), 'price': price}
            save_data(CAKES_FILE, cakes)
            st.success(f"Cake '{name}' added successfully with ID {cake_id}!")
            # Removed experimental_rerun()

    st.markdown("---")
    st.write("### Current Cakes in Menu:")
    if cakes:
        for id_, cake in cakes.items():
            st.write(f"- **{cake['name']}** - ${cake['price']:.2f} (ID: {id_})")
    else:
        st.info("No cakes added yet.")

# ---------- View Cakes (Menu Style) ----------

def view_cakes():
    st.subheader("🎂 Available Cakes")

    cakes = load_data(CAKES_FILE, {})
    if not cakes:
        st.info("No cakes in the menu.")
        return

    cols_per_row = 3
    cake_items = list(cakes.items())

    for i in range(0, len(cake_items), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, (cake_id, cake) in zip(cols, cake_items[i:i+cols_per_row]):
            with col:
                st.markdown(f"### {cake['name']}")
                st.write(f"**Price:** ${cake['price']:.2f}")
                st.markdown("🍰")
                st.caption(f"ID: {cake_id}")

# ---------- Order Management ----------

def place_order():
    st.subheader("🛒 Place Order")
    cakes = load_data(CAKES_FILE, {})
    if not cakes:
        st.warning("No cakes available.")
        return

    customer_name = st.text_input("Customer Name")
    order = []
    total = 0.0

    for id_, cake in cakes.items():
        qty = st.number_input(f"{cake['name']} (${cake['price']:.2f}) - Quantity:", min_value=0, key=id_)
        if qty > 0:
            cost = qty * cake['price']
            total += cost
            order.append({'cake': cake['name'], 'qty': qty, 'cost': cost})

    if st.button("Submit Order"):
        if not customer_name:
            st.error("Customer name is required.")
            return
        if not order:
            st.warning("No items selected.")
            return
        orders = load_data(ORDERS_FILE, [])
        orders.append({'customer': customer_name, 'order': order, 'total': total})
        save_data(ORDERS_FILE, orders)
        st.success(f"Order placed successfully! Total: ${total:.2f}")

        with st.expander("Receipt"):
            st.write(f"**Customer:** {customer_name}")
            for item in order:
                st.write(f"{item['cake']} x{item['qty']} = ${item['cost']:.2f}")
            st.write(f"**Total:** ${total:.2f}")

# ---------- Reviews Management ----------

def show_reviews():
    st.subheader("💬 Customer Reviews")

    reviews = load_data(REVIEWS_FILE, [])

    if reviews:
        for rev in reviews:
            st.markdown(f"**{rev['name']}** says:")
            st.write(f"> {rev['comment']}")
            st.markdown("---")
    else:
        st.info("No reviews yet. Be the first to add one!")

    st.markdown("### Add a Review")
    with st.form("review_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        comment = st.text_area("Your Review")
        submitted = st.form_submit_button("Submit Review")
        if submitted:
            if not name.strip() or not comment.strip():
                st.error("Please fill in both fields.")
            else:
                reviews.append({'name': name.strip(), 'comment': comment.strip()})
                save_data(REVIEWS_FILE, reviews)
                st.success("Thank you for your review!")
                # No rerun needed

# ---------- Main App ----------

def main():
    st.title("🎂 Cake Shop Management System")

    menu = ["Home", "Add Cake", "Place Order", "View Cakes"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.header("Welcome to SweetDelights Cake Shop! 🎂")
        st.write("""
        We bake fresh cakes daily with love and the finest ingredients. 
        Use this system to manage your cakes, place orders, and keep track of everything easily.
        """)

        cakes = load_data(CAKES_FILE, {})
        orders = load_data(ORDERS_FILE, [])

        st.markdown(f"**Total Cakes in Menu:** {len(cakes)}")
        st.markdown(f"**Total Orders Placed:** {len(orders)}")

        st.image("https://images.unsplash.com/photo-1505253210343-04bb4a04a39c?auto=format&fit=crop&w=600&q=80", caption="Freshly baked cakes!")

        st.markdown("> _“A party without cake is just a meeting.”_ 🎉")

        show_reviews()

    elif choice == "Add Cake":
        add_cake()
    elif choice == "Place Order":
        place_order()
    elif choice == "View Cakes":
        view_cakes()

if __name__ == "__main__":
    main()


