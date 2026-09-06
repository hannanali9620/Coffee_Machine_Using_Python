# Coffee_Machine_Using_Python
An interactive, industrial-style virtual espresso machine built with Python and Streamlit. Inspired by commercial 58mm barista units, this web application simulates the end-to-end brewing experience—from customizable recipe configuration and cash payment handling to real-time animated extraction diagnostics.

🌟 Features
Customizable Drinks & Sizing: Choose between Espresso, Latte, and Cappuccino across Small (8 oz), Medium (12 oz), and Large (16 oz) cup sizes with dynamically scaled ingredient ratios and pricing.

Realistic Hardware Visualization: Custom SVG-driven interface rendering an industrial brushed-steel chassis, bean hopper, 58mm group head, dual glass mugs, and steam wand.

Live Machine Diagnostics:

Active coffee grounds dosing into the portafilter basket.

Real-time water piping illumination through the thermocoil boiler.

Dynamic analog pressure barometer scaling up to 12.5 BAR.

Dual-spout liquid streams filling glass cups with rich espresso and golden crema.

Steam wand texturing microfoam for milk-based beverages.

Payment & Cash Handling: Multi-denomination payment slot ($0.25, $1.00, $2.00, $5.00) with automatic balance tracking, change calculation, and transaction rollback/refunds.

Inventory & Tank Management: Tracks live bean, water, and milk levels across sessions with automated stock validation and one-click refills.

🛠️ Built With
Python: Core application and state logic.

Streamlit: Web application framework and session state orchestration.

Custom SVG & CSS: Embedded hardware animation and retro-industrial typography.


coffee-machine/
├── .venv/                      # Python virtual environment
├── src/                        # Modular application components (optional)
│   ├── config.py               # Recipes, dimensions, and machine constants
│   ├── components.py           # SVG hardware rendering functions
│   ├── machine_logic.py        # Stock validation and payment math
│   └── styles.py               # Metallic UI and heading CSS
├── app.py                      # Primary Streamlit application entry point
├── requirements.txt            # Dependency definitions
└── README.md                   # Project overview and setup instructions
