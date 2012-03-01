import urllib2

import kitchen.text.converters as convert
import tw2.core as twc

from datetime import datetime

# TODO -- tw2 internationalization coming soon
#from tw2.core import li8n as _
_ = lambda s: s

class CaptchaValidator(twc.Validator):
    msgs = {
        'incorrect': _("Incorrect value."),
        'timeout': _("Too much time elapsed. Please try again."),
    }
    timeout = 5  # minutes

    def validate_python(self, value, state):
        import tw2.captcha

        payload = urllib2.unquote(value['payload']).encode('utf-8')
        try:
            model = self.captcha_widget.model_from_payload(payload)
        except:
            raise twc.ValidationError('incorrect', self)

        if model.plaintext != value['value']:
            raise twc.ValidationError('incorrect', self)

        elapsed = datetime.utcnow() - model.created
        if elapsed.seconds > self.timeout * 60:
            raise twc.ValidationError('timeout', self)
