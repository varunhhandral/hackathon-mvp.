import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Local Business Promotion Hub", page_icon="🛍️", layout="wide")

CSS = (
    "<style>"
    ".hdr{background:linear-gradient(90deg,#007991,#00b4db);padding:22px;border-radius:12px;color:#fff!important;text-align:center;margin-bottom:18px;}"
    ".hdr h1,.hdr p{color:#fff!important;margin:0;}"
    ".card{background:#ffffff!important;color:#111827!important;border-left:6px solid #009688;padding:15px;border-radius:10px;margin-bottom:12px;box-shadow:0 2px 6px rgba(0,0,0,0.15);}"
    ".card h4,.card p,.card li,.card b,.card small{color:#111827!important;}"
    ".perk{color:#00695c!important;font-weight:700;margin-bottom:0;}"
    ".vbox{border:2px dashed #00796b;background:#e0f2f1!important;color:#111827!important;padding:15px;border-radius:10px;margin-bottom:12px;}"
    ".vbox h4,.vbox p,.vbox b,.vbox i{color:#111827!important;}"
    ".code{background:#004d40;color:#ffffff!important;padding:4px 10px;border-radius:5px;font-family:monospace;font-weight:bold;}"
    "</style>"
)
st.markdown(CSS, unsafe_allow_html=True)

st.markdown('<div class="hdr"><h1>🛍️ Shop Local — Community Business Hub</h1><p>Explore 30 local shops around RNSIT, browse live deals, collect stamps & unlock rewards!</p></div>', unsafe_allow_html=True)

if "stamps" not in st.session_state:
    st.session_state.stamps = [True, True, False, False, False, False]

t1, t2, t3, t4, t5 = st.tabs(["🛣️ 2D Route Simulation", "🛒 Store Catalog", "🎫 Shop Local Passport", "🎟️ Co-Op Vouchers", "🎁 Mystery Box & Events"])

# --- TAB 1: REALISTIC RNSIT ROAD & 30-SHOP SIMULATION ---
with t1:
    st.subheader("🛣️ Live 2D Road Simulation: RNSIT to 30 Mapped Shops")
    st.write("Animated route starting from **RNS Institute of Technology** across **Channasandra Main Rd**, **15th Main Rd**, and **TMS Rd**[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span).")
    c1, c2, c3 = st.columns(3)
    c1.info("🟠 **Food & Drinks** (10 Shops)[span_12](start_span)[span_12](end_span)")
    c2.info("🟣 **Retail & Goods** (10 Shops)[span_13](start_span)[span_13](end_span)")
    c3.info("🔵 **Artisans & Services** (10 Shops)[span_14](start_span)[span_14](end_span)")

    sim_code = """<!DOCTYPE html><html><head><style>
    body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f1f5f9;color:#0f172a;}
    .wrap{display:flex;flex-direction:column;align-items:center;padding:8px;}
    .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-bottom:8px;background:#ffffff;padding:10px;border-radius:10px;width:100%;max-width:900px;box-sizing:border-box;border:1px solid #cbd5e1;}
    button{background:#007991;color:#fff;border:none;padding:8px 12px;border-radius:6px;font-weight:600;cursor:pointer;}
    button.sec{background:#475569;}
    .pill{background:#e0f2fe;border:1px solid #0284c7;color:#0369a1;padding:6px 12px;border-radius:20px;font-size:13px;font-weight:700;}
    canvas{background:#f8fafc;border:2px solid #cbd5e1;border-radius:12px;max-width:100%;height:auto;}
    </style></head><body><div class="wrap">
    <div class="bar">
      <button onclick="togglePlay()" id="pBtn">⏸️ Pause</button>
      <button class="sec" onclick="resetSim()">🔄 Restart RNSIT</button>
      <button class="sec" onclick="chgSpd()">⚡ Speed: <span id="sLbl">1x</span></button>
      <div class="pill" id="banner">🎓 Starting at RNS Institute of Technology...</div>
    </div>
    <canvas id="cv" width="900" height="540"></canvas></div>
    <script>
    const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
    // RNSIT in upper-right matching actual map layout
    const start={id:0,name:"RNS Institute of Technology",cat:"Campus",x:620,y:95,c:"#16a34a"};
    // 30 Real Mapped Shops across Food (#f97316), Retail (#9333ea), Services (#0284c7)
    const shops=[
      {id:1,name:"Absolute Shawarma @RNSIT",cat:"Food & Drinks",x:535,y:155,c:"#f97316"},
      {id:2,name:"The Amritham Cafe",cat:"Food & Drinks",x:445,y:175,c:"#f97316"},
      {id:3,name:"CNS Pastries",cat:"Food & Drinks",x:355,y:175,c:"#f97316"},
      {id:4,name:"Velvet Scoops",cat:"Food & Drinks",x:265,y:175,c:"#f97316"},
      {id:5,name:"Nisarga Gobi Centre",cat:"Food & Drinks",x:205,y:215,c:"#f97316"},
      {id:6,name:"EAT 'N' JOY",cat:"Food & Drinks",x:205,y:270,c:"#f97316"},
      {id:7,name:"Tony's Corner",cat:"Food & Drinks",x:290,y:270,c:"#f97316"},
      {id:8,name:"Bhavanaas Foods",cat:"Food & Drinks",x:380,y:270,c:"#f97316"},
      {id:9,name:"Karnataka Hindu Military Hotel",cat:"Food & Drinks",x:470,y:270,c:"#f97316"},
      {id:10,name:"Park Inn Family Restaurant",cat:"Food & Drinks",x:565,y:270,c:"#f97316"},

      {id:11,name:"ZECODE - RR Nagar",cat:"Retail & Goods",x:655,y:270,c:"#9333ea"},
      {id:12,name:"Trends Footwear & Fashion",cat:"Retail & Goods",x:745,y:275,c:"#9333ea"},
      {id:13,name:"Channasandra Book Mart",cat:"Retail & Goods",x:815,y:285,c:"#9333ea"},
      {id:14,name:"Reliance Smart Point",cat:"Retail & Goods",x:720,y:345,c:"#9333ea"},
      {id:15,name:"Namma Gift & Toys",cat:"Retail & Goods",x:625,y:355,c:"#9333ea"},
      {id:16,name:"Sri Sai Fancy & Jewels",cat:"Retail & Goods",x:535,y:355,c:"#9333ea"},
      {id:17,name:"Metro Sports & Fitness",cat:"Retail & Goods",x:445,y:355,c:"#9333ea"},
      {id:18,name:"Campus Stationery Hub",cat:"Retail & Goods",x:355,y:355,c:"#9333ea"},
      {id:19,name:"Fresh Basket Supermarket",cat:"Retail & Goods",x:265,y:355,c:"#9333ea"},
      {id:20,name:"Royal Home Essentials",cat:"Retail & Goods",x:205,y:355,c:"#9333ea"},

      {id:21,name:"Manjunatha Xerox",cat:"Artisans & Services",x:205,y:425,c:"#0284c7"},
      {id:22,name:"YESHU MOBILES",cat:"Artisans & Services",x:280,y:445,c:"#0284c7"},
      {id:23,name:"Lakshmi Medical & General Store",cat:"Artisans & Services",x:360,y:445,c:"#0284c7"},
      {id:24,name:"Sri Chennakeshwara Provision",cat:"Artisans & Services",x:440,y:445,c:"#0284c7"},
      {id:25,name:"Adishwar Electro World",cat:"Artisans & Services",x:520,y:445,c:"#0284c7"},
      {id:26,name:"Mrs Geetha Sri Sai Boutique",cat:"Artisans & Services",x:600,y:445,c:"#0284c7"},
      {id:27,name:"GAJRAJ MEDICALS",cat:"Artisans & Services",x:680,y:445,c:"#0284c7"},
      {id:28,name:"S.G.R. ENERGY SAVERS",cat:"Artisans & Services",x:760,y:445,c:"#0284c7"},
      {id:29,name:"Muscle Mechanic",cat:"Artisans & Services",x:820,y:405,c:"#0284c7"},
      {id:30,name:"R Skyline Bike Services",cat:"Artisans & Services",x:820,y:475,c:"#0284c7"}
    ];
    const rt=[start,...shops];
    let play=true,spd=1,seg=0,prog=0;
    function togglePlay(){play=!play;document.getElementById("pBtn").innerText=play?"⏸️ Pause":"▶️ Resume";}
    function resetSim(){seg=0;prog=0;play=true;document.getElementById("pBtn").innerText="⏸️ Pause";}
    function chgSpd(){spd=spd===1?2:(spd===2?4:1);document.getElementById("sLbl").innerText=spd+"x";}

    function drawMapBackground(){
      // Light map blocks matching screenshot style
      ctx.fillStyle="#eef2f6";ctx.fillRect(0,0,cv.width,cv.height);
      // Warm commercial zone highlight along Channasandra Main Rd
      ctx.fillStyle="#fef3c7";ctx.fillRect(185,155,660,145);

      // Major Roads (White/Grey Google Maps style)
      ctx.strokeStyle="#cbd5e1";ctx.lineWidth=22;ctx.lineCap="round";ctx.lineJoin="round";
      // Diagonal Highway top-left
      ctx.beginPath();ctx.moveTo(80,260);ctx.lineTo(360,10);ctx.stroke();
      // Channasandra Main Rd (Vertical Left + Horizontal Main)
      ctx.beginPath();ctx.moveTo(205,150);ctx.lineTo(205,510);ctx.stroke();
      ctx.beginPath();ctx.moveTo(120,270);ctx.lineTo(860,285);ctx.stroke();
      // 15th Main Rd & RNSIT Access Rd
      ctx.beginPath();ctx.moveTo(205,175);ctx.lineTo(620,175);ctx.lineTo(620,75);ctx.stroke();
      // TMS Rd & 10th Main Rd
      ctx.beginPath();ctx.moveTo(205,355);ctx.lineTo(840,355);ctx.stroke();
      ctx.beginPath();ctx.moveTo(205,445);ctx.lineTo(840,445);ctx.stroke();
      // Cross streets
      ctx.lineWidth=14;
      [355,535,720,820].forEach(x=>{
        ctx.beginPath();ctx.moveTo(x,140);ctx.lineTo(x,495);ctx.stroke();
      });

      // Inner white road fill
      ctx.strokeStyle="#ffffff";ctx.lineWidth=16;
      ctx.beginPath();ctx.moveTo(205,150);ctx.lineTo(205,510);ctx.stroke();
      ctx.beginPath();ctx.moveTo(120,270);ctx.lineTo(860,285);ctx.stroke();
      ctx.beginPath();ctx.moveTo(205,175);ctx.lineTo(620,175);ctx.lineTo(620,75);ctx.stroke();
      ctx.beginPath();ctx.moveTo(205,355);ctx.lineTo(840,355);ctx.stroke();
      ctx.beginPath();ctx.moveTo(205,445);ctx.lineTo(840,445);ctx.stroke();

      // Road Labels matching actual map
      ctx.fillStyle="#475569";ctx.font="bold 11px sans-serif";ctx.textAlign="left";
      ctx.fillText("15th Main Rd",370,168);
      ctx.fillText("Channasandra Main Rd",220,262);
      ctx.fillText("TMS Rd",225,348);
      ctx.fillText("10th Main Rd",225,438);
    }

    function loop(){
      ctx.clearRect(0,0,cv.width,cv.height);
      drawMapBackground();

      const a=rt[seg],b=rt[Math.min(seg+1,rt.length-1)];
      const mx=a.x+(b.x-a.x)*prog,my=a.y+(b.y-a.y)*prog;

      // Animated blue navigation trail
      ctx.strokeStyle="#0284c7";ctx.lineWidth=5;ctx.lineCap="round";ctx.lineJoin="round";
      ctx.beginPath();ctx.moveTo(rt[0].x,rt[0].y);
      for(let i=1;i<=seg;i++)ctx.lineTo(rt[i].x,rt[i].y);
      ctx.lineTo(mx,my);ctx.stroke();

      // RNSIT Campus Pin
      ctx.fillStyle="#15803d";ctx.beginPath();ctx.arc(start.x,start.y,15,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle="#ffffff";ctx.lineWidth=3;ctx.stroke();
      ctx.fillStyle="#0f172a";ctx.font="bold 12px sans-serif";ctx.textAlign="center";
      ctx.fillText("🎓 RNS INSTITUTE OF TECHNOLOGY",start.x,start.y-22);

      // 30 Shop Pins
      shops.forEach((s,idx)=>{
        const vis=idx<seg;
        ctx.fillStyle=s.c;ctx.beginPath();ctx.arc(s.x,s.y,vis?9:7,0,Math.PI*2);ctx.fill();
        ctx.strokeStyle="#ffffff";ctx.lineWidth=2;ctx.stroke();
        ctx.fillStyle="#0f172a";ctx.font="bold 10px sans-serif";ctx.fillText(s.id,s.x,s.y-11);
      });

      // Live Moving Navigation Marker
      ctx.fillStyle="#facc15";ctx.beginPath();ctx.arc(mx,my,10,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle="#0f172a";ctx.lineWidth=2.5;ctx.stroke();

      if(play){
        if(seg<rt.length-1){
          const d=Math.hypot(b.x-a.x,b.y-a.y);
          prog+=(2*spd)/Math.max(d,1);
          if(prog>=1){prog=0;seg++;const r=rt[seg];document.getElementById("banner").innerText="📍 #"+r.id+"/30: "+r.name+" ("+r.cat+")";}
        }else{document.getElementById("banner").innerText="✅ All 30 Local Shops Connected from RNSIT!";}
      }
      requestAnimationFrame(loop);
    }
    loop();
    </script></body></html>"""
    components.html(sim_code, height=615)

    # Option to open live Google My Map at the bottom
    gmaps_url = "https://www.google.com/maps/d/viewer?mid=1--QGDTttZxVKEhu_C3_CpBBZENSVtNs&ll=12.902901095458713%2C77.52115182023827&z=16"
    st.link_button("🗺️ Open Full Interactive Map in Google Maps", gmaps_url, use_container_width=True)

# --- TAB 2: STORE CATALOG ---
with t2:
    st.subheader("🛒 Featured Local Products & Live Prices")
    cat = st.selectbox("Filter Category:", ["All", "Food & Drinks", "Retail & Goods", "Artisans & Services"])
    items_list = [
        ("The Amritham Cafe & CNS Pastries", "Food & Drinks", "Filter Coffee (₹35), Veg Puff & Pastry (₹45)", "15% OFF with 2 Stamps"),
        ("Absolute Shawarma @RNSIT & Velvet Scoops", "Food & Drinks", "Classic Shawarma (₹90), Gelato Scoop (₹70)", "Free topping on ₹150+"),
        ("ZECODE & Channasandra Retail", "Retail & Goods", "Casual Tees (₹399), Campus Tote Bag (₹160)", "10% Student ID discount"),
        ("Manjunatha Xerox & Stationery", "Artisans & Services", "Spiral Project Binding (₹60), A3 Color Print (₹35)", "20% OFF student printing"),
        ("YESHU MOBILES & Adishwar Electro", "Artisans & Services", "Tempered Glass (₹99), Fast Charger (₹299)", "Free phone cleaning + 1 Stamp"),
        ("Muscle Mechanic & R Skyline Bike Services", "Artisans & Services", "General Bike Checkup (₹199), Chain Lube (₹80)", "15% OFF service with Passport")
    ]
    cols = st.columns(2)
    idx = 0
    for name, c_name, prods, perk in items_list:
        if cat == "All" or cat == c_name:
            with cols[idx % 2]:
                html_card = f'<div class="card"><h4>🏪 {name}</h4><small><b>{c_name}</b></small><p>{prods}</p><p class="perk">🎁 {perk}</p></div>'
                st.markdown(html_card, unsafe_allow_html=True)
            idx += 1

# --- TAB 3: SHOP LOCAL PASSPORT ---
with t3:
    st.subheader("🎫 Digital & Physical Shop Local Passport")
    labels = ["1. ☕ Food & Drinks", "2. 🛍️ Retail & Goods", "3. 🔧 Artisans & Services", "4. 🍔 Local Cafe/Bakery", "5. 📦 Neighborhood Store", "6. ⭐ Any Map Shop"]
    b_cols = st.columns(3)
    for i in range(6):
        with b_cols[i % 3]:
            st_txt = "✅ STAMPED" if st.session_state.stamps[i] else "⬜ Tap to Stamp"
            if st.button(f"{labels[i]} ({st_txt})", key=f"s_{i}", use_container_width=True):
                st.session_state.stamps[i] = not st.session_state.stamps[i]
                st.rerun()

    tot = sum(st.session_state.stamps)
    st.divider()
    st.write(f"### 🏆 Progress: **{tot} / 6 Stamps**")
    st.progress(tot / 6)

    r1, r2, r3 = st.columns(3)
    r1.success("🔓 **2 Stamps:** 5% OFF Next Purchase!") if tot >= 2 else r1.warning("🔒 **2 Stamps:** 5% OFF Next Purchase")
    r2.success("🔓 **4 Stamps:** Custom Sticker of Yourself on the Map!") if tot >= 4 else r2.warning("🔒 **4 Stamps:** Unlock Sticker of Yourself on Map")
    r3.success("🎉 **6 Stamps:** Entered in Mystery Box Draw!") if tot == 6 else r3.warning(f"🔒 **6 Stamps:** Need {6-tot} more for Mystery Box")

    if tot >= 4:
        st.divider()
        st.subheader("📍 Customize Your Live Map Sticker")
        u_name = st.text_input("Your Name on the Map Sticker:", value="RNSIT Explorer")
        u_icon = st.selectbox("Pick Your Map Sticker Avatar:", ["🧑‍🎓 Campus Explorer", "🛍️ Super Shopper", "☕ Coffee Lover", "🎨 Local Supporter"])
        st.info(f"**Active Map Sticker:** {u_icon} — **{u_name}** is now pinned live on the neighborhood map!")

# --- TAB 4: CO-OP VOUCHERS ---
with t4:
    st.subheader("🎟️ Cross-Merchant Co-Op Vouchers")
    v1, v2 = st.columns(2)
    with v1:
        st.markdown('<div class="vbox"><h4>🖨️ Xerox + Cafe Bundle</h4><p>Print notes at <i>Manjunatha Xerox</i> ➔ Get <b>15% OFF</b> at <i>The Amritham Cafe</i></p><span class="code">CODE: RNSITBREW15</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="vbox"><h4>👕 Fashion + Ice Cream Bundle</h4><p>Shop at <i>ZECODE</i> ➔ Get <b>Free Topping</b> at <i>Velvet Scoops</i></p><span class="code">CODE: SCOOPFREE</span></div>', unsafe_allow_html=True)
    with v2:
        st.markdown('<div class="vbox"><h4>🏍️ Bike Service + Shawarma Bundle</h4><p>Service at <i>R Skyline Bike Services</i> ➔ Get <b>₹30 OFF</b> at <i>Absolute Shawarma</i></p><span class="code">CODE: RIDER30</span></div>', unsafe_allow_html=True)
        st.info("💡 **Zero Ad Cost:** Neighboring shops refer customers directly to each other!")

# --- TAB 5: MYSTERY BOX & EVENTS ---
with t5:
    st.subheader("🎁 Community Mystery Box & Campus Perks")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("### 🎁 Weekly Community Mystery Box\n* ☕ Filter Coffee & Pastry Voucher\n* 📱 Mobile Accessory Pack\n* 👕 ZECODE Shopping Coupon\n* 🎟️ ₹500 Combined Dining Vouchers")
    with m2:
        st.markdown("### 🎪 Campus & Street Activation\n* 🎓 **Student Saver Pass:** Extra 5% OFF with RNSIT ID + Passport\n* 📱 **QR Window Stickers:** Scan shop doors for live deals")
        
