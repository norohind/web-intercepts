import falcon
from pathlib import Path
from datetime import datetime
import hashlib
import json


class Upload:
    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        resp.status = falcon.HTTP_OK

        content = req.bounded_stream.read()
        json_content = json.loads(content)
        hostname = json_content['host']

        content_hash = hashlib.md5(content).hexdigest()

        file_path = Path('intercepts').joinpath(hostname)
        file_path.mkdir(exist_ok=True, parents=True)
        filename = file_path.joinpath(f'{datetime.now().isoformat().replace(":", "-")}.{content_hash}.json')

        with open(filename, mode='bw') as file:
            file.write(content)


application = falcon.App(cors_enable=True)
application.add_route('/upload', Upload())

if __name__ == '__main__':
    import waitress
    waitress.serve(application, host='127.0.0.1', port=3241)
