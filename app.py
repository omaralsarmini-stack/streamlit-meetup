import streamlit as st
import json
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path

st.set_page_config(
    page_title="Fællesskab",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get help': None,
        'Report a bug': None,
        'About': None
    }
)

# ========== DATABASE SETUP ==========
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)

DEMO_FRIENDS = [
    {
        'username': 'Kasper',
        'email': 'kasper@example.com',
        'age': 22,
        'hobbies': ['Kaffe', 'Gaming', 'Fodbold'],
        'bio': '☕ Altid klar på kaffe og en snak',
        'emoji': '😄'
    },
    {
        'username': 'Freja',
        'email': 'freja@example.com',
        'age': 24,
        'hobbies': ['Musik', 'Træning', 'Rejser'],
        'bio': '🎵 Elsker musik og gode vibes',
        'emoji': '✨'
    },
    {
        'username': 'Sofie',
        'email': 'sofie@example.com',
        'age': 23,
        'hobbies': ['Design', 'Film', 'Madlavning'],
        'bio': '🎨 Kreativ sjæl med grin på',
        'emoji': '🌸'
    },
]

def load_data(filename):
    """Load data from JSON file"""
    filepath = DB_DIR / filename
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}
    return {}

def save_data(filename, data):
    """Save data to JSON file"""
    filepath = DB_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

# ========== STATE INITIALIZATION ==========
def create_sample_data():
    """Create sample users and data to make app more lively"""
    sample_users = [
        {'username': 'Emma_K', 'email': 'emma@example.com', 'age': 24, 'hobbies': ['Yoga', 'Kaffe', 'Læsning'], 'bio': '☕ Kaffe elsker | Yogaentusiast', 'emoji': '✨'},
        {'username': 'Markus', 'email': 'markus@example.com', 'age': 28, 'hobbies': ['Fotografi', 'Vandring', 'Gaming'], 'bio': '📸 Fotograferer det hele | Gamer', 'emoji': '🎮'},
        {'username': 'Sofia_Art', 'email': 'sofia@example.com', 'age': 26, 'hobbies': ['Kunst', 'Design', 'Musik'], 'bio': '🎨 Artist & designer | Musikk-elsker', 'emoji': '🎨'},
        {'username': 'Lars_Fit', 'email': 'lars@example.com', 'age': 30, 'hobbies': ['Træning', 'Football', 'Sundhed'], 'bio': '💪 Fitnessnørd | Football fan', 'emoji': '⚽'},
        {'username': 'Nora_Chef', 'email': 'nora@example.com', 'age': 25, 'hobbies': ['Madlavning', 'Rejser', 'Kaffe'], 'bio': '👨‍🍳 Elsker at lave mad | Rejsejunkie', 'emoji': '🍳'},
        {'username': 'Alex_Dev', 'email': 'alex@example.com', 'age': 29, 'hobbies': ['Programmering', 'Tech', 'Gaming'], 'bio': '💻 Developer | Tech geek', 'emoji': '👨‍💻'},
        {'username': 'Julie_Dance', 'email': 'julie@example.com', 'age': 23, 'hobbies': ['Dans', 'Musik', 'Film'], 'bio': '💃 Danser | Film-elsker', 'emoji': '🎬'},
        {'username': 'Noah_Music', 'email': 'noah@example.com', 'age': 27, 'hobbies': ['Musik', 'Buskespil', 'Rejser'], 'bio': '🎸 Musiker | Buskespiller', 'emoji': '🎵'},
    ]
    
    users = st.session_state.users
    profiles = st.session_state.profiles
    
    for sample in sample_users:
        username = sample['username']
        if not any(u['username'] == username for u in users.values()):
            user_id = str(uuid.uuid4())
            users[user_id] = {
                'id': user_id,
                'username': username,
                'password': '123456',
                'email': sample['email'],
                'age': sample['age'],
                'created_at': str(datetime.now()),
                'online': True if uuid.uuid4().int % 2 == 0 else False
            }
            
            profiles[user_id] = {
                'user_id': user_id,
                'bio': sample['bio'],
                'hobbies': sample['hobbies'],
                'interests': sample['hobbies'],
                'profile_picture': sample['emoji'],
                'location': 'København',
                'looking_for': ['Venner', 'Fællesskaber']
            }
    
    save_data('users.json', users)
    save_data('profiles.json', profiles)
    st.session_state.users = users
    st.session_state.profiles = profiles

def create_sample_communities():
    """Create sample communities"""
    sample_communities = [
        {
            'name': '☕ Kaffe-Entusiaster',
            'description': 'For alle der elsker kaffe! Vi mødes på hyggelige caféer og diskuterer sorter.',
            'hobbies': ['Kaffe', 'Socialsamvær']
        },
        {
            'name': '🎨 Kunstnere & Designere',
            'description': 'Kreativ fællesskab for kunstnere, designere og kreative sjæle.',
            'hobbies': ['Kunst', 'Design', 'Musik']
        },
        {
            'name': '💪 Fitnessbølgen',
            'description': 'Træn sammen, motivér hinanden! Alle fitnessniveauer velkommen.',
            'hobbies': ['Træning', 'Sundhed']
        },
        {
            'name': '🎮 Gamers Forening',
            'description': 'For alle der elsker at spille! Fra casual til hardcore gamers.',
            'hobbies': ['Gaming', 'Tech']
        },
        {
            'name': '📚 Bog-Klubben',
            'description': 'Vi diskuterer bøger og snakker litteratur over kaffe.',
            'hobbies': ['Læsning', 'Kultur']
        },
        {
            'name': '🚴 Cykelvenner',
            'description': 'Cykelture i og omkring København. Alle niveauer.',
            'hobbies': ['Cykling', 'Udendørs', 'Sundhed']
        }
    ]
    
    communities = st.session_state.communities
    
    for sample in sample_communities:
        if not any(c['name'] == sample['name'] for c in communities.values()):
            comm_id = str(uuid.uuid4())
            communities[comm_id] = {
                'id': comm_id,
                'name': sample['name'],
                'description': sample['description'],
                'hobbies': sample['hobbies'],
                'creator_id': 'system',
                'members': [],
                'settings': {},
                'created_at': str(datetime.now())
            }
    
    save_data('communities.json', communities)
    st.session_state.communities = communities

def create_sample_activity_data():
    """Create sample activity across friends, messages, swipes, calendar, and meetups"""
    users = st.session_state.users
    communities = st.session_state.communities

    if len(users) < 2:
        return

    user_ids = list(users.keys())
    primary = user_ids[0]
    others = user_ids[1:4]

    friendships = st.session_state.friendships
    for uid in [primary] + others:
        if uid not in friendships:
            friendships[uid] = {'friends': [], 'pending': []}

    for uid in others:
        if uid not in friendships[primary]['friends']:
            friendships[primary]['friends'].append(uid)
        if primary not in friendships[uid]['friends']:
            friendships[uid]['friends'].append(primary)

    messages = st.session_state.messages
    existing_signatures = {
        (m.get('sender_id'), m.get('recipient_id'), m.get('text'))
        for m in messages.values()
    }

    sample_messages = [
        (others[0] if len(others) > 0 else None, primary, "Hej! Skal vi tage en kaffe i weekenden? ☕"),
        (primary, others[0] if len(others) > 0 else None, "Ja mega gerne! Lørdag kl. 14 passer mig."),
        (others[1] if len(others) > 1 else None, primary, "Jeg har oprettet et lille fitness meetup i morgen 💪"),
        (others[2] if len(others) > 2 else None, primary, "Kunne være fedt med en brætspilsaften 🎲"),
    ]

    for sender_id, recipient_id, text in sample_messages:
        if sender_id and recipient_id:
            signature = (sender_id, recipient_id, text)
            if signature not in existing_signatures:
                msg_id = str(uuid.uuid4())
                messages[msg_id] = {
                    'id': msg_id,
                    'sender_id': sender_id,
                    'recipient_id': recipient_id,
                    'text': text,
                    'timestamp': str(datetime.now() - timedelta(hours=uuid.uuid4().int % 48)),
                    'read': False
                }

    swipe_history = st.session_state.swipe_history
    if primary not in swipe_history:
        swipe_history[primary] = {'liked': [], 'passed': []}

    if len(others) > 0 and others[0] not in swipe_history[primary]['liked']:
        swipe_history[primary]['liked'].append(others[0])
    if len(others) > 1 and others[1] not in swipe_history[primary]['passed']:
        swipe_history[primary]['passed'].append(others[1])

    availability = st.session_state.availability
    if primary not in availability:
        availability[primary] = {}

    date_1 = str(date.today() + timedelta(days=1))
    date_2 = str(date.today() + timedelta(days=2))
    if date_1 not in availability[primary]:
        availability[primary][date_1] = {}
    if date_2 not in availability[primary]:
        availability[primary][date_2] = {}
    availability[primary][date_1]['12:00-15:00'] = True
    availability[primary][date_1]['18:00-21:00'] = True
    availability[primary][date_2]['09:00-12:00'] = True

    meetups = st.session_state.meetups
    existing_titles = {m.get('title') for m in meetups.values()}

    sample_meetups = [
        {
            'title': 'Kaffe & hygge',
            'description': 'Uformelt meetup på café med plads til nye venner.',
            'creator_id': primary,
            'time': str(datetime.now() + timedelta(days=2, hours=3)),
            'location': 'Café Norden',
            'invited_users': others,
            'responses': {}
        },
        {
            'title': 'Brætspilsaften',
            'description': 'Tag dit yndlingsspil med og mød nye mennesker.',
            'creator_id': primary,
            'time': str(datetime.now() + timedelta(days=4, hours=1)),
            'location': 'Kulturhuset',
            'invited_users': others[:2],
            'responses': {}
        }
    ]

    for sample in sample_meetups:
        if sample['title'] not in existing_titles:
            meetup_id = str(uuid.uuid4())
            meetups[meetup_id] = {
                'id': meetup_id,
                'title': sample['title'],
                'description': sample['description'],
                'creator_id': sample['creator_id'],
                'time': sample['time'],
                'location': sample['location'],
                'invited_users': sample['invited_users'],
                'responses': sample['responses'],
                'created_at': str(datetime.now())
            }

    for community in communities.values():
        if 'members' not in community:
            community['members'] = []
        if primary not in community['members'] and len(community['members']) < 2:
            community['members'].append(primary)

    save_data('friendships.json', friendships)
    save_data('messages.json', messages)
    save_data('swipe_history.json', swipe_history)
    save_data('availability.json', availability)
    save_data('meetups.json', meetups)
    save_data('communities.json', communities)

    st.session_state.friendships = friendships
    st.session_state.messages = messages
    st.session_state.swipe_history = swipe_history
    st.session_state.availability = availability
    st.session_state.meetups = meetups
    st.session_state.communities = communities

def init_state():
    """Initialize session state with default values"""
    defaults = {
        'logged_in': False,
        'current_user': None,
        'users': load_data('users.json'),
        'profiles': load_data('profiles.json'),
        'messages': load_data('messages.json'),
        'communities': load_data('communities.json'),
        'meetups': load_data('meetups.json'),
        'friendships': load_data('friendships.json'),
        'availability': load_data('availability.json'),
        'swipe_history': load_data('swipe_history.json'),
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Create sample data if none exists
    if len(st.session_state.users) == 0:
        create_sample_data()
        create_sample_communities()
    # Add sample communities if none exist (even if users already present)
    if len(st.session_state.communities) == 0:
        create_sample_communities()

    # Add sample activity data if app feels empty
    if len(st.session_state.users) > 1:
        if (
            len(st.session_state.friendships) == 0
            or len(st.session_state.messages) == 0
            or len(st.session_state.meetups) == 0
            or len(st.session_state.availability) == 0
        ):
            create_sample_activity_data()

def ensure_demo_friends_for_user(current_user_id):
    """Ensure visible demo friends (non-Omar names) and first incoming messages for current user"""
    users = st.session_state.users
    profiles = st.session_state.profiles
    friendships = st.session_state.friendships
    messages = st.session_state.messages
    meetups = st.session_state.meetups

    demo_user_ids = []
    for sample in DEMO_FRIENDS:
        existing_id = None
        for uid, user in users.items():
            if user.get('username') == sample['username']:
                existing_id = uid
                break

        if existing_id is None:
            existing_id = str(uuid.uuid4())
            users[existing_id] = {
                'id': existing_id,
                'username': sample['username'],
                'password': '123456',
                'email': sample['email'],
                'age': sample['age'],
                'created_at': str(datetime.now()),
                'online': False
            }

        if existing_id not in profiles:
            profiles[existing_id] = {
                'user_id': existing_id,
                'bio': sample['bio'],
                'hobbies': sample['hobbies'],
                'interests': sample['hobbies'],
                'profile_picture': sample['emoji'],
                'location': 'København',
                'looking_for': ['Venner', 'Fællesskaber']
            }

        demo_user_ids.append(existing_id)

    if current_user_id not in friendships:
        friendships[current_user_id] = {'friends': [], 'pending': []}

    for friend_id in demo_user_ids:
        if friend_id == current_user_id:
            continue

        if friend_id not in friendships[current_user_id]['friends']:
            friendships[current_user_id]['friends'].append(friend_id)

        if friend_id not in friendships:
            friendships[friend_id] = {'friends': [], 'pending': []}

        if current_user_id not in friendships[friend_id]['friends']:
            friendships[friend_id]['friends'].append(current_user_id)

    existing_signatures = {
        (m.get('sender_id'), m.get('recipient_id'), m.get('text'))
        for m in messages.values()
    }

    first_messages = [
        "Hej! Skal vi mødes til kaffe i weekenden? ☕",
        "Hey! Vil du med til træning i morgen? 💪",
        "Hej 😊 Jeg har fundet et hyggeligt event vi kan tage til",
    ]

    for idx, friend_id in enumerate(demo_user_ids):
        if friend_id == current_user_id:
            continue
        text = first_messages[idx % len(first_messages)]
        signature = (friend_id, current_user_id, text)
        if signature not in existing_signatures:
            msg_id = str(uuid.uuid4())
            messages[msg_id] = {
                'id': msg_id,
                'sender_id': friend_id,
                'recipient_id': current_user_id,
                'text': text,
                'timestamp': str(datetime.now() - timedelta(hours=2 + idx)),
                'read': False
            }

    existing_titles = {m.get('title') for m in meetups.values()}
    meetup_samples = [
        ('Kaffe med Kasper', 'Lad os tage en rolig kaffe og lære hinanden bedre at kende', 'Original Coffee'),
        ('Walk & Talk med Freja', 'En gåtur og hyggesnak i byen', 'Botanisk Have'),
    ]
    for idx, sample in enumerate(meetup_samples):
        title, description, location = sample
        if title not in existing_titles:
            meetup_id = str(uuid.uuid4())
            creator_id = demo_user_ids[idx % len(demo_user_ids)]
            meetups[meetup_id] = {
                'id': meetup_id,
                'title': title,
                'description': description,
                'creator_id': creator_id,
                'time': str(datetime.now() + timedelta(days=idx + 1, hours=16)),
                'location': location,
                'invited_users': [current_user_id],
                'responses': {},
                'created_at': str(datetime.now())
            }

    save_data('users.json', users)
    save_data('profiles.json', profiles)
    save_data('friendships.json', friendships)
    save_data('messages.json', messages)
    save_data('meetups.json', meetups)

    st.session_state.users = users
    st.session_state.profiles = profiles
    st.session_state.friendships = friendships
    st.session_state.messages = messages
    st.session_state.meetups = meetups

def create_user(username, password, email, age):
    """Create a new user account"""
    user_id = str(uuid.uuid4())
    users = st.session_state.users
    
    if any(u['username'] == username for u in users.values()):
        return False, "Brugernavnet er allerede taget"
    
    users[user_id] = {
        'id': user_id,
        'username': username,
        'password': password,
        'email': email,
        'age': age,
        'created_at': str(datetime.now()),
        'online': False
    }
    save_data('users.json', users)
    st.session_state.users = users
    
    # Create empty profile
    profiles = st.session_state.profiles
    profiles[user_id] = {
        'user_id': user_id,
        'bio': '',
        'hobbies': [],
        'interests': [],
        'profile_picture': '😊',
        'location': '',
        'looking_for': []
    }
    save_data('profiles.json', profiles)
    st.session_state.profiles = profiles
    
    return True, "Konto oprettet! Log ind nu."

def login_user(username, password):
    """Authenticate user"""
    users = st.session_state.users
    for user_id, user in users.items():
        if user['username'] == username and user['password'] == password:
            user['online'] = True
            save_data('users.json', users)
            st.session_state.users = users
            st.session_state.logged_in = True
            st.session_state.current_user = user_id
            ensure_demo_friends_for_user(user_id)
            return True, "Login succesfuly!"
        elif user['username'] == username:
            return False, "Forkert adgangskode"
    return False, "Bruger ikke fundet"

def logout_user():
    """Logout current user"""
    if st.session_state.current_user:
        users = st.session_state.users
        if st.session_state.current_user in users:
            users[st.session_state.current_user]['online'] = False
            save_data('users.json', users)
            st.session_state.users = users
    
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ========== DATA FUNCTIONS ==========
def get_user(user_id):
    """Get user info"""
    return st.session_state.users.get(user_id, {})

def get_profile(user_id):
    """Get user profile"""
    return st.session_state.profiles.get(user_id, {})

def get_current_user_profile():
    """Get current logged-in user's profile"""
    return get_profile(st.session_state.current_user)

def update_profile(profile_data):
    """Update current user's profile"""
    profiles = st.session_state.profiles
    profiles[st.session_state.current_user] = profile_data
    save_data('profiles.json', profiles)
    st.session_state.profiles = profiles

def add_friend(friend_id):
    """Add a friend"""
    friendships = st.session_state.friendships
    if st.session_state.current_user not in friendships:
        friendships[st.session_state.current_user] = {'friends': [], 'pending': []}
    
    if friend_id not in friendships[st.session_state.current_user]['friends']:
        friendships[st.session_state.current_user]['friends'].append(friend_id)
    
    save_data('friendships.json', friendships)
    st.session_state.friendships = friendships

def get_friends(user_id):
    """Get list of friends"""
    friendships = st.session_state.friendships
    if user_id in friendships:
        raw_friends = friendships[user_id].get('friends', [])
        cleaned = [
            fid for fid in raw_friends
            if fid in st.session_state.users and fid != user_id
        ]
        # remove duplicates while keeping order
        return list(dict.fromkeys(cleaned))
    return []

def send_message(recipient_id, message_text):
    """Send a message"""
    messages = st.session_state.messages
    msg_id = str(uuid.uuid4())
    
    messages[msg_id] = {
        'id': msg_id,
        'sender_id': st.session_state.current_user,
        'recipient_id': recipient_id,
        'text': message_text,
        'timestamp': str(datetime.now()),
        'read': False
    }
    save_data('messages.json', messages)
    st.session_state.messages = messages

def get_conversation(other_user_id):
    """Get messages with a specific user"""
    messages = st.session_state.messages
    current = st.session_state.current_user
    
    conversation = [
        m for m in messages.values()
        if (m['sender_id'] == current and m['recipient_id'] == other_user_id) or
           (m['sender_id'] == other_user_id and m['recipient_id'] == current)
    ]
    return sorted(conversation, key=lambda x: x['timestamp'])

def create_community(name, description, hobbies, settings):
    """Create a new community"""
    communities = st.session_state.communities
    community_id = str(uuid.uuid4())
    
    communities[community_id] = {
        'id': community_id,
        'name': name,
        'description': description,
        'hobbies': hobbies,
        'creator_id': st.session_state.current_user,
        'members': [st.session_state.current_user],
        'settings': settings,
        'created_at': str(datetime.now())
    }
    save_data('communities.json', communities)
    st.session_state.communities = communities
    add_friend(community_id)
    return community_id

def get_matching_profiles(exclude_swipes=True):
    """Get profiles that match current user's interests"""
    current = get_current_user_profile()
    current_hobbies = set(current.get('hobbies', []))
    
    matches = []
    for user_id, profile in st.session_state.profiles.items():
        if user_id == st.session_state.current_user:
            continue
        
        profile_hobbies = set(profile.get('hobbies', []))
        if current_hobbies & profile_hobbies:
            if exclude_swipes:
                history = st.session_state.swipe_history.get(st.session_state.current_user, {})
                swiped_ids = set(history.get('liked', [])) | set(history.get('passed', []))
                if user_id not in swiped_ids:
                    matches.append((user_id, profile))
            else:
                matches.append((user_id, profile))
    
    return matches

def save_swipe(target_id, liked):
    """Record a swipe action"""
    swipe_history = st.session_state.swipe_history
    current = st.session_state.current_user
    
    if current not in swipe_history:
        swipe_history[current] = {'liked': [], 'passed': []}
    
    if liked:
        if target_id not in swipe_history[current]['liked']:
            swipe_history[current]['liked'].append(target_id)
            if current in swipe_history.get(target_id, {}).get('liked', []):
                add_friend(target_id)
    else:
        if target_id not in swipe_history[current]['passed']:
            swipe_history[current]['passed'].append(target_id)
    
    save_data('swipe_history.json', swipe_history)
    st.session_state.swipe_history = swipe_history

def set_availability(date_str, time_slot, available):
    """Set availability for a specific time"""
    availability = st.session_state.availability
    current = st.session_state.current_user
    
    if current not in availability:
        availability[current] = {}
    
    if date_str not in availability[current]:
        availability[current][date_str] = {}
    
    availability[current][date_str][time_slot] = available
    save_data('availability.json', availability)
    st.session_state.availability = availability

def create_meetup(title, description, scheduled_time, location, invited_users):
    """Create a meetup event"""
    meetups = st.session_state.meetups
    meetup_id = str(uuid.uuid4())
    
    meetups[meetup_id] = {
        'id': meetup_id,
        'title': title,
        'description': description,
        'creator_id': st.session_state.current_user,
        'time': str(scheduled_time),
        'location': location,
        'invited_users': invited_users,
        'responses': {},
        'created_at': str(datetime.now())
    }
    save_data('meetups.json', meetups)
    st.session_state.meetups = meetups
    return meetup_id

# ========== UI COMPONENTS ==========
def render_auth_page():
    """Render login/signup page"""
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 👥 Log ind")
        st.caption("Demo login: brug fx Emma_K med kode 123456")
        username = st.text_input("Brugernavn", key="login_username")
        password = st.text_input("Adgangskode", type="password", key="login_password")
        
        if st.button("🔓 Log ind", use_container_width=True):
            success, msg = login_user(username, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    with col2:
        st.markdown("## ✨ Opret konto")
        new_username = st.text_input("Brugernavn", key="signup_username")
        new_email = st.text_input("Email", key="signup_email")
        new_age = st.number_input("Alder", 13, 100, 18, key="signup_age")
        new_password = st.text_input("Adgangskode", type="password", key="signup_password")
        
        if st.button("✨ Opret konto", use_container_width=True):
            if new_username and new_email and new_password:
                success, msg = create_user(new_username, new_password, new_email, new_age)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.error("Udfyld alle felter")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_home_page():
    """Render home page with stats and quick actions"""
    st.markdown("## 🏠 Hjem")
    
    user = get_user(st.session_state.current_user)
    st.markdown(f"### Velkommen, {user.get('username')}! 👋")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        friends = get_friends(st.session_state.current_user)
        st.metric("👥 Venner", len(friends))
        if st.button("👥 Se venner", key="home_view_friends", use_container_width=True):
            st.session_state.current_page = "Venner"
            st.rerun()
    
    with col2:
        st.metric("📅 Møder", len([m for m in st.session_state.meetups.values() if m['creator_id'] == st.session_state.current_user]))
    
    with col3:
        st.metric("💬 Beskeder", len([m for m in st.session_state.messages.values() if m['recipient_id'] == st.session_state.current_user and not m['read']]))
    
    st.markdown("---")
    st.markdown("### 🎯 Hurtig adgang")
    
    # Create quick access cards
    card1, card2 = st.columns(2)
    
    with card1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🔄</div>
            <div style="font-weight: bold; margin-bottom: 10px;">Swipe venner & fællesskaber</div>
            <div style="font-size: 12px; opacity: 0.9;">Find nye forbindelser baseret på dine interesser</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Gå til Swipe →", key="home_swipe", use_container_width=True):
            st.session_state.current_page = "Swipe"
            st.rerun()
    
    with card2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">💬</div>
            <div style="font-weight: bold; margin-bottom: 10px;">Beskeder</div>
            <div style="font-size: 12px; opacity: 0.9;">Chat med dine venner</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Gå til Beskeder →", key="home_messages", use_container_width=True):
            st.session_state.current_page = "Beskeder"
            st.rerun()
    
    card3, card4 = st.columns(2)
    
    with card3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">📅</div>
            <div style="font-weight: bold; margin-bottom: 10px;">Planlæg møde</div>
            <div style="font-size: 12px; opacity: 0.9;">Opret et nyt møde</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Gå til møde planning →", key="home_meetup", use_container_width=True):
            st.session_state.current_page = "Planlæg møde"
            st.rerun()
    
    with card4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">👤</div>
            <div style="font-weight: bold; margin-bottom: 10px;">Min profil</div>
            <div style="font-size: 12px; opacity: 0.9;">Rediger dine hobbyer & info</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Gå til min profil →", key="home_profile", use_container_width=True):
            st.session_state.current_page = "Profil"
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Din aktivitet")
    
    activity_col1, activity_col2 = st.columns(2)
    
    with activity_col1:
        st.markdown("**Din tilgængelighed**")
        if st.button("📅 Planlægningskalender", use_container_width=True, key="home_calendar"):
            st.session_state.current_page = "📅 Planlægningskalender"
            st.rerun()
    
    with activity_col2:
        st.markdown("**App indstillinger**")
        if st.button("⚙️ Indstillinger", use_container_width=True, key="home_settings"):
            st.session_state.current_page = "⚙️ Indstillinger"
            st.rerun()

def render_swipe_page():
    """Render Tinder-style swiping for friends/communities"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_swipe", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 🔄 Swipe venner og fællesskaber")
    
    tab1, tab2 = st.tabs(["👥 Venner", "🏘️ Fællesskaber"])
    
    with tab1:
        st.markdown("### Find nye venner med samme interesser")
        
        matches = get_matching_profiles()
        
        if not matches:
            st.info("Ingen nye venner at vise. Opdater dine interesser!")
        else:
            user_id, profile = matches[0]
            user = get_user(user_id)
            
            st.markdown(f"### {user.get('username', 'Bruger')} {profile.get('profile_picture', '😊')}")
            st.markdown(f"**Alder:** {user.get('age', 'N/A')}")
            
            if profile.get('bio'):
                st.markdown(f"**Bio:** {profile['bio']}")
            
            if profile.get('hobbies'):
                hobbies_str = ", ".join(profile['hobbies'])
                st.markdown(f"**Hobbyer:** {hobbies_str}")
            
            if profile.get('location'):
                st.markdown(f"📍 **Lokation:** {profile['location']}")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("❌ Næste", use_container_width=True):
                    save_swipe(user_id, False)
                    st.rerun()
            
            with col3:
                if st.button("❤️ Følg", use_container_width=True):
                    save_swipe(user_id, True)
                    st.success("Svipted hendet!")
                    st.rerun()
    
    with tab2:
        st.markdown("### Find nye fællesskaber")
        
        communities = list(st.session_state.communities.values())
        
        if not communities:
            st.info("Ingen fællesskaber endnu. Opret en!")
        else:
            for community in communities:
                with st.expander(f"🏘️ {community['name']}"):
                    st.markdown(community['description'])
                    hobbies_str = ", ".join(community['hobbies'])
                    st.markdown(f"**Interesser:** {hobbies_str}")
                    
                    if st.button(f"Deltag", key=f"join_{community['id']}"):
                        community['members'].append(st.session_state.current_user)
                        save_data('communities.json', st.session_state.communities)
                        st.success("Du har sluttet dig til fællesskabet!")
                        st.rerun()

def render_messages_page():
    """Render messaging system"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_messages", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 💬 Beskeder")
    
    friends = get_friends(st.session_state.current_user)
    friend_map = {uid: get_user(uid).get('username', 'Bruger') for uid in friends}
    
    if not friends:
        st.info("Du har ingen venner endnu!")
        return
    
    selected_friend = st.selectbox("Vælg en ven", options=list(friend_map.values()), format_func=lambda x: x)
    selected_friend_id = [uid for uid, name in friend_map.items() if name == selected_friend][0]
    
    st.markdown(f"### Chat med {selected_friend}")
    
    conversation = get_conversation(selected_friend_id)
    
    for msg in conversation:
        sender_name = get_user(msg['sender_id']).get('username', 'Bruger')
        is_current = msg['sender_id'] == st.session_state.current_user
        
        if is_current:
            st.markdown(f"<div style='text-align:right'><b>Du:</b> {msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><b>{sender_name}:</b> {msg['text']}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    new_message = st.text_input("Skriv en besked...")
    if st.button("📤 Send", use_container_width=True):
        if new_message:
            send_message(selected_friend_id, new_message)
            st.success("Besked sendt!")
            st.rerun()

def render_friends_page():
    """Render friends list page"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_friends", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 👥 Venner")

    friends = get_friends(st.session_state.current_user)

    if not friends:
        st.info("Du har ingen venner endnu")
        return

    st.markdown(f"Du har **{len(friends)}** venner")
    st.markdown("---")

    for friend_id in friends:
        user = get_user(friend_id)
        profile = get_profile(friend_id)

        username = user.get('username', 'Bruger')
        age = user.get('age', 'N/A')
        emoji = profile.get('profile_picture', '😊')
        bio = profile.get('bio', '')

        with st.container():
            st.markdown(f"### {emoji} {username}")
            st.markdown(f"**Alder:** {age}")
            if bio:
                st.markdown(f"**Bio:** {bio}")
            st.markdown("---")

def render_profile_page():
    """Render user profile editing"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_profile", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 👤 Profil")
    
    user = get_user(st.session_state.current_user)
    profile = get_current_user_profile()
    
    st.markdown(f"### {user.get('username', 'Bruger')}")
    st.markdown(f"**Email:** {user.get('email', 'N/A')}")
    st.markdown(f"**Alder:** {user.get('age', 'N/A')}")
    
    st.markdown("---")
    st.markdown("### 📝 Rediger profil")
    
    emoji = st.text_input("Profilikon", value=profile.get('profile_picture', '😊'), max_chars=1)
    bio = st.text_area("Biografi", value=profile.get('bio', ''), placeholder="Beskriv dig selv...")
    location = st.text_input("Lokation", value=profile.get('location', ''))
    
    hobbies_input = st.text_input("Hobbyer (komma-separeret)", value=", ".join(profile.get('hobbies', [])))
    hobbies = [h.strip() for h in hobbies_input.split(',') if h.strip()]
    
    interests_input = st.text_input("Interesser (komma-separeret)", value=", ".join(profile.get('interests', [])))
    interests = [i.strip() for i in interests_input.split(',') if i.strip()]
    
    looking_for = st.multiselect(
        "Hvad leder du efter?",
        options=["Venner", "Fællesskaber", "Begge"],
        default=profile.get('looking_for', [])
    )
    
    if st.button("💾 Gem profil", use_container_width=True):
        profile.update({
            'profile_picture': emoji,
            'bio': bio,
            'location': location,
            'hobbies': hobbies,
            'interests': interests,
            'looking_for': looking_for
        })
        update_profile(profile)
        st.success("Profil gemt!")

def render_calendar_page():
    """Render planning calendar for availability"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_calendar", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 📅 Planlægningskalender")
    st.markdown("Vælg hvornår du er tilgængelig for møder")
    
    selected_date = st.date_input("Vælg dato")
    
    time_slots = ["09:00-12:00", "12:00-15:00", "15:00-18:00", "18:00-21:00"]
    
    availability = st.session_state.availability.get(st.session_state.current_user, {}).get(str(selected_date), {})
    
    for slot in time_slots:
        is_available = st.checkbox(
            slot,
            value=availability.get(slot, False),
            key=f"slot_{selected_date}_{slot}"
        )
        set_availability(str(selected_date), slot, is_available)
    
    st.success("Tilgængelighed gemt!")

def render_meetup_planning_page():
    """Render meetup planning and creation"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_meetup", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## 🎉 Planlæg et møde")
    
    title = st.text_input("Mødetitel", placeholder="F.eks. Kaffe ved Central Park")
    description = st.text_area("Beskrivelse", placeholder="Hvad skal vi lave?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meetup_date = st.date_input("Dato")
    
    with col2:
        meetup_time = st.time_input("Tid")
    
    location = st.text_input("Lokation", placeholder="F.eks. Central Park Café")
    
    friends = get_friends(st.session_state.current_user)
    friend_map = {uid: get_user(uid).get('username', 'Bruger') for uid in friends}
    
    invited = st.multiselect(
        "Inviter venner",
        options=list(friend_map.values()),
        format_func=lambda x: x
    )
    
    invited_ids = [uid for uid, name in friend_map.items() if name in invited]
    
    if st.button("📤 Opret møde", use_container_width=True):
        if title and location:
            scheduled_time = datetime.combine(meetup_date, meetup_time)
            create_meetup(title, description, scheduled_time, location, invited_ids)
            st.success("Møde oprettet! Invitationer sendt! 🎉")
            
            for friend_id in invited_ids:
                send_message(friend_id, f"Du er inviteret til: {title} - {location} kl. {meetup_time}")
        else:
            st.error("Udfyld mindst titel og lokation")

    st.markdown("---")
    st.markdown("### 📋 Dine møder")

    current_user = st.session_state.current_user
    relevant_meetups = [
        meetup for meetup in st.session_state.meetups.values()
        if meetup.get('creator_id') == current_user or current_user in meetup.get('invited_users', [])
    ]

    if not relevant_meetups:
        st.info("Du har ingen møder endnu")
    else:
        relevant_meetups = sorted(relevant_meetups, key=lambda m: str(m.get('time', '')))
        for meetup in relevant_meetups:
            creator = get_user(meetup.get('creator_id', '')).get('username', 'Ukendt')
            with st.expander(f"📌 {meetup.get('title', 'Møde')} • {meetup.get('time', '')[:16]}"):
                st.markdown(f"**Arrangør:** {creator}")
                st.markdown(f"**Lokation:** {meetup.get('location', 'Ikke angivet')}")
                if meetup.get('description'):
                    st.markdown(f"**Beskrivelse:** {meetup['description']}")

                invited_names = [
                    get_user(uid).get('username', 'Bruger')
                    for uid in meetup.get('invited_users', [])
                    if uid in st.session_state.users
                ]
                if invited_names:
                    st.markdown(f"**Inviterede:** {', '.join(invited_names)}")

def render_settings_page():
    """Render app settings"""
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Tilbage", key="back_settings", use_container_width=True):
            st.session_state.page = "Hjem"
            st.rerun()
    with col_title:
        st.markdown("## ⚙️ Indstillinger")
    st.markdown("Tilpas din oplevelse og kontroller dine præferencer")
    
    st.markdown("---")
    
    # Theme Section
    st.markdown("### 🎨 Tema & Udseende")
    theme_col1, theme_col2 = st.columns([1, 2])
    with theme_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🎨</div>
            <div style="font-weight: bold;">Tema</div>
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">Vælg dit foretrukne design</div>
        </div>
        """, unsafe_allow_html=True)
    
    with theme_col2:
        theme = st.radio("Vælg tema", ["☀️ Lys", "🌙 Mørk"], horizontal=True)
        st.session_state.theme = theme
    
    st.markdown("---")
    
    # Notifications Section
    st.markdown("### 🔔 Notifikationer")
    notif_col1, notif_col2 = st.columns([1, 2])
    with notif_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🔔</div>
            <div style="font-weight: bold;">Alerts</div>
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">Få besked når der sker noget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with notif_col2:
        st.checkbox("🎉 Notifikation når møder skabes", value=True)
        st.checkbox("💬 Notifikation når venner svarer", value=True)
        st.checkbox("👥 Notifikation fra fællesskaber", value=True)
    
    st.markdown("---")
    
    # Search & Discovery Section
    st.markdown("### 🔍 Søg & Opdag")
    search_col1, search_col2 = st.columns([1, 2])
    with search_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🔍</div>
            <div style="font-weight: bold;">Søgekarakteristika</div>
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">Ret dine søgeindstillinger</div>
        </div>
        """, unsafe_allow_html=True)
    
    with search_col2:
        st.checkbox("💫 Vis communities med andre interesser", value=False)
        age_range = st.slider("📍 Aldersgruppe for søgning", 13, 80, (18, 30))
        st.info(f"Du søger efter personer mellem {age_range[0]} og {age_range[1]} år")
    
    st.markdown("---")
    
    # Privacy & Security Section
    st.markdown("### 🔐 Privatliv & Sikkerhed")
    privacy_col1, privacy_col2 = st.columns([1, 2])
    with privacy_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🔐</div>
            <div style="font-weight: bold;">Sikkerhed</div>
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">Beskyt dine oplysninger</div>
        </div>
        """, unsafe_allow_html=True)
    
    with privacy_col2:
        st.checkbox("🕵️ Privat profil", value=False)
        st.checkbox("📅 Skjul tilgængelighed for andre", value=False)
        st.checkbox("💭 Skjul mine interesser", value=False)
    
    st.markdown("---")
    
    # Account Section
    st.markdown("### 👤 Konto")
    user = get_user(st.session_state.current_user)
    
    if user:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Brugernavn:** {user.get('username')}")
            st.write(f"**Email:** {user.get('email')}")
        with col2:
            st.write(f"**Alder:** {user.get('age')}")
            st.write(f"**Oprettet:** {user.get('created_at')[:10]}")
    
    st.markdown("---")
    
    # Logout Button
    logout_col1, logout_col2, logout_col3 = st.columns([1, 1, 1])
    with logout_col2:
        if st.button("🚪 Log ud fra appen", use_container_width=True):
            logout_user()
            st.session_state.page = "Hjem"
            st.rerun()

# ========== STYLING ==========
def inject_styles():
    """Inject custom CSS for the app"""
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body, .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #eef2f7 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .stSidebar { width: 100% !important; }
        .stMainBlockContainer { padding: 0.5rem !important; }
        .stButton > button { padding: 12px 16px !important; font-size: 14px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 16px !important; }
    }
    
    /* Welcome container */
    .welcome-container {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background: #f5f5f5;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Columns spacing */
    .stColumn { padding: 0 8px; }
    .stColumnBlock { gap: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    init_state()

    inject_styles()
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 👥 Fællesskab")
        st.markdown("Forbind med venner og fællesskaber")
    
    # Authentication check
    if not st.session_state.logged_in:
        render_auth_page()
        return
    
    # Main navigation
    with st.sidebar:
        st.markdown("---")
        user = get_user(st.session_state.current_user)
        st.markdown(f"**Logget ind som:** {user.get('username', 'Bruger')}")
        
        pages = [
            "Hjem",
            "Venner",
            "Swipe",
            "Beskeder",
            "Profil",
            "📅 Planlægningskalender",
            "Planlæg møde",
            "⚙️ Indstillinger"
        ]
        
        current_page = st.session_state.get('current_page', st.session_state.get('page', 'Hjem'))
        page_index = pages.index(current_page) if current_page in pages else 0
        
        page = st.radio("Navigation", pages, index=page_index)
        st.session_state.page = page
        if 'current_page' in st.session_state:
            del st.session_state['current_page']
    
    # Render selected page
    if st.session_state.page == "Hjem":
        render_home_page()
    elif st.session_state.page == "Venner":
        render_friends_page()
    elif st.session_state.page == "Swipe":
        render_swipe_page() 
    elif st.session_state.page == "Beskeder":
        render_messages_page()
    elif st.session_state.page == "Profil":
        render_profile_page()
    elif st.session_state.page == "📅 Planlægningskalender":
        render_calendar_page()
    elif st.session_state.page == "Planlæg møde":
        render_meetup_planning_page()
    elif st.session_state.page == "⚙️ Indstillinger":
        render_settings_page()

if __name__ == "__main__":
    main()
