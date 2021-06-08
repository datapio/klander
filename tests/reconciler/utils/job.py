from .. import data as test_data


class JobAssertions:
    @staticmethod
    def observe(resources):
        assert len(resources) == len(test_data.job_examples)

    @staticmethod
    def match(resources):
        assert len(resources) == len(test_data.job_examples) - 1

    @staticmethod
    def reconcile(capsys):
        capture = capsys.readouterr()
        assert 'job/bad patched' in capture.out
        assert 'Unable to patch resource: raise' in capture.err
