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
│   ├── ProfileScreen.py            # Cat profile with edit sprite button
│   ├── SpriteInspectScreen.py      # Base sprite viewing
│   ├── SpriteEditScreen.py         # NEW: Sprite editing system
│   ├── all_screens.py              # Screen registry
│   └── Screens.py                  # Base screen class
├── scripts/game_structure/
│   ├── ui_elements.py              # Custom UI components
│   └── game_essentials.py         # Core game state
├── scripts/cat/
│   ├── cats.py                     # Cat class with sprite caching
│   ├── pelts.py                    # Pelt/appearance data structures
│   └── sprites.py                  # Sprite loading and management
├── scripts/utility.py              # generate_sprite() function
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

## Sprite Editing System (NEW)
**Location**: `scripts/screens/SpriteEditScreen.py`
- **Access**: Edit sprite button (📝) on cat profiles at position (703, 60)
- **Features**: 6 category tabs (Colors, Patterns, Markings, Accessories, Scars, Other)
- **Real-time Preview**: Changes apply immediately with sprite cache clearing
- **Save/Cancel**: Proper change management with temp_pelt system

### Sprite System Architecture
- **Cat.sprite**: Property with caching via `Cat._sprite`
- **generate_sprite()**: Main sprite generation in `scripts.utility`
- **Pelt Class**: Appearance data (color, pattern, white_patches, eye_colour, etc.)
- **Sprite Cache**: Must clear `cat._sprite = None` for visual updates
- **UI Refresh**: Use `MANAGER.update(0.0)` to force immediate display

### Available Editing Options
- **19 Base Colors**: WHITE, GINGER, BLACK, CHOCOLATE, etc.
- **17+ Patterns**: SingleColour, Tabby, Tortie, Bengal, Smoke, etc.
- **21 Eye Colors**: YELLOW, BLUE, GREEN, AMBER, etc.
- **30+ White Markings**: LITTLE, TUXEDO, VAN, FULLWHITE, etc.
- **3 Fur Lengths**: short, medium, long

### Critical Implementation Notes
- **Sprite Generation Works**: Different pelts create different sprites (verified)
- **UI Display Issue**: pygame_gui UIImage requires aggressive refresh
- **Event Handling**: Process dropdown events before parent class
- **Data Validation**: Ensure dropdown values exist in option lists

## Important Notes
- All UI elements need `ui_scale()` for proper scaling
- Always add cleanup in `exit_screen()` method
- Import `game` from `scripts.game_structure.game_essentials` for clan access
- Use `MANAGER` from `scripts.game_structure.screen_settings` for pygame_gui
- **Sprite Cache**: Always clear `cat._sprite = None` when changing appearance
- **UI Refresh**: Force `MANAGER.update(0.0)` after sprite changes

## COMPLETED FEATURES
✅ **Sprite Editing System**: Full implementation with real-time preview
- Located: `scripts/screens/SpriteEditScreen.py`
- Access: Edit button (📝) on cat profiles  
- Status: FUNCTIONAL - sprites generate correctly, UI display challenges resolved
- Integration: Complete with screen registry and profile button