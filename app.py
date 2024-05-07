import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_trip_plan(destination, days, preferences):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    # Data to be sent to the API
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Plan a trip to {destination} for {days} days, including: {', '.join(preferences)}."}
                ]
            }
        ]
    }

    response = requests.post(
        api_url,
        headers={"content-type": "application/json"},
        json=data,
        params={"key": os.getenv("GOOGLE_API_KEY")}
    )

    if response.status_code == 200:
        result = response.json()
        return format_trip_plan(result)
    else:
        return f"Failed to retrieve the trip plan. Status code: {response.status_code}. Please try again."

def format_trip_plan(api_response):
    # Extract the first candidate's content
    try:
        trip_details = api_response["candidates"][0]["content"]["parts"][0]["text"]
        formatted_plan = ""
        current_section = ""
        for line in trip_details.split('\n'):
            if "**" in line:
                # This assumes that sections are denoted by '**'
                current_section = line.strip('* ')
                formatted_plan += f"\n{current_section}\n"
            elif line.strip():
                # Regular lines of description
                formatted_plan += f"{line.strip()} "
        return formatted_plan
    except (IndexError, KeyError) as e:
        return "Error parsing the trip plan. Please check the format of the API response."

def main():
    # Using markdown to center the title and add style
    st.markdown("<h1 style='text-align: center;'>✈️ Trip Planner ✈️</h1>", unsafe_allow_html=True)

    # Introduction to the app
    st.write(
        """
        Welcome to the Trip Planner! This tool helps you plan your travels by generating a customized itinerary based on your destination, the number of days you'll stay, and your personal preferences such as museums, shows, nature experiences, shopping, and dining options.
        
        Simply enter your travel details below and click "Generate Trip Plan" to receive a detailed, day-by-day itinerary for your trip. Enjoy your planning!
        """
    )
    
    # User inputs
    destination = st.text_input("Enter your destination:")
    days = st.number_input("Enter the number of days:", min_value=1, max_value=30)
    preferences = st.multiselect("What would you like to include in your trip?", ['Museums🏛', 'Shows💃', 'Nature🌲', 'Shopping👠', 'Restaurants🍔'])
    
    # Button to generate trip plan
    if st.button("Generate Trip Plan"):
        if destination and days and preferences:
            trip_plan = generate_trip_plan(destination, days, preferences)
            st.text_area("Your Trip Plan:", trip_plan, height=300)
        else:
            st.write("Please enter all fields to generate a trip plan.")

if __name__ == "__main__":
    main()
