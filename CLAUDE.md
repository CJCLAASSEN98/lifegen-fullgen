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
│   ├── StartScreen.py              # Main menu
│   ├── FartScreen.py               # Custom fart screen
│   ├── all_screens.py              # Screen registry
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

## Essential Code Patterns
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
- **Python**: `python3` 
- **Run Command**: `cd /home/jeff/dev/lifegen-fullgen && python3 main.py`
- **Git Remote**: Fork at `https://github.com/CJCLAASSEN98/lifegen-fullgen`

## Important Notes
- All UI elements need `ui_scale()` for proper scaling
- Always add cleanup in `exit_screen()` method
- Import `game` from `scripts.game_structure.game_essentials` for clan access
- Use `MANAGER` from `scripts.game_structure.screen_settings` for pygame_gui