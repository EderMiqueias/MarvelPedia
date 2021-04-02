import falcon
import json
import requests

from .key_manager import get_hash_ts


class CharactersResource(object):
    def on_get(self, req, resp, character_id=None):
        if character_id is not None:
            rf = ["id", "name", "description", "comics"]
        else:
            rf = ["id", "name"]

        characters = self.get_characters(character_id, rf)
        resp.body = json.dumps(characters)
        resp.status = falcon.HTTP_200

    def get_characters(self, character_id, required_fields, apply_filter=True) -> dict:
        s = f"/{character_id}" if character_id else ""
        my_hash, ts = get_hash_ts()

        url = "https://gateway.marvel.com/v1/public/" \
              "characters" + s + \
              "?ts=" + str(ts) + \
              "&apikey=947107e18f1a91614288b3e65c30d5ae" \
              "&hash=" + my_hash
        r = requests.get(url)

        if apply_filter:
            character_json = self.filter_required_fields(
                json.loads(r.content)['data']["results"],
                required_fields
            )
        else:
            character_json = json.loads(r.content)['data']["results"]

        return character_json

    def filter_required_fields(self, characters_list, required_fields) -> list:
        filtered_list = list()
        for character in characters_list:
            filtered_character = dict()
            for field in required_fields:
                filtered_character[field] = character[field]
            filtered_list.append(filtered_character)
        return filtered_list


app = falcon.API()
characters = CharactersResource()
app.add_route('/characters/{character_id}', characters)
app.add_route('/characters/', characters)
