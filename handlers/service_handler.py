import logging
import os
import json

from aiohttp import web
from git import Repo

from utils.generate_github_signature import generate_github_signature


async def github_pull_updates(request: web.Request) -> web.Response:
    try:
        github_signature = request.headers.get("X-Hub-Signature")
        request_body = await request.json()
        payload = json.dumps(request_body, separators=(',', ':'))
        GITHUB_HOOK_SECRET = os.environ.get("GITHUB_HOOK_SECRET")\

        logging.info(f"Header github webhook signature: {github_signature}")
        logging.info(f"Github webhook payload: {payload}")
        logging.info(f"Secret key: {GITHUB_HOOK_SECRET}")

        generated_signature = generate_github_signature(GITHUB_HOOK_SECRET.encode("utf-8"), payload.encode("utf-8"))
        logging.info(f"Generated signature: {generated_signature}")
        if github_signature != generated_signature:
            logging.info(f"Error. Signatures are not the same")
            return web.Response(text="Error. Secret keys are not the same", status=403)

        logging.info(f"Pulling from repo started")
        repo = Repo()
        repo.git.stash()
        origin = repo.remote("origin")
        origin.pull("develop")
        repo.git.stash("pop")
        logging.info(f"Pulling from repo ended")

        os.popen("sudo supervisorctl restart aiohttp_gunicorn && sudo systemctl reload nginx.service")
        logging.info(f"Server restarted")
        return web.Response(text="Webhook received and application reloaded successfully", status=200)
    except Exception as ex:
        logging.info(f"Error: {str(ex)}")
        return web.Response(text=f"Error. Can`t reload service: {str(ex)}", status=500)


async def api_docs(request: web.Request) -> web.Response:
    # Create pretty docs
    with open("docs_html/docs.html", 'r') as file:
        return web.Response(text=file.read(), content_type="text/html")
