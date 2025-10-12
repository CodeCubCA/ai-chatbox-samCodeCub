import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
def init_groq_client():
    """Initialize Groq API client with API key from environment variables"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in environment variables!")
        st.stop()
    return Groq(api_key=api_key)

# Function to get AI response
def get_ai_response(client, messages, personality="Friendly"):
    """Get response from Groq AI model with personality adjustment"""
    try:
        # Define personality-specific system messages
        personality_prompts = {
            "Friendly": "You are a warm and friendly AI assistant with expertise in Brawl Stars, the popular mobile game by Supercell. Chat like a close friend who loves Brawl Stars! Be enthusiastic, supportive, and use casual language. Help with game strategies, brawler information, game modes, tips, and general Brawl Stars knowledge. Feel free to use emojis to express excitement! 🎮⚔️",

            "Professional": "You are a professional and rigorous Brawl Stars expert. Provide accurate, well-structured advice and analysis about the game. Focus on precise strategies, detailed brawler statistics, meta analysis, and competitive insights. Maintain a formal yet helpful tone. Give thorough explanations backed by game mechanics and data.",

            "Humorous": "You are a fun and humorous Brawl Stars AI companion! Keep conversations light, entertaining, and full of jokes related to the game. Use puns about brawlers, funny comparisons, and witty commentary while still providing helpful advice. Make learning about Brawl Stars an enjoyable and laugh-filled experience! 😄🎯"
        }

        system_message = {
            "role": "system",
            "content": personality_prompts.get(personality, personality_prompts["Friendly"])
        }

        # Prepare messages with system context
        full_messages = [system_message] + messages

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app configuration
st.set_page_config(
    page_title="My Brawl Stars AI Assistant",
    page_icon="🏆",
    layout="wide"
)

# App title and description
st.title("🏆 My Brawl Stars AI Assistant")
st.markdown("""
### Welcome, Brawler! 👋⚔️

I'm your dedicated Brawl Stars AI companion, here to help you dominate the battlefield! Whether you're a beginner just starting your journey or a seasoned pro pushing for higher trophies, I've got you covered.

**What I can help you with:**
- 🎯 Game strategies and tactics
- 💎 Brawler guides and tier lists
- 🗺️ Map-specific tips and best brawlers
- 🏅 Trophy pushing advice
- ⚡ Meta analysis and team compositions
- 🎮 Game modes explanations
- 💪 Brawler counters and synergies

Let's get those wins together! Ask me anything about Brawl Stars! 🚀
""")

# Initialize Groq client
client = init_groq_client()

# Initialize session state for chat history and personality
if "messages" not in st.session_state:
    st.session_state.messages = []
if "personality" not in st.session_state:
    st.session_state.personality = "Friendly"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Brawl Stars strategies, brawlers, or anything else!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(client, st.session_state.messages, st.session_state.personality)
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with additional features
with st.sidebar:
    st.header("⚙️ AI Personality")

    # Personality selection with icons
    personality_options = {
        "😊 Friendly": "Friendly",
        "💼 Professional": "Professional",
        "😄 Humorous": "Humorous"
    }

    selected_personality = st.radio(
        "Choose how your AI assistant responds:",
        options=list(personality_options.keys()),
        index=list(personality_options.values()).index(st.session_state.personality),
        help="Select the personality style for your AI assistant"
    )

    # Update personality in session state
    new_personality = personality_options[selected_personality]
    if new_personality != st.session_state.personality:
        st.session_state.personality = new_personality
        st.success(f"Personality changed to {new_personality}!")

    st.markdown("---")

    st.header("🎮 Brawl Stars Info")
    st.markdown("""
    **Popular Topics to Ask About:**
    - 🏆 Best brawlers for different game modes
    - 🗺️ Strategy tips for specific maps
    - 📈 How to push trophies
    - ⚡ Meta analysis
    - ⚔️ Brawler counters and synergies
    - 🎯 Game mode explanations
    - 🌟 Tips for beginners
    """)

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Made with ❤️ for Brawl Stars fans** 🏆")