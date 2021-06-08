from .. import data as test_data


class PodAssertions:
    @staticmethod
    def observe(resources):
        assert len(resources) == len(test_data.pod_examples)

    @staticmethod
    def match(resources):
        assert len(resources) == len(test_data.pod_examples) - 1

    @staticmethod
    def reconcile(capsys):
        capture = capsys.readouterr()
        assert 'bad deleted' in capture.out
        assert 'Unable to delete resource: raise' in capture.err
