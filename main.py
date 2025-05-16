import requests
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="My APOD",
    page_icon="🌌",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
         p {font-size:20px;}
         background-image: url("https://img.freepik.com/free-vector/bring-night-space-wallpaper-with-glowing-starfield_1017-53512.jpg?semt=ais_hybrid&w=740");
         background-size: 100vw 100vh;  
         background-position: center;
         background-repeat: no-repeat;
         background-size:cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)


API_KEY = st.secrets["api_key"]["my_api"]


with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home","NASA APOD","About"],
        icons=["house" ,"globe", "info"],
        menu_icon="cast",
        default_index=0,
    )

with st.sidebar:
    st.subheader("Github Repository")
    st.code("https://github.com/pariya-tavangar/My-APOD")

match selected:
    case "Home":
        st.title("Hello There!!")
        st.caption(" (definitely a starwars reference)")

        st.write("This mini tiny project shows how to use NASA APOD API and provide easy fast output using streamlit.")
        st.write("---")
        st.header("How to use it?")
        st.write("First, install required imported libraries")
        st.write("To test it out, sign in https://api.nasa.gov/ and get your API key for free")
        st.write("Replace the API_KEY with yours in secrects.toml and run it with the command below")
        st.code('streamlit run <file.py>')
        st.write("---")
        st.header("Customizations")
        st.write("You can either use default streamlit panel settings or use config.toml ")

        st.write("Checkout https://apod.nasa.gov/apod/archivepix.html to access the official archive")


    case "NASA APOD":
        today = datetime.now()
        st.header("NASA Astronomy Picture of the Day")

        selected_time = st.date_input("Select a time",value=datetime.today())
        mydate = selected_time

        if (selected_time == today):
            url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={today}"
            current_date= today
        elif(selected_time == mydate):
            url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={mydate}"
            current_date=mydate
        else:
            st.error(" Unable to load the media ❌")


        try:

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                Dates = data.get("date", "N/A")
                Titles = data.get("title", "N/A")
                Explanation = data.get("explanation", "N/A")
                myIMg = data.get("url", "N/A")
                highres = data.get("hdurl", "N/A") 
                copyrights = data.get("copyright", "N/A")    

                st.title(Titles)
                st.write("📅",current_date)
                st.write(Explanation)
                

                
                if myIMg.endswith('.jpg') or myIMg.endswith('.jpeg') or myIMg.endswith('.png'):
                    st.image(myIMg)
                    st.badge("High Resolution Image")
                    st.write("🔗", highres)

                    if copyrights != "N/A":
                        st.badge("Copyrights")
                        st.write("📷", copyrights)
                else:
                    st.video(myIMg)

                st.write("  ")

            elif response.status_code == 403:
                st.error("No api_key found 🔑")
                st.toast(response)
            
            else:
                st.error("You entered the following date 🕤")
                st.toast(response)

        except requests.exceptions.ConnectionError:
            st.error("No Internet Connection ❌")

    case "About":
        st.write("For further information about the api, visit https://apod.nasa.gov/apod/lib/about_apod.html")


st.markdown("---")
st.caption("Data provided by NASA APOD API")