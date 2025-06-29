#!/usr/bin/env python3
# -*- coding: ascii -*-
import pygame
import pygame_gui
from pygame_gui.elements import UIDropDownMenu
import copy

from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game
from scripts.game_structure.ui_elements import UIImageButton, UISurfaceImageButton
from scripts.utility import (
    generate_sprite,
    shorten_text_to_fit,
    ui_scale_dimensions,
    ui_scale_offset,
    get_text_box_theme,
)
from scripts.utility import ui_scale
from .Screens import Screens
from .SpriteInspectScreen import SpriteInspectScreen
from ..game_structure.screen_settings import MANAGER
from ..game_structure.windows import SaveAsImage
from ..ui.generate_button import get_button_dict, ButtonStyles
from ..ui.get_arrow import get_arrow


class SpriteEditScreen(SpriteInspectScreen):
    """Sprite editing screen that extends SpriteInspectScreen with editing capabilities"""
    
    # Available options for editing
    PELT_PATTERNS = [
        "SingleColour", "TwoColour", "Tabby", "Speckled", "Tortie", "Calico",
        "Smoke", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti",
        "Singlestripe", "Masked", "Bengal", "Marbled", "Rosette"
    ]
    
    BASE_COLORS = [
        "WHITE", "PALEGREY", "SILVER", "GREY", "DARKGREY", "GHOST", "BLACK",
        "CREAM", "PALEGINGER", "GOLDEN", "GINGER", "DARKGINGER", "SIENNA",
        "LIGHTBROWN", "LILAC", "BROWN", "GOLDEN-BROWN", "DARKBROWN", "CHOCOLATE"
    ]
    
    EYE_COLORS = [
        "YELLOW", "AMBER", "HAZEL", "PALEGREEN", "GREEN", "BLUE", "DARKBLUE",
        "GREY", "CYAN", "EMERALD", "PALEBLUE", "PALEYELLOW", "GOLD", "HEATHERBLUE",
        "COPPER", "SAGE", "COBALT", "SUNLITICE", "GREENYELLOW", "BRONZE", "SILVER"
    ]
    
    WHITE_PATCHES = [
        "NONE", "LITTLE", "LIGHTTUXEDO", "BUZZARDFANG", "TIP", "BLAZE", "BIB", 
        "VEE", "PAWS", "TUXEDO", "FANCY", "UNDERS", "DAMIEN", "SKUNK", "MITAINE",
        "ANY", "ANYTWO", "BROKEN", "FRECKLES", "RINGTAIL", "HALFFACE", "PANTSTWO",
        "VAN", "ONEEAR", "LIGHTSONG", "TAIL", "HEART", "MOORISH", "APRON", "FULLWHITE"
    ]
    
    FUR_LENGTHS = ["short", "medium", "long"]
    
    # Common scars for quick selection
    COMMON_SCARS = [
        "ONE", "TWO", "THREE", "TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT",
        "TAILBASE", "BELLY", "LEGBITE", "NECKBITE", "FACE", "LEFTEAR", "RIGHTEAR",
        "NOTAIL", "HALFTAIL", "NOPAW", "BRIGHTHEART"
    ]
    
    # Popular accessories for quick selection
    POPULAR_ACCESSORIES = [
        "RED", "BLUE", "YELLOW", "GREEN", "BLACK", "WHITE", "PINK", "PURPLE",
        "REDBELL", "BLUEBELL", "YELLOWBELL", "GREENBELL", "BLACKBELL", "WHITEBELL",
        "REDBOW", "BLUEBOW", "YELLOWBOW", "GREENBOW", "BLACKBOW", "WHITEBOW",
        "FERNS", "DAISIES", "BERRIES", "FLOWERCROWN", "STICKS"
    ]

    def __init__(self, name=None):
        super().__init__(name)
        
        # Editing state
        self.original_pelt = None
        self.temp_pelt = None
        self.editing_enabled = True
        
        # UI elements for editing
        self.edit_elements = {}
        self.category_buttons = {}
        self.current_category = "colors"
        
        # Change tracking
        self.has_changes = False

    def screen_switches(self):
        """Override to add editing UI elements"""
        super().screen_switches()
        
        # Store original pelt data for undo/cancel
        if self.the_cat:
            self.original_pelt = copy.deepcopy(self.the_cat.pelt)
            self.temp_pelt = copy.deepcopy(self.the_cat.pelt)
        
        # Replace back button with save/cancel
        if self.back_button:
            self.back_button.kill()
        
        self.edit_elements["save_button"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 60), (105, 30))),
            "Save Changes",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        
        self.edit_elements["cancel_button"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((135, 60), (105, 30))),
            "Cancel",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        
        self.edit_elements["reset_button"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((245, 60), (105, 30))),
            "Reset",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        
        # Category tabs
        self.setup_category_tabs()
        
        # Setup editing interface
        self.setup_editing_interface()

    def setup_category_tabs(self):
        """Create tabs for different editing categories"""
        categories = [
            ("colors", "Colors"),
            ("patterns", "Patterns"), 
            ("markings", "Markings"),
            ("accessories", "Accessories"),
            ("scars", "Scars"),
            ("other", "Other")
        ]
        
        tab_width = 90
        start_x = 25
        
        for i, (category_id, label) in enumerate(categories):
            x_pos = start_x + (i * (tab_width + 5))
            
            self.category_buttons[category_id] = UISurfaceImageButton(
                ui_scale(pygame.Rect((x_pos, 130), (tab_width, 25))),
                label,
                get_button_dict(ButtonStyles.SQUOVAL, (tab_width, 25)),
                object_id="@buttonstyles_squoval",
                manager=MANAGER,
            )
    
    def setup_editing_interface(self):
        """Setup the main editing interface based on current category"""
        # Clear existing edit interface
        for key in list(self.edit_elements.keys()):
            if key.startswith("edit_"):
                self.edit_elements[key].kill()
                del self.edit_elements[key]
        
        # Create interface based on current category
        if self.current_category == "colors":
            self.setup_colors_interface()
        elif self.current_category == "patterns":
            self.setup_patterns_interface()
        elif self.current_category == "markings":
            self.setup_markings_interface()
        elif self.current_category == "accessories":
            self.setup_accessories_interface()
        elif self.current_category == "scars":
            self.setup_scars_interface()
        elif self.current_category == "other":
            self.setup_other_interface()
    
    def setup_colors_interface(self):
        """Setup color editing interface"""
        # Base color dropdown - larger and more prominent
        self.edit_elements["edit_base_color_label"] = pygame_gui.elements.UITextBox(
            "Base Color:",
            ui_scale(pygame.Rect((50, 200), (150, 40))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        current_color = self.temp_pelt.colour if self.temp_pelt and self.temp_pelt.colour else "WHITE"
        # Ensure the current color is in our list
        if current_color not in self.BASE_COLORS:
            current_color = "WHITE"
            
        self.edit_elements["edit_base_color"] = UIDropDownMenu(
            relative_rect=ui_scale(pygame.Rect((220, 200), (200, 40))),
            options_list=self.BASE_COLORS,
            starting_option=current_color,
            manager=MANAGER,
        )
        
        # Primary eye color - spaced out more
        self.edit_elements["edit_eye1_label"] = pygame_gui.elements.UITextBox(
            "Eye Color:",
            ui_scale(pygame.Rect((50, 260), (150, 40))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        current_eye1 = self.temp_pelt.eye_colour if self.temp_pelt and self.temp_pelt.eye_colour else "YELLOW"
        # Ensure the current eye color is in our list
        if current_eye1 not in self.EYE_COLORS:
            current_eye1 = "YELLOW"
            
        self.edit_elements["edit_eye1"] = UIDropDownMenu(
            relative_rect=ui_scale(pygame.Rect((220, 260), (200, 40))),
            options_list=self.EYE_COLORS,
            starting_option=current_eye1,
            manager=MANAGER,
        )
        
        # Fur length - right side
        self.edit_elements["edit_length_label"] = pygame_gui.elements.UITextBox(
            "Fur Length:",
            ui_scale(pygame.Rect((450, 200), (150, 40))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        current_length = self.temp_pelt.length if self.temp_pelt and self.temp_pelt.length else "short"
        # Ensure the current length is in our list
        if current_length not in self.FUR_LENGTHS:
            current_length = "short"
            
        self.edit_elements["edit_length"] = UIDropDownMenu(
            relative_rect=ui_scale(pygame.Rect((620, 200), (120, 40))),
            options_list=self.FUR_LENGTHS,
            starting_option=current_length,
            manager=MANAGER,
        )
    
    def setup_patterns_interface(self):
        """Setup pattern editing interface"""
        # Pelt pattern dropdown - larger and centered
        self.edit_elements["edit_pattern_label"] = pygame_gui.elements.UITextBox(
            "Pelt Pattern:",
            ui_scale(pygame.Rect((50, 220), (150, 40))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        current_pattern = self.temp_pelt.name if self.temp_pelt and self.temp_pelt.name else "SingleColour"
        # Ensure the current pattern is in our list
        if current_pattern not in self.PELT_PATTERNS:
            current_pattern = "SingleColour"
            
        self.edit_elements["edit_pattern"] = UIDropDownMenu(
            relative_rect=ui_scale(pygame.Rect((220, 220), (250, 40))),
            options_list=self.PELT_PATTERNS,
            starting_option=current_pattern,
            manager=MANAGER,
        )
    
    def setup_markings_interface(self):
        """Setup markings editing interface"""
        # White patches dropdown
        self.edit_elements["edit_white_label"] = pygame_gui.elements.UITextBox(
            "White Patches:",
            ui_scale(pygame.Rect((50, 180), (120, 30))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        current_white = self.temp_pelt.white_patches if self.temp_pelt and self.temp_pelt.white_patches else "NONE"
        # Ensure the current white patches value is in our list
        if current_white not in self.WHITE_PATCHES:
            current_white = "NONE"
        
        self.edit_elements["edit_white"] = UIDropDownMenu(
            relative_rect=ui_scale(pygame.Rect((180, 180), (150, 30))),
            options_list=self.WHITE_PATCHES,
            starting_option=current_white,
            manager=MANAGER,
        )
    
    def setup_accessories_interface(self):
        """Setup accessories editing interface"""
        self.edit_elements["edit_acc_label"] = pygame_gui.elements.UITextBox(
            "Popular Accessories:",
            ui_scale(pygame.Rect((50, 180), (200, 30))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        # Create buttons for popular accessories in a grid
        cols = 5
        for i, accessory in enumerate(self.POPULAR_ACCESSORIES[:20]):  # Limit to 20 for space
            row = i // cols
            col = i % cols
            x = 50 + (col * 110)
            y = 220 + (row * 35)
            
            # Check if accessory is currently equipped
            is_equipped = (self.temp_pelt and 
                         self.temp_pelt.accessory == accessory or 
                         (hasattr(self.temp_pelt, 'accessories') and 
                          accessory in self.temp_pelt.accessories))
            
            button_style = "@buttonstyles_squoval_pressed" if is_equipped else "@buttonstyles_squoval"
            
            self.edit_elements[f"edit_acc_{accessory}"] = UISurfaceImageButton(
                ui_scale(pygame.Rect((x, y), (100, 30))),
                accessory,
                get_button_dict(ButtonStyles.SQUOVAL, (100, 30)),
                object_id=button_style,
                manager=MANAGER,
            )
    
    def setup_scars_interface(self):
        """Setup scars editing interface"""
        self.edit_elements["edit_scar_label"] = pygame_gui.elements.UITextBox(
            "Common Scars:",
            ui_scale(pygame.Rect((50, 180), (200, 30))),
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
        )
        
        # Create buttons for common scars in a grid
        cols = 4
        for i, scar in enumerate(self.COMMON_SCARS[:16]):  # Limit to 16 for space
            row = i // cols
            col = i % cols
            x = 50 + (col * 130)
            y = 220 + (row * 35)
            
            # Check if scar is currently equipped
            is_equipped = (self.temp_pelt and 
                         hasattr(self.temp_pelt, 'scars') and 
                         scar in self.temp_pelt.scars)
            
            button_style = "@buttonstyles_squoval_pressed" if is_equipped else "@buttonstyles_squoval"
            
            self.edit_elements[f"edit_scar_{scar}"] = UISurfaceImageButton(
                ui_scale(pygame.Rect((x, y), (120, 30))),
                scar,
                get_button_dict(ButtonStyles.SQUOVAL, (120, 30)),
                object_id=button_style,
                manager=MANAGER,
            )
    
    def setup_other_interface(self):
        """Setup other editing options"""
        # Random generation button
        self.edit_elements["edit_random"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((50, 180), (150, 40))),
            "Random Appearance",
            get_button_dict(ButtonStyles.SQUOVAL, (150, 40)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        
        # Reset to original button
        self.edit_elements["edit_restore"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((220, 180), (150, 40))),
            "Restore Original",
            get_button_dict(ButtonStyles.SQUOVAL, (150, 40)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

    def handle_event(self, event):
        """Handle events including editing controls"""
        # Handle dropdown changes first, before parent processing
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            # Handle dropdown changes
            if event.ui_element == self.edit_elements.get("edit_base_color"):
                self.temp_pelt.colour = event.text
                self.has_changes = True
                self.apply_temp_changes()
                return  # Don't pass to parent
            elif event.ui_element == self.edit_elements.get("edit_eye1"):
                self.temp_pelt.eye_colour = event.text
                self.has_changes = True
                self.apply_temp_changes()
                return  # Don't pass to parent
            elif event.ui_element == self.edit_elements.get("edit_length"):
                self.temp_pelt.length = event.text
                self.has_changes = True
                self.apply_temp_changes()
                return  # Don't pass to parent
            elif event.ui_element == self.edit_elements.get("edit_pattern"):
                self.temp_pelt.name = event.text
                self.has_changes = True
                self.apply_temp_changes()
                return  # Don't pass to parent
            elif event.ui_element == self.edit_elements.get("edit_white"):
                self.temp_pelt.white_patches = event.text if event.text != "NONE" else None
                self.has_changes = True
                self.apply_temp_changes()
                return  # Don't pass to parent
        
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            # Handle save/cancel buttons
            if event.ui_element == self.edit_elements.get("save_button"):
                self.save_changes()
                return
            elif event.ui_element == self.edit_elements.get("cancel_button"):
                self.cancel_changes()
                return
            elif event.ui_element == self.edit_elements.get("reset_button"):
                self.reset_changes()
                return
            
            # Handle category tabs
            for category_id, button in self.category_buttons.items():
                if event.ui_element == button:
                    self.current_category = category_id
                    self.setup_editing_interface()
                    return
            
            # Handle accessory buttons
            for key, element in self.edit_elements.items():
                if key.startswith("edit_acc_") and event.ui_element == element:
                    accessory = key.replace("edit_acc_", "")
                    self.toggle_accessory(accessory)
                    return
                elif key.startswith("edit_scar_") and event.ui_element == element:
                    scar = key.replace("edit_scar_", "")
                    self.toggle_scar(scar)
                    return
            
            # Handle other buttons
            if event.ui_element == self.edit_elements.get("edit_random"):
                self.randomize_appearance()
                return
            elif event.ui_element == self.edit_elements.get("edit_restore"):
                self.restore_original()
                return
        
        
        # Call parent handler for other events
        return super().handle_event(event)
    
    def toggle_accessory(self, accessory):
        """Toggle an accessory on/off"""
        if not hasattr(self.temp_pelt, 'accessories'):
            self.temp_pelt.accessories = []
        
        if accessory in self.temp_pelt.accessories:
            self.temp_pelt.accessories.remove(accessory)
        else:
            # Set as primary accessory and add to list
            self.temp_pelt.accessory = accessory
            if accessory not in self.temp_pelt.accessories:
                self.temp_pelt.accessories.append(accessory)
        
        self.has_changes = True
        self.apply_temp_changes()
        self.setup_accessories_interface()  # Refresh buttons
    
    def toggle_scar(self, scar):
        """Toggle a scar on/off"""
        if not hasattr(self.temp_pelt, 'scars'):
            self.temp_pelt.scars = []
        
        if scar in self.temp_pelt.scars:
            self.temp_pelt.scars.remove(scar)
        else:
            self.temp_pelt.scars.append(scar)
        
        self.has_changes = True
        self.apply_temp_changes()
        self.setup_scars_interface()  # Refresh buttons
    
    def apply_temp_changes(self):
        """Apply temporary changes to cat for preview"""
        if self.the_cat and self.temp_pelt:
            self.the_cat.pelt = copy.deepcopy(self.temp_pelt)
            # Clear the cached sprite to force regeneration
            self.the_cat._sprite = None
            self.make_cat_image()
    
    def make_cat_image(self):
        """Override to force sprite regeneration"""
        # Kill existing cat image
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()
        
        # Force complete sprite regeneration
        self.the_cat._sprite = None
        
        # Generate new sprite with current settings
        self.cat_image = generate_sprite(
            self.the_cat,
            life_state=self.valid_life_stages[self.displayed_life_stage] if hasattr(self, 'valid_life_stages') and hasattr(self, 'displayed_life_stage') else "adult",
            scars_hidden=not self.scars_shown if hasattr(self, 'scars_shown') else False,
            acc_hidden=not self.acc_shown if hasattr(self, 'acc_shown') else False,
            always_living=self.override_dead_lineart if hasattr(self, 'override_dead_lineart') else False,
            no_not_working=self.override_not_working if hasattr(self, 'override_not_working') else False,
        )
        
        # Create new UI image element with complete recreation
        scaled_image = pygame.transform.scale(self.cat_image, ui_scale_dimensions((450, 450)))
        
        # Completely recreate the UI element to force visual refresh
        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((225, 100), (350, 350))),
            scaled_image,
            manager=MANAGER,
        )
        
        # Force immediate visual update
        MANAGER.update(0.0)  # Force manager to process changes immediately
        
        # Sprite editing complete
    
    def save_changes(self):
        """Save changes and return to profile screen"""
        if self.the_cat and self.temp_pelt:
            self.the_cat.pelt = copy.deepcopy(self.temp_pelt)
            # Clear the cached sprite to force regeneration
            self.the_cat._sprite = None
        self.change_screen("profile screen")
    
    def cancel_changes(self):
        """Cancel changes and return to profile screen"""
        if self.the_cat and self.original_pelt:
            self.the_cat.pelt = copy.deepcopy(self.original_pelt)
            # Clear the cached sprite to force regeneration
            self.the_cat._sprite = None
        self.change_screen("profile screen")
    
    def reset_changes(self):
        """Reset to original appearance"""
        if self.original_pelt:
            self.temp_pelt = copy.deepcopy(self.original_pelt)
            self.apply_temp_changes()
            self.setup_editing_interface()
            self.has_changes = False
    
    def randomize_appearance(self):
        """Generate random appearance"""
        import random
        
        self.temp_pelt.colour = random.choice(self.BASE_COLORS)
        self.temp_pelt.name = random.choice(self.PELT_PATTERNS)
        self.temp_pelt.eye_colour = random.choice(self.EYE_COLORS)
        self.temp_pelt.eye_colour2 = random.choice(self.EYE_COLORS)
        self.temp_pelt.white_patches = random.choice(self.WHITE_PATCHES)
        self.temp_pelt.length = random.choice(self.FUR_LENGTHS)
        
        self.has_changes = True
        self.apply_temp_changes()
        self.setup_editing_interface()
    
    def restore_original(self):
        """Restore to original appearance (same as reset)"""
        self.reset_changes()
    
    def exit_screen(self):
        """Clean up editing elements"""
        for element in self.edit_elements.values():
            if hasattr(element, 'kill'):
                element.kill()
        self.edit_elements = {}
        
        for element in self.category_buttons.values():
            if hasattr(element, 'kill'):
                element.kill()
        self.category_buttons = {}
        
        return super().exit_screen()