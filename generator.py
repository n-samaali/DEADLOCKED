from google import generativeai as genai
import re

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def call_ai(event, context, prompt=""):
    if prompt=="":
      prompt = f"""

      make a dungeons and dragons game where you are the dungeon master and you have to give me exactly 4 options. 
      output the four options (strength, dexterity, intelligence, charsima) in 
      a clear markdown table to be parsed (Extract rows of the form: | **Strength** | description |). There will be a turn logic where a card will be randomly pulled from the deck and each numbered card will scale the option
      and each figure (J,Q,K) returns an event. The card that was pulled will be provided to you and included in the next event in this format (2H:).
      For each turn, you have to follow the same context (We will feed you back the option that was chosen, but provide answers in a consisten format). Also, the
      character will have hp that will increase or decrease depending on the events. We will also provide the stats, do not assume stats, they will be handled
      programatically, you just have to keep that in mind.
      also output the dungeon maser prompts in a SEPERATE code block. If after I select an action, it results in the player being hurt, you have to give me a marker like Reduce:15 or Increase:20
      so I know to change the player's hp and format it properly. Do not tell the player about coding things like provide me this and that. Just do what you are told in the prompt.

      """
      prompt = context + prompt
    else:
      prompt = event + prompt
    return (chat_session.send_message(prompt)).text

def parse_options(markdown_table: str):
    """
    Parse a 4-option D&D-style table (Strength, Dexterity, Intelligence, Charisma)
    into a dictionary: { option_name: description }
    """

    options = {}

    # Extract rows of the form: | **Strength** | description |
    rows = re.findall(r"\|\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\s*\|", markdown_table, re.DOTALL)

    for option, desc in rows:
        option = option.strip()
        desc = desc.replace("\n", " ").strip()
        options[option] = desc

    return options

def extract_modifier(text: str):
    """
    Scans the entire paragraph and finds:
      - Reduce:X
      - Increase:X
    Returns (action, value) or (None, None)
    """
    match = re.search(r"(Reduce|Increase)\s*:\s*(\d+)", text, re.IGNORECASE)
    if match:
        action = match.group(1).capitalize()
        value = int(match.group(2))
        return action, value
    return None, None

# a = call_ai("")
# print(parse_options(a))