import os
import subprocess

from aiohttp import web

GITHUB_HOOK_SECRET = os.environ.get("GITHUB_HOOK_SECRET")


async def github_pull_updates(request: web.Request) -> web.Response:  # TODO: change subprocess.run to something what can be async
    if request.headers.get("X-Hub-Signature") != GITHUB_HOOK_SECRET:
        return web.Response(text="Error. Secret keys are not the same", status=403)

    try:
        subprocess.run(f"git pull", shell=True)  # Pull changes from the GitHub repository
    except subprocess.CalledProcessError as e:
        return web.Response(text=f"Error pulling from GitHub: {e}", status=500)

    try:
        # Reload app
        subprocess.run(['touch', '/var/www/aiohttpsocialnetworkapi_pythonanywhere_com_wsgi.py'], check=True)
    except subprocess.CalledProcessError as e:
        return web.Response(text=f"Error reloading application: {e}", status=500)

    return web.Response(text="Webhook received and application reloaded successfully", status=200)


async def api_docs(request: web.Request) -> web.Response:
    # Create pretty docs
    with open("docs_html/docs.html", 'r') as file:
        return web.Response(text=file.read(), content_type="text/html")
