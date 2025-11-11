import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client
def init_gemini_client():
    """Initialize Gemini API client with API key from environment variables"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found in environment variables!")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

# Function to get AI response
def get_ai_response(model, messages, personality="Friendly"):
    """Get response from Gemini AI model with personality adjustment"""
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

ADVANCED STRATEGY & DECK BUILDING (COMPREHENSIVE GUIDE):

DECK BUILDING FUNDAMENTALS:
1. **Core Components Every Deck Needs:**
   - Win Condition (1-2 cards): Primary tower damage dealer (Hog Rider, Giant, Balloon, Miner, X-Bow, Graveyard, etc.)
   - Tank/Mini-Tank (1-2 cards): Absorbs damage for pushes (Knight, Valkyrie, Giant, Golem)
   - Splash Damage (1-2 cards): Clears swarms (Baby Dragon, Wizard, Valkyrie, Arrows, Fireball)
   - Anti-Air (1-2 cards): Defends air threats (Musketeer, Mega Minion, Bats, Archers)
   - Small Spell (1 card): Cycle and swarm clear (Log, Zap, Arrows, Snowball)
   - Medium/Heavy Spell (1 card): Tower damage and defensive reset (Fireball, Rocket, Lightning, Poison)
   - Defensive Building (0-1 card): Pulls troops, protects towers (Tesla, Cannon, Inferno Tower)
   - Support/Utility (1-2 cards): Versatile cards (Electro Wizard, Ice Spirit, Skeletons)

2. **Average Elixir Cost Guidelines:**
   - Fast Cycle (2.6-3.2): Quick rotation to win condition, requires high skill
   - Balanced (3.3-3.8): Most versatile, good for ladder and challenges
   - Beatdown (3.9-4.5): Heavy pushes, requires good elixir management
   - Above 4.5: Very risky, slow cycle, vulnerable to faster decks

3. **Deck Archetypes Explained:**

   A) **BEATDOWN** (Build big pushes from back)
   - Strategy: Tank in back, support behind, overwhelm opponent
   - Win Conditions: Golem, Giant, Lava Hound, Mega Knight, Electro Giant
   - Support Cards: Night Witch, Baby Dragon, Lumberjack, Electro Dragon
   - Example Deck: Golem, Night Witch, Baby Dragon, Tornado, Lightning, Lumberjack, Mega Minion, Skeletons
   - Key Skills: Elixir management, knowing when to commit, defending with less
   - Best Against: Siege, Bait decks
   - Weak Against: Fast cycle, Inferno Tower/Dragon

   B) **CYCLE** (Fast rotation to win condition)
   - Strategy: Cycle cheap cards to spam win condition repeatedly
   - Win Conditions: Hog Rider, Miner, Royal Hogs, Wall Breakers
   - Cycle Cards: Ice Spirit, Skeletons, Log, Ice Golem (1-2 elixir cards)
   - Example Deck: Hog Rider 2.6 (Hog, Musketeer, Cannon, Ice Golem, Ice Spirit, Fireball, Log, Skeletons)
   - Key Skills: Fast reactions, elixir counting, precise placement
   - Best Against: Beatdown, slower decks
   - Weak Against: Splash damage, heavy spell decks

   C) **CONTROL** (Defend and counter-push)
   - Strategy: Control tempo with strong defense, punish with counter-pushes
   - Win Conditions: Miner, Graveyard, Hog Rider with heavy support
   - Defense: Tesla, Cannon Cart, Valkyrie, Knight
   - Example Deck: Miner, Poison, Valkyrie, Bats, Spear Goblins, Tesla, Log, Ice Spirit
   - Key Skills: Defending efficiently, elixir advantage, patience
   - Best Against: Beatdown, Bridge Spam
   - Weak Against: Spell chip cycle, outcycle decks

   D) **SIEGE** (Attack from your side)
   - Strategy: Deploy building that attacks tower from your territory
   - Win Conditions: X-Bow, Mortar
   - Defense: Tesla, Knight, Archers, Ice Spirit, Skeletons
   - Example Deck: X-Bow 3.0 (X-Bow, Tesla, Knight, Archers, Ice Spirit, Skeletons, Fireball, Log)
   - Key Skills: Building placement, defensive mastery, prediction
   - Best Against: Beatdown, control
   - Weak Against: Earthquake, Lightning, Rocket, Bridge Spam

   E) **BAIT** (Bait out counters, then punish)
   - Strategy: Use multiple cards that die to same spell, bait it out, then exploit
   - Sub-Types: Log Bait (Goblin Barrel focus), Fireball Bait (multiple Fireball-vulnerable troops)
   - Example Log Bait: Goblin Barrel, Princess, Goblin Gang, Rocket, Knight, Ice Spirit, Inferno Tower, Log
   - Key Skills: Tracking opponent's spells, knowing when they're out of cycle
   - Best Against: Heavy spell decks, beatdown
   - Weak Against: Multiple small spells, splash damage

   F) **BRIDGE SPAM** (Fast aggressive pushes at bridge)
   - Strategy: Deploy troops directly at bridge for immediate pressure
   - Win Conditions: Battle Ram, Ram Rider, Bandit, Royal Ghost
   - Support: Dark Prince, Magic Archer, Electro Wizard, Pekka
   - Example Deck: Pekka Bridge Spam (Pekka, Battle Ram, Bandit, Magic Archer, Ewiz, Zap, Poison, Royal Ghost)
   - Key Skills: Pressure timing, knowing when to defend vs attack
   - Best Against: Siege, slow decks, beatdown
   - Weak Against: Cycle decks, swarm spam

4. **PRO-LEVEL DECK BUILDING TIPS:**

   **Elixir Curve Balance:**
   - Don't have too many high-cost cards (can't defend multiple threats)
   - Include 2-3 cards that cost 3 elixir or less for cycling
   - Avoid having all your counters be expensive

   **Versatility and Flex Cards:**
   - Knight: Defense + counter-push, tanks for support troops
   - Musketeer: Air defense + DPS + ranged support
   - Mega Minion: Air defense + tank killer + survives spells
   - Valkyrie: Splash + mini-tank + counter-push

   **Spell Synergies:**
   - Zap + Arrows: Covers all swarms (overkill, usually avoid)
   - Log + Fireball: Most versatile combo (ground swarm + medium troops)
   - Arrows + Poison: Anti-air swarm + area denial
   - Zap + Rocket: Quick chip + heavy damage finisher

   **Matchup Coverage:**
   - Anti-Swarm: Splash units or small spells (vs Goblin Gang, Skarmy)
   - Anti-Tank: High DPS or Inferno (vs Golem, Giant, Mega Knight)
   - Anti-Air: Ranged units or air-targeting (vs Balloon, Lava Hound)
   - Building Counter: Earthquake, Lightning, or pressure opposite lane

   **Card Synergies (Combos That Work):**
   - Giant + Witch: Tank + splash support
   - Lava Hound + Balloon: Double air pressure (Lavaloon)
   - Golem + Night Witch: Tank + spawn spam support
   - Hog + Freeze: Instant tower damage before counter
   - Miner + Poison: Spell bait tank + area denial
   - Graveyard + Freeze: Skeleton spam + counter freeze
   - X-Bow + Tesla: Double building defense
   - Balloon + Lumberjack: Rage on death buff

   **Common Deck Building Mistakes:**
   - No clear win condition (no reliable tower damage)
   - Too many expensive cards (can't cycle or defend efficiently)
   - No air defense (instant loss to Balloon/Lava Hound)
   - No building (hard to defend tanks and Hog)
   - Only one spell (not enough versatility)
   - Cards with overlapping roles (redundant, wastes deck slot)
   - No tank killer (can't stop Golem/Giant pushes)
   - Average elixir above 4.5 (too slow)

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

PRO PLAYER STRATEGIES & TECHNIQUES:

1. **ELIXIR COUNTING (Essential Pro Skill):**
   - Track EVERY card opponent plays and calculate their elixir
   - Start: Both players begin with 5 elixir
   - If opponent plays 8 elixir of cards, they have ~2-3 elixir left
   - Punish when they're low (play Hog Rider when they have 3 elixir)
   - Don't overcommit when YOU'RE low on elixir
   - In 2x elixir, counting becomes harder but even more important

2. **CARD CYCLING MASTERY:**
   - Know your deck cycle order (what cards come next)
   - Cycle cheap cards to get back to win condition faster
   - Example: If Hog is 4 cards away, play Ice Spirit + Skeletons to get it faster
   - "Out-cycling" = rotating back to counter before opponent gets their win condition
   - Pros intentionally cycle to have the right cards at the right time

3. **DEFENSIVE POSITIONING (Pro Placements):**
   - **Kiting**: Place troop in center to pull enemy troops between both towers
     - Example: Kite Mega Knight or Pekka with Knight in middle
   - **Anti-Lightning Spread**: Don't clump units (Lightning can't hit multiple)
   - **Building Placement**:
     - Center plant (pulls Hog, Giant to middle for both towers)
     - Opposite lane plant (forces long walk, buys time)
   - **Troop Surround**: Place troops in square around tank to DPS it down
   - **Split Push Counter**: Put 1 cheap troop on pressure lane, defend other side

4. **OFFENSIVE TIMING (When Pros Attack):**
   - **Elixir Advantage Push**: When you have +3-4 elixir advantage
   - **Counter Push**: Support surviving defensive troops
   - **Double Lane Pressure**: Force opponent to choose which lane to defend
   - **Spell Chip**: Rocket/Fireball cycling when can't break through
   - **Prediction Plays**: Pre-place Log/Arrows before opponent drops swarm
   - **Opposite Lane Rush**: Push opposite when opponent commits 8+ elixir one side
   - **2x Elixir Timing**: Save elixir right before 2x, then unleash huge push

5. **MATCHUP KNOWLEDGE (How Pros Win Bad Matchups):**
   - Know your deck's counters and what you struggle against
   - Play defensively in bad matchups, chip with spells
   - Force opponent to make mistakes (bait spells, outcycle counters)
   - Example: Hog 2.6 vs Golem = defend and outcycle their counters
   - Don't over-commit on attack if you can't break through
   - Focus on 1-crown win, tower trade, or draw if necessary

6. **MOMENTUM CONTROL:**
   - Pros take risks when ahead (more aggressive)
   - Pros play safe when behind (defend, spell chip, wait for mistake)
   - Don't tilt = stay calm after bad play, refocus
   - Force opponent to respond to YOU (constant pressure)

7. **MOHAMED LIGHT'S LADDER SECRETS:**
   - Master 1-2 decks completely (don't switch constantly)
   - Learn micro-interactions (Ice Spirit timing, Zap timing)
   - Predict opponent patterns (if they always Log barrel, pre-place troops)
   - Never BM until after match (keep mental advantage)
   - Take breaks after losses (don't tilt queue)
   - Review replays of losses to learn mistakes

8. **MORTEN'S X-BOW MASTERY TIPS:**
   - Defensive X-Bow = place for chip damage when can't commit
   - Offensive X-Bow = place when opponent low on elixir or without counter
   - Tesla + X-Bow = double building defense is nearly unbreakable
   - Cycle pressure = always have answer to opponent's push
   - Fireball cycle in overtime when X-Bow can't connect

9. **BOSS CR'S AGGRESSIVE TACTICS:**
   - Never give opponent breathing room (constant pressure)
   - Punish EVERY elixir mistake immediately
   - Take tower trades if favorable (sacrifice 1 tower for 2)
   - Know when to spell cycle for win instead of forcing push
   - Mind games = sometimes don't play predictably (switch lanes unexpectedly)

10. **SURGICAL GOBLIN'S 3M PUMP STRATEGY:**
    - Pump in back when safe (elixir advantage over time)
    - Split 3M at bridge (force opponent to defend both lanes)
    - Battle Ram + Musketeers combo (tank + DPS)
    - Elixir Collector baiting (opponent must choose: destroy pump or defend push)

11. **PRO-LEVEL MICRO SKILLS:**
    - **Zap Timing**: Reset Inferno, Sparky RIGHT before they shoot
    - **Prediction Spell**: Log/Arrows BEFORE opponent drops swarm
    - **Troop Surround**: 4-corner placement around tank
    - **Tower Target Switch**: Use 1 elixir troops to redirect attacks
    - **Spell Baiting**: Show bait card, make opponent waste spell, then punish
    - **Frame-Perfect Timing**: Freeze right as tower is about to die to Balloon

12. **MENTAL GAME (Pro Mindset):**
    - Every loss is a learning opportunity
    - Don't focus on card levels (focus on outplaying)
    - Stay calm = better decisions
    - Emote mute if tilting
    - Know when to stop playing (after 2-3 losses in a row)
    - Confidence without arrogance

LEARNING FROM PROS:
- **Watch Pro Streams/Videos**: Mohamed Light, Morten, Boss, Surgical Goblin
- **Study Replays**: Analyze why pros make specific plays
- **Practice Specific Skills**: Kiting, elixir counting, prediction spells
- **Join Competitive Clans**: Learn from high-level players
- **Follow Meta Changes**: Pros adapt quickly to balance updates
- **Copy Pro Decks**: Use exact deck pros use, learn why each card is there
- **Tournament Practice**: Watch CRL, World Finals for highest level gameplay
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

        # Get system prompt based on personality
        system_prompt = personality_prompts.get(personality, personality_prompts["Friendly"])

        # Format chat history for Gemini
        chat_history = []
        for msg in messages:
            if msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "model", "parts": [msg["content"]]})

        # Start chat with system prompt as first message
        chat = model.start_chat(history=[])

        # Combine system prompt with first user message
        if chat_history:
            first_user_msg = chat_history[-1]["parts"][0] if chat_history[-1]["role"] == "user" else ""
            full_prompt = f"{system_prompt}\n\nUser question: {first_user_msg}"
        else:
            full_prompt = system_prompt

        # Generate response
        response = chat.send_message(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024,
            )
        )
        return response.text
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
    /* Clash Royale Arena background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d1b4e 50%, #1a1a2e 100%);
        background-attachment: fixed;
    }

    /* Chat messages */
    .stChatMessage {
        background-color: rgba(30, 30, 60, 0.9) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    .stChatMessage * {
        color: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Input box */
    .stChatInputContainer {
        background-color: rgba(20, 20, 40, 0.95) !important;
    }

    .stChatInputContainer input {
        color: #FFFFFF !important;
        background-color: rgba(40, 40, 80, 0.9) !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #FFD700 !important;
    }

    /* All text white */
    p, span, div, label, li {
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton button {
        background: #8B4513 !important;
        color: white !important;
        border: 2px solid #FFD700 !important;
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

# Initialize Gemini model
model = init_gemini_client()

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
            response = get_ai_response(model, st.session_state.messages, st.session_state.personality)
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