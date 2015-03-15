# -*- coding: utf8 -*-
"""
Module displaying the number of unread messages
on an IMAP inbox (configurable, may also be a 
comma-separated list of IMAP folders).

@author obb
"""

import imaplib
from time import time


class Py3status:

    # available configuration parameters
    cache_timeout = 60
    criterion = 'UNSEEN'
    imap_server = '<IMAP_SERVER>'
    mailbox = 'INBOX'
    name = 'Mail'
    password = '<PASSWORD>'
    port = '993'
    user = '<USERNAME>'

    def check_mail(self, i3s_output_list, i3s_config):
        mail_count = self._get_mail_count()

        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': '{}: {}'.format(self.name, mail_count)
        }

        new_mail_color = i3s_config['color_good']
        check_failed_color = i3s_config['color_bad']

        if mail_count == 'N/A':
            response['color'] = check_failed_color
        elif mail_count != 0:
            response['color'] = new_mail_color

        return response

    def _get_mail_count(self):
        try:
            mail_count = 0
            directories = self.mailbox.split(',')
            connection = imaplib.IMAP4_SSL(self.imap_server, self.port)
            connection.login(self.user, self.password)
            
            for directory in directories:
                connection.select(directory)
                unseen_response = connection.search(None, self.criterion)
                connection.close()
                mails = unseen_response[1][0].split()
                mail_count += len(mails)
            return mail_count

        except:
            return 'N/A'

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
    }
    while True:
        print(x.check_mail([], config))
        sleep(1)
