"""
Radar Chart Outcome Visualizer
--------------------------------
A simple web app (built with Streamlit) that lets you fill out a set of
outcome scores across categories, each of which is broken into weighted
sub-categories. Instantly see the results plotted on a radar / spider chart.
It also supports comparing multiple outcomes.

"""

import json
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Fast Automated and Smart mobility impact Tool (FAST)", layout="wide")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_CATEGORIES = [
    "Travel Costs",
    "Accessibility",
    "Health",
    "Safety",
    "Living Environment",
    "Economic Activity & Employment",
    "Societal Costs",
    "Infra Efficiency/Flow",    
    "User Acceptance",
    "Convenience and Satisfaction",
    "Traveler Travel time & Efficiency",
]

FORM_CATEGORY_ORDER = [
    "Health",
    "Accessibility",
    "Travel Costs",
    "Traveler Travel time & Efficiency",
    "Convenience and Satisfaction",
    "User Acceptance",
    "Safety",
    "Living Environment",
    "Economic Activity & Employment",
    "Societal Costs",
    "Infra Efficiency/Flow",    
]

DEFAULT_SUBCATEGORIES = {
    "Safety": ["Data privacy", "Traffic safety"],
    "Living Environment": ["Quality of environment", "Public health", 'Community cohesion'],
    "Societal Costs": ['Tax income', 'Mobility costs', 'Environmental costs'],
    "Economic Activity & Employment": ['Business proposition', 'Workforce'],
    "Infra Efficiency/Flow": ['Infrastructure efficiency, Capacity, Congestion or traffic flow efficiency'],
    "Traveler Travel time & Efficiency": ['Reliability/Punctuality', 'Connectivity and frequency of service', 'Travel speed'],
    "User Acceptance": ['Public opinion, Willingness to use the mobility and Technology acceptance'],
    "Convenience and Satisfaction": ['Comfort', 'Ease of use'],
    "Travel Costs": ['Travel costs'],
    "Accessibility": ['Transport points/infrastructure accessibility', 'Destination accessibility', 'Inclusivity', 'Social safety'],
    "Health": ['Physical well-being', 'Social and mental well-being'],
}

DEFAULT_CATEGORY_DESCRIPTIONS = {
    "Safety": """-""",
    
    "Living Environment": """The living environment or liveability of an area considers the impacts of the mobility proposition on the overall suitability and quality of living in a given area, drawing together indicators from other impact areas into an integrated evaluation of their combined effects. While closely related to health and quality of life, it focuses on the collective characteristics of an area rather than individual experiences. It spans a broad range of environmental and socio-economic factors, capturing the combination of elements that together shape a community's quality of life.
    Possible breakdown: Area, Income, Age """,
    
    "Societal Costs": """The impact factor ‘Societal costs’ address the broader financial implications of the mobility proposition for society, covering public revenue effects, the costs associated with mobility infrastructure and services, and the energy resources required to operate them.""",
    
    "Economic Activity & Employment": """Economic activity and employment address the implications of the mobility proposition for economic development and labour dynamics, focusing on its influence on overall economic vitality, the evolution of businesses and the job market, and the skill requirements demanded of the workforce.""",
    
    "Infra Efficiency/Flow": """Infrastructure efficiency is the throughput of a system defined as  the capacity and the number of vehicles or passengers that can travel through the network. Traffic flow efficiency is the ability of the network to serve the required demand without unnecessary delays (time component) and without the creation of congestion. """,
    
    "Traveler Travel time & Efficiency": """This impact area addresses the temporal dimension of travel and how it is impacted by the discussed mobility proposition. It focuses on how much time a trip takes and how efficiently travel is facilitated. Travel time could play a decisive role in shaping whether people choose public transport over private alternatives. Travel time is closely related to accessibility and convenience""",
    
    "User Acceptance": """User acceptance refers to the willingness of individuals to use a system or the acceptance of the system by the surrounding. It is closely influenced by perceptions of safety, trust in future technologies, and the (seamless) integration with existing systems. Public opinion, as a key component, reflects the collective attitudes, beliefs, and sentiments of the community toward these innovations, often shaped by media, personal experiences, and societal norms. High acceptance depends on positive public opinion and willingness to use the system for a successful implementation. """,
    
    "Convenience and Satisfaction": """Convenience and satisfaction represent how the mobility proposition is experienced by the user and the surrounding. Passenger experience is important for long-term adoption of a system. The user’s experience can be pleasant, easy, useful etc. based on the physical and mental state of the user during the journey, influenced by, for instance, comfort, convenience, stress, motion sickness and many more. Additionally, this factor can also include feelings and experiences of ‘non-users’ interacting with the system. 
    Often when travel cost, travel time and accessibility requirements are met, convenience and satisfaction will be a determining factor for long term use. """,
    
    "Travel Costs": """Travel costs area critical factor in mode choice behavior. Offering a strong incentive to change transport type. It also influences the accessibility of the mobility system. Travel costs can include for instance cost to own a vehicle, or public transport ticket fares. """,
    
    "Accessibility": """Accessibility addresses how the mobility proposition affects the ability of individuals to reach destinations, services, and activities at different times of day, and the ability of entrepreneurs and other individuals to receive people and goods in return. More concretely, it reflects the extent to which the spatial and mobility system enables people and goods to reach destinations and activities that matter to them, how efficiently this happens, and how well the transport system connects individuals and businesses while enabling participation and the exchange of information, goods, and services.
    Possible breakdowns: Education, modality, area, age """,
    
    "Health": """Health captures the holistic physical, social and mental well-being effects that a mobility solution has on its users and surrounding population, going beyond the mere absence of fatalities and injuries. It includes both positive effects of mobility, such as physical activity from walking or cycling and the psychological benefits of independence, adventure, and travel itself, and negative effects, such as air and noise pollution linked to respiratory disorders and premature death. Health can also be described as 'quality of life'.
    Possible indicative measures: years of life gained, sleeping problems, respiratory disorders
    Possible breakdowns: Education, income, age, area"""
}

DEFAULT_SUBCATEGORY_DESCRIPTIONS = {
    "Safety": {
        "Data privacy": """Data privacy and security is an increasingly important impact area, driven by the growing role of smart, connected, and automated mobility systems that collect and exchange large amounts of data. This impact area covers both data protection concerns, such as compliance with regulations like the GDPR regarding the collection, use, and storage of personal data, and cybersecurity concerns related to protecting systems from unauthorized access. As vehicles and infrastructure become more connected, the potential impact of data and security breaches extends beyond privacy violations alone to include direct risks to physical safety.""",
        "Traffic safety": """This sub-impact factor addresses the impact of the mobility proposition on the number of accidents and injuries of different gravity. Traffic accidents are determined by factors: exposure, risk and consequence. 
        Possible breakdowns: Modality, age, income
        """
        },
        
    "Health": {
        "Physical well-being": """Physical well-being within the impact factor health, relates to a person's fitness level, meaning their capacity to carry out everyday activities, as well as the number of years spent free of illness or disability. Examples of transport affects that can influence physical well-being are for instance noise pollution, air pollution, physical exercise or permanent injury.  """,
        "Social and mental well-being": """Social well-being connects to feeling a sense of belonging to others or having meaningful and supportive relationships. Mobility can influence social well-being through offering access to social contacts and by having a function of community stimulation also influencing mental well-being. Additionally mental well-being can positively be influenced by for instance the ability to take a walk or drive a bike.  """,
        },
    "Accessibility": {
        "Transport points/infrastructure accessibility":"""This sub-impact factor addresses the access to the mobility proposition. How well can the user access the mobility system or how easy is it to reach transport points/infrastructure? Focusing on the physical side, considering, stops, infrastructure, transport point density etc. """, 
        "Destination accessibility": """This sub-impact factor addresses to which extent the mobility proposition facilitates what locations are actually reachable for individuals through the system, making it possible to reach amenities, jobs, schools, or healthcare. Indirectly influencing financial well-being. """,
        "Inclusivity": """Inclusivity addresses whether different people and population groups, such as those differentiated by age, (dis)ability, income, digital literacy, or area of residence, are able to access and benefit from the accessibility improvements a mobility type offers. It asks whether a mobility solution is usable by and available to these people, rather than only serving the population that already has high levels of accessibility.
            Secondly, this sub-factor can also be looked at from an equity perspective. By considering if people are only partially served or underserved and considering if this proposition narrows or widens the existing accessibility gap for them relative to the general population. 
            """,
        "Social safety": """Social safety in mobility refers to the perception and reality of feeling secure while moving through public spaces, using roads, or accessing transportation. It encompasses freedom from harassment, violence, and accidents, as well as the confidence that infrastructure, policies, and community norms protect all users, especially vulnerable groups like women, children, or the elderly. Well-designed lighting, clear pathways, and visible law enforcement contribute to this sense of safety. When social safety is strong, people are more likely to choose active or shared mobility options, fostering inclusive and sustainable urban environments.
            Possible breakdowns: gender, age
            """,
        },
    "Traveler Travel time & Efficiency": {
        "Reliability/Punctuality": "Punctuality and reliability refer to the deviation between a service's actual and targeted delivery or arrival time. Reliable, punctual services are reflected in on-time performance and reduced waiting times. The promise to an individual to reach for instance work in time can greatly increase  the attractiveness of a mobility system. ",
        "Connectivity and frequency of service": """Connectivity and frequency describe how well-linked a mobility service is and how often it runs, which together determine the flexibility users experience in planning their trips/activities. Higher frequency and better connections reduce waiting and transfer times, shortening overall trip duration and improving convenience. This sub-factor also relates to accessibility, as better connectivity increases the range of destinations that can realistically be reached within a given time.""",
        "Travel speed": """Although travel speed is connected to punctuality and connectivity and highly situation specific, overall, the transportation infrastructure or travel mode can greatly influence the speed of travel, especially on longer trips, travel speed is an important determinant. And therefore, should be considered as an important factor while analyzing the mobility proposition. """
        },
    
    "Convenience and Satisfaction": {
        "Comfort": """Comfort in this context is seen as a broad experience term. Mode-specific amenities can offer physical as well as mental comfort. Factors that influence the comfort experience may include the number of passengers in a vehicle, how time can be used during a trip (e.g. performing non-driving-related activities), ride quality, seating availability, cleanliness and many more. """,
        "Ease of use": """Ease of use in comparison to accessibility goes beyond merely making a trip available and possible, it can be looked at as the experience component of accessibility, and just as comfort greatly influencing satisfaction levels. Aspects influencing the experienced ease of use could include the number of transfers (influencing stress levels) or possibilities for traveling with luggage. Another component of ease of use is the service quality. """
        },
    
    "Living Environment": {
        "Quality of environment": """Quality of environment examines the effect of mobility proposition on how available land is used or freed up, including impacts on infrastructure development. It reflects how land area is allocated across purposes significant to society's activities and functions, capturing the socio-economic and functional character of an area, such as residential, industrial, commercial, agricultural, forestry, and recreational uses. Examples that impact the overall environmental quality include the amount of green space or housing density. """,
        "Public health": """Public health is a combination factor, representing public health in a certain area, it integrates the health outcomes of other impact areas such as traffic safety, behavioral factors, health impacts of air quality, or accessibility to health services. """, 
        "Community cohesion":"""This sub-impact factor discusses the impact of the mobility proposition on formation of social bonds and collective identity within a community. It is related to civic participation, trust, equity, accessibility, and the feeling of safety and security in a neighborhood. """
        },
    
    "Economic Activity & Employment": {
        "Business proposition": """Business proposition addresses the viability of the business models underlying the mobility proposition, in terms of their ability to create value, their technological feasibility, and the validity, coherence, and completeness of the underlying business rules and agreements. Beyond viability in isolation, this sub-factor also considers how well a business model fits within the broader mobility system, including its compatibility and interaction with other mobility services, infrastructure, and stakeholders.""",
        "Workforce": """Workforce addresses the employment implications of the mobility proposition, capturing how it affects both the quantity and nature of jobs available. This includes tracking employment dynamics such as job creation, loss, retention, and transformation because of system adoption. It also considers how the proposition shifts the skills the labour market demands, including changes in the required skill profiles and the emergence or decline of specific professional roles."""
        },
    
    "Societal Costs": {
        "Tax income": """Tax income considers the effect of the mobility proposition on public revenue, for example through changes in fuel and vehicle taxation, road pricing, or other mobility-related levies generally necessary to maintain and improve mobility infrastructure. """,
        "Mobility costs": """Mobility costs address the financial resources required to provide and maintain the mobility proposition. This includes infrastructure investments, such as building new infrastructure or maintaining existing infrastructure, as well as operational costs, defined as the costs of operating a service on an ongoing basis.""", 
        "Environmental costs": """Environmental costs include energy use, but also air pollution/emissions. Energy use covers the amount and type of energy required to operate the mobility proposition, including the resources needed to power vehicles and supporting infrastructure. For emissions caused by the mobility proposition the impact focuses on the environmental impact and the impact it has on sustainability, as the health perspective is already represented under the ‘Health’ impact factor. """
        },
    }

CHART_TITLE = "Impact Outcome"
MIN_VAL = -2.0
MAX_VAL = 2.0
DEFAULT_SUBCATEGORY_NAME = "General"
DEFAULT_WEIGHT = 5.0

COLOR_LIGHT_BLUE = "#a6cee3"
COLOR_DARK_BLUE = "#1f78b4"
COLOR_LIGHT_GREEN = "#b2df8a"
COLOR_DARK_GREEN = "#33a02c"

OUTCOME_COLORS = ["#E69F00", "#D55E00", "#CC79A7", "#F0E442", "#000000"]

# ---------------------------------------------------------------------------
# Session state setup
# ---------------------------------------------------------------------------
if "categories" not in st.session_state:
    st.session_state.categories = DEFAULT_CATEGORIES.copy()

if "subcategories" not in st.session_state:
    st.session_state.subcategories = {cat: DEFAULT_SUBCATEGORIES[cat].copy() for cat in st.session_state.categories}

if "category_descriptions" not in st.session_state:
    st.session_state.category_descriptions = DEFAULT_CATEGORY_DESCRIPTIONS.copy()

if "subcategory_descriptions" not in st.session_state:
    st.session_state.subcategory_descriptions = {
        cat: DEFAULT_SUBCATEGORY_DESCRIPTIONS.get(cat, {}).copy()
        for cat in st.session_state.categories
    }

if "weights" not in st.session_state:
    st.session_state.weights = {
        cat: {DEFAULT_SUBCATEGORY_NAME: DEFAULT_WEIGHT} for cat in st.session_state.categories
    }

if "outcomes" not in st.session_state:
    st.session_state.outcomes = {
        "Outcome 1": {
            cat: {sub: 0.0 for sub in st.session_state.subcategories[cat]}
            for cat in st.session_state.categories
        }
    }

if "current_outcome" not in st.session_state:
    st.session_state.current_outcome = "Outcome 1"

if "open_category" not in st.session_state:
    st.session_state.open_category = None

def sync_structure():
    """Keep subcategories / weights / outcomes consistent with each other.

    Call this after any structural change: adding/removing a sub-category,
    adding/removing/renaming an outcome, or loading a JSON file.
    """
    # Make sure every category has at least one sub-category
    for cat in st.session_state.categories:
        if cat not in st.session_state.subcategories or not st.session_state.subcategories[cat]:
            st.session_state.subcategories[cat] = [DEFAULT_SUBCATEGORY_NAME]

    # Drop subcategory data for categories that no longer exist
    st.session_state.subcategories = {
        cat: subs for cat, subs in st.session_state.subcategories.items()
        if cat in st.session_state.categories
    }

    # Make sure every sub-category has a weight, and drop stale weight entries
    for cat in st.session_state.categories:
        st.session_state.weights.setdefault(cat, {})
        for sub in st.session_state.subcategories[cat]:
            st.session_state.weights[cat].setdefault(sub, DEFAULT_WEIGHT)
        st.session_state.weights[cat] = {
            s: w for s, w in st.session_state.weights[cat].items()
            if s in st.session_state.subcategories[cat]
        }
    st.session_state.weights = {
        cat: w for cat, w in st.session_state.weights.items() if cat in st.session_state.categories
    }

    # Make sure every outcome has a score for every (category, sub-category)
    for outcome in st.session_state.outcomes:
        for cat in st.session_state.categories:
            st.session_state.outcomes[outcome].setdefault(cat, {})
            for sub in st.session_state.subcategories[cat]:
                st.session_state.outcomes[outcome][cat].setdefault(sub, 0.0)
            st.session_state.outcomes[outcome][cat] = {
                s: v for s, v in st.session_state.outcomes[outcome][cat].items()
                if s in st.session_state.subcategories[cat]
            }
        st.session_state.outcomes[outcome] = {
            cat: subs for cat, subs in st.session_state.outcomes[outcome].items()
            if cat in st.session_state.categories
        }

def compute_category_score(outcome: str, cat: str) -> float:
    """Weighted average of sub-category scores, normalized so the result
    stays within [MIN_VAL, MAX_VAL] automatically (a weighted average of
    values in a range can never leave that range, given non-negative
    weights)."""
    subs = st.session_state.subcategories[cat]
    scores = st.session_state.outcomes[outcome][cat]
    weights = st.session_state.weights[cat]

    total_weight = sum(max(weights.get(s, DEFAULT_WEIGHT), 0.0) for s in subs)
    if total_weight <= 0:
        # No positive weight anywhere -> fall back to a plain average
        # rather than dividing by zero.
        return sum(scores.get(s, 0.0) for s in subs) / len(subs) if subs else 0.0

    weighted_sum = sum(scores.get(s, 0.0) * max(weights.get(s, DEFAULT_WEIGHT), 0.0) for s in subs)
    return weighted_sum / total_weight

def hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

def form_categories() -> list:
    """Categories in form order; anything not listed is appended at the end."""
    cats = st.session_state.categories
    ordered = [c for c in FORM_CATEGORY_ORDER if c in cats]
    ordered += [c for c in cats if c not in ordered]
    return ordered

sync_structure()

# ---------------------------------------------------------------------------
# Sidebar: manage outcomes
# ---------------------------------------------------------------------------
st.sidebar.header("Manage Outcomes")

if st.sidebar.button("Add Outcome"):
    new_outcome_name = f"Outcome {len(st.session_state.outcomes) + 1}"
    st.session_state.outcomes[new_outcome_name] = {
        cat: {sub: 0.0 for sub in st.session_state.subcategories[cat]}
        for cat in st.session_state.categories
    }
    st.session_state.current_outcome = new_outcome_name
    st.sidebar.success(f"Added {new_outcome_name}")

outcome_to_rename = st.sidebar.selectbox(
    "Select Outcome to Rename",
    options=list(st.session_state.outcomes.keys())
)
new_outcome_name = st.sidebar.text_input("New Name", value=outcome_to_rename)
if st.sidebar.button("Rename"):
    if new_outcome_name and new_outcome_name != outcome_to_rename:
        if new_outcome_name not in st.session_state.outcomes:
            st.session_state.outcomes[new_outcome_name] = st.session_state.outcomes.pop(outcome_to_rename)
            st.session_state.current_outcome = new_outcome_name
            st.sidebar.success(f"Renamed to {new_outcome_name}")
        else:
            st.sidebar.error("An outcome with this name already exists.")
    else:
        st.sidebar.error("Please enter a valid new name.")

st.session_state.current_outcome = st.sidebar.selectbox(
    "Edit Outcome",
    options=list(st.session_state.outcomes.keys())
)

if len(st.session_state.outcomes) > 1:
    outcome_to_remove = st.sidebar.selectbox(
        "Remove Outcome",
        options=list(st.session_state.outcomes.keys())
    )
    if st.sidebar.button("Remove"):
        del st.session_state.outcomes[outcome_to_remove]
        st.session_state.current_outcome = list(st.session_state.outcomes.keys())[0]
        st.sidebar.success(f"Removed {outcome_to_remove}")

# ---------------------------------------------------------------------------
# Sidebar: save / load
# ---------------------------------------------------------------------------
st.sidebar.header("Save / Load")

export_data = {
    "title": str(CHART_TITLE),
    "min_val": float(MIN_VAL),
    "max_val": float(MAX_VAL),
    "categories": [str(c) for c in st.session_state.categories],
    "subcategories": {
        cat: [str(s) for s in subs] for cat, subs in st.session_state.subcategories.items()
    },
    "weights": {
        cat: {sub: float(w) for sub, w in subs.items()}
        for cat, subs in st.session_state.weights.items()
    },
    "outcomes": {
        outcome: {
            cat: {sub: float(score) for sub, score in subs.items()}
            for cat, subs in st.session_state.outcomes[outcome].items()
        }
        for outcome in st.session_state.outcomes
    }
}
outcome_json = json.dumps(export_data, indent=2, default=str)
st.sidebar.download_button(
    "Download outcomes as JSON",
    data=outcome_json,
    file_name="outcomes.json"
)

uploaded = st.sidebar.file_uploader("Load outcomes from JSON", type=["json"])
if uploaded is not None:
    try:
        loaded = json.load(uploaded)
        st.session_state.categories = loaded.get("categories", st.session_state.categories)
        st.session_state.subcategories = loaded.get("subcategories", st.session_state.subcategories)
        st.session_state.weights = loaded.get("weights", st.session_state.weights)
        st.session_state.outcomes = loaded.get("outcomes", st.session_state.outcomes)
        sync_structure()
        st.sidebar.success("Outcomes loaded.")
    except Exception as e:
        st.sidebar.error(f"Could not load file: {e}")

# ---------------------------------------------------------------------------
# Main area: fill out sub-category scores + weights, and see the radar chart
# ---------------------------------------------------------------------------
st.title("Fast Automated and Smart mobility impact Tool (FAST)")

left, right = st.columns([1, 1.4])

with left:
    st.subheader("Fill out impact factor scores")
    st.caption(
        "Score each impact factors from "
        f"{MIN_VAL:+.0f} (strongly negative impact) to {MAX_VAL:+.0f} (strongly positive impact). "
        "Where an impact factor has multiple sub-factors, adjust the weight sliders to reflect "
        "their relative importance to the overall category score."
    )
    if not st.session_state.categories:
        st.info("Add at least one category to get started.")
    else:
        for cat in form_categories():
            subs = st.session_state.subcategories[cat]
            has_multiple_subs = len(subs) > 1
            computed = compute_category_score(st.session_state.current_outcome, cat)

            with st.expander(
                f"**{cat}**  ·  category score: `{computed:+.2f}`",
                expanded=False,
                key=f"expander_{cat}",
            ):
                if cat_desc:
                    st.caption(cat_desc)

                for sub in subs:
                    sub_desc = st.session_state.subcategory_descriptions.get(cat, {}).get(sub, "") or None

                    if has_multiple_subs:
                        col_score, col_weight = st.columns([2.5, 1.5])
                    else:
                        col_score = st.container()
                        col_weight = None

                    with col_score:
                        current_score = st.session_state.outcomes[st.session_state.current_outcome][cat].get(sub, 0.0)
                        new_score = st.slider(
                            sub,
                            min_value=float(MIN_VAL),
                            max_value=float(MAX_VAL),
                            value=float(current_score),
                            step=1.0,
                            help=sub_desc,
                            key=f"slider_{cat}_{sub}_{st.session_state.current_outcome}",
                            on_change=set_open_category,
                            args=(cat,),
                        )
                        st.session_state.outcomes[st.session_state.current_outcome][cat][sub] = new_score

                    if has_multiple_subs:
                        with col_weight:
                            current_weight = st.session_state.weights[cat].get(sub, DEFAULT_WEIGHT)
                            new_weight = st.slider(
                                "Weight",
                                min_value=1,
                                max_value=10,
                                value=int(current_weight),
                                step=1,
                                key=f"weight_{cat}_{sub}",
                                on_change=set_open_category,
                                args=(cat,),
                            )
                            st.session_state.weights[cat][sub] = new_weight

                            total_weight_in_cat = sum(st.session_state.weights[cat].values())
                            pct_share = (new_weight / total_weight_in_cat * 100) if total_weight_in_cat > 0 else 0
                            st.caption(f"{pct_share:.0f}% of this category's weight")

                            low_label, high_label = st.columns([1, 1])
                            with low_label:
                                st.caption("Low")
                            with high_label:
                                st.markdown("<div style='text-align: right;'><span style='font-size: 0.8em; color: gray;'>High</span></div>", unsafe_allow_html=True)
            st.divider()

with right:
    st.subheader(CHART_TITLE)
    categories = st.session_state.categories
    if categories:
        fig = go.Figure()

        blue_categories = [
            "Safety",
            "Living Environment",
            "Societal Costs",
            "Economic Activity & Employment",
            "Infra Efficiency/Flow",
        ]

        for cat in categories:
            color = COLOR_DARK_BLUE if cat in blue_categories else COLOR_DARK_GREEN
            fig.add_trace(go.Scatterpolar(
                r=[MIN_VAL, MAX_VAL],
                theta=[cat, cat],
                mode="lines",
                line=dict(color=color, width=1.5),
                showlegend=False,
                hoverinfo="skip",
            ))

        # Updated outcome plotting loop
        for i, outcome_name in enumerate(st.session_state.outcomes):
            plot_categories = categories + [categories[0]]
            plot_values = [compute_category_score(outcome_name, c) for c in categories]
            plot_values = plot_values + [plot_values[0]]
            color = OUTCOME_COLORS[i % len(OUTCOME_COLORS)]

            fig.add_trace(go.Scatterpolar(
                r=plot_values,
                theta=plot_categories,
                fill="toself",
                name=outcome_name,
                line=dict(color=color, width=2.5),
                fillcolor=hex_to_rgba(color, 0.3),
            ))

        colored_ticktext = [
            f'<span style="color:{COLOR_DARK_BLUE}">{cat}</span>' if cat in blue_categories
            else f'<span style="color:{COLOR_DARK_GREEN}">{cat}</span>'
            for cat in categories
        ]

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[MIN_VAL, MAX_VAL],
                    dtick=1,
                ),
                angularaxis=dict(
                    showgrid=False,
                    tickmode="array",
                    tickvals=categories,
                    ticktext=colored_ticktext,
                    tickfont=dict(size=11),
                ),
            ),
            showlegend=True,
            margin=dict(l=100, r=100, t=80, b=80),
            height=650,
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No categories to plot yet.")
