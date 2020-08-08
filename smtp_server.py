from __future__ import print_function
from datetime import datetime
import asyncore
from smtpd import SMTPServer


class EmlServer(SMTPServer):
    no = 0

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                                       self.no)
        f = open(filename, 'wb')
        f.write(data)
        f.close()
        print('%s saved.' % filename)
        self.no += 1


def run():
    # start the smtp server on localhost:25
    foo = EmlServer(('localhost', 25), None)
    print("started")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
