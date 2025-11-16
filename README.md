# DEADLOCKED

Welcome, Travelers, to DEADLOCKED!

## Inspiration

Inspired by the famous Dungeons & Dragons fantasy role-playing game, DEADLOCKED adds chaos to the world-building by allowing cards to interact with the player and letting a soulless Dungeon Master lead the game...

## What it does

Do you want to explore a floating archipelago powered by lost clockwork giants? Or are you feeling more cozy and want to be a farmer in a calm village? Whatever your heart desires, DEADLOCKED is here to deliver!

## How we made it

As we were all familiar with web and model-based development, we really wanted to experiment with a new UI/UX for this, and we stumbled on the concept of a TUI (Text-based User Interface). And so, we used Python to make a fun game where the user relies solely on their keyboard to interact with the entire storyline! To make the game even more interactive, DEADLOCKED is an AI Wrapper where the storyline is decided by the user... or not? All prompts are AI-generated to make each story unique.

## Challenges we ran into

The hardest part was definitely integrating the backend and the frontend. User interactions were buggy; the actions, stats, and cards failed to display or behave appropriately on the game's interface. To ensure consistency, we had to provide the AI with a strict prompt to obtain consistent response bodies that could be parsed and fed back into the AI, allowing it to continue the story. Parsing was an essential but challenging task, as we needed responses to have a common structure to execute the algorithm. 

## Accomplishments we're proud of

System33 is especially proud of the UI of the game; the game is fully accessible and interactive solely through the terminal, which was definitely a huge limitation to the design. The color scheme also aligns with the vibe of the original *Dungeons & Dragons* name, which is intentional. On the backend, the AI's output is parsed to output a consistent response, tying the entire game experience together.

## What we learned

We all learned different things throughout this process, whether it was learning how to use CSS, frontend on Python, or how to create fun .md files for some... Developing a TUI game from the ground up definitely required a learning curve for all of us.

## What's next for DEADLOCKED?

Incorporating a persistence layer into the game is something we want to explore to keep track of the player's progress over time. In its current iteration, DEADLOCKED is available only in single-player mode. However, we want to allow multiple players to access the same story. The more, the merrier.