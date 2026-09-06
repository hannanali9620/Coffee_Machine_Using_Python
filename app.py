import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Barista Touch Espresso System", page_icon="☕", layout="centered")

# --- Industrial Heading & Theme Typography ---
st.markdown("""
<style>
    /* Main Machine Title */
    .app-title {
        font-family: 'Montserrat', 'Helvetica Neue', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #ffffff 20%, #ced4da 60%, #6c757d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));
    }

    /* Machine Subtitle Tag */
    .app-subtitle {
        text-align: center;
        font-size: 0.8rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #00d2d3;
        margin-bottom: 18px;
        font-weight: 600;
    }

    /* Metallic Step Headers */
    .step-header {
        display: flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(90deg, #1e293b 0%, rgba(30, 41, 59, 0) 100%);
        padding: 8px 14px;
        border-left: 4px solid #d90429;
        border-radius: 0 8px 8px 0;
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 16px 0;
        text-transform: uppercase;
    }

    /* Hardware Badges */
    .step-badge {
        background: #d90429;
        color: #ffffff;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 800;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- Title Header ---
st.markdown('<div class="app-title">☕ Barista Touch Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Commercial 58mm Dual-Spout Espresso Unit</div>', unsafe_allow_html=True)

# --- Recipe Menu ---
BASE_MENU = {
    "1": {
        "name": "Espresso",
        "base_price": 2.50,
        "beans": 18,
        "water": 40,
        "milk": 0,
        "target_bar": 12.5,
        "steaming": False,
        "icon": "☕"
    },
    "2": {
        "name": "Latte",
        "base_price": 3.75,
        "beans": 18,
        "water": 40,
        "milk": 150,
        "target_bar": 11.8,
        "steaming": True,
        "icon": "🥛"
    },
    "3": {
        "name": "Cappuccino",
        "base_price": 4.25,
        "beans": 18,
        "water": 40,
        "milk": 100,
        "target_bar": 12.0,
        "steaming": True,
        "icon": "☕"
    }
}

# --- Cup Sizing Configuration ---
SIZES = {
    "Small": {
        "multiplier": 1.0,
        "price_add": 0.00,
        "cup_w": 24,
        "cup_h": 26,
        "cup_y": 272,
        "label": "Small (8 oz)"
    },
    "Medium": {
        "multiplier": 1.4,
        "price_add": 0.75,
        "cup_w": 28,
        "cup_h": 32,
        "cup_y": 265,
        "label": "Medium (12 oz)"
    },
    "Large": {
        "multiplier": 1.8,
        "price_add": 1.50,
        "cup_w": 32,
        "cup_h": 38,
        "cup_y": 258,
        "label": "Large (16 oz)"
    }
}

# --- State Management ---
defaults = {
    "beans": 250.0,
    "water": 1200.0,
    "milk": 600.0,
    "order_step": "select",
    "selected_drink": None,
    "selected_size": "Medium",
    "total_price": 0.0,
    "inserted": 0.0,
    "last_change": 0.0,
    "deducted": False
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- SVG Visual Engine ---
def render_machine(
    pressure=0.0,
    status="READY",
    grinding=False,
    water_flowing=False,
    pouring=False,
    steaming=False,
    liquid_fill=0,
    size_name="Medium"
):
    size_spec = SIZES[size_name]
    cup_w = size_spec["cup_w"]
    cup_h = size_spec["cup_h"]
    cup_y = size_spec["cup_y"]

    angle = -90 + (pressure / 16.0) * 180
    angle = max(-90, min(90, angle))

    indicator_fill = "#2ec4b6" if (pouring or steaming or grinding or water_flowing) else "#6c757d"
    water_pipe_color = "#00d2d3" if water_flowing else "#485460"
    water_pipe_dash = "stroke-dasharray='6,4'" if water_flowing else ""
    grind_opacity = "1.0" if grinding else "0.0"
    pour_color = "#4a2511" if pouring else "transparent"
    crema_color = "#d4a373" if (liquid_fill > 10) else "transparent"
    steam_opacity = "0.75" if steaming else "0.0"
    cup_steam_opacity = "0.70" if (liquid_fill > 40) else "0.0"

    fill_h = min(cup_h - 4, int((cup_h - 4) * (liquid_fill / 100.0)))
    fill_y = (cup_y + cup_h - 2) - fill_h

    cup1_x = 219 - (cup_w / 2)
    cup2_x = 241 - (cup_w / 2)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background: transparent;
            }}
            @keyframes pulse {{
                0% {{ opacity: 0.2; transform: translateY(0); }}
                50% {{ opacity: 0.8; transform: translateY(-4px); }}
                100% {{ opacity: 0.2; transform: translateY(-8px); }}
            }}
            .steam-rise {{
                animation: pulse 1.2s infinite ease-in-out;
            }}
        </style>
    </head>
    <body>
        <svg width="460" height="410" viewBox="0 0 460 410" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="chassisMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#f5f6fa"/>
                    <stop offset="50%" stop-color="#dcdde1"/>
                    <stop offset="100%" stop-color="#718093"/>
                </linearGradient>
                <linearGradient id="hopperGlass" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#3d3d3d" stop-opacity="0.2"/>
                    <stop offset="100%" stop-color="#222f3e" stop-opacity="0.7"/>
                </linearGradient>
                <linearGradient id="cupGlass" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.55"/>
                    <stop offset="25%" stop-color="#dcdde1" stop-opacity="0.2"/>
                    <stop offset="75%" stop-color="#ffffff" stop-opacity="0.2"/>
                    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.65"/>
                </linearGradient>
            </defs>

            <!-- Chassis Frame -->
            <rect x="30" y="45" width="400" height="345" rx="20" fill="url(#chassisMetal)" stroke="#2f3640" stroke-width="3"/>
            <rect x="50" y="60" width="360" height="85" rx="10" fill="#2f3640"/>

            <!-- Transparent Water Reservoir (Left Tank) -->
            <rect x="55" y="150" width="45" height="150" rx="4" fill="#0abde3" fill-opacity="0.25" stroke="#718093" stroke-width="1.5"/>
            <rect x="57" y="170" width="41" height="128" fill="#00d2d3" fill-opacity="0.6"/>
            <text x="77" y="165" font-size="7" fill="#ffffff" font-family="sans-serif" text-anchor="middle" font-weight="bold">WATER</text>
            <path d="M 100 210 L 150 210 L 150 145 L 205 145" fill="none" stroke="{water_pipe_color}" stroke-width="4" {water_pipe_dash}/>

            <!-- Hopper & Beans -->
            <polygon points="180,45 280,45 265,10 195,10" fill="url(#hopperGlass)" stroke="#718093" stroke-width="2"/>
            <ellipse cx="230" cy="10" rx="35" ry="5" fill="#1e272e"/>
            <circle cx="215" cy="35" r="4.5" fill="#6F4E37"/>
            <circle cx="230" cy="25" r="5" fill="#4B3621"/>
            <circle cx="245" cy="38" r="4.5" fill="#6F4E37"/>
            <circle cx="225" cy="42" r="4" fill="#3E2723"/>

            <!-- Ground Coffee Falling -->
            <g opacity="{grind_opacity}">
                <circle cx="220" cy="148" r="1.8" fill="#4B3621"/>
                <circle cx="228" cy="155" r="2.2" fill="#6F4E37"/>
                <circle cx="236" cy="150" r="1.8" fill="#3E2723"/>
                <circle cx="224" cy="162" r="2.0" fill="#4B3621"/>
                <circle cx="232" cy="160" r="2.0" fill="#6F4E37"/>
            </g>

            <!-- Digital LCD Status Display -->
            <rect x="70" y="75" width="105" height="35" rx="4" fill="#000000" stroke="#00f2fe" stroke-width="1.5"/>
            <text x="122" y="93" fill="#00f2fe" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">{status}</text>
            <text x="122" y="104" fill="#747d8c" font-size="7" font-family="monospace" text-anchor="middle">SIZE: {size_name.upper()}</text>

            <!-- Center Extraction Pressure Gauge -->
            <circle cx="230" cy="102" r="32" fill="#ffffff" stroke="#2f3640" stroke-width="3"/>
            <circle cx="230" cy="102" r="28" fill="#f8f9fa" stroke="#ced6e0" stroke-width="1"/>
            <path d="M 230 76 A 26 26 0 0 1 252 94" fill="none" stroke="#2ed573" stroke-width="3"/>
            <text x="230" y="122" font-size="7" fill="#747d8c" font-family="sans-serif" text-anchor="middle" font-weight="bold">PRESSURE</text>
            <text x="230" y="96" font-size="11" fill="#c0392b" font-family="sans-serif" text-anchor="middle" font-weight="bold">{pressure:.1f}</text>
            <line x1="230" y1="102" x2="230" y2="78" stroke="#c0392b" stroke-width="2" transform="rotate({angle}, 230, 102)"/>

            <!-- Buttons & Lights -->
            <circle cx="340" cy="90" r="7" fill="{indicator_fill}" stroke="#2f3640" stroke-width="2"/>
            <circle cx="370" cy="90" r="11" fill="#dcdde1" stroke="#2f3640" stroke-width="2"/>

            <!-- Group Head, Portafilter & Dual Spouts -->
            <rect x="185" y="145" width="90" height="22" rx="3" fill="#1e272e"/>
            <polygon points="200,167 260,167 252,190 208,190" fill="#adb5bd" stroke="#2f3640" stroke-width="2"/>
            <rect x="255" y="172" width="70" height="12" rx="6" fill="#111111"/>
            <rect x="216" y="190" width="6" height="10" rx="2" fill="#2f3640"/>
            <rect x="238" y="190" width="6" height="10" rx="2" fill="#2f3640"/>

            <!-- Espresso Liquid Streams -->
            <line x1="219" y1="200" x2="219" y2="{cup_y}" stroke="{pour_color}" stroke-width="3" stroke-dasharray="6,2"/>
            <line x1="241" y1="200" x2="241" y2="{cup_y}" stroke="{pour_color}" stroke-width="3" stroke-dasharray="6,2"/>

            <!-- Dual Glass Cups with Dynamic Fill & Handles -->
            <!-- Left Cup -->
            <path d="M {cup1_x - 3} {cup_y + 8} C {cup1_x - 12} {cup_y + 8}, {cup1_x - 12} {cup_y + 24}, {cup1_x - 3} {cup_y + 24}" fill="none" stroke="#dcdde1" stroke-width="2.5" stroke-linecap="round"/>
            <rect x="{cup1_x}" y="{cup_y}" width="{cup_w}" height="{cup_h}" rx="4" fill="url(#cupGlass)" stroke="#ced6e0" stroke-width="1.8"/>
            <rect x="{cup1_x + 2}" y="{fill_y}" width="{cup_w - 4}" height="{fill_h}" fill="{pour_color}" rx="2"/>
            <ellipse cx="{cup1_x + (cup_w / 2)}" cy="{fill_y}" rx="{(cup_w - 4) / 2}" ry="2.5" fill="{crema_color}"/>
            <path d="M {cup1_x + (cup_w / 2)} {cup_y - 6} Q {cup1_x + (cup_w / 2) - 4} {cup_y - 14} {cup1_x + (cup_w / 2)} {cup_y - 20}" fill="none" stroke="#f1f2f6" stroke-width="2" stroke-linecap="round" opacity="{cup_steam_opacity}" class="steam-rise"/>

            <!-- Right Cup -->
            <rect x="{cup2_x}" y="{cup_y}" width="{cup_w}" height="{cup_h}" rx="4" fill="url(#cupGlass)" stroke="#ced6e0" stroke-width="1.8"/>
            <path d="M {cup2_x + cup_w + 3} {cup_y + 8} C {cup2_x + cup_w + 12} {cup_y + 8}, {cup2_x + cup_w + 12} {cup_y + 24}, {cup2_x + cup_w + 3} {cup_y + 24}" fill="none" stroke="#dcdde1" stroke-width="2.5" stroke-linecap="round"/>
            <rect x="{cup2_x + 2}" y="{fill_y}" width="{cup_w - 4}" height="{fill_h}" fill="{pour_color}" rx="2"/>
            <ellipse cx="{cup2_x + (cup_w / 2)}" cy="{fill_y}" rx="{(cup_w - 4) / 2}" ry="2.5" fill="{crema_color}"/>
            <path d="M {cup2_x + (cup_w / 2)} {cup_y - 6} Q {cup2_x + (cup_w / 2) + 4} {cup_y - 14} {cup2_x + (cup_w / 2)} {cup_y - 20}" fill="none" stroke="#f1f2f6" stroke-width="2" stroke-linecap="round" opacity="{cup_steam_opacity}" class="steam-rise"/>

            <!-- Steam Wand -->
            <path d="M 330 145 L 345 230 L 360 255" fill="none" stroke="#ced4da" stroke-width="5" stroke-linecap="round"/>
            <ellipse cx="360" cy="255" rx="14" ry="22" fill="#ffffff" opacity="{steam_opacity}" class="steam-rise"/>

            <!-- Base Grill -->
            <rect x="50" y="315" width="360" height="50" rx="6" fill="#2f3640"/>
            <line x1="65" y1="330" x2="395" y2="330" stroke="#718093" stroke-width="2"/>
            <line x1="65" y1="345" x2="395" y2="345" stroke="#718093" stroke-width="2"/>
        </svg>
    </body>
    </html>
    """
    components.html(html_code, height=420)

# --- Top Reservoir Status Drawer ---
with st.expander("Machine Reservoirs & Status", expanded=False):
    col1, col2, col3 = st.columns(3)
    col1.metric("Bean Hopper", f"{st.session_state.beans:.1f} g")
    col2.metric("Water Tank", f"{st.session_state.water:.1f} ml")
    col3.metric("Milk Pitcher", f"{st.session_state.milk:.1f} ml")
    if st.button("Replenish Reservoirs"):
        st.session_state.beans = 250.0
        st.session_state.water = 1200.0
        st.session_state.milk = 600.0
        st.rerun()

st.write("")

# --- Step 1: Beverage & Size Selection ---
if st.session_state.order_step == "select":
    render_machine(pressure=0.0, status="READY", liquid_fill=0, size_name=st.session_state.selected_size)

    st.markdown("""
    <div class="step-header">
        <span class="step-badge">STEP 01</span> Select Beverage & Cup Size
    </div>
    """, unsafe_allow_html=True)

    col_drink, col_size = st.columns([1.2, 1])

    with col_drink:
        choice = st.radio(
            "Select Beverage:",
            options=list(BASE_MENU.keys()),
            format_func=lambda k: f"[{k}] {BASE_MENU[k]['icon']} {BASE_MENU[k]['name']} — from ${BASE_MENU[k]['base_price']:.2f}"
        )
        base_drink = BASE_MENU[choice]

    with col_size:
        size_choice = st.radio(
            "Select Cup Size:",
            options=list(SIZES.keys()),
            format_func=lambda s: f"{SIZES[s]['label']} (+${SIZES[s]['price_add']:.2f})"
        )
        st.session_state.selected_size = size_choice

    size_info = SIZES[size_choice]
    mult = size_info["multiplier"]
    final_price = base_drink["base_price"] + size_info["price_add"]

    active_recipe = {
        "name": base_drink["name"],
        "size": size_choice,
        "price": final_price,
        "beans": round(base_drink["beans"] * mult, 1),
        "water": round(base_drink["water"] * mult, 1),
        "milk": round(base_drink["milk"] * mult, 1),
        "target_bar": base_drink["target_bar"],
        "steaming": base_drink["steaming"]
    }

    st.info(
        f"**Selected:** {size_choice} {active_recipe['name']} | "
        f"**Price:** ${final_price:.2f} | "
        f"Ingredients: {active_recipe['beans']}g beans, {active_recipe['water']}ml water, {active_recipe['milk']}ml milk"
    )

    can_brew = (
        st.session_state.beans >= active_recipe["beans"] and
        st.session_state.water >= active_recipe["water"] and
        st.session_state.milk >= active_recipe["milk"]
    )

    if not can_brew:
        st.error("⚠️ Insufficient ingredients for this cup size. Please refill reservoirs above.")
    elif st.button("Confirm Selection & Proceed to Pay"):
        st.session_state.selected_drink = active_recipe
        st.session_state.total_price = final_price
        st.session_state.order_step = "pay"
        st.rerun()

# --- Step 2: Payment (Coins & Cash) ---
elif st.session_state.order_step == "pay":
    drink = st.session_state.selected_drink
    render_machine(pressure=0.0, status="INSERT COIN", liquid_fill=0, size_name=drink["size"])

    st.markdown(f"""
    <div class="step-header">
        <span class="step-badge">STEP 02</span> Payment for {drink['size']} {drink['name']}
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"Total Amount Due: **${drink['price']:.2f}**")

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("+$0.25 (Quarter)"):
        st.session_state.inserted += 0.25
        st.rerun()
    if c2.button("+$1.00 (Bill)"):
        st.session_state.inserted += 1.00
        st.rerun()
    if c3.button("+$2.00 (Bill)"):
        st.session_state.inserted += 2.00
        st.rerun()
    if c4.button("+$5.00 (Bill)"):
        st.session_state.inserted += 5.00
        st.rerun()

    due = max(0.0, drink["price"] - st.session_state.inserted)
    m1, m2 = st.columns(2)
    m1.metric("Remaining Needed", f"${due:.2f}")
    m2.metric("Inserted Cash", f"${st.session_state.inserted:.2f}")

    b_brew, b_cancel = st.columns(2)
    with b_brew:
        if st.session_state.inserted >= drink["price"]:
            if st.button("Engage Machine Extraction", type="primary"):
                st.session_state.order_step = "brewing"
                st.rerun()
        else:
            st.button("Engage Machine Extraction", disabled=True)

    with b_cancel:
        if st.button("Refund & Cancel"):
            st.session_state.inserted = 0.0
            st.session_state.selected_drink = None
            st.session_state.order_step = "select"
            st.rerun()

# --- Step 3: Complete Machine Processing Display ---
elif st.session_state.order_step == "brewing":
    drink = st.session_state.selected_drink

    if not st.session_state.deducted:
        st.session_state.beans -= drink["beans"]
        st.session_state.water -= drink["water"]
        st.session_state.milk -= drink["milk"]
        st.session_state.deducted = True

    change = st.session_state.inserted - drink["price"]

    st.markdown(f"""
    <div class="step-header">
        <span class="step-badge">STEP 03</span> Processing {drink['size']} {drink['name']}
    </div>
    """, unsafe_allow_html=True)

    machine_slot = st.empty()
    status_msg = st.empty()
    bar = st.progress(0)

    # 1. Grinder Active
    with machine_slot:
        render_machine(pressure=0.0, status="GRINDING", grinding=True, liquid_fill=0, size_name=drink["size"])
    status_msg.info(f"🪨 Conical Burr Grinder active: Dosing {drink['beans']}g into 58mm portafilter...")
    bar.progress(20)
    time.sleep(1.3)

    # 2. Water Pumping Active
    with machine_slot:
        render_machine(pressure=2.5, status="PUMPING WATER", water_flowing=True, liquid_fill=0, size_name=drink["size"])
    status_msg.info(f"💧 Heating & pumping {drink['water']}ml water through thermocoil boiler...")
    bar.progress(40)
    time.sleep(1.1)

    # 3. Liquid Fills Cups with Streams & Rising Crema
    for fill_pct in [25, 50, 75, 100]:
        curr_bar = 6.0 + (fill_pct / 100.0) * (drink["target_bar"] - 6.0)
        with machine_slot:
            render_machine(
                pressure=curr_bar,
                status="EXTRACTING",
                water_flowing=True,
                pouring=True,
                liquid_fill=fill_pct,
                size_name=drink["size"]
            )
        status_msg.warning(f"☕ Dual-spout flow: Extracting {drink['size']} cup ({fill_pct}% full) at {curr_bar:.1f} BAR...")
        bar.progress(40 + int(fill_pct * 0.45))
        time.sleep(0.7)

    # 4. Milk Steaming Wand (for Latte & Cappuccino)
    if drink["steaming"]:
        with machine_slot:
            render_machine(pressure=1.5, status="STEAMING", steaming=True, liquid_fill=100, size_name=drink["size"])
        status_msg.info(f"💨 Steam Wand purging: Texturing {drink['milk']}ml velvety microfoam...")
        bar.progress(95)
        time.sleep(1.3)

    with machine_slot:
        render_machine(pressure=0.0, status="READY", liquid_fill=100, size_name=drink["size"])
    bar.progress(100)

    st.session_state.last_change = change
    st.session_state.order_step = "complete"
    st.session_state.deducted = False
    time.sleep(0.6)
    st.rerun()

# --- Step 4: Finished Order ---
elif st.session_state.order_step == "complete":
    drink = st.session_state.selected_drink
    render_machine(pressure=0.0, status="ENJOY!", liquid_fill=100, size_name=drink["size"])
    st.balloons()

    st.markdown("""
    <div class="step-header" style="border-left-color: #2ec4b6;">
        <span class="step-badge" style="background: #2ec4b6;">READY</span> Extraction Complete
    </div>
    """, unsafe_allow_html=True)

    st.success(f"✅ **Your {drink['size']} {drink['name']} is ready on the tray!**")
    if st.session_state.last_change > 0:
        st.info(f"🪙 Dispensing Change: **${st.session_state.last_change:.2f}**")

    if st.button("Prepare Another Beverage", type="primary"):
        st.session_state.inserted = 0.0
        st.session_state.selected_drink = None
        st.session_state.order_step = "select"
        st.rerun()