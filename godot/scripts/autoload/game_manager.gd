extends Node
## Global game state and scene-switching, accessible from anywhere without
## manual references between scenes. Grows as each build phase needs it -
## deliberately empty beyond the basics for now.

var current_level: int = 1
var player_health: int = 100
