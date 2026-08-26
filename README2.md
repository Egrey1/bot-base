# Discord Bot Base — My Production Template

This is my go-to template for building Discord bots on **disnake**. I use it for every freelance project to ensure consistent architecture, rapid feature delivery, and easy maintenance.

It's designed for developers who value clean separation of concerns and want to avoid reinventing the wheel on every new bot.

## 🗺️ Project Structure

The architecture is built for scalability and reusability.

- **`classes/`** — Core abstractions and utility classes. These are the building blocks used across all cogs.
  - `objects/` — Domain-specific objects and data containers.
  - `handlers.py` — Custom event handling logic.
- **`cogs/`** — Modular command groups.
  - **Smart Grouping**: Commands are grouped by functionality (e.g., `mod_command`).
  - **Deep Structure**: Each group has a `commands/` subfolder containing individual command implementations (e.g., `kick.py`).
  - **Auto-Registration**: Each group contains a `__init__.py` with a `setup(bot)` function. This automatically registers the cog without touching `main.py`.
  - **Inheritance Pattern**: Groups often inherit from a base assembly class to enforce consistent behavior.
    ```python
    # Example: cogs/mod_command/__init__.py
    from .commands import * 

    class ModCommand(Kick): 
        pass

    def setup(bot):
        bot.add_cog(ModCommand())
    ```
- **`data/`** — Data access layer.
  - `dbConnect.py` — Handles connections and interactions with databases (SQLite, JSON, etc.). Keeps business logic clean from SQL queries.
- **`dependencies/`** — Global shared state and constants.
  - `main_deps.py` — Centralized place for global variables, shared configs, and type hints.
- **`config.py`** — Configuration entry point.
  - Initializes variables from `dependencies`.
  - **Security First**: Loads sensitive tokens from a `.env` file (using `os.getenv`), never hardcoded.
- **`main.py`** — The entry point.
  - Imports config and dependencies, then starts the bot instance.

## 🚀 Why This Structure?

As a developer working on multiple bots, this setup solves three main pain points:

1.  **Zero-Friction Onboarding**: Adding a new command group is as simple as dropping a folder into `cogs/`. No changes needed in `main.py`.
2.  **Clean Separation**: Logic (classes), Behavior (cogs), and Data (data) never mix, making the codebase easy to audit and debug.
3.  **Reusability**: Your custom classes in `classes/` and DB connectors in `data/` can be instantly dropped into any new bot project.

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+
- `disnake`
- `python-dotenv` (for secure environment variables)

### Configuration
1. Create a `.env` file in the root directory:
```env
TOKEN=your_bot_token_here
```
2. Ensure `.gitignore` includes `.env` to prevent leaking secrets.
3. The bot automatically picks up the token from `config.py` via `os.getenv`.
```bash
python main.py
```

### 💡 Key Features for Developers
- **Modular Cogs:** The `setup()` pattern in `cogs/*/__init__.py` allows for dynamic loading. You can enable/disable entire feature sets by simply commenting out the import in `main.py` or removing the folder.
- **Command Granularity:** Storing individual commands in `cogs/*/commands/` keeps files small and focused. A single command file rarely exceeds 100 lines.
- **Global Dependencies:** The `dependencies/` folder ensures that shared constants and complex type definitions are available everywhere without circular import issues.

### 🔒 Security Note
This template follows security best practices:

- **Never commit tokens:** The `.gitignore` file excludes `.env`, `venv` and `__pycache__`.
- **Environment Variables:** Tokens are loaded at runtime, not hardcoded in the source code.

### 🤝 Contributing
This template is a living document. If you have suggestions for improving the cog loading mechanism, data layer, or class structures, feel free to open an issue or submit a pull request.

Maintained by Egrey.
