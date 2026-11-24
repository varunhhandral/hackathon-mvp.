import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Local Business Promotion Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #007991 0%, #00b4db 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 800;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    .shop-card {
        background-color: #f8f9fa;
        border-left: 5px solid #009688;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .voucher-box {
        border: 2px dashed #009688;
        background-color: #e0f2f1;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stamp-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 10px;
    }
    .stamp-box {
        border: 2px solid #007991;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        background: white;
        font-weight: bold;
    }
    .stamp-done {
        background: #009688;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🛍️ Shop Local — Community Business Hub</h1>
    <p>Discover 30+ neighborhood shops, browse live deals, collect passport stamps & unlock rewards!</p>
</div>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR PASSPORT STAMPS ---
if "stamps" not in st.session_state:
    st.session_state.stamps = [True, True, False, False, False, False]  # 2 pre-stamped for demo

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Live Shop Map",
    "🛒 Store Catalog & Deals",
    "🎫 Shop Local Passport",
    "🎟️ Co-Op Vouchers",
    "🎁 Mystery Box & Events"
])

# ==========================================
# TAB 1: INTERACTIVE GOOGLE MY MAP
# ==========================================
with tab1:
    st.subheader("📍 Interactive Neighborhood Business Directory")
    st.write("Explore **30 local shops** across **Food & Drinks**, **Retail & Goods**, and **Artisans & Services**. Click any pin to see offers!")

    col_legend1, col_legend2, col_legend3 = st.columns(3)
    col_legend1.info("🟠 **Food & Drinks** (10 Shops)")
    col_legend2.info("🔵 **Retail & Goods** (10 Shops)")
    col_legend3.info("🟢 **Artisans & Services** (10 Shops)")

    # Converted your /edit link to /embed link with your exact coordinates & zoom
    map_embed_url = "https://www.google.com/maps/d/u/0/embed?mid=1--QGDTttZxVKEhu_C3_CpBBZENSVtNs&ll=12.902901095458713%2C77.52115182023827&z=16"
    
    components.iframe(map_embed_url, height=520, scrolling=True)
    st.caption("💡 Tip: Use the top-left icon inside the map to toggle categories on/off.")

# ==========================================
# TAB 2: STORE ITEMS & LIVE CATALOG
# ==========================================
with tab2:
    st.subheader("🛒 Featured Local Products & Live Prices")
    st.write("Browse popular items in stock right now—zero delivery fees or e-commerce markups.")

    category_filter = st.selectbox(
        "Filter by Category:",
        ["All Categories", "Food & Drinks", "Retail & Goods", "Artisans & Services"]
    )

    shops_data = [
        {
            "name": "Brew & Bites Cafe",
            "category": "Food & Drinks",
            "items": [("Signature Filter Coffee", "₹40"), ("Fresh Cinnamon Roll", "₹80"), ("Masala Bun", "₹35")],
            "perk": "15% OFF total bill with 2 Passport Stamps"
        },
        {
            "name": "Neighborhood Book & Stationery Corner",
            "category": "Retail & Goods",
            "items": [("Exam Prep Notebook Set", "₹150"), ("Bestseller Fiction", "₹299"), ("Art Sketchbook", "₹180")],
            "perk": "Free bookmark + 10% OFF on ₹200+ purchase"
        },
        {
            "name": "Craft & Clay Studio",
            "category": "Artisans & Services",
            "items": [("Handmade Terracotta Planter", "₹220"), ("Scented Soy Candle", "₹190"), ("Custom Keychain", "₹90")],
            "perk": "Buy 2 items, get 1 mini candle free"
        },
        {
            "name": "Spice & Crisp Bakery",
            "category": "Food & Drinks",
            "items": [("Veg Puff (2 pcs)", "₹50"), ("Plum Cake Slice", "₹70"), ("Badam Milk", "₹45")],
            "perk": "Free tea with any snack combo above ₹100"
        },
        {
            "name": "Urban Style Tailors & Boutique",
            "category": "Retail & Goods",
            "items": [("Cotton Kurti / Shirt", "₹550"), ("Express Alteration", "₹80"), ("Canvas Tote Bag", "₹160")],
            "perk": "10% Student ID discount + 1 Passport Stamp"
        },
        {
            "name": "QuickPrint & Design Hub",
            "category": "Artisans & Services",
            "items": [("Spiral Project Binding", "₹60"), ("Color Poster Print (A3)", "₹40"), ("Custom Mug Print", "₹200")],
            "perk": "20% OFF project printing for college students"
        }
    ]

    filtered_shops = [
        s for s in shops_data
        if category_filter == "All Categories" or s["category"] == category_filter
    ]

    cols = st.columns(2)
    for idx, shop in enumerate(filtered_shops):
        with cols[idx % 2]:
            items_html = "".join([f"<li>{item} — <b>{price}</b></li>" for item, price in shop["items"]])
            st.markdown(f"""
            <div class="shop-card">
                <h4>🏪 {shop['name']}</h4>
                <small><b>Category:</b> {shop['category']}</small>
                <ul>{items_html}</ul>
                <p style="color:#007991; margin-bottom:0;"><b>🎁 Passport Perk:</b> {shop['perk']}</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: INTERACTIVE SHOP LOCAL PASSPORT
# ==========================================
with tab3:
    st.subheader("🎫 Digital & Physical Shop Local Passport")
    st.write("Collect stamps across local stores to unlock instant discounts and Mystery Box entries!")

    stamp_labels = [
        "1. ☕ Food & Drinks",
        "2. 🛍️ Retail & Goods",
        "3. 🎨 Artisans & Crafts",
        "4. 🍔 Local Bakery/Snack",
        "5. 📦 Neighborhood Store",
        "6. ⭐ Any Map Shop"
    ]

    st.write("### Tap boxes below to simulate collecting stamps:")
    btn_cols = st.columns(3)
    for i in range(6):
        with btn_cols[i % 3]:
            status_text = "✅ STAMPED" if st.session_state.stamps[i] else "⬜ Tap to Stamp"
            if st.button(f"{stamp_labels[i]}\n({status_text})", key=f"stamp_{i}", use_container_width=True):
                st.session_state.stamps[i] = not st.session_state.stamps[i]
                st.rerun()

    total_stamps = sum(st.session_state.stamps)
    st.divider()

    # Prize Progress Tracker
    st.write(f"### 🏆 Your Reward Progress: **{total_stamps} / 6 Stamps**")
    st.progress(total_stamps / 6)

    tier1, tier2, tier3 = st.columns(3)
    with tier1:
        if total_stamps >= 2:
            st.success("🔓 **2 Stamps Unlocked:**\n5% OFF Next Purchase!")
        else:
            st.warning("🔒 **2 Stamps:**\n5% OFF Next Purchase")
    with tier2:
        if total_stamps >= 4:
            st.success("🔓 **4 Stamps Unlocked:**\nFree Entry to Night Market!")
        else:
            st.warning("🔒 **4 Stamps:**\nFree Entry to Night Market")
    with tier3:
        if total_stamps == 6:
            st.success("🎉 **6 Stamps Unlocked:**\nEntered into Community Mystery Box Draw!")
        else:
            st.warning(f"🔒 **6 Stamps:**\nNeed {6 - total_stamps} more stamp(s) for Mystery Box!")

# ==========================================
# TAB 4: CROSS-MERCHANT CO-OP VOUCHERS
# ==========================================
with tab4:
    st.subheader("🎟️ Cross-Merchant Co-Op Voucher Bundles")
    st.write("Shop at one neighborhood store and automatically unlock a voucher for the shop next door!")

    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.markdown("""
        <div class="voucher-box">
            <h4>📚 Book + Brew Bundle</h4>
            <p><b>Step 1:</b> Spend ₹200 at <i>Neighborhood Book Corner</i></p>
            <p><b>Step 2:</b> Get <b>15% OFF any coffee/tea</b> at <i>Brew & Bites Cafe</i></p>
            <code>CODE: LOCALBREW15</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="voucher-box">
            <h4>🎨 Print + Snack Bundle</h4>
            <p><b>Step 1:</b> Print project notes at <i>QuickPrint Hub</i></p>
            <p><b>Step 2:</b> Get a <b>Free Veg Puff</b> on ₹100+ order at <i>Spice & Crisp Bakery</i></p>
            <code>CODE: CAMPUSPUFF</code>
        </div>
        """, unsafe_allow_html=True)

    with v_col2:
        st.markdown("""
        <div class="voucher-box">
            <h4>👕 Style + Craft Bundle</h4>
            <p><b>Step 1:</b> Shop at <i>Urban Style Boutique</i></p>
            <p><b>Step 2:</b> Get <b>₹50 OFF</b> handmade gifts at <i>Craft & Clay Studio</i></p>
            <code>CODE: CRAFT50</code>
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 **How Merchants Benefit:** Zero ad spend—neighboring shops refer customers directly to each other!")

# ==========================================
# TAB 5: MYSTERY BOX, QR & EVENTS
# ==========================================
with tab5:
    st.subheader("🎁 Community Mystery Box & Pop-Up Events")

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("""
        ### 🎁 This Week's Community Mystery Box
        Every participating store contributes **1 signature item or gift voucher** into a single grand prize box:
        * ☕ Artisanal Filter Coffee Pack
        * 🕯️ Hand-poured Scented Soy Candle
        * 📚 Bestseller Paperback Novel
        * 🎟️ ₹500 Combined Local Dining Vouchers
        
        **How to Win:** Complete all 6 stamps on your Passport and drop your card at any participating counter!
        """)

    with m_col2:
        st.markdown("""
        ### 🎪 Monthly Pop-Up Night Market & Campus Perks
        * **Street Activation:** Live music, local food stalls, and handmade craft pop-ups.
        * **🎓 Student Saver Pass:** Show your College ID + Passport at any mapped shop for an **extra 5% discount**.
        * **📱 QR Window Badges:** Look for our green QR stickers on shop doors to scan and view live deals on the spot.
        """)

    st.divider()
    with st.expander("📋 Quick Vendor Sign-Up (For New Local Shops)"):
        with st.form("vendor_form"):
            shop_name = st.text_input("Shop Name")
            shop_cat = st.selectbox("Category", ["Food & Drinks", "Retail & Goods", "Artisans & Services"])
            shop_offer = st.text_input("Sample Passport Offer (e.g., 10% off)")
            submitted = st.form_submit_button("Join Map Directory")
            if submitted and shop_name:
                st.success(f"✅ Thank you! **{shop_name}** ({shop_cat}) has been submitted for map onboarding.")
        
