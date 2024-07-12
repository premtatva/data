import streamlit as st
import pandas as pd

st.header("Fitness Tracker🏋🏽🔥💪🏼🏃")

# Initialize session state lists if they don't already exist
if "daylist" not in st.session_state:
    st.session_state.daylist = []
if "datelist" not in st.session_state:
    st.session_state.datelist = []
if "distancelist" not in st.session_state:
    st.session_state.distancelist = []
if "timelist" not in st.session_state:
    st.session_state.timelist = []
if "calorielist" not in st.session_state:
    st.session_state.calorielist = []
if "previous_activity" not in st.session_state:
    st.session_state.previous_activity = ""

# Select Fitness Activity
act_sel = st.selectbox("Select Fitness Activity:", ["Running", "Walking", "Cycling"])

# Reset user inputs if activity changes
if st.session_state.previous_activity != act_sel:
    st.session_state['daylist'] = []
    st.session_state['datelist'] = []
    st.session_state['distancelist'] = []
    st.session_state['timelist'] = []
    st.session_state['calorielist'] = []
    st.session_state.previous_activity = act_sel

# Update session state keys based on activity selection
if act_sel == "Running":
    day_count = st.number_input("Number of Days:", min_value=0, step=1, key='running_day_count')
    date = st.date_input("Date", key='running_date')
    distance = st.number_input("Total Distance in kilometers:", min_value=0.0, step=0.1, key='running_distance')
    time_input = st.text_input("Enter the time taken for the activity (In Minutes):", key='running_time_input')
    weight = st.slider("Enter Your Weight (kg):", min_value=0.0, max_value=200.0, step=0.1, key='running_weight')

if act_sel == "Cycling":
    day_count = st.number_input("Number of Days:", min_value=0, step=1, key='cycling_day_count')
    date = st.date_input("Date", key='cycling_date')
    distance = st.number_input("Total Distance in kilometers:", min_value=0.0, step=0.1, key='cycling_distance')
    time_input = st.text_input("Enter the time taken for the activity (In Minutes):", key='cycling_time_input')
    weight = st.slider("Enter Your Weight (kg):", min_value=0.0, max_value=200.0, step=0.1, key='cycling_weight')
    velocity = st.slider("Enter The Velocity:", min_value=0.0, step=0.1, max_value=100.0, key='cycling_velocity')

if act_sel == "Walking":
    day_count = st.number_input("Number of Days:", min_value=0, step=1, key='walking_day_count')
    date = st.date_input("Date", key='walking_date')
    distance = st.number_input("Total Distance in kilometers:", min_value=0.0, step=0.1, key='walking_distance')
    time_input = st.text_input("Enter the time taken for the activity (In Minutes):", key='walking_time_input')
    weight = st.slider("Enter Your Weight (kg):", min_value=0.0, max_value=200.0, step=0.1, key='walking_weight')

show_button = st.button("Calculate the Calories Burned In The Exercise:")

if show_button:
    try:
        time_float = float(time_input)
        if time_float <= 0:
            st.error("Time taken must be greater than zero.")
        else:
            if act_sel == "Running":
                calories = weight * distance * 1.036
            elif act_sel == "Cycling":
                calories = velocity * 0.0175 * weight * time_float
            elif act_sel == "Walking":
                calories = weight * distance * 1.036
            
            st.subheader(f"Calories Burnt: {calories:.2f}")
            st.session_state.calorielist.append(calories)
    except ValueError:
        st.error("Please enter a valid number for the time taken.")

add_button = st.button("Click Here to Add the Activity In Database")

if add_button:
    try:
        time_float = float(time_input)
        if time_float <= 0:
            st.error("Time taken must be greater than zero.")
        else:
            # Add entries to the session state lists
            st.session_state.daylist.append(day_count)
            st.session_state.datelist.append(date)
            st.session_state.distancelist.append(distance)
            st.session_state.timelist.append(time_input)

            # Check if calories have been calculated
            if len(st.session_state.calorielist) > len(st.session_state.daylist) - 1:
                calories = st.session_state.calorielist[-1]
            else:
                # If calories were not calculated, append None
                if act_sel == "Running" or act_sel == "Walking":
                    calories = weight * distance * 1.036 if distance and weight else None
                elif act_sel == "Cycling":
                    calories = velocity * 0.0175 * weight * time_float if velocity and weight else None
                st.session_state.calorielist.append(calories)

            # Prepare the data to be displayed in the DataFrame
            data = {
                "Number of Days": st.session_state.daylist,
                "Date": st.session_state.datelist,
                "Distance (km)": st.session_state.distancelist,
                "Time Taken (min)": st.session_state.timelist,
                "Calories Burnt": st.session_state.calorielist
            }
            df = pd.DataFrame(data)
            df["Time Taken (min)"] = pd.to_numeric(df["Time Taken (min)"], errors='coerce')
            st.write(df)
            st.subheader("Number Of Calories Burnt Per Day")
            chart_data = pd.DataFrame(df["Calories Burnt"])
            st.line_chart(chart_data.set_index(df["Date"]))
            st.subheader("Time Spent In The Activity Per Day")
            chart2_data = pd.DataFrame(df["Time Taken (min)"])
            st.line_chart(chart2_data.set_index(df["Date"]), color="#FF0000")
            st.subheader("Distance Covered In The Activity Per day")
            chart3_data = pd.DataFrame(df["Distance (km)"])
            st.line_chart(chart3_data.set_index(df["Date"]), color="#00FF00")
            st.subheader("Highlights")
            max_calorie_index = df['Calories Burnt'].idxmax()
            max_calorie_burnt = df.loc[max_calorie_index, 'Calories Burnt']
            max_calorie_date = df.loc[max_calorie_index, 'Date']
            st.write(f"Maximum calories burnt (Your Best): {max_calorie_burnt} on {max_calorie_date}")
            avg_calorie_burnt = df['Calories Burnt'].mean()
            st.write(f"Average calorie burnt: {avg_calorie_burnt}")
            avg_time=df["Time Taken (min)"].mean()
            st.write(f"Average Time Spent:{avg_time}")
            avg_distance=df["Distance (km)"].mean()
            st.write(f"Average Distance:{avg_distance}")

    except ValueError:
        st.error("Please enter a valid number for the time taken.")
