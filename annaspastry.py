import streamlit as st
import json
import os
from PIL import Image
import requests
from io import BytesIO
import re

CAKES_FILE = 'cakes.json'
ORDERS_FILE = 'orders.json'
REVIEWS_FILE = 'reviews.json'

# ---------- Utility Functions ----------

def load_data(file, default):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return default

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- Admin Authentication ----------

def admin_login():
    st.sidebar.subheader("🔒 Admin Login")
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if "login_trigger" not in st.session_state:
        st.session_state.login_trigger = False

    password = st.sidebar.text_input("Enter Admin Password:", type="password")
    if st.sidebar.button("Login as Admin"):
        if password == "olsi08":
            st.session_state.admin_authenticated = True
            st.session_state.login_trigger = not st.session_state.login_trigger
        else:
            st.sidebar.error("Incorrect password.")
        st.stop()
    elif not st.session_state.admin_authenticated:
        st.stop()

# ---------- Cake Management (Add, Edit, Remove) ----------

def add_cake():
    st.subheader("🍰 Cake Management Panel")

    cakes = load_data(CAKES_FILE, {})

    if not os.path.exists("cake_images"):
        os.makedirs("cake_images")

    # Add Cake
    st.markdown("### ➕ Add a New Cake")
    name = st.text_input("Cake Name")
    price = st.number_input("Price", min_value=0.01, step=0.01, format="%.2f")
    uploaded_file = st.file_uploader("Upload Cake Image", type=['png', 'jpg', 'jpeg'])

    if st.button("Add Cake"):
        if not name.strip():
            st.error("Cake name cannot be empty.")
        elif price <= 0:
            st.error("Price must be greater than 0.")
        elif uploaded_file is None:
            st.error("Please upload an image of the cake.")
        else:
            cake_id = name.strip().replace(" ", "_").lower()
            if cake_id in cakes:
                st.error("A cake with this name already exists. Please use a unique name.")
                return

            image = Image.open(uploaded_file)
            image.thumbnail((300, 200))  # resize max 300x200 px
            image_path = f"cake_images/{cake_id}_{uploaded_file.name}"
            image.save(image_path)

            cakes[cake_id] = {
                'name': name.strip(),
                'price': price,
                'image_path': image_path
            }

            save_data(CAKES_FILE, cakes)
            st.success(f"Cake '{name}' added successfully!")

    st.markdown("---")

    # Edit Cake
    st.markdown("### ✏️ Edit Existing Cake")

    if not cakes:
        st.info("No cakes to edit.")
    else:
        cake_names = {cake['name']: cid for cid, cake in cakes.items()}
        selected_name = st.selectbox("Select a cake to edit", list(cake_names.keys()), key="edit_select")
        cake_id = cake_names[selected_name]
        cake = cakes[cake_id]

        new_name = st.text_input("New Cake Name", value=cake['name'], key="edit_name")
        new_price = st.number_input("New Price", value=float(cake['price']), min_value=0.01, step=0.01, format="%.2f", key="edit_price")
        new_image = st.file_uploader("Replace Cake Image (optional)", type=["png", "jpg", "jpeg"], key="edit_image")

        if st.button("Update Cake"):
            new_id = new_name.strip().replace(" ", "_").lower()
            if new_id != cake_id and new_id in cakes:
                st.error("Another cake already exists with this name.")
                return

            if new_image is not None:
                if cake.get("image_path") and os.path.exists(cake["image_path"]):
                    os.remove(cake["image_path"])
                image = Image.open(new_image)
                image.thumbnail((300, 200))
                new_image_path = f"cake_images/{new_id}_{new_image.name}"
                image.save(new_image_path)
            else:
                new_image_path = cake["image_path"]

            if new_id != cake_id:
                del cakes[cake_id]

            cakes[new_id] = {
                "name": new_name.strip(),
                "price": new_price,
                "image_path": new_image_path
            }

            save_data(CAKES_FILE, cakes)
            st.success(f"Cake '{new_name}' updated successfully!")

    st.markdown("---")

    # Remove Cake
    st.markdown("### ❌ Remove a Cake")

    if not cakes:
        st.info("No cakes to remove.")
    else:
        cake_names = {cake['name']: cid for cid, cake in cakes.items()}
        selected_delete = st.selectbox("Select a cake to remove", list(cake_names.keys()), key="delete_select")

        if st.button("Remove Selected Cake"):
            cake_id = cake_names[selected_delete]
            image_path = cakes[cake_id].get("image_path")
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            del cakes[cake_id]
            save_data(CAKES_FILE, cakes)
            st.success(f"Cake '{selected_delete}' removed successfully!")

# ---------- View Cakes (Menu) ----------

def view_cakes():
    st.subheader("🍰 Menu")
    cakes = load_data(CAKES_FILE, {})

    if not cakes:
        st.info("No cakes in the menu.")
        return

    cols = st.columns(3)
    cake_list = list(cakes.values())

    for idx, cake in enumerate(cake_list):
        # Check all needed keys to avoid errors
        if not all(k in cake for k in ('name', 'price', 'image_path')):
            continue

        with cols[idx % 3]:
            if cake.get('image_path') and os.path.exists(cake['image_path']):
                try:
                    image = Image.open(cake['image_path'])
                    image = image.resize((300, 200))
                    st.image(image)
                except:
                    st.image("https://via.placeholder.com/300x200.png?text=No+Image")
            else:
                st.image("https://via.placeholder.com/300x200.png?text=No+Image")
            st.markdown(f"### {cake['name']}")
            st.write(f"**Price:** ${cake['price']:.2f}")

# ---------- Order Management ----------

def place_order():
    st.subheader("🛒 Place Order")
    cakes = load_data(CAKES_FILE, {})
    if not cakes:
        st.warning("No cakes available.")
        return

    customer_name = st.text_input("Customer Name")
    customer_surname = st.text_input("Customer Surname")
    customer_email = st.text_input("Email")
    customer_phone = st.text_input("Phone Number")
    customer_email_password = st.text_input("Email Password", type="password")

    def valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def valid_phone(phone):
        pattern = r"^\+?[\d\s\-\(\)]{7,20}$"
        return re.match(pattern, phone) is not None

    order = []
    total = 0.0

    for id_, cake in cakes.items():
        qty = st.number_input(f"{cake['name']} (${cake['price']:.2f}) - Quantity:", min_value=0, key=id_)
        if qty > 0:
            cost = qty * cake['price']
            total += cost
            order.append({'cake': cake['name'], 'qty': qty, 'cost': cost})

    if st.button("Submit Order"):
        if not customer_name.strip():
            st.error("Customer name is required.")
            return
        if not customer_surname.strip():
            st.error("Customer surname is required.")
            return
        if not customer_email.strip() or not valid_email(customer_email.strip()):
            st.error("Please enter a valid email address.")
            return
        if not customer_phone.strip() or not valid_phone(customer_phone.strip()):
            st.error("Please enter a valid phone number (digits, +, spaces, dashes, parentheses allowed).")
            return
        if not customer_email_password.strip():
            st.error("Email password is required.")
            return
        if not order:
            st.warning("No items selected.")
            return

        orders = load_data(ORDERS_FILE, [])
        orders.append({
            'customer': {
                'name': customer_name.strip(),
                'surname': customer_surname.strip(),
                'email': customer_email.strip(),
                'phone': customer_phone.strip(),
                'email_password': customer_email_password.strip()
            },
            'order': order,
            'total': total
        })
        save_data(ORDERS_FILE, orders)

        st.success(f"Order placed successfully! Total: ${total:.2f}")
        with st.expander("Receipt"):
            st.write(f"**Customer:** {customer_name} {customer_surname}")
            st.write(f"**Email:** {customer_email}")
            st.write(f"**Phone:** {customer_phone}")
            for item in order:
                st.write(f"{item['cake']} x{item['qty']} = ${item['cost']:.2f}")
            st.write(f"**Total:** ${total:.2f}")

# ---------- Reviews with Star Ratings ----------

def show_reviews():
    st.subheader("💬 Customer Reviews")
    reviews = load_data(REVIEWS_FILE, [])

    if reviews:
        for rev in reviews:
            stars = "⭐" * rev.get('rating', 0)
            st.markdown(f"**{rev['name']}** {stars} says:")
            st.write(f"> {rev['comment']}")
            st.markdown("---")
    else:
        st.info("No reviews yet. Be the first to add one!")

    st.markdown("### Add a Review")
    with st.form("review_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        rating = st.slider("Rating", min_value=1, max_value=5, value=5)
        comment = st.text_area("Your Review")
        submitted = st.form_submit_button("Submit Review")
        if submitted:
            if not name.strip() or not comment.strip():
                st.error("Please fill in both fields.")
            else:
                reviews.append({'name': name.strip(), 'comment': comment.strip(), 'rating': rating})
                save_data(REVIEWS_FILE, reviews)
                st.success("Thank you for your review!")

# ---------- View Orders (Admin Only) ----------

def view_orders():
    st.subheader("📦 All Orders (Admin Only)")
    orders = load_data(ORDERS_FILE, [])
    if not orders:
        st.info("No orders placed yet.")
        return

    for idx, order in enumerate(orders, 1):
        st.markdown(f"### Order #{idx}")
        customer = order.get('customer', {})
        name = customer.get('name', 'N/A')
        surname = customer.get('surname', '')
        email = customer.get('email', 'N/A')
        phone = customer.get('phone', 'N/A')
        email_password = customer.get('email_password', '')
        masked_password = '*' * len(email_password) if email_password else 'N/A'

        st.write(f"**Customer:** {name} {surname}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Email Password:** {masked_password}")

        for item in order['order']:
            st.write(f"- {item['cake']} x{item['qty']} = ${item['cost']:.2f}")
        st.write(f"**Total:** ${order['total']:.2f}")
        st.markdown("---")

# ---------- Main ----------

def main():
    st.set_page_config(page_title="Anna's Pastry", page_icon="🍰")

    logo_path = "annas_logo.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=150)

    st.sidebar.title("🍰 Anna's Pastry")

    role = st.sidebar.radio("Login as:", ["Customer", "Admin"])

    if role == "Admin":
        admin_login()

    st.title("🍰 Anna's Pastry Management System")

    if role == "Admin" and st.session_state.get("admin_authenticated", False):
        menu = ["Home", "Add Cake", "Place Order", "View Cakes", "View Orders"]
    else:
        menu = ["Home", "Place Order", "View Cakes"]

    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.header("Welcome to Anna's Pastry!")
        st.write("""
        We bake fresh cakes daily with love and the finest ingredients.
        Use this system to manage cakes, place orders, and share your experience.
        """)

        # About Us Section
        st.markdown("## About Us")
        st.write("""
        At Anna's Pastry, we are passionate about creating delicious, beautiful cakes for every occasion.  
        Our team uses only the highest quality ingredients and traditional baking methods to ensure every bite delights.  
        Whether you're celebrating a birthday, wedding, or just want a sweet treat, Anna's Pastry is here to make your day special.
        """)

        if os.path.exists(logo_path):
            st.image(logo_path, caption="Freshly baked cakes!", use_column_width=True)
        else:
            st.warning("Anna's logo image not found.")

        st.markdown("> _“A party without cake is just a meeting.”_ 🎉")
        show_reviews()

    elif choice == "Add Cake":
        add_cake()
    elif choice == "Place Order":
        place_order()
    elif choice == "View Cakes":
        view_cakes()
    elif choice == "View Orders":
        view_orders()

if __name__ == "__main__":
    main()
