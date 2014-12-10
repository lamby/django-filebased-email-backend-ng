import os
import shutil
import mimetypes

from django.conf import settings
from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    def send_messages(self, messages):
        try:
            shutil.rmtree(settings.EMAIL_FILE_PATH)
        except OSError:
            pass

        os.makedirs(settings.EMAIL_FILE_PATH)

        for idx, message in enumerate(messages):
            base = os.path.join(settings.EMAIL_FILE_PATH, '%s' % idx)

            os.makedirs(base)

            # Write out raw email
            with open(os.path.join(base, 'raw.log'), 'w') as f:
                print >>f, '%s' % message.message().as_string()
                print >>f, '-' * 79

            # Write out alternatives
            alternatives = getattr(message, 'alternatives', ())
            for idx, alternative in enumerate(alternatives):
                content, mimetype = alternative

                filename = os.path.join(base, 'alternative-%d%s' % (
                    idx,
                    mimetypes.guess_extension(mimetype)
                        or '.%s' % DEFAULT_ATTACHMENT_MIME_TYPE,
                ))

                with open(filename, 'w') as f:
                    f.write(content.encode('utf8'))

            # Write out attachments
            for idx, attachment in enumerate(message.attachments):
                _, content, mimetype = attachment

                if mimetype is None:
                    mimetype = DEFAULT_ATTACHMENT_MIME_TYPE

                filename = os.path.join(base, 'attachment-%d%s' % (
                    idx,
                    mimetypes.guess_extension(mimetype) or '.txt',
                ))

                with open(filename, 'w') as f:
                    f.write(content)
