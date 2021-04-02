import falcon
import json
import requests

from .key_manager import get_hash_ts


class BaseResource(object):
    def get_content(self, content_id, required_fields, content_type, apply_filter=True) -> dict:
        s = f"/{content_id}" if content_id else ""
        my_hash, ts = get_hash_ts()
        if content_type not in ("characters", "comics"):
            raise TypeError("content_type must be 'characters' or 'comics'")

        url = "https://gateway.marvel.com/v1/public/" + \
              content_type + s + \
              "?ts=" + str(ts) + \
              "&apikey=947107e18f1a91614288b3e65c30d5ae" \
              "&hash=" + my_hash
        r = requests.get(url)

        if apply_filter:
            content_json = self.filter_required_fields(
                json.loads(r.content)['data']["results"],
                required_fields
            )
        else:
            content_json = json.loads(r.content)['data']["results"]

        return content_json

    @staticmethod
    def filter_required_fields(comics_list, required_fields) -> list:
        filtered_list = list()
        for character in comics_list:
            filtered_character = dict()
            for field in required_fields:
                filtered_character[field] = character[field]
            filtered_list.append(filtered_character)
        return filtered_list


class CharactersResource(BaseResource):
    def on_get(self, req, resp, character_id=None):
        if character_id is not None:
            rf = ["id", "name", "description", "comics"]
        else:
            rf = ["id", "name"]

        my_characters = self.get_content(character_id, rf, "characters")
        resp.body = json.dumps(my_characters)
        resp.status = falcon.HTTP_200


class ComicsResource(BaseResource):
    def on_get(self, req, resp, comic_id=None):
        if comic_id is not None:
            rf = ["id", "title", "variantDescription", "characters"]
        else:
            rf = ["id", "title"]

        comics = self.get_content(comic_id, rf, "comics")
        resp.body = json.dumps(comics)
        resp.status = falcon.HTTP_200


app = falcon.API()
characters = CharactersResource()
comics = ComicsResource()

app.add_route('/characters/{character_id}', characters)
app.add_route('/characters/', characters)
app.add_route('/comics/{comic_id}', comics)
app.add_route('/comics/', comics)
