from __future__ import print_function

import os
import hashlib
import inspect
import shutil
import mimetypes

from django.conf import settings
from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    def send_messages(self, messages):
        base_dir = settings.EMAIL_FILE_PATH

        # Files will be stored in a dir which name is calculated
        # with inspection of where this method is called from.
        #
        # Knowing that a same function calling send_mail() multiple times
        # will have the same frame stack,
        # the emails sent by a same usage will be aggregated in a unique folder
        usage_aggregation_dir = hashlib.sha1(str(
            inspect.getouterframes(inspect.currentframe())
        ).encode('utf-8')).hexdigest()

        # we can now safely delete everything in base dir
        # except usage aggregation folder
        for d in os.listdir(base_dir):
            if d != usage_aggregation_dir:
                shutil.rmtree(os.path.join(base_dir, d), ignore_errors=True)

        for message in messages:
            message_dir = '__'.join(message.to).replace('@', '_AT_')
            target_dir = os.path.join(base_dir, usage_aggregation_dir, message_dir)
            os.makedirs(target_dir)

            # Write out raw email
            with open(os.path.join(target_dir, 'raw.log'), 'w') as f:
                print('%s' % message.message().as_string(), file=f)
                print('-' * 79, file=f)

            # Write out alternatives
            alternatives = getattr(message, 'alternatives', ())
            for idx, alternative in enumerate(alternatives):
                content, mimetype = alternative

                filename = os.path.join(target_dir, 'alternative-%d%s' % (
                    idx,
                    mimetypes.guess_extension(mimetype)
                        or '.%s' % DEFAULT_ATTACHMENT_MIME_TYPE,
                ))

                with open(filename, 'wb') as f:
                    f.write(content.encode('utf8'))

            # Write out attachments
            for idx, attachment in enumerate(message.attachments):
                _, content, mimetype = attachment

                if mimetype is None:
                    mimetype = DEFAULT_ATTACHMENT_MIME_TYPE

                filename = os.path.join(target_dir, 'attachment-%d%s' % (
                    idx,
                    mimetypes.guess_extension(mimetype) or '.txt',
                ))

                with open(filename, 'wb') as f:
                    f.write(content)
