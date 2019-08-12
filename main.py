#from srcds.rcon import RconConnection
import random
import threading
from collections import Counter
import logging
import re

class Vote:
    config = {
        "vote_duration": 1.0,
        "num_map_candidates": 3,
        "vote_delay": 5
    }

    map_candidates = {}
    votes = {}
    voting_active = False

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename='mapvote.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Squad Map Voter initialized')
        self.load_config()
        t = threading.Thread(target=self.start_log_stream, args=())
        t.start()
        #self.rcon = RconConnection(self.config.get("rcon_ip"), port=int(self.config.get("rcon_port")), password=self.config.get("rcon_password"))

    def load_config(self):
        try:
            config = open("./options.cfg", "r")
            if config.mode == "r":
                line = config.readline()
                while line:
                    if line[0] != "#":
                        val = line.rstrip().split('=')
                        try:
                            self.config.update({val[0]: val[1]})
                        except:
                            logging.error('Error in configuration file format!')
                    line = config.readline()
        except:
            logging.error('Error loading configuration file!')
        else:
            logging.debug('Configuration file loaded successfully')
        finally:
            config.close()

    def start_vote_delay(self):
        time = float(self.config.get("vote_delay"))
        vote_delay_timer = threading.Timer(time, self.start_vote)
        vote_delay_timer.start()
        logging.info('Voting will begin in %f seconds.', time)

    def start_vote(self):
        if self.voting_active:
            logging.error('Voting cannot be started while a vote is still ongoing.')
            return

        self.map_candidates = self.get_map_candidates()

        candidates_string = ""
        for key in self.map_candidates:
            candidates_string += f"{key}. {self.map_candidates[key]} | "

        logging.info('Map candidates are %s', candidates_string)

        # Change to admin broadcast RCON
        msg = f"Map voting has begun! Type !vote followed by a number to vote. | {candidates_string}"
        print(msg)
        #self.rcon.exec_command(f'AdminBroadcast "{msg}"')

        time = float(self.config.get("vote_duration"))
        vote_timer = threading.Timer(time, self.end_vote)
        vote_timer.start()
        self.voting_active = True

        logging.info('Voting has been started and will end in %f seconds.', time)

    def end_vote(self):
        logging.info('Voting has been ended.')
        self.voting_active = False

        if not self.get_winning_map():
            logging.info('Voting has ended. No votes were cast!')
            #self.rcon.exec_command(f'AdminBroadcast "Voting has ended. No votes were cast!"')
            return

        winning_map, winning_map_votes = self.get_winning_map()

        if winning_map is None:
            logging.info('There was no winning map!')
            return

        # Change to admin broadcast RCON
        msg = f"Voting has ended. {winning_map} has won with {winning_map_votes} votes!"
        #self.rcon.exec_command(f'AdminBroadcast "{msg}"')

        #set next map to winning map
        #self.rcon.exec_command(f'AdminSetNextMap "{winning_map}"')

    def detect_match_start(self, log_line):
        match = re.search(r"LogOnline: GotoState: NewState: Playing", log_line)
        if match:
            self.start_vote_delay()

    def detect_user_vote(self, log_line):
        match = re.search(r"!vote", log_line)
        if match:
            if self.voting_active:
                self.parse_user_vote(log_line)
            else:
                logging.debug('A vote has been detected outside of the voting period: %s', log_line)

    def start_log_stream(self):
        try:
            server_log = open(self.config.get('server_log_path'), 'r')
            server_log.seek(0, 2)
            while True:
                line = server_log.readline()
                if line != "\n" and line != "":
                    self.detect_match_start(line)
                    self.detect_user_vote(line)
        except:
            logging.error('Error loading server log file!', exc_info=True)
        finally:
            server_log.close()

    def parse_user_vote(self, log_line):
        #save vote
        #TODO: parse out vote choice and user id
        voter_id = 123456
        vote_choice = 2
        if self.store_vote(voter_id, vote_choice):
            #notifiy voting user SUCCESS via Warn
            #self.rcon.exec_command(f'AdminWarnById "{voter_id}" Your vote has been recorded!')

            pass
        else:
            #notifiy voting user FAIL via warn
            #self.rcon.exec_command(f'AdminWarnById "{voter_id}" Your vote has not been recorded! Please make sure there is an ongoing vote and try again.')

            pass

    def store_vote(self, voter_id, vote_choice):
        if vote_choice not in self.map_candidates.keys():
            logging.debug('User with ID %i has submitted an invalid vote (%i).', voter_id, vote_choice)
            return False
        else:
            self.votes.update({voter_id:vote_choice})
            logging.info('User with ID %i has voted for option %i', voter_id, vote_choice)
            return True

    def get_winning_map(self):
        options = []
        if len(self.votes) <= 0:
            return False

        for key in self.votes:
            options.append(self.votes[key])

        votes_count = Counter(options)
        winning_value = votes_count.most_common(1)[0]
        winning_map_id = winning_value[0]
        winning_map_votes = winning_value[1]
        winning_map = self.map_candidates.get(winning_map_id)
        logging.info('Winning map is %s with %i / %i votes.', winning_map, winning_map_votes, len(self.votes))

        return [winning_map, winning_map_votes]

    def get_map_list(self):
        map_list = open(self.config.get('map_rotation_path'), 'r')
        maps = []
        try:
            if map_list.mode == "r":
                line = map_list.readline()
                while line:
                    if line != "\n":
                        maps.append(line)
                    line = map_list.readline()
        except:
            logging.error('Failed to load Map Rotation file.')
        finally:
            map_list.close()
        return maps

    def get_map_candidates(self):
        map_list = self.get_map_list()
        candidates = {}
        for i in range(int(self.config.get('num_map_candidates'))):
            candidates.update({i+1:map_list[random.randint(0,len(map_list))].rstrip()})
        return candidates

if __name__ == "__main__":
    v = Vote()
