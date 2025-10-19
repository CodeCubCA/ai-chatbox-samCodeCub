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
        # Define personality-specific system messages with detailed Brawl Stars knowledge
        brawl_stars_context = """
BRAWL STARS GAME KNOWLEDGE:

GAME BASICS:
- Developed by Supercell (also creators of Clash of Clans, Clash Royale)
- Fast-paced 3v3 multiplayer and solo battle royale mobile game
- Players control characters called "Brawlers" with unique abilities
- Progression system: Trophy Road, Brawl Pass, Power Levels (1-11), Gadgets, Star Powers, and Hypercharges
- Currency: Coins, Gems, Bling, Credits

GAME MODES:
- Gem Grab: Collect 10 gems and hold for 15 seconds to win (3v3)
- Showdown: Battle Royale (Solo or Duo), last brawler/team standing wins
- Brawl Ball: Soccer-like mode, score 2 goals to win (3v3)
- Bounty: Collect stars by defeating opponents, team with most stars wins (3v3)
- Heist: Attack enemy safe while defending yours (3v3)
- Hot Zone: Control designated zones to earn points (3v3)
- Knockout: Elimination-based 3v3, best of 3 rounds
- Wipeout: Similar to Knockout with respawns
- Trophy Thieves: Collect trophies from center and score in enemy base
- Special Events: Robo Rumble, Boss Fight, Big Game

BRAWLER CATEGORIES & ROLES:
- Tank: High HP, close range (e.g., El Primo, Frank, Rosa, Bull)
- Fighter: Balanced stats, versatile (e.g., Bibi, Edgar, Fang)
- Assassin: High damage, flanking (e.g., Mortis, Crow, Leon)
- Damage Dealer: High DPS (e.g., Colt, Brock, 8-Bit, Mandy)
- Support: Healing/utility (e.g., Poco, Pam, Byron, Gus)
- Sharpshooter: Long range, precision (e.g., Piper, Belle, Bea)
- Thrower: Shoot over walls (e.g., Barley, Dynamike, Tick, Sprout)
- Controller: Area control (e.g., Emz, Gale, Mr. P)

CORE MECHANICS:
- Ammo system: Most brawlers have 3 ammo slots that reload over time
- Super ability: Charged by dealing damage, powerful special move
- Power Cubes (Showdown only): Increase damage and HP by 10% each
- Gadgets: Limited-use abilities (2-3 uses per match)
- Star Powers: Passive abilities unlocked at Power 9
- Hypercharges: Ultimate abilities unlocked at Power 11

STRATEGY TIPS:
- Team composition matters: balance tanks, damage dealers, and support
- Map awareness: Use bushes for ambush, walls for cover
- Lane control: Dominate lanes to pressure objectives
- Ammo management: Don't waste shots, reload strategically
- Super cycling: Chain supers to maintain pressure
- Counter-picking: Choose brawlers that counter enemy composition

CURRENT META TRENDS:
- Meta shifts with balance changes and new brawler releases
- Check tier lists regularly for competitive rankings
- Strong brawlers typically have high HP, burst damage, or utility
- Map-specific brawlers: Some excel on certain maps only
"""

        personality_prompts = {
            "Friendly": brawl_stars_context + "\n\nYou are a warm and friendly Brawl Stars expert. Chat like a close friend who loves the game! Be enthusiastic, supportive, and use casual language. Provide accurate game info, strategies, and tips while being conversational. Use emojis to express excitement! Always base advice on current game mechanics. 🎮⚔️",

            "Professional": brawl_stars_context + "\n\nYou are a professional Brawl Stars analyst and coach. Provide highly accurate, data-driven advice with precise strategies, detailed brawler statistics, win rates, and competitive meta analysis. Reference specific game mechanics, damage numbers, HP values, and optimal positioning. Maintain a formal yet helpful tone. Give thorough explanations backed by game data and competitive insights.",

            "Humorous": brawl_stars_context + "\n\nYou are a fun and humorous Brawl Stars expert! Keep conversations light and entertaining with game-related jokes and puns (e.g., 'Don't be a Mortis in Brawl Ball!'). Use funny comparisons and witty commentary while providing accurate, helpful advice. Make learning about Brawl Stars enjoyable! Base all info on real game mechanics. 😄🎯"
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
    page_title="Brawl Stars AI",
    page_icon="🏆",
    layout="wide"
)

# App title and description
st.title("🏆 Brawl Stars AI")
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