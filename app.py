import streamlit as st
import requests
import os
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure 5 Calls API
FIVE_CALLS_API_KEY = os.getenv("FIVE_CALLS_API_KEY")
FIVE_CALLS_API_BASE = "https://api.5calls.org/v1"
FIVE_CALLS_HEADERS = (
    {"X-5Calls-Token": FIVE_CALLS_API_KEY} if FIVE_CALLS_API_KEY else {}
)


def get_representatives_by_zip(zip_code: str) -> Optional[List[Dict]]:
    """Fetch representatives data from 5 Calls API using ZIP code."""
    if not FIVE_CALLS_API_KEY:
        st.warning(
            "5 Calls API key not configured. Please add your API key to the .env file."
        )
        return None

    try:
        url = f"{FIVE_CALLS_API_BASE}/representatives"
        params = {
            "location": zip_code,
            "areas": "US House,US Senate",  # Only get federal legislators
        }

        response = requests.get(url, params=params, headers=FIVE_CALLS_HEADERS)

        if response.status_code == 200:
            data = response.json()
            if data.get("lowAccuracy"):
                st.warning(
                    "Note: ZIP code may map to multiple districts. Showing the closest match."
                )
            return data.get("representatives", [])
        else:
            st.error(f"Error fetching representatives: {response.status_code}")
            if response.content:
                error_data = response.json()
                if error_data.get("error"):
                    st.error(f"API Error: {error_data['error']}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def get_rep_display_name(rep: Dict) -> str:
    """Generate a display name for a representative."""
    title = f"{rep.get('area', '')} - {rep.get('state', '')}"
    if rep.get("district"):
        title += f" District {rep['district']}"
    return f"{rep.get('name', '')} ({rep.get('party', 'N/A')}) - {title}"


def generate_personalized_script(
    name: str, zip_code: str, email: str, selected_issues: List[str], rep: Dict
) -> str:
    """Generate a personalized script for the selected representative."""
    contact_method = "I'm emailing you" if "@" in (email or "") else "I'm calling"

    # Get the appropriate title
    if rep.get("area") == "US Senate":
        title = "Senator"
    else:
        title = "Representative"

    script = f"""
Dear {title} {rep.get('name', '')},

Hi, my name is {name or '[NAME]'} and {contact_method} from {zip_code or '[ZIP CODE]'}. I'm {contact_method.lower()} to ask for your support on the following issues:

{chr(10).join(selected_issues)}

As my {title.lower()} in Congress, I urge you to take action on these critical matters.

Thank you for your time and consideration.
"""

    if email:
        script += f"\n\nI would kindly appreciate a response at {email}."

    return script.strip()


st.title("📞 Contact Congress for Gaza and Justice")

# Collect user info
name = st.text_input("Your Name")
zip_code = st.text_input("ZIP Code")
email = st.text_input("Email or Phone (optional)")

# Issue checkboxes
st.subheader("📢 What do you want to say?")
issues = {
    "ceasefire": st.checkbox("Call for immediate ceasefire in Gaza"),
    "ethnic_cleansing": st.checkbox("Condemn Trump's ethnic cleansing proposal"),
    "humanitarian_aid": st.checkbox("Demand humanitarian aid access to Gaza"),
    "military_aid": st.checkbox("Stop military aid to Israel"),
}

if zip_code:
    reps = get_representatives_by_zip(zip_code)
    if reps:
        st.subheader("📍 Your Representatives")
        # Store representatives in session state
        st.session_state.representatives = reps

        # Create a selection box for representatives
        rep_options = [get_rep_display_name(rep) for rep in reps]
        selected_rep_index = st.selectbox(
            "Select a representative to contact:",
            range(len(rep_options)),
            format_func=lambda x: rep_options[x],
            key="selected_rep_index",  # Add this key to track the selection in session state
        )

        # Display detailed info for the selected representative
        selected_rep = reps[selected_rep_index]
        with st.expander("Representative Details", expanded=True):
            if selected_rep.get("reason"):
                st.write(f"ℹ️ {selected_rep['reason']}")
            if selected_rep.get("phone"):
                st.write(f"📞 DC Office: {selected_rep['phone']}")
            if selected_rep.get("field_offices"):
                st.write("🏢 Local Offices:")
                for office in selected_rep["field_offices"]:
                    st.write(
                        f"   • {office.get('city', '')}: {office.get('phone', '')}"
                    )
            if selected_rep.get("url"):
                st.write(f"🌐 [Official Website]({selected_rep['url']})")

if st.button("Generate My Script"):
    st.markdown("---")
    st.subheader("📜 Your Message Script")

    if not zip_code:
        st.error("Please enter your ZIP code first.")
    elif not hasattr(st.session_state, "representatives"):
        st.error("Please wait for representatives to load.")
    else:
        selected_issues = []
        if issues["ceasefire"]:
            selected_issues.append("1. Implementing and upholding a ceasefire in Gaza.")
        if issues["ethnic_cleansing"]:
            selected_issues.append(
                "2. Condemning Trump's proposal to ethnically cleanse the Palestinian Territories."
            )
        if issues["humanitarian_aid"]:
            selected_issues.append(
                "3. Allowing unrestricted humanitarian aid into Gaza."
            )
        if issues["military_aid"]:
            selected_issues.append(
                "4. Ending the use of U.S. tax dollars for military aid to Israel."
            )

        if not selected_issues:
            st.warning("Please select at least one issue to discuss.")
        else:
            # Use the selected_rep_index directly from session state
            selected_rep = st.session_state.representatives[
                st.session_state.selected_rep_index
            ]
            script = generate_personalized_script(
                name, zip_code, email, selected_issues, selected_rep
            )
            st.text_area("Personalized Script", value=script, height=300)

            # Contact information reminder
            st.info(
                f"""
            📞 To contact {selected_rep.get('name')}:
            - DC Office: {selected_rep.get('phone', 'N/A')}
            - Website: {selected_rep.get('url', 'N/A')}
            """
            )

    # Backup links
    st.markdown("---")
    st.markdown(
        """
    ### Additional Resources
    If you need to double-check your representatives' information:
    - 📍 [Official House Directory](https://www.house.gov/representatives/find-your-representative)
    - 🏛️ [Senate Directory](https://www.senate.gov/senators/senators-contact.htm)
    - 📱 [Common Cause - Contact Congress](https://www.commoncause.org/find-your-representative/)
    """
    )
