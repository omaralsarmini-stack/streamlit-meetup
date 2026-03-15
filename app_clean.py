import json
import uuid
from datetime import date, datetime, time
from pathlib import Path

import streamlit as st

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
FILES = {
    "users": "users.json",
    "profiles": "profiles.json",
    "messages": "messages.json",
    "friendships": "friendships.json",
    "meetups": "meetups.json",
}


def _load(name: str):
    path = DATA_DIR / FILES[name]
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save(name: str):
    path = DATA_DIR / FILES[name]
    path.write_text(json.dumps(st.session_state[name], indent=2, ensure_ascii=False), encoding="utf-8")


def init_state():
    for k in FILES:
        st.session_state.setdefault(k, _load(k))
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("page", "Home")

    if not st.session_state["users"]:
        seed_demo()


def seed_demo():
    demo = [
        ("omar", "123456", "omar@example.com", 20, "Coffee and football", ["Coffee", "Football"]),
        ("freja", "123456", "freja@example.com", 24, "Music and travel", ["Music", "Travel"]),
        ("kasper", "123456", "kasper@example.com", 22, "Gaming and movies", ["Gaming", "Movies"]),
    ]
    ids = []
    for username, password, email, age, bio, hobbies in demo:
        uid = str(uuid.uuid4())
        ids.append(uid)
        st.session_state["users"][uid] = {
            "id": uid,
            "username": username,
            "password": password,
            "email": email,
            "age": age,
            "online": False,
            "created_at": str(datetime.now()),
        }
        st.session_state["profiles"][uid] = {"user_id": uid, "bio": bio, "location": "Copenhagen", "hobbies": hobbies}
        st.session_state["friendships"][uid] = {"friends": [x for x in ids if x != uid]}

    for uid in ids:
        st.session_state["friendships"][uid]["friends"] = [x for x in ids if x != uid]

    for k in FILES:
        _save(k)


def user(uid: str):
    return st.session_state["users"].get(uid, {})


def profile(uid: str):
    return st.session_state["profiles"].get(uid, {})


def me():
    return st.session_state.get("current_user")


def friends(uid: str):
    rows = st.session_state["friendships"].get(uid, {}).get("friends", [])
    return [x for x in rows if x in st.session_state["users"] and x != uid]


def create_user(username: str, password: str, email: str, age: int):
    if any(u["username"].lower() == username.lower() for u in st.session_state["users"].values()):
        return False, "Username already exists"
    uid = str(uuid.uuid4())
    st.session_state["users"][uid] = {
        "id": uid,
        "username": username,
        "password": password,
        "email": email,
        "age": age,
        "online": False,
        "created_at": str(datetime.now()),
    }
    st.session_state["profiles"][uid] = {"user_id": uid, "bio": "", "location": "", "hobbies": []}
    st.session_state["friendships"][uid] = {"friends": []}
    _save("users")
    _save("profiles")
    _save("friendships")
    return True, "Account created"


def login(username: str, password: str):
    for uid, u in st.session_state["users"].items():
        if u["username"].lower() == username.lower():
            if u["password"] != password:
                return False, "Wrong password"
            u["online"] = True
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = uid
            _save("users")
            return True, "Logged in"
    return False, "User not found"


def logout():
    uid = me()
    if uid in st.session_state["users"]:
        st.session_state["users"][uid]["online"] = False
        _save("users")
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = None
    st.session_state["page"] = "Home"


def send_message(to_uid: str, text: str):
    msg_id = str(uuid.uuid4())
    st.session_state["messages"][msg_id] = {
        "id": msg_id,
        "sender_id": me(),
        "recipient_id": to_uid,
        "text": text,
        "timestamp": str(datetime.now()),
    }
    _save("messages")


def convo(with_uid: str):
    mine = me()
    rows = [
        m
        for m in st.session_state["messages"].values()
        if (m["sender_id"] == mine and m["recipient_id"] == with_uid)
        or (m["sender_id"] == with_uid and m["recipient_id"] == mine)
    ]
    return sorted(rows, key=lambda x: x["timestamp"])


def create_meetup(title: str, when: datetime, location: str, invited: list[str], description: str):
    mid = str(uuid.uuid4())
    st.session_state["meetups"][mid] = {
        "id": mid,
        "title": title,
        "time": str(when),
        "location": location,
        "description": description,
        "creator_id": me(),
        "invited_users": invited,
    }
    _save("meetups")


def auth_ui():
    st.title("MeetUp")
    st.caption("Demo user: omar / 123456")
    t1, t2 = st.tabs(["Login", "Create account"])

    with t1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login", use_container_width=True):
            ok, msg = login(u, p)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()

    with t2:
        u = st.text_input("Username", key="signup_u")
        e = st.text_input("Email", key="signup_e")
        a = st.number_input("Age", min_value=13, max_value=100, value=18)
        p = st.text_input("Password", type="password", key="signup_p")
        if st.button("Create account", use_container_width=True):
            if u and e and p:
                ok, msg = create_user(u, p, e, int(a))
                (st.success if ok else st.error)(msg)
            else:
                st.error("Fill all fields")


def home_ui():
    st.title("Home")
    st.write(f"Welcome {user(me()).get('username', '')}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Friends", len(friends(me())))
    c2.metric("Messages", len(st.session_state["messages"]))
    c3.metric("Meetups", len(st.session_state["meetups"]))


def friends_ui():
    st.title("Friends")
    ids = friends(me())
    if not ids:
        st.info("No friends")
        return
    for uid in ids:
        u = user(uid)
        p = profile(uid)
        with st.expander(u.get("username", "User")):
            st.write(f"Age: {u.get('age', '')}")
            if p.get("bio"):
                st.write(p["bio"])
            if p.get("hobbies"):
                st.write("Hobbies:", ", ".join(p["hobbies"]))


def messages_ui():
    st.title("Messages")
    ids = friends(me())
    if not ids:
        st.info("No friends to message")
        return
    names = {uid: user(uid).get("username", "User") for uid in ids}
    selected_name = st.selectbox("Friend", options=list(names.values()))
    selected_id = next(uid for uid, n in names.items() if n == selected_name)

    for m in convo(selected_id):
        sender = "You" if m["sender_id"] == me() else names[selected_id]
        st.write(f"{sender}: {m['text']}")

    text = st.text_input("Message")
    if st.button("Send", use_container_width=True) and text.strip():
        send_message(selected_id, text.strip())
        st.rerun()


def meetups_ui():
    st.title("Meetups")
    ids = friends(me())
    labels = {uid: user(uid).get("username", "User") for uid in ids}

    title = st.text_input("Title")
    description = st.text_area("Description")
    d = st.date_input("Date", value=date.today())
    t = st.time_input("Time", value=time(18, 0))
    location = st.text_input("Location")
    invited_names = st.multiselect("Invite friends", options=list(labels.values()))

    if st.button("Create meetup", use_container_width=True):
        if not title.strip() or not location.strip():
            st.error("Title and location are required")
        else:
            invited = [uid for uid, n in labels.items() if n in invited_names]
            create_meetup(title.strip(), datetime.combine(d, t), location.strip(), invited, description.strip())
            st.success("Meetup created")

    st.subheader("Your meetups")
    mine = me()
    rows = [m for m in st.session_state["meetups"].values() if m.get("creator_id") == mine or mine in m.get("invited_users", [])]
    for m in sorted(rows, key=lambda x: x.get("time", "")):
        with st.expander(f"{m.get('title', 'Meetup')} - {m.get('time', '')[:16]}"):
            st.write(f"Location: {m.get('location', '')}")
            if m.get("description"):
                st.write(m["description"])


def profile_ui():
    st.title("Profile")
    uid = me()
    u = user(uid)
    p = profile(uid)
    st.write(f"Username: {u.get('username', '')}")
    st.write(f"Email: {u.get('email', '')}")
    st.write(f"Age: {u.get('age', '')}")

    bio = st.text_area("Bio", value=p.get("bio", ""))
    location = st.text_input("Location", value=p.get("location", ""))
    hobbies_raw = st.text_input("Hobbies (comma separated)", value=", ".join(p.get("hobbies", [])))
    if st.button("Save profile", use_container_width=True):
        st.session_state["profiles"][uid] = {
            "user_id": uid,
            "bio": bio,
            "location": location,
            "hobbies": [h.strip() for h in hobbies_raw.split(",") if h.strip()],
        }
        _save("profiles")
        st.success("Saved")


def settings_ui():
    st.title("Settings")
    st.checkbox("Enable notifications", value=True)
    st.slider("Preferred age range", 13, 80, (18, 30))
    if st.button("Log out", use_container_width=True):
        logout()
        st.rerun()


def main():
    st.set_page_config(page_title="MeetUp", layout="wide")
    init_state()

    if not st.session_state["logged_in"]:
        auth_ui()
        return

    with st.sidebar:
        st.header("Navigation")
        options = ["Home", "Friends", "Messages", "Meetups", "Profile", "Settings"]
        st.session_state["page"] = st.radio("Page", options, index=options.index(st.session_state.get("page", "Home")))

    pages = {
        "Home": home_ui,
        "Friends": friends_ui,
        "Messages": messages_ui,
        "Meetups": meetups_ui,
        "Profile": profile_ui,
        "Settings": settings_ui,
    }
    pages[st.session_state["page"]]()


if __name__ == "__main__":
    main()
