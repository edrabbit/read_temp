import sys
import time
import urllib
import urllib2

import read_temp


ACCESS_TOKEN = "YOUR ACCESS TOKEN HERE"
PROJECT_ID = "YOUR PROJECT ID HERE"

class StormLog(object):
    """A simple example class to send logs to a Splunk Storm project.

    Your ``access_token`` and ``project_id`` are available from the Storm UI.
    """

    def __init__(self, access_token, project_id, input_url=None):
        self.url = input_url or 'https://api.splunkstorm.com/1/inputs/http'
        self.project_id = project_id
        self.access_token = access_token

        self.pass_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.pass_manager.add_password(None, self.url, '', access_token)
        self.auth_handler = urllib2.HTTPBasicAuthHandler(self.pass_manager)
        self.opener = urllib2.build_opener(self.auth_handler)
        urllib2.install_opener(self.opener)

    def send(self, event_text, sourcetype='syslog', host=None, source=None):
        params = {'project': self.project_id,
                  'sourcetype': sourcetype}
        if host:
            params['host'] = host
        if source:
            params['source'] = source
        url = '%s?%s' % (self.url, urllib.urlencode(params))
        try:
            req = urllib2.Request(url, event_text)
            response = urllib2.urlopen(req)
            return response.read()
        except (IOError, OSError), ex:
            # An error occured during URL opening or reading
            raise


if __name__ == "__main__":
    log = StormLog(ACCESS_TOKEN, PROJECT_ID)
    if (len(sys.argv) > 1):
        while True:
            log_line = read_temp.log_line()
            log.send(log_line, sourcetype='temp_sensor', host='raspberrypi')
            time.sleep(float(sys.argv[1]))
    else:
        log_line = read_temp.log_line()
        log.send(log_line, sourcetype='temp_sensor', host='raspberrypi')
        exit()