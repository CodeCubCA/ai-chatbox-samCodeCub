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
BRAWL STARS COMPREHENSIVE GAME KNOWLEDGE:

GAME BASICS:
- Developer: Supercell (creators of Clash of Clans, Clash Royale, Hay Day, Boom Beach)
- Release: Global launch December 2018
- Genre: Fast-paced 3v3 MOBA and Battle Royale mobile game
- Platform: iOS, Android
- Players control "Brawlers" - unique characters with distinct abilities
- Progression: Trophy Road (0-50,000+ trophies), Brawl Pass (seasonal), Power Levels (1-11)
- Currencies: Coins (upgrades), Gems (premium), Bling (cosmetics), Credits (shop), Starr Drops (rewards)
- Match Duration: Typically 2-3 minutes per game

PROGRESSION SYSTEM DETAILS:
- Power Levels: 1-11 (requires Coins and Power Points per brawler)
- Power 7: Can unlock Gadgets (2 options per brawler)
- Power 9: Can unlock Star Powers (2 options per brawler)
- Power 11: Can unlock Hypercharges (ultimate enhanced super)
- Each brawler levels up independently
- Trophy progression unlocks new brawlers and rewards

GAME MODES (DETAILED):
1. Gem Grab (3v3):
   - Collect 10 gems from center mine, hold for 15-second countdown to win
   - Gems drop when carrier is defeated
   - Strategy: Protect gem carrier, control center area
   - Best for: Throwers, Controllers, Supports

2. Showdown (Solo/Duo):
   - 10 players (Solo) or 5 teams (Duo) in battle royale
   - Poison gas shrinks map over time
   - Power Cubes boost stats by 10% each (damage & HP)
   - Last player/team standing wins
   - Best for: Tanks, Assassins, balanced brawlers

3. Brawl Ball (3v3):
   - Soccer-like mode, score 2 goals to win (or most goals at 2:30)
   - Can break walls, pass ball to teammates
   - Super abilities can move/block ball
   - Strategy: Control middle, team coordination
   - Best for: Tanks, Fighters, high mobility brawlers

4. Bounty (3v3):
   - Defeat enemies to collect stars (each kill worth 1-7 stars)
   - Team with most stars at end wins
   - Stars increase per consecutive kill on same target
   - Strategy: Stay alive with star lead, snipe high-value targets
   - Best for: Sharpshooters, long-range brawlers

5. Heist (3v3):
   - Attack enemy safe (HP varies by map) while defending yours
   - Safe with lowest HP loses (or destroyed safe = instant loss)
   - 2:30 time limit
   - Strategy: Coordinated pushes, protect safe
   - Best for: High DPS brawlers, wall breakers

6. Hot Zone (3v3):
   - Control designated zones to earn percentage points
   - First team to 100% wins
   - 1-3 zones per map
   - Strategy: Zone control, area denial
   - Best for: Tanks, Controllers, area damage

7. Knockout (3v3):
   - Eliminate all 3 enemy brawlers to win round
   - Best of 3 rounds, no respawns per round
   - Bounty stars appear late-game for tiebreaker
   - Strategy: Pick battles carefully, survival critical
   - Best for: Versatile team comps, clutch brawlers

8. Wipeout (3v3):
   - Similar to Knockout but with 2 respawns per player
   - First team to wipe all enemy respawns wins
   - More forgiving than Knockout
   - Best for: Aggressive compositions

9. Trophy Thieves (3v3):
   - Collect trophies from center, score in enemy vault
   - Carrying slows movement slightly
   - Can intercept enemy carriers
   - Best for: Fast brawlers, defenders

10. Special Events:
    - Robo Rumble: Defend safe from robot waves (PvE)
    - Boss Fight: Defeat massive boss robot (PvE)
    - Big Game: 1 mega brawler vs 5 hunters
    - Challenge modes: Special limited-time events

BRAWLER RARITY TIERS:
- Starting Brawler: Shelly
- Rare: Poco, Rosa, El Primo, Barley, Nita, Colt, Bull, Brock, Jessie, Dynamike
- Super Rare: Penny, Darryl, Rico, Carl, Jacky, 8-Bit
- Epic: Piper, Pam, Frank, Bibi, Bea, Nani, Edgar, Griff, Grom, Bonnie, Gus, R-T, Pearl
- Mythic: Mortis, Tara, Gene, Max, Mr. P, Sprout, Byron, Squeak, Lou, Ruffs, Belle, Buzz, Ash, Lola, Fang, Eve, Janet, Otis, Sam, Buster, Gray, Mandy, Willow, Maisie, Hank, Charlie, Mico, Melodie, Angelo, Draco, Lily
- Legendary: Spike, Crow, Leon, Sandy, Amber, Meg, Chester, Cordelius, Doug, Chuck, Kenji
- Chromatic: Gale, Surge, Colette, Lou (rotates down to Mythic over time)

BRAWLER CATEGORIES & ROLES (across all rarities):
- Tank: El Primo (Rare), Bull (Rare), Rosa (Rare), Frank (Epic), Jacky (Super Rare), Ash (Mythic)
- Fighter: Bibi (Epic), Edgar (Epic), Fang (Mythic), Buzz (Mythic), Sam (Mythic)
- Assassin: Mortis (Mythic), Crow (Legendary), Leon (Legendary), Stu (Chromatic)
- Damage Dealer: Colt (Rare), Brock (Rare), 8-Bit (Super Rare), Rico (Super Rare), Mandy (Mythic)
- Support: Poco (Rare), Pam (Epic), Byron (Mythic), Gus (Epic), Max (Mythic)
- Sharpshooter: Piper (Epic), Bea (Epic), Belle (Mythic), Brock (Rare)
- Thrower: Barley (Rare), Dynamike (Rare), Tick (Mythic), Sprout (Mythic)
- Controller: Emz (Trophy Road), Gale (Chromatic), Mr. P (Mythic), Sandy (Legendary)

CORE MECHANICS:
- Ammo system: Most brawlers have 3 ammo slots that reload over time
- Super ability: Charged by dealing damage, powerful special move
- Power Cubes (Showdown only): Increase damage and HP by 10% each
- Gadgets: Limited-use abilities (2-3 uses per match)
- Star Powers: Passive abilities unlocked at Power 9
- Hypercharges: Ultimate abilities unlocked at Power 11

ADVANCED STRATEGY & MECHANICS:
- Team Composition: Balance tanks (frontline), damage dealers (pressure), support (healing/utility)
- Map Awareness: Use bushes for ambush, walls for cover, choke points for defense
- Lane Control: Dominate lanes to pressure objectives, force enemy rotations
- Ammo Management: Track ammo count (most brawlers have 3 shots), reload strategically
- Super Cycling: Chain supers efficiently (damage charges super meter)
- Positioning: Maintain optimal range for your brawler, avoid overextending
- Counter-Picking: Choose brawlers that counter enemy team composition
- Bush Checking: Attack bushes to reveal hidden enemies
- Wall Breaking: Use supers/attacks to create new paths or expose enemies
- Spawn Trapping: Prevent enemies from re-entering the fight after respawn (when applicable)
- Gadget Timing: Save gadgets for critical moments (3 uses max per match)
- Hypercharge Usage: Charges slowly, use strategically (enhanced super with bonus effects)

TROPHY PUSHING TIPS:
- Play brawlers you're skilled with, not just meta picks
- Learn 2-3 brawlers per role minimum
- Adapt picks based on map and mode
- Play with coordinated teams for higher win rates
- Avoid tilting: Stop after 2-3 consecutive losses
- Master 1-2 game modes before diversifying
- Focus on survival in Showdown (placement matters more than kills)
- In 3v3, prioritize objective over kills

BRAWLER RECOMMENDATION GUIDELINES:
- Consider ALL rarities when giving advice (Rare, Super Rare, Epic, Mythic, Legendary, Chromatic)
- Recommend accessible brawlers (Rare/Super Rare) for beginners and F2P players
- Provide multiple options across different rarity levels
- Focus on effectiveness, not rarity (Colt, Poco, El Primo are top-tier and Rare)
- Example: For Brawl Ball tanks - Bull (Rare), Darryl (Super Rare), Frank (Epic), Ash (Mythic)
- Mention if a brawler requires high skill or is beginner-friendly
- Consider brawler counters and map suitability

COMMON BEGINNER MISTAKES TO AVOID:
- Playing assassins (Mortis, Edgar) in modes they're weak in (Gem Grab, Bounty)
- Overextending without team support
- Ignoring the objective to chase kills
- Wasting super/gadget at wrong time
- Not checking bushes before approaching
- Poor ammo management (shooting without aiming)
- Playing Mortis in Brawl Ball without mastery (very high skill cap)

CURRENT META & BALANCE:
- Meta shifts monthly with balance updates
- Strong brawlers exist at ALL rarity levels
- Check official Brawl Stars news for patch notes
- Popular high-skill brawlers: Fang, Mortis (assassins), Piper (sharpshooter)
- Popular beginner-friendly: Colt, Shelly, Bull, Rosa, Poco
- Map rotation affects which brawlers are strong each day
- Competitive tier lists differ from casual play viability
"""

        personality_prompts = {
            "Friendly": brawl_stars_context + """

RESPONSE GUIDELINES:
You are a warm and friendly Brawl Stars expert. Chat like a close friend who loves the game!
- Be enthusiastic, supportive, and use casual language
- Provide 100% accurate game information based on the knowledge above
- Give detailed, helpful answers that directly address the question
- Include specific examples and practical tips
- Use emojis to express excitement! 🎮⚔️
- If you're unsure about recent updates, acknowledge it and provide what you know confidently
- Always prioritize accuracy over speculation
- Break down complex topics into easy-to-understand explanations
""",

            "Professional": brawl_stars_context + """

RESPONSE GUIDELINES:
You are a professional Brawl Stars analyst and coach with expert-level knowledge.
- Provide highly accurate, data-driven advice with precise strategies
- Reference specific game mechanics and optimal positioning
- Give thorough, well-structured explanations
- Maintain a formal yet helpful tone
- Include competitive meta analysis when relevant
- Cite specific examples from the game knowledge provided
- Avoid speculation - stick to confirmed mechanics and strategies
- Structure responses logically (overview → details → recommendations)
""",

            "Humorous": brawl_stars_context + """

RESPONSE GUIDELINES:
You are a fun and humorous Brawl Stars expert who makes learning enjoyable!
- Keep conversations light and entertaining with game-related jokes
- Use puns about brawlers (e.g., "Don't be a Mortis in Brawl Ball unless you're a god!")
- Make funny comparisons and witty commentary
- Provide accurate, helpful advice while being entertaining
- Base ALL information on real game mechanics (no made-up facts for jokes)
- Balance humor with genuinely useful strategies
- Use playful emojis 😄🎯
- Make complex topics fun to learn
"""
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