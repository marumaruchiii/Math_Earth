# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
NPC_ICON_SIZE = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/BoutiqueBitmap9x9_1.7.ttf'
UI_FONT_SIZE = 18
CHAT_FONT_SIZE = 36
MENU_FONT_SIZE = 48

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#444444'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# NPC
NPC_AVAILABLE_DISTANCE = 1.5 * TILESIZE

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'./graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'./graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'./graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'./graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'./graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 4,'graphic':'./graphics/particles/flame/fire.png'},
	'Ice1': {'strength': 10,'cost': 10,'graphic':'./graphics/particles/Ice1/Ice1.png'},
	'heal' : {'strength': 20,'cost': 4,'graphic':'./graphics/particles/heal/heal.png'}}

# item
item_data = {
	'item_0': {'graphic':'./graphics/item/book/0.png'},
	'item_1': {'graphic':'./graphics/item/book/1.png'},
	'item_2': {'graphic':'./graphics/item/book/2.png'},
	'item_3': {'graphic':'./graphics/item/book/3.png'},
	'item_4': {'graphic':'./graphics/item/food/0.png'},
	'item_5': {'graphic':'./graphics/item/food/1.png'},
	'item_6': {'graphic':'./graphics/item/food/2.png'},
	'item_7': {'graphic':'./graphics/item/food/3.png'},
	'item_8': {'graphic':'./graphics/item/food/4.png'},
	'item_9': {'graphic':'./graphics/item/book/0.png'},
    }

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'./audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'Cyclope2': {'health': 100,'exp':110,'damage':8,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo yellow': {'health': 70,'exp':120,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
