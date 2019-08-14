
# This project is a work in progress and is currently untested!

# Squad Map Voter
A simple script to allow users to vote for the next map to be played on a Squad game server. Battlemetrics and chat log streaming are required.

# Configuration
*Configuration setup is required*

To configure Squad Map Voter, copy the mapvote.example.ini to a file named mapvote.ini or include the following configuration options in an existing ini file.

[MapVoter]
bm_token=<battlemetrics authentication token>
bm_server_id=<battlemetrics server ID>
map_rotation_path=<path to server map rotation file>
server_log_path=<path to server log file>
vote_duration=<how many seconds to open voting>
num_map_candidates=<how many map choices for voting (max is 9)>
vote_delay=<how many seconds to wait after match start to start voting>
chat_log_path=<path to your chat logs>


# Usage
`python3 main.py <path to configuration file>`

Squad Map Voter will automatically select `<num_map_candidates>` random maps from the supplied map rotation file and open up a vote for `<vote_duration>` seconds. Players will be able to vote in the chat using `!vote <choice>` where `<choice>` is the respective number for the map they would like to vote for. Voting will last for `<vote_duration>` seconds. When voting is complete, Squad Map Voter will broadcast the winner and set the next map.
