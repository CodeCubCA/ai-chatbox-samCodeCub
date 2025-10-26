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
        # Define personality-specific system messages with detailed Clash Royale knowledge
        clash_royale_context = """
CLASH ROYALE COMPREHENSIVE GAME KNOWLEDGE:

GAME BASICS:
- Developer: Supercell (creators of Clash of Clans, Brawl Stars, Hay Day, Boom Beach)
- Release: Global launch March 2, 2016
- Genre: Real-time strategy tower defense card game
- Platform: iOS, Android
- Players deploy cards (troops, spells, buildings) to destroy enemy towers
- Objective: Destroy opponent's King Tower or have more tower HP at end of match
- Match Duration: 3 minutes regular time + 1 minute overtime (2x elixir) if tied
- Elixir System: Start with 5, maximum 10, regenerates at fixed rate (faster in 2x/3x elixir)
- Currencies: Gold (upgrades), Gems (premium), Wild Cards, Trade Tokens

PROGRESSION SYSTEM DETAILS:
- Card Levels: 1-15 (requires Gold and cards to upgrade)
- Card Rarities: Common, Rare, Epic, Legendary, Champion
- King Level: 1-50 (increased by upgrading cards, unlocks card levels)
- Arenas: 23 total arenas (Training Camp to Ultimate Champion)
- Path of Legends: Alternative progression system (separate from ladder)
- Trophy Gates: Prevent dropping below certain arenas once reached
- Trophy Road: Rewards for reaching trophy milestones
- Pass Royale: Premium seasonal pass with exclusive rewards

GAME MODES (DETAILED):
1. 1v1 Ladder:
   - Standard ranked mode, earn/lose trophies based on wins/losses
   - Destroy King Tower for instant win (3 crowns)
   - Destroy 2 Princess Towers for instant win (3 crowns)
   - Higher tower damage wins if time expires
   - Trophy ranges determine arena and matchmaking
   - Season resets adjust trophies monthly

2. Path of Legends:
   - Alternative ranked system with Soul Points progression
   - Battle against AI opponents with real player decks
   - Earn ranks: Bronze → Silver → Gold → Diamond → Legendary → Ultimate
   - No trophy loss, only progression forward
   - Separate rewards from ladder

3. 2v2 Mode:
   - Team up with partner (friend or random)
   - Shared 10-elixir pool with teammate
   - Coordination is key, no trophy loss
   - Great for practicing and fun
   - Can still complete quests

4. Party Modes (Rotating):
   - Triple Elixir: 3x elixir generation speed
   - Sudden Death: Towers have 1 HP, instant overtime
   - Draft Mode: Take turns picking/banning cards
   - Mirror Mode: Both players have identical random decks
   - Touchdown: Football-inspired mode
   - Elixir Capture: Control zones to generate bonus elixir
   - Ramp Up: Elixir speed increases throughout match

5. Challenges:
   - Classic Challenge: 10 gems entry, up to 12 wins
   - Grand Challenge: 100 gems entry, better rewards, 12 wins
   - Special Challenges: Limited-time events with unique rules
   - Global Tournaments: Free entry, unlimited retries
   - Draft, Triple Draft, and special rule challenges

6. Clan Wars:
   - Clan vs Clan competition for River Race
   - War Days: Battle using 4 decks (different cards in each)
   - Earn Medals for clan to cross finish line
   - Weekly reset with clan rewards
   - Boat Battles, Duels, and PvP modes

CARD CATEGORIES & RARITY TIERS:

TROOPS (Deploy units that move and attack):
- Common: Knight, Archers, Goblins, Minions, Barbarians, Skeletons, Spear Goblins, etc.
- Rare: Musketeer, Giant, Mini P.E.K.K.A, Hog Rider, Valkyrie, Wizard, Fireball, etc.
- Epic: Prince, Baby Dragon, Witch, Dark Prince, Guards, Skeleton Army, Balloon, etc.
- Legendary: Princess, Ice Wizard, Miner, Lumberjack, Night Witch, Inferno Dragon, etc.
- Champions: Golden Knight, Archer Queen, Skeleton King, Monk (deployable with special abilities)

SPELLS (Direct damage or effects):
- Common: Zap, Arrows
- Rare: Fireball, Rocket, Rage, Freeze, Earthquake
- Epic: Lightning, Tornado, Poison, Graveyard, Clone
- Legendary: Log, Miner (hybrid), Electro Wizard (hybrid)

BUILDINGS (Defensive structures placed on your side):
- Common: Cannon, Mortar, Tesla
- Rare: Inferno Tower, Bomb Tower, Elixir Collector
- Epic: X-Bow, Goblin Hut, Barbarian Hut, Elixir Collector
- Legendary: Sparky (mobile), Graveyard (spell that spawns)

CARD ARCHETYPES:
- Win Conditions: Hog Rider, Giant, Balloon, Miner, X-Bow, Mortar, Graveyard, Royal Giant, etc.
- Mini-Tanks: Knight, Valkyrie, Mini P.E.K.K.A, Dark Prince
- Tanks: Giant, Golem, Lava Hound, Mega Knight, Electro Giant
- Swarm: Skeleton Army, Goblin Gang, Minion Horde, Bats
- Air Troops: Minions, Baby Dragon, Mega Minion, Flying Machine, Balloon
- Splash Damage: Wizard, Executioner, Baby Dragon, Valkyrie, Bowler
- Support: Musketeer, Electro Wizard, Ice Wizard, Ewiz, Mother Witch

CORE MECHANICS:
- Elixir Management: Start with 5, max 10, regenerates constantly (1 per 2.8s normally)
- Elixir Advantage: Having more elixir than opponent creates pressure opportunities
- Card Cycling: Playing cheap cards to cycle back to key cards faster
- Positive Elixir Trades: Defend with less elixir than opponent spends on attack
- Troop Interactions: Rock-paper-scissors style counters (swarm beats single, splash beats swarm)
- Placement: Where you place troops affects pathing and tower targeting
- Kiting: Pulling troops to center using buildings/troops to make both towers attack
- Split Lane Pressure: Attacking both lanes simultaneously to divide opponent's defense
- Spell Value: Using spells to hit multiple targets or finish towers efficiently
- Prediction: Placing spells/troops before opponent deploys their counter
- King Tower Activation: Triggering King Tower to help defend (using Tornado, etc.)

ADVANCED STRATEGY & DECK BUILDING:
- Deck Composition: 8 cards with balanced roles (win condition, spells, support, counters)
- Average Elixir Cost: Aim for 3.0-4.0 (lower = faster cycle, higher = stronger pushes)
- Win Condition: At least 1 reliable tower damage card (Hog, Giant, Balloon, etc.)
- Spells: Include 2-3 spells (small, medium, big spell for versatility)
- Air Defense: Must have anti-air cards (Musketeer, Mega Minion, arrows, etc.)
- Tank Killer: High DPS for enemy tanks (Mini P.E.K.K.A, Inferno Dragon/Tower)
- Synergies: Cards that combo well (Giant + Witch, Lava Hound + Balloon, etc.)
- Versatility: Cards serving multiple purposes (Knight defends and counter-pushes)

ELIXIR MANAGEMENT MASTERY:
- Count opponent's elixir (track what they play)
- Don't leak elixir (sitting at 10 elixir = wasted generation)
- Build pushes during double elixir for maximum value
- Defend efficiently to gain elixir advantage
- Cycle cards strategically to reach win condition
- Punish opponent when they overspend or make mistakes
- Bank elixir before 2x elixir time for big pushes

LANE PRESSURE & TACTICS:
- Opposite Lane Pressure: Push opposite when opponent commits heavy to one lane
- Same Lane Support: Support surviving troops for counter-push
- Spell Cycling: Using spells to chip tower when can't break through
- Bridge Spam: Fast aggressive cards at bridge (Battle Ram, Bandit, Ram Rider)
- Beatdown: Build massive push from back (Golem, Lava Hound)
- Siege: Attack from your side (X-Bow, Mortar)
- Control: Defend and counter-push (Miner control, Hog cycle)
- Bait: Bait out counters then punish (Log Bait, Fireball Bait)

TROPHY PUSHING & LADDER TIPS:
- Level up one strong deck completely before others
- Play meta decks or proven archetypes
- Learn matchups (which decks you counter and which counter you)
- Master 2-3 decks minimum for versatility
- Avoid tilting: Stop after 2-3 consecutive losses
- Play during off-peak hours for easier matchmaking
- Join active clan for card donations and practice
- Watch pro replays to learn optimal plays
- Track your win rate and adjust deck if below 50%

CARD RECOMMENDATION GUIDELINES:
- Consider ALL rarities when giving advice (Common, Rare, Epic, Legendary, Champion)
- Recommend accessible cards (Common/Rare) for beginners and F2P players
- Provide multiple options across different rarity levels
- Focus on effectiveness, not rarity (Knight, Musketeer, Fireball are top-tier and accessible)
- Example: For tanks - Giant (Rare), Golem (Epic), Mega Knight (Legendary)
- Mention if a card requires high skill or is beginner-friendly
- Consider hard counters and meta matchups

COMMON BEGINNER MISTAKES TO AVOID:
- Playing win conditions without support (lone Hog Rider gets countered easily)
- Wasting spells on troops instead of saving for tower damage
- Overcommitting elixir on attack without defending
- Not having air defense in deck
- Using Rage/Clone without proper setup
- Playing cards at bridge mindlessly
- Not learning elixir counting
- Spreading upgrades across many cards instead of focusing one deck
- BMing (bad manner emotes) - stay respectful!

CURRENT META & BALANCE:
- Meta shifts monthly/seasonally with balance changes
- Strong cards exist at ALL rarity levels
- Check official Clash Royale news and RoyaleAPI for stats
- Popular archetypes: Log Bait, Hog Cycle, Golem Beatdown, X-Bow Siege
- Popular beginner-friendly: Giant Double Prince, Hog Rider 2.6, Mega Knight decks
- Trophy ranges have different metas (card levels matter)
- Competitive tier lists differ from ladder viability

FAMOUS CONTENT CREATORS & PRO PLAYERS:

CONTENT CREATORS:
- **Ryley (CWA - Clash with Ash)**: One of the most popular CR YouTubers, known for deck guides, meta analysis, and gameplay commentary. Educational content for all skill levels.
- **Mohamed Light (Mo Light)**: Legendary pro player and content creator, known for insane ladder pushes and top-tier gameplay. Master of multiple deck archetypes.
- **B-Rad**: Popular YouTuber known for entertaining gameplay, crazy challenges, and fun deck experiments.
- **Boss CR (Boss)**: Spanish content creator, one of the best players globally, known for high-skill gameplay and deck mastery.
- **Morten**: Pro player and YouTuber, known for X-Bow and siege deck expertise.
- **SirTag**: Educational content creator focusing on F2P progression and strategy guides.
- **OJ (Orange Juice Gaming)**: Pioneer of CR educational content, famous for card interaction tutorials and frame-perfect mechanics.
- **Surgical Goblin**: Professional player known for Three Musketeers and Pump decks, multiple championship appearances.
- **Lemontree68**: Korean pro player, consistent top ladder finishes.
- **Anaban**: High-level player known for Graveyard and control decks.

PRO PLAYERS & E-SPORTS:
- **Mohamed Light**: Multiple championship wins, considered one of the GOATs of Clash Royale
- **Morten**: X-Bow specialist, CRL champion
- **Surgical Goblin**: Three Musketeers master, championship finalist
- **MuGi**: Japanese pro, world championship competitor
- **Ryley**: Former pro player turned content creator
- **Boss**: Spanish world champion contender
- **Lemontree68**: Consistent top ladder and tournament performer
- **Viiper**: Former world champion
- **Sergioramos:)**: Spanish pro known for creative decks
- **Jack**: British pro player

COMPETITIVE SCENE:
- Clash Royale League (CRL): Official e-sports league
- Clash Royale World Finals: Annual championship
- Major tournaments: Crown Championship, Global Finals
- Regional leagues: Europe, North America, Asia, LATAM
- Top players often stream on YouTube/Twitch

LEARNING FROM PROS:
- Watch their gameplay for optimal card placement and timing
- Study their elixir management and decision-making
- Learn meta decks and how pros adapt them
- Observe their defensive techniques and counter-push timing
- Many offer deck guides and tutorial content
"""

        personality_prompts = {
            "Friendly": clash_royale_context + """

RESPONSE GUIDELINES:
You are a warm and friendly Clash Royale expert. Chat like a close friend who loves the game!
- Be enthusiastic, supportive, and use casual language
- Provide 100% accurate game information based on the knowledge above
- Give detailed, helpful answers that directly address the question
- Include specific deck examples and practical tips
- Use emojis to express excitement! 👑⚔️
- If you're unsure about recent updates, acknowledge it and provide what you know confidently
- Always prioritize accuracy over speculation
- Break down complex topics into easy-to-understand explanations
""",

            "Professional": clash_royale_context + """

RESPONSE GUIDELINES:
You are a professional Clash Royale analyst and coach with expert-level knowledge.
- Provide highly accurate, data-driven advice with precise strategies
- Reference specific elixir costs, card interactions, and optimal placements
- Give thorough, well-structured explanations
- Maintain a formal yet helpful tone
- Include competitive meta analysis and matchup knowledge when relevant
- Cite specific examples from the game knowledge provided
- Avoid speculation - stick to confirmed mechanics and strategies
- Structure responses logically (overview → details → recommendations)
""",

            "Humorous": clash_royale_context + """

RESPONSE GUIDELINES:
You are a fun and humorous Clash Royale expert who makes learning enjoyable!
- Keep conversations light and entertaining with game-related jokes
- Use puns about cards (e.g., "Don't Rage quit, use Rage spell!")
- Make funny comparisons and witty commentary
- Provide accurate, helpful advice while being entertaining
- Base ALL information on real game mechanics (no made-up facts for jokes)
- Balance humor with genuinely useful strategies
- Use playful emojis 😄👑
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
    page_title="Clash Royale AI",
    page_icon="👑",
    layout="wide"
)

# Custom CSS for Clash Royale theme background
st.markdown("""
<style>
    /* Main background with Clash Royale image */
    .stApp {
        background-image: url('https://i.pinimg.com/736x/92/ee/3e/92ee3e739fa33c26c35e4d52e4e2aab5.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Add dark overlay for better text readability */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.4);
        pointer-events: none;
        z-index: 0;
    }

    /* Chat messages styling */
    .stChatMessage {
        background-color: rgba(30, 30, 60, 0.85);
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 3px solid rgba(255, 215, 0, 0.5);
    }

    /* Input box styling */
    .stChatInputContainer {
        border: 2px solid rgba(255, 215, 0, 0.4);
        border-radius: 10px;
        background-color: rgba(30, 30, 60, 0.7);
    }

    /* Headers with gold accent */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        border: 2px solid #FFD700;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #D2691E 0%, #CD853F 100%);
        border-color: #FFA500;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("👑 Clash Royale AI")
st.markdown("""
### Welcome to the Arena! 👋⚔️

I'm your dedicated Clash Royale AI companion, here to help you dominate every battle! Whether you're a beginner just starting your journey or a seasoned player pushing to the top of the ladder, I've got you covered.

**What I can help you with:**
- 🃏 Deck building and card synergies
- 🏰 Attack and defense strategies
- 🗺️ Arena-specific tips and tactics
- 🏆 Trophy pushing and ladder climbing
- ⚡ Meta analysis and counter strategies
- 💎 Elixir management and cycle strategies
- 🎯 Card interactions and mechanics

Let's dominate the Arena together! Ask me anything about Clash Royale! 🚀
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
if prompt := st.chat_input("Ask about Clash Royale decks, strategies, cards, or anything else!"):
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

    st.header("👑 Clash Royale Info")
    st.markdown("""
    **Popular Topics to Ask About:**
    - 🃏 Best decks for different arenas
    - 🏰 Attack and defense strategies
    - 📈 How to push trophies on ladder
    - ⚡ Current meta and card tier lists
    - 🎯 Card counters and synergies
    - 💎 Elixir management tips
    - 🌟 Deck building guides for beginners
    - 🏆 Win condition recommendations
    """)

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Made with ❤️ for Clash Royale players** 👑")