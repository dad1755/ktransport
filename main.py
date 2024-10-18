import streamlit as st
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sample data for destinations and pickup locations
destinations = ["Kuala Lumpur", "Singapore", "Penang", "Malacca", "Johor Bahru", "Langkawi"]
pickup_locations = ["KLIA", "Changi Airport", "Kuala Lumpur City Center", "Chinatown", "Penang Airport"]

# Function to send an email
def send_email(name, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes):
    sender_email = st.secrets["email"]  # Get the sender email from secrets
    password = st.secrets["password"]     # Get the password from secrets
    receiver_email = "dad1755@gmail.com"

    # Create the email content
    subject = "New Booking Confirmation"
    body = f"""
    Booking Confirmation Details:

    Name: {name}
    Destination: {destination}
    Pickup Location: {pickup_location}
    Adults: {adults}
    Kids: {kids}
    Infants: {infants}
    Pickup Date: {pickup_date}
    Pickup Time: {pickup_time}
    Luggage Sizes: {luggage}
    Notes: {notes}
    """

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the email server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # For Gmail
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS
            server.login(sender_email, password)
            server.send_message(msg)
        st.success("Booking email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")

# Function to process form submission
def submit_booking(name, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes):
    st.success(f"Booking Confirmed for {name}!")
    st.write(f"**Destination:** {destination}")
    st.write(f"**Pickup Location:** {pickup_location}")
    st.write(f"**Adults:** {adults}")
    st.write(f"**Kids:** {kids}")
    st.write(f"**Infants:** {infants}")
    st.write(f"**Pickup Date:** {pickup_date}")
    st.write(f"**Pickup Time:** {pickup_time}")
    st.write(f"**Luggage Sizes:** {luggage}")
    st.write(f"**Notes:** {notes}")

    # Send email
    send_email(name, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes)

# Title of the app
st.title("KL Transport Booking Form")

# Welcome message
st.markdown("<h4>Welcome! Please fill out the booking form below to schedule your ride.</h4>", unsafe_allow_html=True)

# Container 1: Name, Destination, Pickup Location
with st.container():
    st.subheader("Booking Details")
    name = st.text_input("Full Name")
    destination = st.text_input("Destination", placeholder="Enter your destination")
    st.write(f"**Your Destination:** {destination}")
    pickup_location = st.text_input("Pickup Location", placeholder="Enter your pickup location")
    st.write(f"**Selected Pickup Location:** {pickup_location}")

# Container 2: Date and Pickup Time
with st.container():
    st.subheader("Pickup Information")
    pickup_date = st.date_input("Pickup Date", min_value=date.today())
    st.write(f"**Selected Pickup Date :** {pickup_date}")

    # Create hour and minute options for AM/PM
    hours = list(range(1, 13))  # 1 to 12
    minutes = list(range(0, 60, 5))  # Every 5 minutes
    am_pm = ["AM", "PM"]  # AM and PM options

    # Create columns for a side-by-side layout
    col1, col2, col3 = st.columns(3)

    with col1:
        hour = st.selectbox("Hour", hours)

    with col2:
        minute = st.selectbox("Minute", minutes)

    with col3:
        period = st.selectbox("Period", am_pm)

    # Format the pickup time as a single string
    pickup_time = f"{hour}:{minute:02d} {period}"

    # Display formatted pickup time
    st.write(f"**Selected Pickup Time:** {pickup_time}")

# Container 3: Passengers
with st.container():
    st.subheader("Passenger Details")
    adults = st.number_input("Number of Adults", min_value=0, step=1)
    kids = st.number_input("Number of Kids", min_value=0, step=1)
    infants = st.number_input("Number of Infants", min_value=0, step=1)

# Container 4: Luggage
with st.container():
    st.subheader("Luggage Information")
    luggage_s = st.number_input("Number of Luggage Size S (19-21 inch)", min_value=0, step=1)
    luggage_m = st.number_input("Number of Luggage Size M (23-25 inch)", min_value=0, step=1)
    luggage_l = st.number_input("Number of Luggage Size L (26-28 inch)", min_value=0, step=1)
    luggage_xl = st.number_input("Number of Luggage Size XL (29-32 inch)", min_value=0, step=1)

    luggage = {
        "S": luggage_s,
        "M": luggage_m,
        "L": luggage_l,
        "XL": luggage_xl
    }

# Container 5: Notes
with st.container():
    st.subheader("Additional Notes")
    notes = st.text_area("Any additional notes or requests")

# Submit button outside the containers
submit_button = st.button(label="Submit Booking")

# Handle form submission
if submit_button:
    if not name:
        st.error("Please fill out all required fields.")
    else:
        submit_booking(name, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes)
