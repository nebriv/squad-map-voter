
# This project is a work in progress and does not currently work! 

# Squad Map Voter
A simple script to allow users to vote for the next map to be played.

# Installation

## Configuration
*Configuration setup is required*

To configure Squad Map Voter, use the options.cfg file located in the same directory as the program.

`rcon_ip`: The IP address of your server.

`rcon_port`: The RCON port on your server.

`rcon_password`: The RCON password.

`map_rotation_path`: The file path to your MapRotation.cfg file. You may also use a separate file containing a list of only the maps you want to be used for voting in the same format as MapRotation.cfg.

`server_log_path`: The file path to your SquadGame.log

`vote_duration`: How long (in seconds) players will have to place their votes for a map.

`num_map_candidates`: The number of options users will have to choose from when voting. The recommended amount is 3.

`vote_delay`: How long to wait (in seconds) after the start of a match before initiating a map vote.


# Usage

Squad Map Voter will automatically select `<num_map_candidates>` random maps from the supplied `MapRotation.cfg` file and open up a vote for `<vote_duration>` seconds. Players will be able to vote in the chat using `!vote <choice>` where `<choice>` is the respective number for the map they would like to vote for. Voting will last for `<vote_duration>` seconds. When voting is complete, Squad Map Voter will broadcast the winner and set the next map.
