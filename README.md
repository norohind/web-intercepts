An application to log results of XHR queries on web applications.

Frontend is a js script (tm_intercept_script.js) which installs using tampermonkey.
It intercepts result of every XHR query and sends to backend sent and received payload,
endpoint, status code, used http method, hostname.

Backend is web application with single available endpoint - `/upload`.
Frontend, on every intercepted XHR query, uploads intercepted data to `/upload` endpoint.
Backend stores received data organising it in tree like structure using files and directories
which can be found in folder `intercepts` in project root (will be created when needed by 
server automatically).

Every received record stores in `interpects/<domain.name>/datetime-md5(content).json` file.

There are options to reduce size of database and perform deduplication (based on content):
```shell
zstd --rm -z intercepts/*/*.json 2>&1 | grep -v "No such file or directory -- ignored" && python3 deduplication.py
```
Which will compress all raw json files using zstd and delete original files. Then, using
script `deduplication.py` will find duplicates and remove most old duplicates.