# My Discord Bot Base Template

Hey there! 👋 This is my go-to template for building Discord bots. I use it for all my freelance projects, from simple utility bots to complex economy systems.

It’s built with **disnake** and designed for speed, clean code, and easy handover to clients or teammates.

## 📂 What's Inside?

I organized this repo so I never have to reinvent the wheel:

*   **`/classes`** – The engine room. All my custom classes live here (like the EventHandler system we discussed). They’re reusable across different bots.
*   **`/cogs`** – The brains. All commands and logic are split into separate cogs.  
    *   *Pro Tip:* The `__init__.py` auto-loads them, so I don’t waste time editing `main.py` every time I add a new command.
*   **`/data`** – The memory. Handles connections to databases (JSON, SQLite, etc.). Keeps the logic clean and the data safe.
*   **`/dependencies`** – Global constants and shared variables. Everything I need everywhere, in one place.
*   **`config.py`** – The control panel. Sets up all variables and secrets. (In production, I load tokens from a `.env` file, not directly here).
*   **`main.py`** – The starter button. Just runs this, and the bot goes online.

## ⚡ Why use this base?

*   **Fast Delivery**: Since the structure is ready, I can focus 100% on the client's specific feature, not setting up the project.
*   **Team Friendly**: If I work with other devs (like in my team workflow), everyone knows exactly where to put code. No "Where does this go?" questions.
*  **Teaching Ready**: I also use this structure in my courses for kids. It teaches good habits early: separating logic, commands, and data.

## 🛠️ How to Use It

1.  **Clone it**: `git clone [URL]`
2.  **Install deps**: `pip install -r requirements.txt`
3.  **Set up config**: Edit `config.py` (or better, use a `.env` file) to add your bot token.
4.  **Run**: `python main.py`

## 💡 Tips for Developers

*   **Adding a new command?** Just drop a new file in `/cogs`. The auto-loader finds it automatically.
*   **Need a helper?** Put it in `/classes` so you can reuse it in other bots later.
*   **Working in a team?** Use feature branches. The modular structure makes merging changes much safer.

## 🤝 Want to collaborate?

If you're looking for a Discord bot developer or want to contribute to this template, feel free to reach out! I'm always open to discussing projects or improving this base.

---
*This template is maintained by Egrey*
