import pygame
import pygame_gui
import random
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game
from scripts.game_structure.ui_elements import UISurfaceImageButton
from scripts.utility import ui_scale
from .Screens import Screens
from ..game_structure.screen_settings import MANAGER
from ..ui.generate_button import get_button_dict, ButtonStyles


class FartScreen(Screens):
    """
    The Fart Screen - where cats let it rip! 💨
    """

    def __init__(self, name=None):
        super().__init__(name)
        self.back_button = None
        self.fart_again_button = None
        self.fart_text = None
        self.cat_image = None
        self.fart_messages = [
            "💨 PFFFFFT! 💨",
            "💨 *TOOT* 💨", 
            "💨 BRAAAAP! 💨",
            "💨 *squeaky fart* 💨",
            "💨 THUNDEROUS FART! 💨",
            "💨 Silent but deadly... 💨",
            "💨 MEGA FART! 💨",
            "💨 *poot poot* 💨"
        ]
        self.current_fart_message = random.choice(self.fart_messages)

    def handle_event(self, event):
        """Handle events on the fart screen"""
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen("start screen")
            elif event.ui_element == self.fart_again_button:
                # Change the fart message and print to console
                self.current_fart_message = random.choice(self.fart_messages)
                self.fart_text.set_text(self.current_fart_message)
                if game.clan and game.clan.your_cat:
                    cat_name = game.clan.your_cat.name
                    print(f"🐱 {cat_name} says: {self.current_fart_message}")
                else:
                    print(f"🐱 Cat says: {self.current_fart_message}")

    def exit_screen(self):
        """Clean up UI elements when leaving the screen"""
        if self.back_button:
            self.back_button.kill()
        if self.fart_again_button:
            self.fart_again_button.kill()
        if self.fart_text:
            self.fart_text.kill()
        if self.cat_image:
            self.cat_image.kill()

    def screen_switches(self):
        """Set up the fart screen UI"""
        super().screen_switches()
        
        # Set a simple background
        self.set_bg("default")
        
        # Hide the main menu buttons
        self.hide_menu_buttons()
        
        # Get the player's cat and use their actual sprite
        if game.clan and game.clan.your_cat:
            your_cat = game.clan.your_cat
            
            # Get the cat's sprite and scale it up for display
            cat_sprite = your_cat.sprite.convert_alpha()
            # Scale up the sprite (it's normally 50x50, let's make it bigger)
            scaled_cat_sprite = pygame.transform.scale(cat_sprite, (150, 150))
            
            # Create a larger surface to add fart effects
            cat_surface = pygame.Surface((300, 200), pygame.SRCALPHA)
            cat_surface.fill((0, 0, 0, 0))  # Transparent background
            
            # Blit the cat sprite to the center-left of the surface
            cat_surface.blit(scaled_cat_sprite, (75, 25))
            
            # Add realistic mist-like fart clouds behind the cat
            def draw_mist_cloud(surface, center_x, center_y, base_radius):
                """Draw a realistic mist cloud with multiple layers and transparency"""
                # Create a temporary surface for alpha blending
                mist_surface = pygame.Surface((base_radius * 3, base_radius * 3), pygame.SRCALPHA)
                
                # Draw multiple overlapping circles with varying opacity for mist effect
                for i in range(8):
                    radius = base_radius - i * 3
                    if radius <= 0:
                        break
                    alpha = 30 - i * 3  # Decreasing transparency
                    if alpha <= 0:
                        break
                    
                    # Intense swamp green - super toxic fart color!
                    color_variation = i * 3  # Minimal variation for intense green
                    color = (50 + color_variation, 200, 40 + color_variation, alpha)
                    
                    # Offset each layer slightly for wispy effect
                    offset_x = (i % 3 - 1) * 2
                    offset_y = (i % 2) * 2
                    
                    pygame.draw.circle(mist_surface, color, 
                                     (base_radius + offset_x, base_radius + offset_y), radius)
                
                # Blit the mist surface to the main surface
                cat_surface.blit(mist_surface, (center_x - base_radius, center_y - base_radius), 
                               special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Draw multiple mist clouds - moved even further to the right
            draw_mist_cloud(cat_surface, 120, 100, 25)   # Main fart cloud
            draw_mist_cloud(cat_surface, 90, 80, 18)     # Upper cloud
            draw_mist_cloud(cat_surface, 110, 120, 12)   # Lower cloud
            draw_mist_cloud(cat_surface, 100, 90, 8)     # Small wispy cloud
            
        else:
            # Fallback to simple drawn cat if no clan exists
            cat_surface = pygame.Surface((300, 200))
            cat_surface.fill((139, 69, 19))  # Brown color for cat
            
            # Add some simple "cat" features
            pygame.draw.circle(cat_surface, (255, 192, 203), (75, 50), 20)  # Pink nose
            pygame.draw.circle(cat_surface, (255, 192, 203), (225, 50), 20)  # Pink nose
            pygame.draw.circle(cat_surface, (0, 0, 0), (60, 40), 8)  # Left eye
            pygame.draw.circle(cat_surface, (0, 0, 0), (240, 40), 8)  # Right eye
            
            # Add mist-like fart cloud behind the simple cat too
            def draw_simple_mist_cloud(surface, center_x, center_y, base_radius):
                """Draw a mist cloud for the fallback cat"""
                # Draw multiple overlapping circles with decreasing opacity
                for i in range(6):
                    radius = base_radius - i * 2
                    if radius <= 0:
                        break
                    alpha = max(20, 60 - i * 8)  # Decreasing transparency
                    
                    # Create intense swamp green color with alpha
                    temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    color = (50 + i * 5, 200, 40 + i * 5, alpha)
                    pygame.draw.circle(temp_surface, color, (radius, radius), radius)
                    
                    # Offset for wispy effect
                    offset_x = (i % 2) * 3
                    offset_y = (i % 3 - 1) * 2
                    
                    surface.blit(temp_surface, (center_x - radius + offset_x, center_y - radius + offset_y),
                               special_flags=pygame.BLEND_ALPHA_SDL2)
            
            draw_simple_mist_cloud(cat_surface, 120, 150, 25)   # Main fart cloud
            draw_simple_mist_cloud(cat_surface, 90, 130, 18)    # Smaller cloud
        
        self.cat_image = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((250, 150), (300, 200))),
            cat_surface,
            manager=MANAGER
        )
        
        # Create the fart text
        self.fart_text = pygame_gui.elements.UITextBox(
            self.current_fart_message,
            ui_scale(pygame.Rect((200, 100), (400, 50))),
            object_id="#text_box_30_horizcenter",
            manager=MANAGER
        )
        self.fart_text.background_colour = pygame.Color('#FFE4E1')  # Light pink background
        
        # Create title
        title_text = pygame_gui.elements.UITextBox(
            "🐱 THE FARTING CAT ZONE 🐱",
            ui_scale(pygame.Rect((150, 50), (500, 40))),
            object_id="#text_box_30_horizcenter",
            manager=MANAGER
        )
        title_text.background_colour = pygame.Color('#98FB98')  # Light green
        
        # Create buttons
        self.fart_again_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((250, 400), (200, 30))),
            "💨 FART AGAIN! 💨",
            image_dict=get_button_dict(ButtonStyles.SQUOVAL, (200, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER
        )
        
        self.back_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 400), (200, 30))),
            "Back to Menu",
            image_dict=get_button_dict(ButtonStyles.SQUOVAL, (200, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
            anchors={"top_target": self.fart_again_button}
        )
        
        # Show welcome message with cat's name if available
        if game.clan and game.clan.your_cat:
            cat_name = game.clan.your_cat.name
            print(f"🎉 Welcome to the Fart Screen! {cat_name} says: {self.current_fart_message}")
        else:
            print(f"🎉 Welcome to the Fart Screen! Current fart: {self.current_fart_message}")