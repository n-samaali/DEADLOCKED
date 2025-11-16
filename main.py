import csv
import io
from math import sin

from textual.app import App, ComposeResult
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import Traceback
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.reactive import reactive

from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, SQUARE, HEAVY
from rich.text import Text
from rich.console import RenderableType
from rich.align import Align

from textual.color import Gradient
from textual.containers import Center, Middle
from textual.widgets import ProgressBar

from textual import containers, events, lazy, on, widget
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.demo.data import COUNTRIES, DUNE_BIOS, MOVIES, MOVIES_TREE
from textual.demo.page import PageScreen
from textual.reactive import reactive, var
from textual.suggester import SuggestFromList
from textual.theme import BUILTIN_THEMES
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Digits,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Log,
    Markdown,
    MaskedInput,
    OptionList,
    RadioButton,
    RadioSet,
    RichLog,
    Select,
    Sparkline,
    Static,
    Switch,
    TabbedContent,
    TextArea,
    Tree,
)

from game import Game

class ActionButtons(containers.VerticalGroup):
    """Buttons demo."""

    ALLOW_MAXIMIZE = True
    DEFAULT_CLASSES = "column"
    DEFAULT_CSS = """
    ActionButtons {
        ItemGrid { margin-bottom: 0;}
        Button { width: 1fr; }
        border: heavy white 20%;
        border-title-align: left;
    }
    """
    
    def compose(self) -> ComposeResult:
        with containers.HorizontalGroup():
            yield Button(
                "Strength",
                id="strength-button",
                variant="success",
                disabled=self.app.DISABLE_BUTTONS,
            )
            yield Button(
                "Dexterity",
                id="dexterity-button",
                variant="primary",
                disabled=self.app.DISABLE_BUTTONS,
            )
            yield Button(
                "Intelligence",
                id="intelligence-button",
                variant="warning",
                disabled=self.app.DISABLE_BUTTONS,
            )
            yield Button(
                "Charisma",
                id="charisma-button",
                variant="error",
                disabled=self.app.DISABLE_BUTTONS,
            )

    def on_mount(self):
        # Store references to the buttons
        self.str_button = self.query_one("#strength-button")
        self.dex_button = self.query_one("#dexterity-button")
        self.int_button = self.query_one("#intelligence-button")
        self.cha_button = self.query_one("#charisma-button")

    def watch_app_DISABLE_BUTTONS(self, value: bool):
        """Automatically called whenever the app variable changes."""
        self.str_button.disabled = value
        self.dex_button.disabled = value
        self.int_button.disabled = value
        self.cha_button.disabled = value
        self.refresh()
        
class UserStats(containers.VerticalGroup) :
    
    def compose(self):
        
        gradient_health = Gradient.from_colors(
            "#689d6a",
            "#8ec07c",
        )
        
        gradient_strength = Gradient.from_colors(
            "#b7bb26",
            "#d7d74c",
        )
        
        gradient_dexterity = Gradient.from_colors(
            "#85a598",
            "#b4d4c7",
        )
        
        gradient_intelligence = Gradient.from_colors(
            "#fd8019",
            "#f59e3f",
        )
        
        gradient_charisma = Gradient.from_colors(
            "#fa4934",
            "#f56d52",
        )
        
        with containers.VerticalGroup() :
            with Center() :
                with Middle() :
                    yield Label("Health", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_health, id="health", show_percentage=True, show_eta=False)
                    yield Label("Strength", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_strength, id="strength", show_percentage=True, show_eta=False)
                    yield Label("Dexterity", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_dexterity, id="dexterity", show_percentage=True, show_eta=False)
                    yield Label("Intelligence", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_intelligence, id="intelligence", show_percentage=True, show_eta=False)
                    yield Label("Charisma", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_charisma, id="charisma", show_percentage=True, show_eta=False)

        
    def on_mount(self) -> None:
        self.app.curr_health = self.app.game.person.hp
        self.app.curr_strength = self.app.game.person.strength
        self.app.curr_dexterity = self.app.game.person.dexterity
        self.app.curr_intelligence = self.app.game.person.intelligence
        self.app.curr_charisma = self.app.game.person.charisma
        
        self.query_one("#health").update(progress=self.app.curr_health)
        self.query_one("#strength").update(progress=self.app.curr_strength)
        self.query_one("#dexterity").update(progress=self.app.curr_dexterity)
        self.query_one("#intelligence").update(progress=self.app.curr_intelligence)
        self.query_one("#charisma").update(progress=self.app.curr_charisma)

    def update_user_stats(self) :
        
        logs = self.app.screen.query_one("#dungeon-master")
        
        self.app.prev_health = self.app.curr_health
        self.app.prev_strength = self.app.curr_strength
        self.app.prev_dexterity = self.app.curr_dexterity
        self.app.prev_intelligence = self.app.curr_intelligence
        self.app.prev_charisma = self.app.curr_charisma
        
        
        self.app.curr_health = self.app.game.person.hp
        self.app.curr_strength = self.app.game.person.strength
        self.app.curr_dexterity = self.app.game.person.dexterity
        self.app.curr_intelligence = self.app.game.person.intelligence
        self.app.curr_charisma = self.app.game.person.charisma
        
        health_factor = self.app.curr_health - self.app.prev_health
        strength_factor = self.app.curr_strength - self.app.prev_strength
        dexterity_factor = self.app.curr_dexterity - self.app.prev_dexterity
        intelligence_factor = self.app.curr_intelligence - self.app.prev_intelligence
        charisma_factor = self.app.curr_charisma - self.app.prev_charisma
        
        if health_factor != 0 :
            message = f"Your health increased {health_factor}%" if health_factor > 0 else f"Your health decreased {abs(health_factor)}%"
            logs.write_action_message("health", message)
        if strength_factor != 0 :
            message = f"Your strength increased {strength_factor}%" if strength_factor > 0 else f"Your strength decreased {abs(strength_factor)}%"
            logs.write_action_message("strength", message)
        if dexterity_factor != 0 :
            message = f"Your dexterity increased {dexterity_factor}%" if dexterity_factor > 0 else f"Your dexterity decreased {abs(dexterity_factor)}%"
            logs.write_action_message("dexterity", message)
        if intelligence_factor != 0 :
            message = f"Your intelligence increased {intelligence_factor}%" if intelligence_factor > 0 else f"Your intelligence decreased {abs(intelligence_factor)}%"
            logs.write_action_message("intelligence", message)
        if charisma_factor != 0 :
            message = f"Your charisma increased {charisma_factor}%" if charisma_factor > 0 else f"Your charisma decreased {abs(charisma_factor)}%"
            logs.write_action_message("charisma", message)

        self.query_one("#health").update(progress=self.app.curr_health)
        self.query_one("#strength").update(progress=self.app.curr_strength)
        self.query_one("#dexterity").update(progress=self.app.curr_dexterity)
        self.query_one("#intelligence").update(progress=self.app.curr_intelligence)
        self.query_one("#charisma").update(progress=self.app.curr_charisma)
        
class Logs(containers.VerticalGroup):

    DEFAULT_CLASSES = "column"
    
    DEFAULT_CSS = """
    Logs {
        height: 1fr;
        border: heavy white 20%;
        border-title-align: left;
    }
    Logs RichLog {
        width: 1fr;
        height: 1fr;
        padding: 1;
        overflow-x: auto;
        &:focus {
            border: wide $border;
        }
        background-tint: #282828;
    }
    Logs TabPane { padding: 0; }
    Logs TabbedContent.-maximized {
        height: 1fr;
        Log, RichLog { height: 1fr; }
    }
    """

    YOU_DIED_TITLE = """                                                                      
    ___       ___       ___            ___       ___       ___       ___        
   /\__\     /\  \     /\__\          /\  \     /\  \     /\  \     /\  \       
  |::L__L   /::\  \   /:/ _/_        /::\  \   _\:\  \   /::\  \   /::\  \      
  |:::\__\ /:/\:\__\ /:/_/\__\      /:/\:\__\ /\/::\__\ /::\:\__\ /:/\:\__\     
  /:;;/__/ \:\/:/  / \:\/:/  /      \:\/:/  / \::/\/__/ \:\:\/  / \:\/:/  /     
  \/__/     \::/  /   \::/  /        \::/  /   \:\__\    \:\/  /   \::/  /      
             \/__/     \/__/          \/__/     \/__/     \/__/     \/__/       
                                                                                
                       and yes, it's a Dark Souls reference                     
    """

    def compose(self) -> ComposeResult:
        yield RichLog(max_lines=10_000, wrap=True, markup=True)

    def on_mount(self) -> None:
        pass
    
    def write_framed_message(self, message: str, box_style: Box = ROUNDED, 
                           title: str = "", style: str = "white") -> None:
        """Write a message wrapped in an ASCII frame"""
        rich_log = self.query_one(RichLog)
        
        # Create a panel with the message
        panel = Panel(
            message,
            box=box_style,
            title=title,
            title_align="left",
            style=style,
            padding=(0, 1)
        )
        rich_log.write(panel)

    def write_action_message(self, action_type: str, message: str) -> None:
        """Write action messages with themed frames"""
        box_styles = {
            "strength": (ROUNDED, "bold #b7bb26"),
            "dexterity": (ROUNDED, "bold #85a598"), 
            "intelligence": (ROUNDED, "bold #fd8019"),
            "charisma": (ROUNDED, "bold #fa4934"),
            "default": (ROUNDED, "bold #ebdbb2"),
            "options": (ROUNDED, "#595959"),
            "game-over" : (ROUNDED, "bold #fa4934"),
            "health" : (ROUNDED, "bold #8ec07c")
        }
        
        box, style = box_styles.get(action_type.lower(), box_styles["default"])
        
        # Custom title for default action type
        if action_type.lower() == "default":
            title = "DUNGEON MASTER"
        elif action_type.lower() == "options":
            title = "CHOOSE YOUR ACTION"
        elif action_type.lower() == "game-over":
            title = "GAME OVER"
        else:
            title = f"{action_type.upper()}"
        
        self.write_framed_message(
            message,
            box_style=box,
            title=title,
            style=style
        )
        
    def write_death_msg(self) :
        self.write_action_message("game-over", self.YOU_DIED_TITLE)
        
        
        
class SidePanel(containers.VerticalGroup) :
    
    DEFAULT_CSS="""
    
    #user_stats {
        height: 1fr;
        background-tint: #282828;
        border: round white 10%;
        border-title-align: center;
    }
    
    #card_description {
        height: 1fr;
        background-tint: #282828;
    }
    
    #card_display {
        height: 2fr;
        background-tint: #282828;
        border: round white 10%;
    }
    
    
    """
    
    CARD_SAMPLE = """
┌───────────┐
│0X         │
│           │
│           │
│     #     │
│           │
│           │
│         0x│
└───────────┘
    """
    
    def compose(self) -> ComposeResult:
        with containers.Container():
            
            user_stats = UserStats(id="user_stats")
            user_stats.border_title = "Your Stats"
            yield user_stats
            
            # card_description = TextArea("This text area will show card descriptions.", language=None, id="card_description", read_only=True, show_cursor=False)
            # card_description.border_title = "Card Description"
            # yield card_description
            
            # Use Static widget with Rich alignment instead of TextArea
            card_description = Static(id="card_description")
            yield card_description

            
            # Use Static widget with Rich alignment instead of TextArea
            card_display = Static(id="card_static")
            yield card_display

    def on_mount(self) -> None:
        self.update_card_display(self.CARD_SAMPLE)
        self.update_card_description("No description.")
        
    def update_card_display(self, card_ascii) :
        card_display = self.query_one("#card_static", Static)
    
        # Use the same color for both border and title
        border_and_title_color = "#454545"  # Using the card color for consistency
        card_color = "#ebdbb2"
        
        # Style the card content
        styled_card = f"[{card_color}]{card_ascii.strip()}[/]"
        centered_card = Align.center(styled_card)
        
        # Panel with border color matching the title color
        panel = Panel(
            centered_card,
            box=ROUNDED,
            style=border_and_title_color,  # Border now matches title color
            title=f"[{border_and_title_color}]Drawn Card[/]",  # Title with same color
            title_align="center"
        )
        card_display.update(panel)
        
    def update_card_description(self, description) :
        
        card_display = self.query_one("#card_description", Static)

        # Defensive
        if not isinstance(description, str):
            description = ""

        # Split only once
        parts = description.split(":", 1)
        left = parts[0] if len(parts) >= 1 else ""
        right = parts[1] if len(parts) == 2 else ""

        # CASE 1 — FORMAT LIKE "8H:"  → action factor only
        if left and right == "":  
            # left is like "8H" → numeric part is everything except last char (suit)
            numeric = left[:-1] if left[-1].isalpha() else left
            description_output = f"Most recent action performed with a scale factor of {numeric} points." if numeric.isdigit() else "No description."

        # CASE 2 — FORMAT LIKE "7H:xyz" → action factor + text
        elif left and right:
            numeric = left[:-1] if left[-1].isalpha() else left
            description_output = f"{right}"

        # Render
        border_and_title_color = "#454545"
        card_color = "#ebdbb2"

        styled_card = f"[{card_color}]{description_output.strip()}[/]"
        centered_card = Align.center(styled_card)

        panel = Panel(
            centered_card,
            box=ROUNDED,
            style=border_and_title_color,
            title=f"[{border_and_title_color}]Card Description[/]",
            title_align="center"
        )

        card_display.update(panel)
           
class MainPanel(containers.VerticalGroup) :
    
    DEFAULT_CSS = """
    #dungeon-master {
        border-title-align: center;
    }

    #action-buttons {
        border-title-align: center;
    }
    """
    
    def compose(self) -> ComposeResult:
        
        logs = Logs(id="dungeon-master")
        logs.border_title = "Dungeon Master"
        yield logs
        
        actions = ActionButtons(id="action-buttons")
        actions.border_title = "Actions"
        yield actions
    
    @on(Button.Pressed, "#strength-button")
    def on_button_press_strength(self, event: Button.Pressed) -> None:
        if self.app.game.person.is_dead == False:
            log_widget = self.query_one(Logs)
            log_widget.write_action_message(
                "strength", 
                "You flex your muscles and prepare to overcome the obstacle with raw power!"
            )
            self.app.DISABLE_BUTTONS = True
            self.update_game("Strength")


        
    @on(Button.Pressed, "#dexterity-button")
    def on_button_press_dexterity(self, event: Button.Pressed) -> None:
        if self.app.game.person.is_dead == False:
            log_widget = self.query_one(Logs)
            log_widget.write_action_message(
                "dexterity",
                "With lightning reflexes, you attempt to navigate the challenge with precision and grace."
            )
            self.app.DISABLE_BUTTONS = True
            self.update_game("Dexterity")


        
    @on(Button.Pressed, "#intelligence-button")
    def on_button_press_intelligence(self, event: Button.Pressed) -> None:
        if self.app.game.person.is_dead == False:
            log_widget = self.query_one(Logs)
            log_widget.write_action_message(
                "intelligence", 
                "You analyze the situation carefully, searching for patterns and logical solutions."
            )
            self.app.DISABLE_BUTTONS = True
            self.update_game("Intelligence")


        
    @on(Button.Pressed, "#charisma-button")
    def on_button_press_charisma(self, event: Button.Pressed) -> None:
        if self.app.game.person.is_dead == False:
            log_widget = self.query_one(Logs)
            log_widget.write_action_message(
                "charisma",
                "You turn on the charm, using wit and persuasion to sway the situation in your favor."
            )
            self.app.DISABLE_BUTTONS = True
            self.update_game("Charisma")

    def update_game(self, option):
        new_card = self.app.game.draw_card()
        side_panel = self.screen.query_one("#display-panel", SidePanel)
        
        story, options = self.app.game.next_turn(option, new_card)
        
        self.app.current_story = story.split(":")[1]
        self.app.current_option = options
        
        DM_OUTPUT = self.query_one("#dungeon-master")
        
        DM_OUTPUT.write_action_message("default", self.app.current_story)
        
        output_options = f"""
1. Strength : {self.app.current_option["Strength"]}
2. Dexterity : {self.app.current_option["Dexterity"]}
3. Intelligence : {self.app.current_option["Intelligence"]}
4. Charisma : {self.app.current_option["Charisma"]}
        """
        
        DM_OUTPUT.write_action_message("options", output_options)
        
        self.app.current_story = story
        self.app.current_option = option
        
        user_stats = self.app.screen.query_one("#user_stats", UserStats)
        user_stats.update_user_stats()
        
        if self.app.game.person.is_dead == True :
            logs = self.query_one("#dungeon-master")
            logs.write_action_message("game-over", logs.YOU_DIED_TITLE)
            return
        
        side_panel.update_card_display(new_card[1])
        
        side_panel.update_card_description(new_card[0])
        
        self.app.DISABLE_BUTTONS = False
          
class GameUI(Screen):
    
    DEFAULT_CSS = """
    #side_panel {
        width: 2fr;
        border: heavy white 20%;
        border-title-align: center;

    }
    #main_panel {
        width: 5fr; 
    }
    """

    def compose(self) -> ComposeResult:
        with containers.HorizontalGroup():
            v_group = containers.Vertical(id="side_panel")
            v_group.border_title = "Player's Deck"
            with v_group :
                yield SidePanel(id="display-panel")
            with containers.VerticalGroup(id="main_panel"):
                yield MainPanel()
                
    def on_mount(self):
        game_response = self.app.game.start(self.app.story_prompt)
        self.app.current_story = game_response[0]
        self.app.current_option = game_response[1]
        
        DM_OUTPUT = self.query_one("#dungeon-master")
        
        DM_OUTPUT.write_action_message("default", self.app.current_story)
        
        output_options = f"""
1. Strength : {self.app.current_option["Strength"]}
2. Dexterity : {self.app.current_option["Dexterity"]}
3. Intelligence : {self.app.current_option["Intelligence"]}
4. Charisma : {self.app.current_option["Charisma"]}
        """

        DM_OUTPUT.write_action_message("options", output_options)
        
        self.app.DISABLE_BUTTONS = False
        
class StartScreen(Screen):
    
    DISPLAY_TITLE = """
    ___       ___       ___       ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\  \     /\  \     /\  \     /\__\     /\  \     /\  \     /\__\     /\  \     /\  \  
  /::\  \   /::\  \   /::\  \   /::\  \   /:/  /    /::\  \   /::\  \   /:/ _/_   /::\  \   /::\  \ 
 /:/\:\__\ /::\:\__\ /::\:\__\ /:/\:\__\ /:/__/    /:/\:\__\ /:/\:\__\ /::-"\__\ /::\:\__\ /:/\:\__\\
 \:\/:/  / \:\:\/  / \/\::/  / \:\/:/  / \:\  \    \:\/:/  / \:\ \/__/ \;:;-",-" \:\:\/  / \:\/:/  /
  \::/  /   \:\/  /    /:/  /   \::/  /   \:\__\    \::/  /   \:\__\    |:|  |    \:\/  /   \::/  / 
   \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \|__|     \/__/     \/__/  
                                                                                                    
                                             by System33
    """
    
    DEFAULT_CSS = """
    StartScreen {
        align: center middle;
        background: $surface;
        background-tint: #282828;
    }

    Horizontal {
        width: 100%;
        align-horizontal: center;
    }

    /* Title styling */
    #title {
        width: auto;
        height: auto;
        /* border: heavy white 10%; */
        padding: 1;
        background: $boost;
        align-horizontal: center;
        background-tint: #282828;
    }

    #form-container {
        width: 60;
    }

    .form-field {
        width: 100%;
    }

    #api-key-input {
        height: 3;
        background-tint: #282828;
    }

    #story-input {
        height: 8;
        background-tint: #282828;
    }

    #button-container {
        width: 100%;
        height: auto;
        align-horizontal: center;
        margin: 1 0;
    }

    #start-button {
        width: 30;
    }
    """
    
    def compose(self) -> ComposeResult:
        # Main container that centers everything
        with containers.Center():
            with containers.Middle():
                
                # Title section - centered
                with containers.Horizontal():
                    yield Static(self.DISPLAY_TITLE, id="title")
                
                # Form section - centered  
                with containers.Horizontal():
                    with containers.Vertical(id="form-container"):
                        # API Key input
                        yield Input(
                            placeholder="Insert your dungeon key (API key) ...",
                            password=True,
                            id="api-key-input",
                            classes="form-field"
                        )
                        
                        # Story prompt input
                        yield TextArea(
                            "Insert how you want your story to begin...",
                            id="story-input",
                            classes="form-field",
                        )
                        
                        # Button container to center the narrower button
                        with containers.Horizontal(id="button-container"):
                            yield Button(
                                "Begin Adventure!",
                                variant="success",
                                id="start-button"
                            )
                            
    def on_mount(self) -> None:
        # Focus the API key input by default for better UX
        self.query_one("#api-key-input", Input).focus()

    @on(Button.Pressed, "#start-button")
    def on_start_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the start button press"""
        api_key_input = self.query_one("#api-key-input", Input)
        story_input = self.query_one("#story-input", TextArea)
        
        api_key = api_key_input.value.strip()
        story_prompt = story_input.text.strip()
        
        # Basic validation
        if not api_key:
            self.notify("Please enter an API key", severity="error")
            api_key_input.focus()
            return
            
        if not story_prompt:
            self.notify("Please enter a story prompt", severity="error")
            story_input.focus()
            return
        
        # Store the data (you can access these from other screens)
        self.app.api_key = api_key
        self.app.story_prompt = story_prompt
        
        self.app.game = Game(self.app.api_key)
        
        self.notify("Adventure begins!", severity="information")

        # Navigate to the game scro", outeen
        self.app.switch_screen("game-ui")  # Changed from push_screen to switch_screen
           
class GameApp(App[None]):
    
    DISABLE_BUTTONS = reactive(False)
    
    def compose(self) -> ComposeResult:
        self.app.theme = "gruvbox"
        self.app.DISABLE_BUTTONS = False

        # Install the screen but don't compose anything yet
        self.install_screen(StartScreen(), name="start-screen")
        self.install_screen(GameUI(), name="game-ui")
        # You need to yield at least one widget, even if it's empty
        yield Static()  # Or any placeholder widget

    def on_mount(self) -> None:
        # Push the screen after mounting
        self.push_screen("start-screen")

if __name__ == "__main__":
    app = GameApp()
    app.run()