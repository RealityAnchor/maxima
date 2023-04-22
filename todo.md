# github
- readme
- comments

# features
- pathfinding

# abandon pygame
- backend: Django (Model-Template-View)
- frontend: Vue (needs node.js)
- database: MongoDB
- hosting: Heroku

# API endpoints: 
- `/login` to authenticate users and start a session
- `/logout` to end a user's session
- `/gamestate` to send the client the current gamestate
- `/move` to allow the client to make a move and update the gamestate

# balance knobs
- islands per world
- regions/portals per island (256/6)
- food per citizen spawn (12)
- abundance density (0-5: 14, 144, 72, 12, 8, 6 ... up to +12 units per turn per island)
- player spawn density
- flanking bonus
- vision

# discord
- server = gameworld
- channel = team
- multiple AI or human players per team
- subordinates, delegation via team leadership hierarchy
  - (general, colonel, major, captain, lieutenant, sergeant, corporal, private)
- thread = island

# portals
- if portal_id == 0, the region has no portal