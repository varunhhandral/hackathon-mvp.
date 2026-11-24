import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Local Business Promotion Hub", page_icon="🛍️", layout="wide")

# Safe CSS injection (short lines so mobile paste never truncates)
CSS = (
    "<style>"
    ".hdr{background:linear-gradient(90deg,#007991,#00b4db);padding:24px;border-radius:12px;color:#fff!important;text-align:center;margin-bottom:20px;}"
    ".hdr h1,.hdr p{color:#fff!important;margin:0;}"
    ".card{background:#ffffff!important;color:#111827!important;border-left:6px solid #009688;padding:16px;border-radius:10px;margin-bottom:12px;box-shadow:0 2px 6px rgba(0,0,0,0.15);}"
    ".card h4,.card p,.card li,.card b,.card small{color:#111827!important;}"
    ".perk{color:#00695c!important;font-weight:700;margin-bottom:0;}"
    ".vbox{border:2px dashed #00796b;background:#e0f2f1!important;color:#111827!important;padding:16px;border-radius:10px;margin-bottom:12px;}"
    ".vbox h4,.vbox p,.vbox b,.vbox i{color:#111827!important;}"
    ".code{background:#004d40;color:#ffffff!important;padding:4px 10px;border-radius:5px;font-family:monospace;font-weight:bold;}"
    "</style>"
)
st.markdown(CSS, unsafe_allow_html=True)

st.markdown('<div class="hdr"><h1>🛍️ Shop Local — Community Business Hub</h1><p>Explore 30 shops from RNSIT, browse live deals, collect stamps & unlock rewards!</p></div>', unsafe_allow_html=True)

if "stamps" not in st.session_state:
    st.session_state.stamps = [True, True, False, False, False, False]

t1, t2, t3, t4, t5 = st.tabs(["🛣️ 2D Route Simulation", "🛒 Store Catalog", "🎫 Shop Local Passport", "🎟️ Co-Op Vouchers", "🎁 Mystery Box & Events"])

# --- TAB 1: 2D ANIMATED ROAD SIMULATION ---
with t1:
    st.subheader("🛣️ Live 2D Road Simulation: RNSIT to 30 Local Shops")
    st.write("Watch the animated shopper route start from **RNSIT Campus** and connect across **30 local shops**.")
    c1, c2, c3 = st.columns(3)
    c1.info("🟠 **Food & Drinks** (10 Shops)")
    c2.info("🔵 **Retail & Goods** (10 Shops)")
    c3.info("🟢 **Artisans & Services** (10 Shops)")

    sim_code = """<!DOCTYPE html><html><head><style>
    body{margin:0;font-family:sans-serif;background:#0f172a;color:#f8fafc;}
    .wrap{display:flex;flex-direction:column;align-items:center;padding:10px;}
    .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-bottom:10px;background:#1e293b;padding:10px;border-radius:10px;width:100%;max-width:900px;box-sizing:border-box;}
    button{background:#009688;color:#fff;border:none;padding:8px 12px;border-radius:6px;font-weight:600;cursor:pointer;}
    button.sec{background:#334155;}
    .pill{background:#0f172a;border:1px solid #38bdf8;color:#38bdf8;padding:6px 12px;border-radius:20px;font-size:13px;font-weight:600;}
    canvas{background:#111827;border:2px solid #334155;border-radius:12px;max-width:100%;height:auto;}
    </style></head><body><div class="wrap">
    <div class="bar">
      <button onclick="togglePlay()" id="pBtn">⏸️ Pause</button>
      <button class="sec" onclick="resetSim()">🔄 Restart RNSIT</button>
      <button class="sec" onclick="chgSpd()">⚡ Speed: <span id="sLbl">1x</span></button>
      <div class="pill" id="banner">📍 Starting at RNSIT Campus Gate...</div>
    </div>
    <canvas id="cv" width="900" height="520"></canvas></div>
    <script>
    const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
    const start={id:0,name:"RNSIT Campus",cat:"Start",x:85,y:260,c:"#ef4444"};
    const shops=[
      {id:1,name:"Brew & Bites Cafe",cat:"Food & Drinks",x:165,y:170,c:"#f97316"},
      {id:2,name:"Campus Xerox & Print",cat:"Artisans & Services",x:235,y:110,c:"#22c55e"},
      {id:3,name:"Krishna Book Corner",cat:"Retail & Goods",x:315,y:110,c:"#3b82f6"},
      {id:4,name:"Spice & Crisp Bakery",cat:"Food & Drinks",x:395,y:110,c:"#f97316"},
      {id:5,name:"Urban Style Boutique",cat:"Retail & Goods",x:475,y:110,c:"#3b82f6"},
      {id:6,name:"Craft & Clay Studio",cat:"Artisans & Services",x:555,y:110,c:"#22c55e"},
      {id:7,name:"Filter Kaapi Junction",cat:"Food & Drinks",x:635,y:110,c:"#f97316"},
      {id:8,name:"Namma Stationery Mart",cat:"Retail & Goods",x:715,y:110,c:"#3b82f6"},
      {id:9,name:"Artisan Frame Works",cat:"Artisans & Services",x:795,y:110,c:"#22c55e"},
      {id:10,name:"Chaat & Juice Corner",cat:"Food & Drinks",x:835,y:180,c:"#f97316"},
      {id:11,name:"Fresh Mart Store",cat:"Retail & Goods",x:765,y:260,c:"#3b82f6"},
      {id:12,name:"QuickStitch Tailors",cat:"Artisans & Services",x:685,y:260,c:"#22c55e"},
      {id:13,name:"Dosa Plaza Express",cat:"Food & Drinks",x:605,y:260,c:"#f97316"},
      {id:14,name:"Metro Footwear",cat:"Retail & Goods",x:525,y:260,c:"#3b82f6"},
      {id:15,name:"Pottery & Decor Hub",cat:"Artisans & Services",x:445,y:260,c:"#22c55e"},
      {id:16,name:"Healthy Bowl Kitchen",cat:"Food & Drinks",x:365,y:260,c:"#f97316"},
      {id:17,name:"Gadget Mobile Care",cat:"Artisans & Services",x:285,y:260,c:"#22c55e"},
      {id:18,name:"Daily Needs Store",cat:"Retail & Goods",x:205,y:260,c:"#3b82f6"},
      {id:19,name:"Tandoori Grill Spot",cat:"Food & Drinks",x:165,y:340,c:"#f97316"},
      {id:20,name:"GreenLeaf Organic",cat:"Retail & Goods",x:235,y:410,c:"#3b82f6"},
      {id:21,name:"Handmade Candle Co.",cat:"Artisans & Services",x:315,y:410,c:"#22c55e"},
      {id:22,name:"Sweet Tooth Mithai",cat:"Food & Drinks",x:395,y:410,c:"#f97316"},
      {id:23,name:"Trendz Apparel",cat:"Retail & Goods",x:475,y:410,c:"#3b82f6"},
      {id:24,name:"Woodcraft & Gifts",cat:"Artisans & Services",x:555,y:410,c:"#22c55e"},
      {id:25,name:"Boba Cold Coffee Bar",cat:"Food & Drinks",x:635,y:410,c:"#f97316"},
      {id:26,name:"Home Essentials",cat:"Retail & Goods",x:715,y:410,c:"#3b82f6"},
      {id:27,name:"Cycle Repair Shop",cat:"Artisans & Services",x:795,y:410,c:"#22c55e"},
      {id:28,name:"South Spice Tiffins",cat:"Food & Drinks",x:835,y:340,c:"#f97316"},
      {id:29,name:"Campus Sports Gear",cat:"Retail & Goods",x:755,y:475,c:"#3b82f6"},
      {id:30,name:"Mehendi & Art Corner",cat:"Artisans & Services",x:635,y:475,c:"#22c55e"}
    ];
    const rt=[start,...shops];
    let play=true,spd=1,seg=0,prog=0;
    function togglePlay(){play=!play;document.getElementById("pBtn").innerText=play?"⏸️ Pause":"▶️ Resume";}
    function resetSim(){seg=0;prog=0;play=true;document.getElementById("pBtn").innerText="⏸️ Pause";}
    function chgSpd(){spd=spd===1?2:(spd===2?4:1);document.getElementById("sLbl").innerText=spd+"x";}
    function loop(){
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle="#1e293b";ctx.fillRect(135,55,730,440);
      ctx.strokeStyle="#334155";ctx.lineWidth=20;ctx.lineCap="round";ctx.lineJoin="round";
      ctx.beginPath();ctx.moveTo(rt[0].x,rt[0].y);
      for(let i=1;i<rt.length;i++)ctx.lineTo(rt[i].x,rt[i].y);
      ctx.stroke();
      ctx.strokeStyle="#64748b";ctx.lineWidth=2;ctx.setLineDash([8,8]);
      ctx.beginPath();ctx.moveTo(rt[0].x,rt[0].y);
      for(let i=1;i<rt.length;i++)ctx.lineTo(rt[i].x,rt[i].y);
      ctx.stroke();ctx.setLineDash([]);
      const a=rt[seg],b=rt[Math.min(seg+1,rt.length-1)];
      const mx=a.x+(b.x-a.x)*prog,my=a.y+(b.y-a.y)*prog;
      ctx.strokeStyle="#00e5ff";ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(rt[0].x,rt[0].y);
      for(let i=1;i<=seg;i++)ctx.lineTo(rt[i].x,rt[i].y);
      ctx.lineTo(mx,my);ctx.stroke();
      ctx.fillStyle="#ef4444";ctx.beginPath();ctx.arc(start.x,start.y,14,0,Math.PI*2);ctx.fill();
      ctx.fillStyle="#fff";ctx.font="bold 12px sans-serif";ctx.textAlign="center";ctx.fillText("🎓 RNSIT",start.x,start.y-20);
      shops.forEach((s,idx)=>{
        ctx.fillStyle=s.c;ctx.beginPath();ctx.arc(s.x,s.y,idx<seg?9:7,0,Math.PI*2);ctx.fill();
        ctx.fillStyle="#fff";ctx.font="bold 10px sans-serif";ctx.fillText(s.id,s.x,s.y-11);
      });
      ctx.fillStyle="#facc15";ctx.beginPath();ctx.arc(mx,my,10,0,Math.PI*2);ctx.fill();
      if(play){
        if(seg<rt.length-1){
          const d=Math.hypot(b.x-a.x,b.y-a.y);
          prog+=(2*spd)/Math.max(d,1);
          if(prog>=1){prog=0;seg++;const r=rt[seg];document.getElementById("banner").innerText="🛍️ #"+r.id+"/30: "+r.name+" ("+r.cat+")";}
        }else{document.getElementById("banner").innerText="✅ All 30 Shops Connected from RNSIT!";}
      }
      requestAnimationFrame(loop);
    }
    loop();
    </script></body></html>"""
    components.html(sim_code, height=600)

# --- TAB 2: STORE CATALOG ---
with t2:
    st.subheader("🛒 Featured Local Products & Live Prices")
    cat = st.selectbox("Filter Category:", ["All", "Food & Drinks", "Retail & Goods", "Artisans & Services"])
    items_list = [
        ("Brew & Bites Cafe", "Food & Drinks", "Filter Coffee (₹40), Cinnamon Roll (₹80)", "15% OFF with 2 Stamps"),
        ("Neighborhood Book Corner", "Retail & Goods", "Exam Notebook Set (₹150), Sketchbook (₹180)", "10% OFF on ₹200+"),
        ("Craft & Clay Studio", "Artisans & Services", "Terracotta Planter (₹220), Soy Candle (₹190)", "Buy 2, get 1 mini candle free"),
        ("Spice & Crisp Bakery", "Food & Drinks", "Veg Puff 2pcs (₹50), Plum Cake (₹70)", "Free tea on ₹100+ combo"),
        ("Urban Style Boutique", "Retail & Goods", "Cotton Shirt (₹550), Canvas Tote (₹160)", "10% Student ID discount"),
        ("QuickPrint & Design Hub", "Artisans & Services", "Spiral Binding (₹60), A3 Poster (₹40)", "20% OFF student printing")
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
    labels = ["1. ☕ Food & Drinks", "2. 🛍️ Retail & Goods", "3. 🎨 Artisans", "4. 🍔 Local Bakery", "5. 📦 General Store", "6. ⭐ Any Map Shop"]
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
        st.markdown('<div class="vbox"><h4>📚 Book + Brew Bundle</h4><p>Spend ₹200 at <i>Book Corner</i> ➔ Get <b>15% OFF</b> at <i>Brew & Bites</i></p><span class="code">CODE: LOCALBREW15</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="vbox"><h4>🎨 Print + Snack Bundle</h4><p>Print notes at <i>QuickPrint</i> ➔ Get <b>Free Veg Puff</b> at <i>Spice Bakery</i></p><span class="code">CODE: CAMPUSPUFF</span></div>', unsafe_allow_html=True)
    with v2:
        st.markdown('<div class="vbox"><h4>👕 Style + Craft Bundle</h4><p>Shop at <i>Urban Style</i> ➔ Get <b>₹50 OFF</b> at <i>Craft & Clay Studio</i></p><span class="code">CODE: CRAFT50</span></div>', unsafe_allow_html=True)
        st.info("💡 **Zero Ad Cost:** Neighboring shops refer customers directly to each other!")

# --- TAB 5: MYSTERY BOX & EVENTS ---
with t5:
    st.subheader("🎁 Community Mystery Box & Campus Perks")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("### 🎁 Weekly Community Mystery Box\n* ☕ Filter Coffee Pack\n* 🕯️ Scented Soy Candle\n* 📚 Bestseller Novel\n* 🎟️ ₹500 Dining Vouchers")
    with m2:
        st.markdown("### 🎪 Campus & Street Activation\n* 🎓 **Student Saver Pass:** Extra 5% OFF with College ID + Passport\n* 📱 **QR Window Stickers:** Scan shop doors for live deals")
        
