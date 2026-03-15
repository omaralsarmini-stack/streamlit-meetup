const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

const DATA_DIR = path.join(__dirname, 'data');
const DATASETS = {
  users: 'users.json',
  profiles: 'profiles.json',
  communities: 'communities.json',
  meetups: 'meetups.json',
  messages: 'messages.json',
  friendships: 'friendships.json',
  availability: 'availability.json',
  swipe_history: 'swipe_history.json',
};

function dbFile(name) {
  return path.join(DATA_DIR, DATASETS[name]);
}

async function ensureDataDir() {
  await fs.mkdir(DATA_DIR, { recursive: true });
}

async function load(name) {
  try {
    const text = await fs.readFile(dbFile(name), 'utf8');
    return JSON.parse(text);
  } catch {
    return {};
  }
}

async function save(name, data) {
  await fs.writeFile(dbFile(name), JSON.stringify(data, null, 2), 'utf8');
}

function sanitizeUser(user) {
  const { password, ...safeUser } = user;
  return safeUser;
}

function listValues(mapObj) {
  return Object.values(mapObj || {});
}

async function bootstrap() {
  await ensureDataDir();
  for (const key of Object.keys(DATASETS)) {
    const data = await load(key);
    if (typeof data !== 'object' || data === null || Array.isArray(data)) {
      await save(key, {});
    }
  }

  const users = await load('users');
  if (Object.keys(users).length === 0) {
    const id = uuidv4();
    users[id] = {
      id,
      username: 'demo',
      password: 'demo',
      email: 'demo@example.com',
      age: 25,
      createdAt: new Date().toISOString(),
      online: false,
    };
    await save('users', users);

    const profiles = await load('profiles');
    profiles[id] = {
      user_id: id,
      bio: 'Demo profile',
      hobbies: ['Coding'],
      interests: ['Coding'],
      profile_picture: '😊',
      location: 'København',
      looking_for: ['Venner'],
    };
    await save('profiles', profiles);
  }
}

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.get('/', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>MeetUp API</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; line-height: 1.5; }
          h1 { margin-bottom: 8px; }
          ul { padding-left: 18px; }
          code { background: #f4f4f4; padding: 2px 6px; border-radius: 6px; }
          .box { background: #fafafa; border: 1px solid #eee; border-radius: 10px; padding: 14px; margin: 14px 0; }
          a { text-decoration: none; }
        </style>
      </head>
      <body>
        <h1>MeetUp Trimmed API</h1>
        <p>Server is running. This is a backend API (JSON), not the full mobile/web UI.</p>

        <div class="box">
          <h3>Quick Links (GET)</h3>
          <ul>
            <li><a href="/health">/health</a></li>
            <li><a href="/users">/users</a></li>
            <li><a href="/communities">/communities</a></li>
            <li><a href="/meetups">/meetups</a></li>
          </ul>
        </div>

        <div class="box">
          <h3>POST/PUT Examples (PowerShell)</h3>
          <p><code>Invoke-RestMethod -Method Post -Uri http://localhost:3000/auth/register -ContentType 'application/json' -Body '{"username":"test1","password":"123","email":"test1@mail.com"}'</code></p>
          <p><code>Invoke-RestMethod -Method Post -Uri http://localhost:3000/auth/login -ContentType 'application/json' -Body '{"username":"test1","password":"123"}'</code></p>
        </div>
      </body>
    </html>
  `);
});

app.post('/auth/register', async (req, res) => {
  const { username, password, email, age = null } = req.body;
  if (!username || !password || !email) {
    return res.status(400).json({ error: 'username, password and email are required' });
  }

  const users = await load('users');
  if (listValues(users).some((u) => u.username === username)) {
    return res.status(409).json({ error: 'username already taken' });
  }

  const id = uuidv4();
  users[id] = {
    id,
    username,
    password,
    email,
    age,
    createdAt: new Date().toISOString(),
    online: false,
  };
  await save('users', users);

  const profiles = await load('profiles');
  profiles[id] = {
    user_id: id,
    bio: '',
    hobbies: [],
    interests: [],
    profile_picture: '😊',
    location: '',
    looking_for: [],
  };
  await save('profiles', profiles);

  return res.json({ success: true, user: sanitizeUser(users[id]) });
});

app.post('/auth/login', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'username and password are required' });
  }

  const users = await load('users');
  const user = listValues(users).find((u) => u.username === username && u.password === password);
  if (!user) {
    return res.status(401).json({ error: 'invalid credentials' });
  }

  users[user.id].online = true;
  await save('users', users);
  return res.json({ success: true, user: sanitizeUser(users[user.id]) });
});

app.post('/auth/logout', async (req, res) => {
  const { userId } = req.body;
  if (!userId) {
    return res.status(400).json({ error: 'userId is required' });
  }

  const users = await load('users');
  if (!users[userId]) {
    return res.status(404).json({ error: 'user not found' });
  }

  users[userId].online = false;
  await save('users', users);
  return res.json({ success: true });
});

app.get('/users', async (req, res) => {
  const users = await load('users');
  return res.json(listValues(users).map(sanitizeUser));
});

app.get('/profiles/:userId', async (req, res) => {
  const profiles = await load('profiles');
  const profile = profiles[req.params.userId];
  if (!profile) {
    return res.status(404).json({ error: 'profile not found' });
  }
  return res.json(profile);
});

app.put('/profiles/:userId', async (req, res) => {
  const profiles = await load('profiles');
  const current = profiles[req.params.userId] || { user_id: req.params.userId };
  profiles[req.params.userId] = { ...current, ...req.body, user_id: req.params.userId };
  await save('profiles', profiles);
  return res.json({ success: true, profile: profiles[req.params.userId] });
});

app.post('/friends', async (req, res) => {
  const { userId, friendId } = req.body;
  if (!userId || !friendId || userId === friendId) {
    return res.status(400).json({ error: 'valid userId and friendId are required' });
  }

  const friendships = await load('friendships');
  const key = [userId, friendId].sort().join('_');
  friendships[key] = {
    id: key,
    users: [userId, friendId],
    createdAt: new Date().toISOString(),
  };
  await save('friendships', friendships);
  return res.json({ success: true, friendship: friendships[key] });
});

app.get('/friends/:userId', async (req, res) => {
  const { userId } = req.params;
  const friendships = await load('friendships');
  const friendIds = listValues(friendships)
    .filter((f) => Array.isArray(f.users) && f.users.includes(userId))
    .map((f) => f.users.find((id) => id !== userId))
    .filter(Boolean);

  const users = await load('users');
  const friends = friendIds.map((id) => users[id]).filter(Boolean).map(sanitizeUser);
  return res.json(friends);
});

app.post('/messages', async (req, res) => {
  const { senderId, recipientId, text } = req.body;
  if (!senderId || !recipientId || !text) {
    return res.status(400).json({ error: 'senderId, recipientId and text are required' });
  }

  const messages = await load('messages');
  const id = uuidv4();
  messages[id] = {
    id,
    senderId,
    recipientId,
    text,
    createdAt: new Date().toISOString(),
  };
  await save('messages', messages);
  return res.json({ success: true, message: messages[id] });
});

app.get('/messages/conversation', async (req, res) => {
  const { userA, userB } = req.query;
  if (!userA || !userB) {
    return res.status(400).json({ error: 'userA and userB are required' });
  }

  const messages = await load('messages');
  const conversation = listValues(messages)
    .filter(
      (m) =>
        (m.senderId === userA && m.recipientId === userB) ||
        (m.senderId === userB && m.recipientId === userA),
    )
    .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

  return res.json(conversation);
});

app.post('/communities', async (req, res) => {
  const { name, description = '', hobbies = [], creatorId = null, settings = {} } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'name is required' });
  }

  const communities = await load('communities');
  const id = uuidv4();
  communities[id] = {
    id,
    name,
    description,
    hobbies,
    creatorId,
    members: creatorId ? [creatorId] : [],
    settings,
    createdAt: new Date().toISOString(),
  };
  await save('communities', communities);
  return res.json({ success: true, community: communities[id] });
});

app.get('/communities', async (req, res) => {
  const communities = await load('communities');
  return res.json(listValues(communities));
});

app.post('/swipes', async (req, res) => {
  const { userId, targetId, liked } = req.body;
  if (!userId || !targetId || typeof liked !== 'boolean') {
    return res.status(400).json({ error: 'userId, targetId and liked(boolean) are required' });
  }

  const swipes = await load('swipe_history');
  const id = uuidv4();
  swipes[id] = {
    id,
    userId,
    targetId,
    liked,
    createdAt: new Date().toISOString(),
  };
  await save('swipe_history', swipes);
  return res.json({ success: true, swipe: swipes[id] });
});

app.get('/swipes/:userId/matches', async (req, res) => {
  const { userId } = req.params;
  const swipes = await load('swipe_history');
  const users = await load('users');

  const myLikes = new Set(
    listValues(swipes)
      .filter((s) => s.userId === userId && s.liked)
      .map((s) => s.targetId),
  );

  const reciprocalLikes = new Set(
    listValues(swipes)
      .filter((s) => s.targetId === userId && s.liked)
      .map((s) => s.userId),
  );

  const matchIds = [...myLikes].filter((id) => reciprocalLikes.has(id));
  const matches = matchIds.map((id) => users[id]).filter(Boolean).map(sanitizeUser);
  return res.json(matches);
});

app.put('/availability/:userId', async (req, res) => {
  const { userId } = req.params;
  const { date, timeSlot, available } = req.body;
  if (!date || !timeSlot || typeof available !== 'boolean') {
    return res.status(400).json({ error: 'date, timeSlot and available(boolean) are required' });
  }

  const availability = await load('availability');
  const key = `${userId}_${date}_${timeSlot}`;
  availability[key] = {
    id: key,
    userId,
    date,
    timeSlot,
    available,
    updatedAt: new Date().toISOString(),
  };
  await save('availability', availability);
  return res.json({ success: true, availability: availability[key] });
});

app.get('/availability/:userId', async (req, res) => {
  const { userId } = req.params;
  const availability = await load('availability');
  return res.json(listValues(availability).filter((a) => a.userId === userId));
});

app.post('/meetups', async (req, res) => {
  const {
    title,
    description = '',
    scheduledTime,
    location = '',
    organizerId = null,
    invitedUsers = [],
  } = req.body;

  if (!title || !scheduledTime) {
    return res.status(400).json({ error: 'title and scheduledTime are required' });
  }

  const meetups = await load('meetups');
  const id = uuidv4();
  meetups[id] = {
    id,
    title,
    description,
    scheduledTime,
    location,
    organizerId,
    invitedUsers,
    createdAt: new Date().toISOString(),
  };
  await save('meetups', meetups);
  return res.json({ success: true, meetup: meetups[id] });
});

app.get('/meetups', async (req, res) => {
  const meetups = await load('meetups');
  return res.json(listValues(meetups));
});

const PORT = process.env.PORT || 3000;

bootstrap().then(() => {
  app.listen(PORT, () => {
    console.log(`Trimmed full API running on http://localhost:${PORT}`);
  });
});
