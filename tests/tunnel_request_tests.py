import jsondiff
import requests
import unittest


# class TestJa3erRequest(unittest.TestCase):
#
#     def setUp(self) -> None:
#         pass
#
#     def test_tunnel_request(self):
#         response_json: dict = None
#         validation_json: dict = {
#             'ja3_hash': 'b32309a26951912be7dba376398abc3b',
#             'ja3': '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
#         }
#         # todo: check difference
#
#         differce = jsondiff.diff(validation_json, response_json)


class TestHowsMySSLRequest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_tunnel_request(self):
        response_json: dict = None
        validation_json: dict = {
            'given_cipher_suites': [
                'TLS_GREASE_IS_THE_WORD_AA',
                'TLS_AES_128_GCM_SHA256',
                'TLS_AES_256_GCM_SHA384',
                'TLS_CHACHA20_POLY1305_SHA256',
                'TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256',
                'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
                'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384',
                'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384',
                'TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256',
                'TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256',
                'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA',
                'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                'TLS_RSA_WITH_AES_128_GCM_SHA256',
                'TLS_RSA_WITH_AES_256_GCM_SHA384',
                'TLS_RSA_WITH_AES_128_CBC_SHA',
                'TLS_RSA_WITH_AES_256_CBC_SHA'
            ],
            'ephemeral_keys_supported': True,
            'session_ticket_supported': True,
            'tls_compression_supported': False,
            'unknown_cipher_suite_supported': False,
            'beast_vuln': False,
            'able_to_detect_n_minus_one_splitting': False,
            'insecure_cipher_suites': {},
            'tls_version': 'TLS 1.3',
            'rating': 'Probably Okay'}

        differce = jsondiff.diff(validation_json, response_json)
        # self.assertIn()


if __name__ == '__main__':
    unittest.main()

