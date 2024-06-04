import os
import subprocess

from aiohttp import web
from git import Repo

from utils.generate_github_signature import generate_github_signature


async def github_pull_updates(request: web.Request) -> web.Response:
    github_signature = request.headers.get("X-Hub-Signature")
    payload = await request.json()
    GITHUB_HOOK_SECRET = os.environ.get("GITHUB_HOOK_SECRET")

    print("Signature header from request:", github_signature)
    print("Secret from config:", GITHUB_HOOK_SECRET)
    print("Request body:", payload)

    generated_signature = generate_github_signature(GITHUB_HOOK_SECRET.encode("utf-8"), payload)
    if github_signature != generated_signature:
        print("X-Hub-Signature is incorrect")
        print("Generated signature is:", generated_signature)
        return web.Response(text="Error. Secret keys are not the same", status=403)

    repo = Repo()
    repo.git.stash()
    repo.remotes.origin.fetch()
    develop_branch = repo.remote().refs['develop']
    repo.git.merge(develop_branch)

    repo.git.stash("pop")

    try:
        # TODO: Reload app restart nginx, supervisor
        subprocess.run("sudo supervisorctl reread & sudo supervisorctl update & sudo systemctl reload nginx", check=True)
    except subprocess.CalledProcessError as ex:
        print("Can`t reload site")
        return web.Response(text=f"Error reloading application: {ex}", status=500)
    print("Webhook received and application reloaded successfully")
    return web.Response(text="Webhook received and application reloaded successfully", status=200)


async def api_docs(request: web.Request) -> web.Response:
    # Create pretty docs
    with open("docs_html/docs.html", 'r') as file:
        return web.Response(text=file.read(), content_type="text/html")
