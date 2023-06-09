# Overview
Maxima is a massively multiplayer simultaneous-turn FFA strategy game

Players command civilians, soldiers, and heroes to farm, fight, and explore in a massive world interconnected by portals. Challenge limited # of players to skirmish in limited space.

# Victory
Persistent Match
no overall victory condition, so how to incentivize combat goal?
monthly leaderboards
-

Quick Match

# data (overworld_n.json)
- i_, r_, p_, u_ = island, region, portal, user

# Menu
Persistent Match
	show ~3x2 grid of matches as large rectangles
	map shows extent of player vision
	name #1 generic (eg. 24-47205)
	name #2 editable by player (eg. Bob's 
Quick Match
	click once to start search
	Quick Match Settings
		turn time
Map Editor
Help
Settings

# Player

# World
The game world is a network of islands connected vertically by portals
An island is a network of regions connected by footpaths

# Island
Random Generation
- on islands with randomly generated region locations, use Delaunay triangulation to determine which regions should have paths between them
- rotational symmetry for competitive matches
- increase density of regions to represent difficulty of terrain
- consider pacing difference between persistent/quick matches

## Overworld
bespoke graph theory for the civilized gamer

looks: heavenly, angular, geometric

## Underworld
weird math ghouls practicing stochastic necromancy

looks: twisted, warped, curvy

portals between both

Manual Generation
- that bespoke feel
- allow user-created maps

# Region
a region is a vertex in a graph of other regions
	
Structure
	Artificial
		Civilian (eg. farm, town, city, weather station, portal)
			consume 12 food at a civilian structure to create 1 new civilian unit (civ) there next turn
		Military (eg. watchtower, fort, castle, barracks)
			bring civ to military structure to upgrade it to soldier
		Hero
			bring civ to special structure to upgrade it to specialist
		
	Natural
		lake, 
Abundance
each turn, a region generates meals equal to its abundance
determined by five binary variables
	Terrain type
		fertile +1 / barren 0
	Season
		summer +1 / winter 0
		seasons affect a whole world at once
	Weather
		rainy +1 / sunny 0
		weather affects a whole island at once
		some heroes and structures predict weather
	Structure
		natural +1 / human 0
		forests have honeybees (yum), but parking lots don't (dumb)
	Combat
		bloodied +1 / pristine 0
		a region is bloodied for twelve turns when a unit dies in it

# Portal
portals are special structures in regions
when an army enters a portal region as its designated move:
	1. complete combat in that region
	2. if an army entering the region won combat

Portal Storms
- rare weather event

# Path
the connection along which units can move between two regions
Movement Mechanics
	press leftclick with mouse cursor over friendly region
	release leftclick with mouse cursor over valid path
	select number of soldiers to split (if more than one)
	select number of meals to split (if any soldiers split)
	both selection options should be skippable without clicking
	undo button
one-way paths
constricted paths

# Terrain
Vision
	infinite range
	no horizon
	blocking: mountains, hero abilities, structures
		
# Region
Slope
1-6 lanes visual
Gives one team
Each turn lasts the same length of time (eg. 30 second turn blitz or 24 hour turn correspondence). Players may set up zero or arbitarily many actions in planning phase of each turn. When turn timer dings periodically, all actions happen simultaneously and a new planning phase begins immediately.
 ARMY: the collection of units on a region

# Unit
All (?) player action in Maxima is done via units

Units are born as civilians in human structures

Transform into professionals when entering regions that have training structures
	soldier, messenger 100%
	cavalry? archers?
	
## Messenger
"Don't Shoot The Messenger
- 
Carry text messages written by user
	maximum 255 characters? (twitter? code efficiency?)
	canned messages to minimize toxicity/moderation? 
	complex canned system (contrast hearthstone w/ 6 canned emotes)
Move 1 region per turn with or without army
Coded messages can't be read when intercepted
Intercepted messages can be kept? Codebreaking minigame?
	Store length, turn generated, turn captured, origin region, player written
Decode by capturing origin region
Spy can't be intercepted except by another spy
Soldiers
	Combat strength = number of armies + number of regions supporting troops are arriving from. The region which combat occurs on is not a supporting region.
	Team differentiation: player name, colour, symbol, terrain, heroes
		Aesthetic: microbes, orcs/elves, aliens, digital/arcade, bugs, robots, gunpowder, beasts
	Distinct combat values?
		3/1 = 3 combat strength while moving and 1 combat strength while staying still
		different unit types in same formation?

# Combat
Combat happens once per turn in any region or path that contain units from 
at least two players and soldiers from at least one. The player with the highest combat strength wins outright with no losses. All units belonging to other players are removed from the game.

Resolve path combats first, then region combats.
Player combat strength at a region
	1. Add following values:
		# of armies ending their turn on that region
		# of directions
		buffs/debuffs from terrain, structures, heroes
Path combat: aA from rX moves into rY the same turn that aB from rY moves into rX
Region combat

Items
Generation
Upgrade quests from structs

# Food
regions generate 1 meal per abundance per turn
units consume 1 meal per unit per turn
allow players to press one button to generate new civilians on all valid units across the map, costing 12 food
total abundance in an area is the upper stable limit for units there
when turn rolls over, if an army has less food than it needs

surplus is stored (up to 30 per unit)

Correspondence time control options
	X moves over Y duration every Z days at T time
	4 moves over 30 minutes every 1 day at 19:00
		turns tick every day at 19:00, 19:10, 19:20, and 19:30
	1 move over 7 days every 7 day at Sundays 08:00 MST
		turns tick once per week on Sunday mornings
	"Ready" toggle to advance game if everyone is ready? Can portal logic handle asynchronous worlds?
		
allow players to view turn history (on delay?)
make a publically visible turn history once game ends

# Hero
- (maybe scrap for more types of professionals)

One hero per region max
- move function disallows allied heroes moving to other allied heroes
- after opposing armies clash, losing hero goes back to home structure
- heroes can't be hired by an army already led by a hero
- instead of hero units, transform every unit into different type when brought onto appropriate structure
  - all units start life as civilians with low or zero food upkeep, no combat value, no abilities
  - one-time food cost per unit transformed (5 civs -> 5 soldiers = 5 food, 5 civs -> 5 knights = 15 food)
  - disallow mixing of different allied unit types
  - messenger, engineer, 

Hiring
- when bringing an army to a hero structure, check:
	- is the hero not currently hired and active elsewhere?
	- does the army have enough food to feed itself this turn?
	- after feeding itself, enough food to hire the hero?
	- is the army not currently led by a hero?
- if yes to all above, then hiring cost is applied, occupying army gains a hero unit, and next turn player may issue commands to the new hire
	
Food
- hiring cost should be vary from normal 12-meal regular citizen birth

## Hero ability brainstorming
	Decoy armies - fake armies with no combat value that look normal to opponents.
	Roadbuilding - increase unit movement across a path.
	Catapult - bombard a region from a distance.
	Balloon - increases sight range by x/x+y/x+2y while stationary for 1/2/3+ turns.
	Far Sight - pick a direction (any of 360°) and a distance (in km), then reveal an area around that point until a new area is picked.
	Portal - create a portal structure on the current region (maximum 2). Units moving into one portal structure region will instead move into the other and deal combat damage there. Units starting their turn in a portal structure region can move as if they are in either one.
	Arson - destroy all structures on current region.
	Scribe's
	Swap hero's struct (anywhere) with the struct at hero's location
	Necromancer
		If part of an attack victory, create 1 skeleton army behind.
	Drummer
		Combat strength 0 when moving more than 1. +1 movement.
	Skeleton King
		No army death from starvation. (Starved armies instead become skeletons?)