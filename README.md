# Pokémon Type Rankings
Ranks each Pokémon type mathematically. Still very WIP with more advanced features coming soon. Supports triple types (offesive, defensive, and total).

## View it Online
You can view the data online at: https://pokemon-type-ranking.onrender.com. If the website seems down it is either being updated or is taking awhile to load. New visuals are being worked on.

## Building it Yourself
All files for assembling the data are available in the build folder. It's not very well sorted because I plan on creating a master build file. Until then use pkmjson2.py to assemble the pkm-score.json from pkmtypes.py. pkmoff2.py will create the basic .csvs, pkm-def.py will create the defensive score for each type combination. Use pkm-defupd8.py to merge the defence and offence .csvs (the base csv must be called '{number}type_combinations.csv' for this to work. Then run totalupd8.py to finalise the .csvs. You can then delete any extraneous .csvs and the visualiser should work at 127.0.0.1:8050 by default. Sorry it's unnecesarily complicated, the website version works much better.
