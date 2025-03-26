import os
import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceChatGPTBot:
    def __init__(self):
        # Configure OpenAI API
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Configure TTS properties
        self.engine.setProperty('rate', 150)  # Speaking rate
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    def recognize_speech(self):
        """Capture audio input from microphone"""
        with sr.Microphone() as source:
            st.info("Listening... Speak now")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source, timeout=5)
            
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.error("Sorry, could not understand audio")
                return None
            except sr.RequestError:
                st.error("Could not request results from speech recognition service")
                return None

    def generate_chatgpt_response(self, user_question):
        """Generate response using ChatGPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful, intelligent voice assistant designed to provide comprehensive and accurate responses."
                    },
                    {
                        "role": "user", 
                        "content": user_question
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def speak_response(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")

def main():
    # Streamlit page configuration
    st.set_page_config(
        page_title="Voice ChatGPT Bot", 
        page_icon="🎙️", 
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App title
    st.title("🎙️ Voice-Enabled ChatGPT Bot")
    st.subheader("Speak, Listen, Interact!")
    
    # Initialize voice bot
    voice_bot = VoiceChatGPTBot()
    
    # Create columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Speech recognition button
        if st.button("🎤 Speak Your Question"):
            # Capture speech input
            user_speech = voice_bot.recognize_speech()
            
            if user_speech:
                # Display recognized text
                st.markdown("### 🗣️ You Said:")
                st.write(user_speech)
                
                # Generate response
                with st.spinner('Generating response...'):
                    response = voice_bot.generate_chatgpt_response(user_speech)
                
                # Display response
                st.markdown("### 💡 ChatGPT Response:")
                st.write(response)
                
                # Speak the response
                voice_bot.speak_response(response)
    
    with col2:
        # Text input alternative
        st.markdown("### 💬 Or Type Your Question")
        text_question = st.text_area(
            "Enter your question:", 
            placeholder="Type your question here if you prefer typing..."
        )
        
        # Text-based response generation
        if st.button("Generate Text Response"):
            if text_question:
                # Generate response
                with st.spinner('Generating response...'):
                    response = voice_bot.generate_chatgpt_response(text_question)
                
                # Display response
                st.markdown("### 💡 ChatGPT Response:")
                st.write(response)
                
                # Speak the response
                voice_bot.speak_response(response)
    
    # Additional information
    st.markdown("---")
    st.info("""
    🌟 How to Use:
    - Click "Speak Your Question" to use voice input
    - Or type your question in the text box
    - Get instant AI-powered responses
    """)

if __name__ == "__main__":
    main()