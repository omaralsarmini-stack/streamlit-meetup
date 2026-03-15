MeetUp — Prototype (Streamlit)

This is a small, local prototype of the MeetUp app to demo core flows (Create Meetup, Notifications, Responses, Friends, Profile).

Run locally (Windows / macOS / Linux):

1. Create a virtual environment (recommended):
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```

   Note: use `python3` on systems where `python` points to Python 2.x. You can also run Streamlit without activating the venv by invoking the interpreter directly: `python -m streamlit run app.py`.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

   Or in VS Code:
   - Use the Run view and select the **Streamlit: Run app.py** configuration (added in `.vscode/launch.json`), then press the green ▶️ to start and open the app.
   - Or run the **Run Streamlit** task from the Command Palette (Tasks: Run Task) which runs `streamlit run app.py` in an integrated terminal.

   Note: Running `python app.py` directly will not start the Streamlit server — use `streamlit run` or the VS Code Streamlit debug configuration.

Usage notes:
- Use the sidebar "Act as" control to simulate different users and see their notifications.
- Create a meetup and invite friends to see notifications and respond as other users.
- The app uses in-memory session state, so data resets when you restart Streamlit.

Quick test (fast check that Streamlit is working):

1. Install Streamlit (if not already):
   ```bash
   pip install streamlit
   ```

2. Run the small test app:
   - macOS / Linux:
     ```bash
     streamlit run hello.py
     ```
   - Windows (PowerShell / CMD):
     ```powershell
     streamlit run hello.py
     ```

3. Or use the helper scripts:
   - Windows: double-click `run_hello.bat` or run it in PowerShell/CMD.
   - macOS / Linux: `bash run_hello.sh` (make executable with `chmod +x run_hello.sh` if needed).

   Note: these helper scripts only run `hello.py`; install dependencies once with `pip install -r requirements.txt`.

This will open a browser with a tiny test app showing "My First Streamlit App" and the "Hello, VSCode + Streamlit!" message.

## Trimmed JavaScript Version (Full Core Logic)

If you want a simpler codebase, use `simple_app.js`. It is a compact Node/Express API version that covers users, profiles, friendships, messages, communities, swipes, availability, and meetups.

1. Install Node dependencies:
   ```bash
   npm install express uuid
   ```

2. Run the API:
   ```bash
   node simple_app.js
   ```

3. Server URL:
   - `http://localhost:3000`

4. Main endpoints:
   - `POST /auth/register`
   - `POST /auth/login`
   - `POST /auth/logout`
   - `GET /users`
   - `GET/PUT /profiles/:userId`
   - `POST /friends`, `GET /friends/:userId`
   - `POST /messages`, `GET /messages/conversation?userA=...&userB=...`
   - `POST/GET /communities`
   - `POST /swipes`, `GET /swipes/:userId/matches`
   - `PUT/GET /availability/:userId`
   - `POST/GET /meetups`
