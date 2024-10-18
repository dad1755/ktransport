import streamlit as st
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote  # For URL encoding the message

# Sample data for destinations and pickup locations
destinations = ["Kuala Lumpur", "Singapore", "Penang", "Malacca", "Johor Bahru", "Langkawi"]
pickup_locations = ["KLIA", "Changi Airport", "Kuala Lumpur City Center", "Chinatown", "Penang Airport"]

# Set page configuration
st.set_page_config(page_title="KLTransport", page_icon="💬", layout="centered")

def send_email(name, phone, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes):
    sender_email = st.secrets["email"]  # Get the sender email from secrets
    password = st.secrets["password"]     # Get the password from secrets
    receiver_email = st.secrets["receiver"]

    # Create the WhatsApp link
    whatsapp_link = f"https://wa.me/{phone.replace(' ', '')}"  # Remove any spaces from the phone number

    # Create the email content with HTML format
    subject = "New Booking Confirmation"
    body = f"""
    <html>
    <body>
        <h2>Booking Confirmation Details:</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> <a href="{whatsapp_link}">{phone}</a></p>
        <p><strong>Destination:</strong> {destination}</p>
        <p><strong>Pickup Location:</strong> {pickup_location}</p>
        <p><strong>Adults:</strong> {adults}</p>
        <p><strong>Kids:</strong> {kids}</p>
        <p><strong>Infants:</strong> {infants}</p>
        <p><strong>Pickup Date:</strong> {pickup_date}</p>
        <p><strong>Pickup Time:</strong> {pickup_time}</p>
        <p><strong>Luggage Sizes:</strong> {luggage}</p>
        <p><strong>Notes:</strong> {notes}</p>
    </body>
    </html>
    """

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Send as HTML format

    try:
        # Connect to the email server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # For Gmail
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS
            server.login(sender_email, password)
            server.send_message(msg)
        return True  # Successful email sending
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False  # Email sending failed

def send_whatsapp_message(phone, message):
    # Get the phone number and API key from secrets
    recipient_number = st.secrets["whatsapp_number"]  # Phone number with country code
    api_key = st.secrets["api_key"]  # Your CallMeBot API key

    # URL encode the message
    encoded_message = quote(message)

    # Construct the API URL
    api_url = f"https://api.callmebot.com/whatsapp.php?phone={recipient_number}&text={encoded_message}&apikey={api_key}"

    try:
        # Sending the WhatsApp message via the API (this can be a GET request in practice)
        response = st.experimental_get_request(api_url)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to send WhatsApp message: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error sending WhatsApp message: {str(e)}")
        return False

# Function to process form submission
def submit_booking(name, phone, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes):
    # Display confirmation message
    st.success(f"Booking Confirmed for {name}!")
    
    # Send email
    if send_email(name, phone, destination, pickup_location, adults, kids, infants, pickup_date, pickup_time, luggage, notes):
        # Clear form fields if email sent successfully
        st.session_state.name = ""
        st.session_state.phone = ""
        st.session_state.destination = ""
        st.session_state.pickup_location = ""
        st.session_state.adults = 0
        st.session_state.kids = 0
        st.session_state.infants = 0
        st.session_state.luggage_s = 0
        st.session_state.luggage_m = 0
        st.session_state.luggage_l = 0
        st.session_state.luggage_xl = 0
        st.session_state.notes = ""

        # Prepare the message to send via WhatsApp
        whatsapp_message = f"New Booking: {name}, Phone: {phone}, Destination: {destination}, Pickup Location: {pickup_location}, Adults: {adults}, Kids: {kids}, Infants: {infants}, Pickup Date: {pickup_date}, Pickup Time: {pickup_time}, Luggage: {luggage}, Notes: {notes}"

        # Send WhatsApp message
        send_whatsapp_message(phone, whatsapp_message)

# Title of the app
st.title("KL Transport Booking Form")

# Initialize session state for form fields if not already done
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'phone' not in st.session_state:
    st.session_state.phone = ""
if 'destination' not in st.session_state:
    st.session_state.destination = ""
if 'pickup_location' not in st.session_state:
    st.session_state.pickup_location = ""
if 'adults' not in st.session_state:
    st.session_state.adults = 0
if 'kids' not in st.session_state:
    st.session_state.kids = 0
if 'infants' not in st.session_state:
    st.session_state.infants = 0
if 'luggage_s' not in st.session_state:
    st.session_state.luggage_s = 0
if 'luggage_m' not in st.session_state:
    st.session_state.luggage_m = 0
if 'luggage_l' not in st.session_state:
    st.session_state.luggage_l = 0
if 'luggage_xl' not in st.session_state:
    st.session_state.luggage_xl = 0
if 'notes' not in st.session_state:
    st.session_state.notes = ""

# Welcome message
st.markdown("<h4>Welcome! Please fill out the booking form below to schedule your ride.</h4>", unsafe_allow_html=True)

# Container 1: Name, Phone, Destination, Pickup Location
with st.container():
    st.subheader("KL Transport Booking Details")
    st.session_state.name = st.text_input("Full Name", value=st.session_state.name)

    # Create columns for side-by-side layout
    col1, col2 = st.columns([1, 3])  # Adjust the width ratios as needed

    with col1:
        phone_code = st.selectbox("Phone Code", options=["+60", "+65", "+62", "+84", "+66"], index=0)  # Example codes for ASEAN countries

    with col2:
        phone_number = st.text_input("Phone Number", placeholder="Enter your phone number")

    # Combine phone code and number only if the phone number is not empty
    if phone_number.strip():  # Ensure phone number is not empty or whitespace
        st.session_state.phone = f"{phone_code} {phone_number}"
    else:
        st.session_state.phone = ""  # Reset if empty

    st.session_state.destination = st.text_input("Destination", value=st.session_state.destination, placeholder="Enter your destination")
    st.session_state.pickup_location = st.text_input("Pickup Location", value=st.session_state.pickup_location, placeholder="Enter your pickup location")

# Container 2: Date and Pickup Time
with st.container():
    st.subheader("Pickup Information")
    pickup_date = st.date_input("Pickup Date", min_value=date.today())

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

# Container 3: Passengers
with st.container():
    st.subheader("Passenger Details")
    # Adults input remains below the two columns
    st.session_state.adults = st.number_input("Number of Adults", min_value=0, value=st.session_state.adults, step=1)

    # Create two columns for Kids and Infants
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.kids = st.number_input("Number of Kids", min_value=0, value=st.session_state.kids, step=1)

    with col2:
        st.session_state.infants = st.number_input("Number of Infants", min_value=0, value=st.session_state.infants, step=1)

# Container 4: Luggage
with st.container():
    st.subheader("Luggage Information")
    st.session_state.luggage_s = st.number_input("Number of Luggage Size S (19-21 inch)", min_value=0, value=st.session_state.luggage_s, step=1)
    st.session_state.luggage_m = st.number_input("Number of Luggage Size M (23-25 inch)", min_value=0, value=st.session_state.luggage_m, step=1)
    st.session_state.luggage_l = st.number_input("Number of Luggage Size L (26-28 inch)", min_value=0, value=st.session_state.luggage_l, step=1)
    st.session_state.luggage_xl = st.number_input("Number of Luggage Size XL (29-32 inch)", min_value=0, value=st.session_state.luggage_xl, step=1)

    luggage = {
        "S": st.session_state.luggage_s,
        "M": st.session_state.luggage_m,
        "L": st.session_state.luggage_l,
        "XL": st.session_state.luggage_xl
    }

# Container 5: Notes
with st.container():
    st.subheader("Additional Notes")
    st.session_state.notes = st.text_area("Any additional notes or requests", value=st.session_state.notes)

# Submit button outside the containers
submit_button = st.button(label="Submit Booking")

# Handle form submission
if submit_button:
    # Check for empty fields and ensure at least one adult is present
    if not st.session_state.name or not st.session_state.phone.strip():  # Check for empty name and phone
        st.error("Please fill out all required fields.")
    elif st.session_state.adults < 1:  # Check if at least one adult is selected
        st.error("Please specify at least one adult.")
    else:
        # Call submit_booking function with all parameters
        submit_booking(st.session_state.name, st.session_state.phone, st.session_state.destination, st.session_state.pickup_location,
                       st.session_state.adults, st.session_state.kids, st.session_state.infants, pickup_date, pickup_time, luggage, st.session_state.notes)
        # Display a clickable Facebook link after successful submission
        st.markdown("""
            <p>Thank you for your submission! You can follow us on <a href="https://web.facebook.com/profile.php?id=100094313717882" target="_blank">Facebook</a>.</p>
        """, unsafe_allow_html=True)
