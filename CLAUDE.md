# CLAUDE Context - LifeGen-FullGen Project

## Project Overview
**LifeGen-FullGen** - Python-based Warrior Cats clan simulation game (ClanGen mod)
- **Tech Stack**: Python + pygame + pygame_gui
- **Architecture**: Screen-based UI system with inheritance
- **Location**: `/home/jeff/dev/lifegen-fullgen/`

## Key Files & Structure
```
lifegen-fullgen/
├── main.py                          # Main entry point & game loop
├── scripts/screens/
│   ├── StartScreen.py              # Main menu (MODIFIED)
│   ├── FartScreen.py               # Custom fart screen (NEW)
│   ├── all_screens.py              # Screen registry (MODIFIED)
│   └── Screens.py                  # Base screen class
├── scripts/game_structure/
│   ├── ui_elements.py              # Custom UI components
│   └── game_essentials.py         # Core game state
└── resources/theme/                # JSON-based theming system
```

## Core Architecture Patterns
- **Screen System**: Each UI view = separate screen class inheriting from `Screens`
- **UI Framework**: pygame_gui with custom `UISurfaceImageButton` components
- **Cat Sprites**: Real game sprites via `game.clan.your_cat.sprite`
- **Theming**: JSON-based with object IDs (`@buttonstyles_mainmenu`)
- **Scaling**: `ui_scale()` for responsive positioning

## Changes Made This Session

### 1. Main Menu Fart Button (`StartScreen.py`)
**Lines Modified**: ~244, ~112, ~171
- Added fart button after quit button
- Event handler: navigates to "fart screen" 
- Cleanup: `self.fart_button.kill()` in exit_screen()

### 2. New FartScreen (`FartScreen.py` - NEW FILE)
**Created**: Full new screen class with:
- **Real Cat Sprites**: Uses `game.clan.your_cat.sprite.convert_alpha()`
- **Fallback System**: Simple drawn cat if no clan exists
- **Mist Effects**: Advanced layered transparency fart clouds
- **Personalization**: Shows cat's name in messages
- **Navigation**: "Fart Again" button + "Back to Menu" button

### 3. Screen Registry (`all_screens.py`)
**Lines Modified**: ~37, ~108, ~159
- Added `from .FartScreen import FartScreen`
- Added `fart_screen = FartScreen("fart screen")`
- Added screen to rebuild method

### 4. Fart Visual Effects
**Advanced Mist System**:
- **Multi-layered clouds**: 8 overlapping circles with decreasing opacity
- **Color**: Intense swamp green RGB(50-74, 200, 40-64) 
- **Positioning**: Behind cat at x=90-120 (right side)
- **Alpha blending**: `pygame.BLEND_ALPHA_SDL2` for smooth transparency

## Code Patterns Learned
```python
# Screen navigation
self.change_screen("screen_name")

# Cat sprite access
your_cat = game.clan.your_cat
cat_sprite = your_cat.sprite.convert_alpha()

# UI button creation
self.button = UISurfaceImageButton(
    ui_scale(pygame.Rect((x, y), (w, h))),
    "text",
    image_dict=get_button_dict(ButtonStyles.MAINMENU, (w, h)),
    object_id="@buttonstyles_mainmenu",
    manager=MANAGER,
    anchors={"top_target": self.other_button}
)

# Event handling
if event.ui_element == self.button:
    # action here

# Cleanup
self.button.kill()
```

## Development Environment
- **Python**: `/home/jeff/.nvm/versions/node/v22.17.0/bin/python3`
- **Run Command**: `cd /home/jeff/dev/lifegen-fullgen && python3 main.py`
- **Cat Name**: "Bigkit" (current player cat)

## Future Context Notes
- All UI elements need `ui_scale()` for proper scaling
- Always add cleanup in `exit_screen()` method
- Import `game` from `scripts.game_structure.game_essentials` for clan access
- Use `MANAGER` from `scripts.game_structure.screen_settings` for pygame_gui

## Last Updated
Current session - Added functional fart screen with real cat sprites and advanced mist effects