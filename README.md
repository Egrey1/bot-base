# Discord Bot Base — Technical Overview

This repository contains my standardized base template for disnake bots. The goal is to maximize code reuse and minimize boilerplate when starting a new project.

## 📂 Directory Structure

### `classes/`
Core logic and abstractions.
- `objects/`: Data models and DTOs.
- `handlers.py`: Custom event handlers and utility functions.

### `cogs/`
Command modules. This is the most critical part of the architecture.
- **Grouping**: Commands are grouped by feature (e.g., `mod_command`, `economy`).
- **Implementation**: Inside each group, there is a `commands/` folder. Individual commands live here (e.g., `kick.py`, `ban.py`).
- **Assembly**: The group's `__init__.py` acts as an assembly unit. It imports all commands from `commands/` and defines a parent class that inherits from them.
  
  **Example (`cogs/mod_command/__init__.py`):**
  ```python
  from .commands import * 

  # Inherits behavior from imported commands
  class ModCommand(Kick): 
      pass

  def setup(bot):
      bot.add_cog(ModCommand())
  ```
- **Auto-Load**: The main loader in `main.py` (or a helper in `cogs/__init__.py`) iterates through these groups and calls their `setup()` functions automatically.

### `data/`
Data access layer.
- `dbConnect.py`: Handles database connections and CRUD operations.

### `dependencies/`
Global shared resources.
- `main_deps.py`: Global constants, shared configuration objects, and type aliases.

### `config.py`
Configuration bootstrapper.
- Initializes dependencies.
- Loads secrets from `.env` (e.g., `TOKEN`).

### `main.py`
Entry point.
- Imports `config` and `dependencies`.
- Starts the bot instance.

## ⚙️ How It Works

1.  **Startup**: `main.py` runs, loading global config and dependencies.
2.  **Cog Loading**: The system scans `cogs/` for folders containing `setup()` functions.
3.  **Command Resolution**: When a user triggers a command, the bot resolves it through the assembled cog class (e.g., `ModCommand`).
4.  **Data Access**: Any cog needing data calls helpers from `data/`.

## 🔐 Security & Best Practices

- **Secrets Management**: Tokens are never stored in code. They are loaded from the `.env` file via `os.getenv` in `config.py`.
- **Git Hygiene**: `.gitignore` prevents `__pycache__`, `venv`, `.env`

## 📝 Notes for Contributors

- **Adding a New Command**:
  1. Create a new file in `cogs/<group>/commands/`.
  2. Ensure the group's `__init__.py` imports it (usually via `from .commands import *`).
  3. No changes are required in `main.py`.
- **Creating a New Group**:
  1. Create a folder in `cogs/`.
  2. Add `commands/` subfolder and `__init__.py` with the `setup()` function.
  3. The loader will pick it up automatically.

## 📄 Requirements

- `disnake`
- `python-dotenv`

Install with: `pip install -r requirements.txt`
