import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Local Business Promotion Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM STYLING (DARK & LIGHT MODE SAFE) ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #007991 0%, #00b4db 100%);
        padding: 1.8rem;
        border-radius: 12px;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1, .main-header p {
        color: #ffffff !important;
        margin: 0;
    }
    .main-header p {
        margin-top: 0.5rem;
        font-size: 1.05rem;
    }
    .shop-card {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-left: 6px solid #009688;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    }
    .shop-card h4, .shop-card small, .shop-card li, .shop-card b, .shop-card p {
        color: #111827 !important;
    }
    .shop-card .perk-text {
        color: #00695c !important;
        font-weight: 700;
        margin-bottom: 0;
    }
    .voucher-box {
        border: 2px dashed #00796b;
        background-color: #e0f2f1 !important;
        color: #111827 !important;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .voucher-box h4, .voucher-box p, .voucher-box b, .voucher-box i {
        color: #111827 !important;
    }
    .voucher-code {
        background-color: #004d40;
        color: #ffffff !important;
        padding: 4px 10px;
        border-radius: 5px;
        font-family: monospace;
        font-weight: bold;
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
    st.session_state.stamps = [True, True, False, False, False, False]

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
    st.write("Explore **30 local shops** across **Food & Drinks**, **Retail & Goods**, and **Artisans & Services**.")

    col_legend1, col_legend2, col_legend3 = st.columns(3)
    col_legend1.info("🟠 **Food & Drinks** (10 Shops)")
    col_legend2.info("🔵 **Retail & Goods** (10 Shops)")
    col_legend3.info("🟢 **Artisans & Services** (10 Shops)")

    # Clean public embed URL (removed /u/0/ which causes Google to refuse iframe connection)
    map_embed_url = "https://www.google.com/maps/d/embed?mid=1--QGDTttZxVKEhu_C3_CpBBZENSVtNs&ll=12.902901095458713%2C77.52115182023827&z=16"
    map_viewer_url = "https://www.google.com/maps/d/viewer?mid=1--QGDTttZxVKEhu_C3_CpBBZENSVtNs&ll=12.902901095458713%2C77.52115182023827&z=16"

    components.iframe(map_embed_url, height=500, scrolling=True)

    st.link_button("🗺️ Open Full Map in Google Maps App", map_viewer_url, use_container_width=True)
    st.caption("⚠️ If the map box looks blank, open Google My Maps → Share → turn ON 'Anyone with this link can view'.")

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
                <p class="perk-text">🎁 Passport Perk: {shop['perk']}</p>
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
            <span class="voucher-code">CODE: LOCALBREW15</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="voucher-box">
            <h4>🎨 Print + Snack Bundle</h4>
            <p><b>Step 1:</b> Print project notes at <i>QuickPrint Hub</i></p>
            <p><b>Step 2:</b> Get a <b>Free Veg Puff</b> on ₹100+ order at <i>Spice & Crisp Bakery</i></p>
            <span class="voucher-code">CODE: CAMPUSPUFF</span>
        </div>
        """, unsafe_allow_html=True)

    with v_col2:
        st.markdown("""
        <div class="voucher-box">
            <h4>👕 Style + Craft Bundle</h4>
            <p><b>Step 1:</b> Shop at <i>Urban Style Boutique</i></p>
            <p><b>Step 2:</b> Get <b>₹50 OFF</b> handmade gifts at <i>Craft & Clay Studio</i></p>
            <span class="voucher-code">CODE: CRAFT50</span>
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
                
