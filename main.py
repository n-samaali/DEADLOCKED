import csv
import io
from math import sin

from textual.app import App, ComposeResult
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import Traceback
from textual.containers import Horizontal, Vertical

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
                #tooltip="",
                #action="notify('You chose Strength')",
            )
            yield Button(
                "Dexterity",
                id="dexterity-button",
                variant="primary",
                #tooltip="The primary button style - carry out the core action of the dialog",
                #action="notify('You chose Dexterity')",
            )
            yield Button(
                "Intelligence",
                id="intelligence-button",
                variant="warning",
                #tooltip="The warning button style - warn the user that this isn't a typical button",
                #action="notify('You chose Intelligence')",
            )
            yield Button(
                "Charisma",
                id="charisma-button",
                variant="error",
                #tooltip="The error button style - clicking is a destructive action",
                #action="notify('You chose Charisma')",                
            )
            
        # with containers.ItemGrid(min_column_width=20, regular=True):
        #     yield Button("Default", disabled=True)
        #     yield Button("Primary", variant="primary", disabled=True)
        #     yield Button("Warning", variant="warning", disabled=True)
        #     yield Button("Error", variant="error", disabled=True)
        
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
                    yield Label("Dexteritiy", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_dexterity, id="dexterity", show_percentage=True, show_eta=False)
                    yield Label("Intelligence", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_intelligence, id="intelligence", show_percentage=True, show_eta=False)
                    yield Label("Charisma", classes="stat-label")
                    yield ProgressBar(total=100, gradient=gradient_charisma, id="charisma", show_percentage=True, show_eta=False)

        
    def on_mount(self) -> None:
        self.query_one("#health").update(progress=100)
        self.query_one("#strength").update(progress=70)
        self.query_one("#dexterity").update(progress=70)
        self.query_one("#intelligence").update(progress=70)
        self.query_one("#charisma").update(progress=70)

        
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

    DISPLAY_TITLE = """                                                                          
     ___       ___       ___       ___       ___                 ___            
    /\__\     /\  \     /\  \     /\__\     /\  \               /\__\           
   /:/  /    /::\  \   /::\  \   /:/ _/_   /::\  \             /:| _|_          
  /:/__/    /::\:\__\ /::\:\__\ /::-"\__\ /\:\:\__\           /::|/\__\         
  \:\  \    \:\:\/  / \/\::/  / \;:;-",-" \:\:\/__/           \/|::/  /         
   \:\__\    \:\/  /    /:/  /   |:|  |    \::/  /              |:/  /          
    \/__/     \/__/     \/__/     \|__|     \/__/               \/__/           
     ___       ___       ___       ___       ___       ___       ___            
    /\__\     /\  \     /\  \     /\  \     /\__\     /\  \     /\  \           
   /:/  /    /::\  \   /::\  \   /::\  \   /:| _|_   /::\  \   /::\  \          
  /:/__/    /::\:\__\ /:/\:\__\ /::\:\__\ /::|/\__\ /:/\:\__\ /\:\:\__\         
  \:\  \    \:\:\/  / \:\:\/__/ \:\:\/  / \/|::/  / \:\/:/  / \:\:\/__/         
   \:\__\    \:\/  /   \::/  /   \:\/  /    |:/  /   \::/  /   \::/  /          
    \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/           
                                                                                
                                by System33                                    
    
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
        self.write_action_message("default", self.DISPLAY_TITLE)
    
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
            "default": (ROUNDED, "bold #ebdbb2")
        }
        
        box, style = box_styles.get(action_type.lower(), box_styles["default"])
        
        # Custom title for default action type
        if action_type.lower() == "default":
            title = "DM"
        else:
            title = f"{action_type.upper()} ACTION"
        
        self.write_framed_message(
            message,
            box_style=box,
            title=title,
            style=style
        )
        
        
        
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
        border: round white 10%;
        border-title-align: center;
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
            
            card_description = TextArea("This text area will show card descriptions.", language=None, id="card_description", read_only=True, show_cursor=False)
            card_description.border_title = "Card Description"
            yield card_description
            
            # Use Static widget with Rich alignment instead of TextArea
            card_display = Static(id="card_static")
            yield card_display

    def on_mount(self) -> None:
        self.update_card_display(self.CARD_SAMPLE)
        
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
        log_widget = self.query_one(Logs)
        log_widget.write_action_message(
            "strength", 
            "You flex your muscles and prepare to overcome the obstacle with raw power!"
        )
        
    @on(Button.Pressed, "#dexterity-button")
    def on_button_press_dexterity(self, event: Button.Pressed) -> None:
        log_widget = self.query_one(Logs)
        log_widget.write_action_message(
            "dexterity",
            "With lightning reflexes, you attempt to navigate the challenge with precision and grace."
        )
        
    @on(Button.Pressed, "#intelligence-button")
    def on_button_press_intelligence(self, event: Button.Pressed) -> None:
        log_widget = self.query_one(Logs)
        log_widget.write_action_message(
            "intelligence", 
            "You analyze the situation carefully, searching for patterns and logical solutions."
        )
        
    @on(Button.Pressed, "#charisma-button")
    def on_button_press_charisma(self, event: Button.Pressed) -> None:
        log_widget = self.query_one(Logs)
        log_widget.write_action_message(
            "charisma",
            "You turn on the charm, using wit and persuasion to sway the situation in your favor."
        )
        
class GameApp(App[None]):
    
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
        self.app.theme = "gruvbox"
        with containers.HorizontalGroup():
            
            v_group = containers.Vertical(id="side_panel")
            v_group.border_title = "Player's Deck"
            with v_group :
                yield SidePanel()
            with containers.VerticalGroup(id="main_panel"):
                yield MainPanel()

if __name__ == "__main__":
    app = GameApp()
    app.run()