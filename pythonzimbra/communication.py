""" Zimbra communication handler. """

import requests


class Communication(object):

    """ Zimbra communication handler.

    Sends requests to the zimbra SOAP server and returns the responses in a
/   dictionary.

    """

    url = None

    """ URL to the zimbra soap interface """

    timeout = None

    """ Timeout of the request """

    def __init__(self, url, cert, timeout=None):

        """ Initialize the communication handler.
        """

        self.url = url
        self.timeout = timeout
        self.cert = cert

    def send_request(self, request, response):

        """ Send the request.

        Sends the request and retrieves the results, formats them and returns
         them in a dict or a list (when it's a batchresponse). If something
         goes wrong, raises a SoapFailure or a HTTPError on system-side
         failures. Note: AuthRequest raises an HTTPError on failed
         authentications!

        :param request: The request to send
        :type request: pythonzimbra.request.Request
        :param response: A prebuilt response object
        :type response: pythonzimbra.response.Response
        :raises: pythonzimbra.exceptions.communication.SoapFailure or
                urllib2.HTTPError
        """

        #server_request = urllib2.urlopen(
        #    self.url,
        #    request.get_request(),
        #    self.timeout
        #)

        server_request = requests.post(self.url, data=request.get_request(),
                            #headers=request.headers, cert=self.cert,
                            cert=self.cert,
                            verify=False)

        try:

            server_response = server_request.content.decode('utf-8')

        except requests.HTTPError as e:

            # Return the exception to the caller on HTTPerrors

            raise e

        # Find the response for

        response.set_response(server_response.encode('utf-8'))
