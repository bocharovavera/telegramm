import json
import logging

import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

#from .utils import parse_planetpy_rss

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

#logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


#def _display_planetpy_feed():
   # return render_to_string('feed.md', {'items': parse_planetpy_rss()})
def repeat_all_messages(message): # Название функции не играет никакой роли, в $
    TelegramBot.send_message(message.chat.id, message.text)


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            'help': _display_help,
            'feed': repeat_all_messages,
        }

        raw = request.body.decode('utf-8')
   #     logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)


