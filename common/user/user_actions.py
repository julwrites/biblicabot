
# Local modules
from common import debug, text_utils
from common.telegram import telegram_utils
from common.classes import action


SUPPORTED_VERSIONS = ["NIV", "ESV", "KJV", "NASB", "NLT", "AMP"]

CMD_VERSION = "/version"
CMD_VERSION_PROMPT = "Please select a version of your choosing\n\
(if unsure, always go with the one you are comfortable with!)"
CMD_VERSION_BADQUERY = "I don't have this version!"

STATE_VERSION_PROMPT = "I\'ve changed your version to {}!"

class BibleUserAction(action.Action):
    def identifier(self):
        return '/version'

    def resolve(self, user_obj, msg):
        query = telegram_utils.strip_command(msg, self.identifier())

        if text_utils.is_valid(query):

            for ver in SUPPORTED_VERSIONS:

                if text_utils.text_compare(query, ver):
                    user_obj.set_version(ver)
                    user_obj.set_state(None)

                    telegram_utils.send_close_keyboard(\
                    STATE_VERSION_PROMPT.format(ver), user_obj.get_uid())
                    break
            else:
                telegram_utils.send_msg(CMD_VERSION_BADQUERY, user_obj.get_uid())

        else:
            telegram_utils.send_msg_keyboard(\
            CMD_VERSION_PROMPT, user_obj.get_uid(), SUPPORTED_VERSIONS)

            user_obj.set_state(self.identifier())

        return True

def get():
    return [
        BibleUserAction()
    ]