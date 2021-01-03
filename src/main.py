
from flask import Blueprint, request

# from . import  config
from .. import config
from .main_controller import processUpdate
from .utils import make_request_simple


token = config.TOKEN
url_base = 'https://api.telegram.org/'

bp = Blueprint("main", __name__, url_prefix=f"/{config.NAME}")


@bp.route("/test", methods = ("GET",))
def test():
    return 'ok'


@bp.route('/getMe', methods=('GET',))
def index():
    return  make_request_simple(command = 'getMe')


@bp.route('/webhookInfo', methods=('GET',))
def getWebhookInfo():
    return make_request_simple(command = 'getWebhookInfo').text


@bp.route('/deleteWebhook', methods=('GET',))
def deleteWebhook():
    return make_request_simple(command = 'deleteWebhook').text


@bp.route("/postUpdate", methods = ("POST",))
def postUpdate():
    update = request.get_json()
    processUpdate(update, fake=True)
    return "ok"













