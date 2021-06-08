from .. import data as test_data


class SecretAssertions:
    @staticmethod
    def observe(resources):
        assert len(resources) == len(test_data.secret_examples)

    @staticmethod
    def match(resources):
        assert len(resources) == len(test_data.secret_examples) - 1

    @staticmethod
    def reconcile(capsys):
        capture = capsys.readouterr()
        assert 'secret/bad patched' in capture.out
        assert 'Webhook sent back an error:' in capture.err
        assert 'Unable to send request to webhook:' in capture.err
        assert 'Unable to parse webhook response:' in capture.err
        assert 'Invalid webhook response:' in capture.err
