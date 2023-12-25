import streamlit as st 
import pandas as pd
import numpy as np
import os
import pickle
import warnings
from openai import OpenAI
client = OpenAI()
import requests




warnings.filterwarnings("ignore", message="Trying to unpickle estimator")

st.set_page_config(page_title="Agro Analytica", page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@master/assets/72x72/1f33f.png", layout='centered', initial_sidebar_state="collapsed")
# Function to interact with the ChatGPT API
def get_chat_response(prompt, model="gpt-3.5-turbo"):
    api_endpoint = "https://chatgpt-api.shn.hk/v1/"
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(api_endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('choices', [])[0].get('message', '')
    else:
        return f"Error: {response.status_code}"
    

def load_model(modelfile):
	loaded_model = pickle.load(open(modelfile, 'rb'))
	return loaded_model

def main():
    # title
    html_temp = """
    <div>
    <h1 style="color:MEDIUMSEAGREEN;text-align:center;"> Agro Analytica: Intelligent Crop Recommendation 🌱 </h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    col = st.columns(1)[0]

    with col:
        st.subheader(" Find out the most suitable crop to grow in your farm 👨‍🌾")
        N = st.number_input("Nitrogen", 1,10000)
        P = st.number_input("Phosporus", 1,10000)
        K = st.number_input("Potassium", 1,10000)
        temp = st.number_input("Temperature",0.0,100000.0)
        humidity = st.number_input("Humidity in %", 0.0,100000.0)
        ph = st.number_input("Ph", 0.0,100000.0)
        rainfall = st.number_input("Rainfall in mm",0.0,100000.0)

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1,-1)
        # Assuming you have the custom-made test data stored in a DataFrame named 'custom_test_data'
        # Make sure it has the same features as your training data

        # Example custom-made test data (replace this with your actual data)
        custom_test_data = pd.DataFrame({
            'N': [N],
            'P': [P],
            'K': [K],
            'temperature': [temp],
            'humidity': [humidity],
            'ph': [ph],
            'rainfall': [rainfall],
        })

# Note: Replace [value_N], [value_P], etc. with the actual values you want to test


        crop_dict = {
            1: 'rice',
            2: 'maize',
            3: 'jute',
            4: 'cotton',
            5: 'coconut',
            6: 'papaya',
            7: 'orange',
            8: 'apple',
            9: 'muskmelon',
            10: 'watermelon',
            11: 'grapes',
            12: 'mango',
            13: 'banana',
            14: 'pomegranate',
            15: 'lentil',
            16: 'blackgram',
            17: 'mungbean',
            18: 'mothbeans',
            19: 'pigeonpeas',
            20: 'kidneybeans',
            21: 'chickpea',
            22: 'coffee'
        }


       # Sample options for the dropdown
        options = ['Decision TreeModel', 'Random Forest Model']

        # Create a dropdown button
        selected_option = st.selectbox('Select an option:', options)
        sel_model=0
        if selected_option == options[0]:
              sel_model=1
        else:
              sel_model=2
        

        if st.button('Predict'):
            if sel_model==1:      
                loaded_model = load_model('descision_tree_model.pkl')
                prediction = loaded_model.predict(single_pred)
                print(prediction)
            else:
                loaded_model = load_model('random_forest_model.pkl')
                prediction = loaded_model.predict(single_pred)
                print(prediction)
            # Use the swapped dictionary to get the crop name
            recommended_crop = crop_dict.get(prediction[0], 'Unknown Crop')
    
            col.write('''
            ## Results 🔍 
            ''')
    
            col.success(f"{'Recommended ' + recommended_crop if prediction[0] else 'Not recommended'} by the A.I for your farm.")

             # Call ChatGPT API for response
            chat_prompt = f"Explain why {recommended_crop} is best for your land as suggested by {options[sel_model - 1]}"
            chat_response = get_chat_response(chat_prompt)
        
            col.write(f"Ai Response: {chat_response}")
            # completion = client.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {"role": "system", "content": "You are Ai smart crop recommendation system, skilled in explaining why our Ai model is suggesting following crop for your land"},
            #         {"role": "user", "content": "Explan why "+ recommended_crop +" is best for you land as suggested by "+options[sel_model-1]}
            #      ]
            # )

            # print(completion.choices[0].message)
            # col.write(completion.choices[0].message)
            # col.success(f"{'Recommended ' + recommended_crop if prediction[0] else 'Not recommended'} by the A.I for your farm.")




            
    #code for html ☘️ 🌾 🌳 👨‍🌾  🍃
    hide_menu_style = """
    <style>
    .block-container {padding: 2rem 1rem 3rem;}
    #MainMenu {visibility: hidden;}
    </style>
    """

hide_menu_style = """
        <style>
        .block-container {padding: 2rem 1rem 3rem;}
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

if __name__ == '__main__':
	main()