from .. import data as test_data


class ConfigMapAssertions:
    @staticmethod
    def observe(resources):
        assert len(resources) == len(test_data.configmap_examples)

    @staticmethod
    def match(resources):
        assert len(resources) == len(test_data.configmap_examples) - 1

    @staticmethod
    def reconcile(capsys):
        capture = capsys.readouterr()
        assert 'bad deleted' in capture.out
        assert 'Webhook sent back an error:' in capture.err
        assert 'Unable to send request to webhook:' in capture.err
        assert 'Unable to parse webhook response:' in capture.err
        assert 'Invalid webhook response:' in capture.err
