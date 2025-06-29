# LifeGen-FullGen Developer Documentation

## 🎮 Project Overview

**LifeGen-FullGen** is a Python-based mod of the ClanGen game - a Warrior Cats clan simulation where players control their own cat character. Built with pygame and pygame_gui for cross-platform desktop gaming.

### Technology Stack
- **Language**: Python 3.x
- **GUI Framework**: pygame + pygame_gui
- **Graphics**: 2D sprite-based rendering
- **Audio**: pygame.mixer
- **Configuration**: JSON-based settings and themes
- **Threading**: PropagatingThread for background operations
- **Package Management**: pyproject.toml

## 📁 Project Structure

```
lifegen-fullgen/
├── main.py                          # 🚀 Main application entry point
├── pyproject.toml                   # 📦 Project dependencies and config
├── scripts/                         # 🧠 Core game logic
│   ├── screens/                     # 🖥️  UI Screen management
│   │   ├── StartScreen.py          # 🏠 Main menu (ADD BUTTONS HERE)
│   │   ├── Screens.py              # 🎯 Base screen class
│   │   ├── all_screens.py          # 📋 Screen registry
│   │   ├── ClanScreen.py           # 🏕️  Main camp screen
│   │   ├── ProfileScreen.py        # 🐱 Cat profile screen
│   │   └── [25+ other screens]     # 📄 Game-specific screens
│   ├── game_structure/             # 🏗️  Core game architecture
│   │   ├── ui_elements.py          # 🔲 Custom UI components
│   │   ├── screen_settings.py      # 🖼️  Display/scaling management
│   │   ├── ui_manager.py           # 🎛️  pygame_gui wrapper
│   │   ├── game_essentials.py      # ⚙️  Core game state
│   │   └── audio.py                # 🔊 Sound management
│   ├── cat/                        # 🐾 Cat system
│   │   ├── cats.py                 # 🐱 Main cat class
│   │   └── [cat-related modules]   # 🎨 Cat generation/management
│   └── ui/                         # 🎨 UI generation
│       └── generate_button.py      # 🔘 Button styling system
├── resources/                      # 📚 Game assets
│   ├── theme/                      # 🎨 UI themes and styling
│   │   ├── themes/dark.json        # 🌙 Dark theme colors
│   │   ├── buttons.json            # 🔘 Button styles
│   │   ├── text_boxes_dark.json    # 📝 Text styling
│   │   └── windows.json            # 🪟 Window styling
│   ├── images/                     # 🖼️  UI graphics/icons
│   ├── menus/                      # 🖼️  Menu backgrounds
│   ├── screen_config.json          # 🖥️  Display settings
│   ├── game_config.json            # ⚙️  Game mechanics
│   └── gamesettings.json           # 👤 User preferences
└── sprites/                        # 🎭 Cat sprites and generation
    ├── genemod/                    # 🧬 Advanced genetics system
    └── [sprite components]         # 👁️  Eyes, pelts, accessories
```

## 🏗️ UI Architecture

### Screen-Based System
- **Base Class**: `scripts/screens/Screens.py` - All screens inherit from this
- **Screen Registry**: `scripts/screens/all_screens.py` - Central screen management
- **Screen Switching**: `change_screen(screen_name)` method handles navigation

### UI Component Hierarchy
```
pygame_gui.UIManager (MANAGER)
├── Screen Classes (inherit from Screens)
│   ├── UISurfaceImageButton (custom buttons)
│   ├── UIImageButton (icon buttons)
│   ├── UITextBox (text display)
│   └── Standard pygame_gui elements
```

### Key UI Classes
- **UISurfaceImageButton**: Main menu buttons with custom styling
- **UIImageButton**: Icon-based buttons (social media, settings)
- **Custom theming**: JSON-based with object IDs (`#dark`, `@buttonstyles_mainmenu`)

## 🎯 Key Files for UI Development

### Main Entry Points
1. **`main.py`** - Application startup, pygame loop, screen management
2. **`scripts/screens/StartScreen.py`** - Main menu (ADD NEW BUTTONS HERE)
3. **`scripts/screens/Screens.py`** - Base screen functionality

### UI Development Files
1. **`scripts/game_structure/ui_elements.py`** - Custom UI components
2. **`scripts/ui/generate_button.py`** - Button styling system
3. **`resources/theme/`** - All styling and theming files

### Configuration Files
1. **`resources/screen_config.json`** - Display settings
2. **`resources/gamesettings.json`** - User preferences
3. **`pyproject.toml`** - Dependencies and project config

## 🔧 How to Add UI Elements

### Adding a Button to Main Menu

1. **Open**: `scripts/screens/StartScreen.py`
2. **Find**: `screen_switches()` method (around line 174)
3. **Add button creation** (around line 243, after quit button):
```python
self.your_button = UISurfaceImageButton(
    ui_scale(pygame.Rect((70, 15), (200, 30))),
    "button text",
    image_dict=get_button_dict(ButtonStyles.MAINMENU, (200, 30)),
    object_id="@buttonstyles_mainmenu",
    manager=MANAGER,
    anchors={"top_target": self.quit},  # Position relative to quit button
)
```

4. **Add event handler** in `handle_event()` method (around line 82):
```python
screens = {
    # existing buttons...
    self.your_button: "target_screen",  # or custom logic
}
```

5. **Add cleanup** in `exit_screen()` method (around line 161):
```python
self.your_button.kill()
```

### Button Styling Options
- **ButtonStyles.MAINMENU**: Main menu button style
- **ButtonStyles.SQUOVAL**: Rounded rectangular buttons
- **ButtonStyles.ROUNDED_RECT**: Fully rounded buttons

### UI Positioning
- **Absolute positioning**: `pygame.Rect((x, y), (width, height))`
- **Relative positioning**: Use `anchors` parameter
- **UI scaling**: Always wrap coordinates in `ui_scale()`

## 🎨 Theming System

### Theme Files Location
- **`resources/theme/themes/dark.json`** - Color definitions
- **`resources/theme/buttons.json`** - Button styling
- **`resources/theme/text_boxes_dark.json`** - Text styling

### Custom Object IDs
- **`@buttonstyles_mainmenu`** - Main menu button style
- **`#dark`** - Dark theme elements
- **`#text_box_22_horizleft`** - Text box styling

## 🚀 Development Workflow

### Running the Game
```bash
cd /home/jeff/dev/lifegen-fullgen
python main.py
```

### Key Development Areas

1. **Main Menu Changes**: Edit `scripts/screens/StartScreen.py`
2. **New Screens**: Create new file in `scripts/screens/` inheriting from `Screens`
3. **Custom UI Elements**: Modify `scripts/game_structure/ui_elements.py`
4. **Styling**: Edit JSON files in `resources/theme/`
5. **Game Logic**: Add to relevant modules in `scripts/`

### Important Patterns

- **Always use `ui_scale()`** for positioning and sizing
- **Kill UI elements** in `exit_screen()` to prevent memory leaks
- **Use `MANAGER`** as the UI manager for all pygame_gui elements
- **Follow naming conventions**: `self.element_name` for UI elements

## 🎮 Game Architecture

### Core Game Loop (main.py)
1. **Pygame initialization**
2. **Screen management system**
3. **Event handling**
4. **Display scaling and fullscreen support**
5. **Audio management**

### Screen Lifecycle
1. **`__init__()`** - Initial setup
2. **`screen_switches()`** - Called when screen becomes active
3. **`handle_event()`** - Process user input
4. **`exit_screen()`** - Cleanup when leaving screen

### Data Flow
```
User Input → pygame events → Screen.handle_event() → Game Logic → UI Updates
```

## 🔍 Quick Reference

### Most Common UI Tasks
- **Add main menu button**: Edit `StartScreen.py` around line 243
- **Change button text**: Modify first parameter in button creation
- **Change colors**: Edit `resources/theme/themes/dark.json`
- **Add new screen**: Create file in `scripts/screens/` + register in `all_screens.py`

### Important Constants
- **MANAGER**: Main pygame_gui manager
- **ui_scale()**: Scales coordinates for different screen sizes
- **get_button_dict()**: Gets button styling assets

### Debugging Tips
- **Check console output** for pygame_gui errors
- **Use `print()` statements** in event handlers
- **Pygame inspector** available via F12 (if enabled)
- **Error handling** built into main game loop

---

## 🎯 Ready to Code!

You now have everything you need to start modifying the UI. The most common starting point is adding buttons to the main menu in `StartScreen.py`. All the key files, patterns, and workflows are documented above.

**Happy coding!** 🚀