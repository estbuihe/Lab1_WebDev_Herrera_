"""
Web Development Lab 01 - Part 2: Quarter-Final Ticket Demand 

"""

import streamlit as st
import pandas as pd

# We need this section for the session initialization

if "chosen_tier" not in st.session_state:
    st.session_state.chosen_tier = None

if "calculated" not in st.session_state:
    st.session_state.calculated = False

st.title("World Cup Quater Final Market Valuation and Demand quiz 🎟️")

st.write("""
Welcome to the Ticket Demand Index quiz!  
Answer the following questions to find out your fan demand tier and willingness to pay profile for a Quarter-Final match of the World Cup.
""")

# Banner Image (Requirement: Image 1)

col1, col2, col3 = st.columns(3) #I need to devide the screen in 3 so that I can have a centered photo

with col2:
    st.image("Images/qphoto1.JPG", caption="World Cup Atmosphere", width=300)

st.write("---")


# Question 1, the max Budget slider

q1 = st.slider(
    "💰 What is the absolute maximum price ($ USD) you would pay for a premium Quarter-Final seat?",
    100, 3000, 800, step=100
)

# Question 2, travel willingness of the client/fan

col1, col2, col3 = st.columns(3) 

with col2:
    st.image("Images/qphoto2.JPG", caption="Host City Stadium Travel", width=300)

q2 = st.radio(
    "✈️️ How far would you travel on a 24 hours notice to attend?",
    ["I'd only go if it's in my city", "Up to a 6-hour drive", "I'll book an international flight immediately"]
)

# Question 3, what sacrifies would they make
q3 = st.multiselect(
    "💪 Which financial & personal tradeoffs are you willing to accept?",
    ["Skip work/school", "Camp outside overnight", "Accept a standing room only", "Pay surge prices for hotels"]
)

# Question 4, World Cup importance level, priority organization
col1, col2, col3 = st.columns(3) 

with col2:
    st.image("Images/qphoto3.JPG", caption="Final title celebration", width=300)
    
q4 = st.selectbox(
    "🌍 How special is this World Cup to you compared to regular soccer matches?",
    [
        "Once in a lifetime exception ( clear your schedule completely)",
        "Major priority event ( prioritizing key matches)",
        "Casual viewing ( watching if you get to be free)"
    ]
)

# Question 5, game watching preferences 
q5 = st.selectbox(
    "What is your main match day goal?",
    ["Experience world cup knockout intense passion in person", "Watch world class players live", "Enjoy the stadium atmosphere", "Watch comfortably with friends or family"]
)

st.write("---")


if st.button("Calculate market valuation and Elasticity"):
    st.session_state.calculated = True
    st.balloons()  
    
if st.session_state.calculated:

    
    # econ values and coversions
    
    
    # bAse market value the avg of a QF ticket
    market_benchmark = 1200
    
    # 1 Personal market value
    tradeoff_bonus = len(q3) * 150
    travel_bonus = 400 if "international" in q2 else (150 if "drive" in q2 else 0)
    
    # World Cup Priority Bonus and the Q4 elasticity impact
    if "Once-in-a-lifetime" in q4:
        priority_bonus = 350
        priority_elasticity_reduction = 0.25
    elif "Major priority" in q4:
        priority_bonus = 150
        priority_elasticity_reduction = 0.10
    else:  
        priority_bonus = 0
        priority_elasticity_reduction = 0.0

    # addtion for total market value
    estimated_market_value = q1 + tradeoff_bonus + travel_bonus + priority_bonus

    # 2 Price elasticity of Demand 
    base_elasticity = 1.2
    elasticity_reduction = (
        (q1 / 3000) * 0.4 + 
        (len(q3) * 0.1) + 
        (0.2 if "international" in q2 else 0) + 
        priority_elasticity_reduction
    )
    
    price_elasticity = round(max(0.15, base_elasticity - elasticity_reduction), 2)

    # Determine the tier putcome
    if price_elasticity < 0.6:
        tier_name = "Tier 1: Inelastic Superfan (You are a costumer with an high willingness to pay!)"
        tier_color = "#FFD700"  # the color here is gold
        tier_desc = "The price is not a concern. You consider this a one time event and plan to pay premium market values."
    elif price_elasticity < 1.0:
        tier_name = "Tier 2: Dedicated Stadium Attendee (Your profile is relative Inelastic)"
        tier_color = "#C0C0C0"  # silver
        tier_desc = "You are highly motivated to attend, however, you keep a sensible budget relative to the market prices of the game."
    else:
        tier_name = "Tier 3: Price-Sensitive Spectator (Elastic Demand)"
        tier_color = "#CD7F32"  #brronze
        tier_desc = "Your demand has a high price elastic value. You prefer fan zones or broadcast viewing if prices are high."


    # results
    
    st.subheader("Economic & Demand Analysis")
    
    # Display our results side by side 
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric(
            label="Estimated Market Valuation",
            value=f"${estimated_market_value:,}",
            delta=f"${estimated_market_value - market_benchmark:,} vs Avg"
        )
        
    with m2:
        st.metric(
            label="Price Elasticity (Ed)",
            value=f"{price_elasticity}",
            delta="Inelastic (<1.0)" if price_elasticity < 1.0 else "Elastic (≥1.0)",
            delta_color="normal" if price_elasticity < 1.0 else "inverse"
        )
        
    with m3:
        st.metric(
            label="Max Budget Cap",
            value=f"${q1:,}"
        )

    st.write("---")

    # place for the tier badge 
    st.markdown(
        f"<h2 style='background-color:{tier_color};color:black;padding:12px;border-radius:10px;text-align:center;'>"
        f"{tier_name}</h2>",
        unsafe_allow_html=True
    )
    
    st.write(f"**Profile Summary:** {tier_desc}")

    # feedback option yay yay
    st.write("---")
    st.subheader("Rate this economic valuation:")
    rating = st.feedback("stars")
    if rating is not None:
        st.write(f"Thank you for your rating of {rating + 1} star(s)! ⭐")
