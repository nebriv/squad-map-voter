import requests
import time
import logging

class ServerCommands:

    def __init__(self, config):
        self.config = config
        logging.basicConfig(level=logging.DEBUG, filename='mapvote.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    def send_command(self, command):
        header = {'Authorization': self.config['MapVoter']['bm_token']}
        data = {"data":{"type":"rconCommand","attributes":{"command":"raw","options":{"raw":command}}}}
        try:
            requests.post(f"https://api.battlemetrics.com/servers/{self.config['MapVoter']['mb_server_id']}/command", headers=header, json=data)

        except:
            time.sleep(1)
            try:
                requests.post(f"https://api.battlemetrics.com/servers/{self.config['MapVoter']['mb_server_id']}/command", headers=header, json=data)
            except:
                logging.error(f'Error sending server command: {command}', exc_info=True)

    def broadcast(self, message):
        logging.info(f'[COMMAND] Broadcasting message: {message}')
        self.send_command(f'AdminBroadcast "{message}"')

    def set_map(self, map_name):
        logging.info(f'[COMMAND] Setting next map to: {map_name}')
        self.send_command(f'AdminSetNextMap "{map_name}"')
