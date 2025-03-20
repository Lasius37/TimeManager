# -------------------- IMPORTS --------------------
from pathlib import Path


# -------------------- CONSTANTS --------------------
# Path
ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"

# Titles
MAIN_TITLE = ""
CHRONO = "Chronomètre"
MULTICHRONO = "Chronomètres alternés"
TIMER = "Minuteur"
MULTITIMER = "Minuteur Tiers Temps"
SIMCHRONOS = "Chronomètres simultanés"

# Dimensions
BUTTON_WIDTH = 30
SPINBOX_WIDTH = 2
SMALL_DIAMETER = 120
BIG_DIAMETER = 240
MARGIN = 4
SMALL_PAD = 5
BIG_PAD = 10

# Sounds
ALARM = ASSETS / "alarm.wav"

# Fonts
SMALL_FONT = "Verdana", 12
BIG_FONT = "Verdana", 24
VERY_BIG_FONT = "Verdana", 48

# Images
ICONE = ASSETS / "icone.ico"
HOME = ASSETS / "home.png"
RUN = ASSETS / "run.png"
PAUSE = ASSETS / "pause.png"
RESET = ASSETS / "reset.png"
DOWN = ASSETS / "down.png"
UP = ASSETS / "up.png"

# Colors
CHRONO_COLOR = "#909090"
BG_COLOR = "#f0f0f0"
TXT_COLOR = "#000000"

# Time Manager
COEFFICIENT = 4/3
NUMBER = 2
MAX_SIM_CHRONOS = 16
MAX_MLT_CHRONOS = 10
