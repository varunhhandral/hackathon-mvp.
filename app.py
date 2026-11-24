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
    <p>Explore 30 neighborhood shops from RNSIT, browse live deals, collect passport stamps & unlock rewards!</p>
</div>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR PASSPORT STAMPS ---
if "stamps" not in st.session_state:
    st.session_state.stamps = [True, True, False, False, False, False]

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛣️ 2D Route Simulation",
    "🛒 Store Catalog & Deals",
    "🎫 Shop Local Passport",
    "🎟️ Co-Op Vouchers",
    "🎁 Mystery Box & Events"
])

# ==========================================
# TAB 1: 2D ANIMATED ROAD & 30-SHOP SIMULATION
# ==========================================
with tab1:
    st.subheader("🛣️ Live 2D Road Simulation: RNSIT to 30 Local Shops")
    st.write("Watch the animated shopper route start from **RNSIT Campus** and connect across **30 local shops** along neighborhood roads.")

    col_legend1, col_legend2, col_legend3 = st.columns(3)
    col_legend1.info("🟠 **Food & Drinks** (10 Shops)")
    col_legend2.info("🔵 **Retail & Goods** (10 Shops)")
    col_legend3.info("🟢 **Artisans & Services** (10 Shops)")

    simulation_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a;
            color: #f8fafc;
        }
        .sim-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 12px;
        }
        .controls {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            background: #1e293b;
            padding: 10px 16px;
            border-radius: 10px;
            width: 100%;
            max-width: 920px;
            box-sizing: border-box;
        }
        button {
            background: #009688;
            color: white;
            border: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 13px;
        }
        button:hover { background: #00796b; }
        button.secondary { background: #334155; }
        button.secondary:hover { background: #475569; }
        .status-pill {
            background: #0f172a;
            border: 1px solid #38bdf8;
            color: #38bdf8;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        canvas {
            background: #111827;
            border: 2px solid #334155;
            border-radius: 12px;
            max-width: 100%;
            height: auto;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }
    </style>
    </head>
    <body>
    <div class="sim-wrapper">
        <div class="controls">
            <button onclick="togglePlay()" id="playBtn">⏸️ Pause Route</button>
            <button class="secondary" onclick="resetSim()">🔄 Restart from RNSIT</button>
            <button class="secondary" onclick="changeSpeed()">⚡ Speed: <span id="speedLabel">1x</span></button>
            <div class="status-pill" id="liveBanner">📍 Starting at RNSIT Campus Gate...</div>
        </div>
        <canvas id="mapCanvas" width="920" height="540"></canvas>
    </div>

    <script>
    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");

    // 30 Shops + RNSIT Starting Hub laid out along a realistic road grid
    const startNode = { id: 0, name: "RNSIT Campus (Start)", cat: "Hub", x: 90, y: 270, color: "#ef4444" };

    // Road waypoints connecting RNSIT through North, Central, and South commercial streets
    const shops = [
        // North Main Road (10 shops)
        { id: 1,  name: "Brew & Bites Cafe",        cat: "Food & Drinks",       x: 170, y: 180, color: "#f97316" },
        { id: 2,  name: "Campus Xerox & Print",     cat: "Artisans & Services", x: 240, y: 120, color: "#22c55e" },
        { id: 3,  name: "Krishna Book Corner",      cat: "Retail & Goods",      x: 320, y: 120, color: "#3b82f6" },
        { id: 4,  name: "Spice & Crisp Bakery",     cat: "Food & Drinks",       x: 400, y: 120, color: "#f97316" },
        { id: 5,  name: "Urban Style Boutique",     cat: "Retail & Goods",      x: 480, y: 120, color: "#3b82f6" },
        { id: 6,  name: "Craft & Clay Studio",      cat: "Artisans & Services", x: 560, y: 120, color: "#22c55e" },
        { id: 7,  name: "Filter Kaapi Junction",    cat: "Food & Drinks",       x: 640, y: 120, color: "#f97316" },
        { id: 8,  name: "Namma Stationery Mart",    cat: "Retail & Goods",      x: 720, y: 120, color: "#3b82f6" },
        { id: 9,  name: "Artisan Frame Works",      cat: "Artisans & Services", x: 800, y: 120, color: "#22c55e" },
        { id: 10, name: "Chaat & Juice Corner",     cat: "Food & Drinks",       x: 840, y: 190, color: "#f97316" },

        // Central Avenue (10 shops)
        { id: 11, name: "Fresh Mart General Store", cat: "Retail & Goods",      x: 770, y: 270, color: "#3b82f6" },
        { id: 12, name: "QuickStitch Tailors",      cat: "Artisans & Services", x: 690, y: 270, color: "#22c55e" },
        { id: 13, name: "Dosa Plaza Express",       cat: "Food & Drinks",       x: 610, y: 270, color: "#f97316" },
        { id: 14, name: "Metro Footwear & Bags",    cat: "Retail & Goods",      x: 530, y: 270, color: "#3b82f6" },
        { id: 15, name: "Pottery & Decor Hub",      cat: "Artisans & Services", x: 450, y: 270, color: "#22c55e" },
        { id: 16, name: "Healthy Bowl Kitchen",     cat: "Food & Drinks",       x: 370, y: 270, color: "#f97316" },
        { id: 17, name: "Gadget & Mobile Care",     cat: "Artisans & Services", x: 290, y: 270, color: "#22c55e" },
        { id: 18, name: "Daily Needs Superstore",   cat: "Retail & Goods",      x: 210, y: 270, color: "#3b82f6" },
        { id: 19, name: "Tandoori & Grill Spot",    cat: "Food & Drinks",       x: 170, y: 350, color: "#f97316" },
        { id: 20, name: "GreenLeaf Organic Shop",   cat: "Retail & Goods",      x: 240, y: 420, color: "#3b82f6" },

        // South Market Road (10 shops)
        { id: 21, name: "Handmade Candle Co.",      cat: "Artisans & Services", x: 320, y: 420, color: "#22c55e" },
        { id: 22, name: "Sweet Tooth Mithai",       cat: "Food & Drinks",       x: 400, y: 420, color: "#f97316" },
        { id: 23, name: "Trendz Apparel Studio",    cat: "Retail & Goods",      x: 480, y: 420, color: "#3b82f6" },
        { id: 24, name: "Woodcraft & Gifts",        cat: "Artisans & Services", x: 560, y: 420, color: "#22c55e" },
        { id: 25, name: "Boba & Cold Coffee Bar",   cat: "Food & Drinks",       x: 640, y: 420, color: "#f97316" },
        { id: 26, name: "Home Essentials Bazaar",   cat: "Retail & Goods",      x: 720, y: 420, color: "#3b82f6" },
        { id: 27, name: "Cycle & Repair Workshop",  cat: "Artisans & Services", x: 800, y: 420, color: "#22c55e" },
        { id: 28, name: "South Spice Tiffins",      cat: "Food & Drinks",       x: 840, y: 350, color: "#f97316" },
        { id: 29, name: "Campus Sports & Gear",     cat: "Retail & Goods",      x: 760, y: 485, color: "#3b82f6" },
        { id: 30, name: "Mehendi & Art Corner",     cat: "Artisans & Services", x: 640, y: 485, color: "#22c55e" }
    ];

    const route = [startNode, ...shops];

    let isPlaying = true;
    let speedMultiplier = 1;
    let currentSegment = 0;
    let segmentProgress = 0;
    let visitedCount = 0;

    function togglePlay() {
        isPlaying = !isPlaying;
        document.getElementById("playBtn").innerText = isPlaying ? "⏸️ Pause Route" : "▶️ Resume Route";
    }

    function resetSim() {
        currentSegment = 0;
        segmentProgress = 0;
        visitedCount = 0;
        isPlaying = true;
        document.getElementById("playBtn").innerText = "⏸️ Pause Route";
    }

    function changeSpeed() {
        speedMultiplier = speedMultiplier === 1 ? 2 : (speedMultiplier === 2 ? 4 : 1);
        document.getElementById("speedLabel").innerText = speedMultiplier + "x";
    }

    function drawRoads() {
        // Subtle neighborhood blocks
        ctx.fillStyle = "#1e293b";
        ctx.fillRect(140, 60, 730, 445);

        // Road network background (asphalt)
        ctx.strokeStyle = "#334155";
        ctx.lineWidth = 22;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

        ctx.beginPath();
        ctx.moveTo(route[0].x, route[0].y);
        for (let i = 1; i < route.length; i++) {
            ctx.lineTo(route[i].x, route[i].y);
        }
        ctx.stroke();

        // Dashed center road markings
        ctx.strokeStyle = "#64748b";
        ctx.lineWidth = 2;
        ctx.setLineDash([8, 8]);
        ctx.beginPath();
        ctx.moveTo(route[0].x, route[0].y);
        for (let i = 1; i < route.length; i++) {
            ctx.lineTo(route[i].x, route[i].y);
        }
        ctx.stroke();
        ctx.setLineDash([]);
    }

    function drawCompletedRoute(moverX, moverY) {
        ctx.strokeStyle = "#00e5ff";
        ctx.lineWidth = 5;
        ctx.shadowColor = "#00e5ff";
        ctx.shadowBlur = 10;

        ctx.beginPath();
        ctx.moveTo(route[0].x, route[0].y);
        for (let i = 1; i <= currentSegment; i++) {
            ctx.lineTo(route[i].x, route[i].y);
        }
        ctx.lineTo(moverX, moverY);
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    function drawNodes() {
        // Draw RNSIT Hub
        ctx.fillStyle = "#ef4444";
        ctx.beginPath();
        ctx.arc(startNode.x, startNode.y, 15, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("🎓 RNSIT", startNode.x, startNode.y - 22);

        // Draw 30 Shops
        shops.forEach((shop, idx) => {
            const isVisited = idx < currentSegment;
            ctx.fillStyle = shop.color;
            ctx.beginPath();
            ctx.arc(shop.x, shop.y, isVisited ? 9 : 7, 0, Math.PI * 2);
            ctx.fill();

            if (isVisited) {
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            // Shop number label
            ctx.fillStyle = "#f8fafc";
            ctx.font = "bold 10px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(shop.id, shop.x, shop.y - 12);
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        drawRoads();

        const fromNode = route[currentSegment];
        const toNode = route[Math.min(currentSegment + 1, route.length - 1)];

        const moverX = fromNode.x + (toNode.x - fromNode.x) * segmentProgress;
        const moverY = fromNode.y + (toNode.y - fromNode.y) * segmentProgress;

        drawCompletedRoute(moverX, moverY);
        drawNodes();

        // Draw animated shopper avatar dot
        ctx.fillStyle = "#facc15";
        ctx.beginPath();
        ctx.arc(moverX, moverY, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#0f172a";
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // Direction arrow / pulse ring
        ctx.strokeStyle = "rgba(250, 204, 21, 0.5)";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(moverX, moverY, 16, 0, Math.PI * 2);
        ctx.stroke();

        if (isPlaying) {
            if (currentSegment < route.length - 1) {
                const dist = Math.hypot(toNode.x - fromNode.x, toNode.y - fromNode.y);
                const step = (1.8 * speedMultiplier) / Math.max(dist, 1);
                segmentProgress += step;

                if (segmentProgress >= 1) {
                    segmentProgress = 0;
                    currentSegment++;
                    const reached = route[currentSegment];
                    document.getElementById("liveBanner").innerText =
                        `🛍️ Shop #${reached.id}/30: ${reached.name} (${reached.cat})`;
                }
            } else {
                document.getElementById("liveBanner").innerText =
                    "✅ All 30 Local Shops Connected from RNSIT!";
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
    </script>
    </body>
    </html>
    """

    components.html(simulation_html, height=620)

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
    st.write("Collect stamps across local stores to unlock instant discounts, your custom map sticker, and Mystery Box entries!")

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
            st.success("🔓 **4 Stamps Unlocked:**\nCustom Map Sticker — Put Yourself on the Live Map!")
        else:
            st.warning("🔒 **4 Stamps:**\nUnlock Custom Sticker of Yourself on the Map")
    with tier3:
        if total_stamps == 6:
            st.success("🎉 **6 Stamps Unlocked:**\nEntered into Community Mystery Box Draw!")
        else:
            st.warning(f"🔒 **6 Stamps:**\nNeed {6 - total_stamps} more stamp(s) for Mystery Box!")

    # Interactive Custom Map Sticker Preview when 4+ stamps unlocked
    if total_stamps >= 4:
        st.divider()
        st.subheader("📍 Customize Your Live Map Sticker")
        s_col1, s_col2 = st.columns([2, 1])
        with s_col1:
            user_tag = st.text_input("Your Name / Handle on the Map Pin:", value="RNSIT Explorer")
            avatar_choice = st.selectbox("Choose Your Map Sticker Character:", ["🧑‍🎓 Campus Explorer", "🛍️ Super Shopper", "☕ Coffee Lover", "🎨 Local Supporter"])
        with s_col2:
            st.info(f"**Live Map Sticke
