import streamlit as st
import pint
import re

# Initialize Unit Registry
ureg = pint.UnitRegistry()

# Streamlit App Header
st.markdown("<h2>🔄 Google-Like Unit Converter</h2>", unsafe_allow_html=True)

# Unit categories
categories = {
    "Length": ["meter", "kilometer", "mile", "inch", "foot", "yard", "centimeter"],
    "Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liter", "milliliter", "gallon", "cup", "fluid_ounce"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second"],
    "Time": ["second", "minute", "hour", "day", "week"]
}

# Flatten unit list for easy searching
all_units = {unit: unit for sublist in categories.values() for unit in sublist}

# Add plural variations
plural_units = {"meters": "meter", "kilometers": "kilometer", "miles": "mile", "inches": "inch", "feet": "foot", "yards": "yard", "centimeters": "centimeter",
                 "grams": "gram", "kilograms": "kilogram", "pounds": "pound", "ounces": "ounce", "tons": "ton",
                 "liters": "liter", "milliliters": "milliliter", "gallons": "gallon", "cups": "cup", "fluid ounces": "fluid_ounce",
                 "seconds": "second", "minutes": "minute", "hours": "hour", "days": "day", "weeks": "week"}
all_units.update(plural_units)

# Smart Search Bar for Direct Queries
search_query = st.text_input("🔍 Smart Search (e.g., '1 kilogram to gram')")

# Extract value and units from query
match = re.search(r"(\d*\.?\d+)\s*(\w+)\s*to\s*(\w+)", search_query, re.IGNORECASE)

if match:
    value = float(match.group(1))
    from_unit = match.group(2).lower()
    to_unit = match.group(3).lower()
    from_unit = all_units.get(from_unit, from_unit)  # Convert plural to singular
    to_unit = all_units.get(to_unit, to_unit)  # Convert plural to singular
    if from_unit in all_units.values() and to_unit in all_units.values():
        auto_convert = True
    else:
        st.warning("⚠️ Units not found. Please check spelling.")
        auto_convert = False
else:
    value = 0.0
    from_unit, to_unit = None, None
    auto_convert = False

# UI: Category Selection
category = st.selectbox("📌 Select a category", list(categories.keys()))

# UI: Searchable Dropdowns for Units
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("🔄 Convert from", categories[category], index=categories[category].index(from_unit) if from_unit in categories[category] else 0)
with col2:
    to_unit = st.selectbox("➡️ Convert to", categories[category], index=categories[category].index(to_unit) if to_unit in categories[category] else 0)

# UI: Instant Conversion on Input
value = st.number_input("✍️ Enter value", min_value=0.0, format="%.2f", value=value if auto_convert else 0.0, key="input_value")

# Perform Conversion in Real-time
if value:
    try:
        converted_value = (value * ureg(from_unit)).to(to_unit)
        st.markdown(f"""
            <div style='text-align: center; font-size: 28px; font-weight: bold; color: #008000; margin-top: 20px;'>
                ✅ {value} {from_unit} = {converted_value:.2f} {to_unit}
            </div>
        """, unsafe_allow_html=True)
    except pint.errors.UndefinedUnitError:
        st.error("⚠️ Invalid unit selection! Please try again.")
    except Exception:
        st.error("⚠️ Conversion error! Please try again.")

# Footer with Larger Font and Extra Top Space
st.markdown("""
    <div style='margin-top: 50px;'>
        <h3 style='text-align: center; font-size: 22px;'>⚡ Built by Streamlit | Design by Basit Khalil 🚀</h3>
    </div>
""", unsafe_allow_html=True)
