from Classifier.utils import read_yaml
from pathlib import Path 
import pytest
from ensure.main import EnsureError

class Test_read_yaml:

    all_yaml_path=[
        'tests/data/empty.yaml',
        'tests/data/somthing.yaml',
    ]
    # def test_read_yaml_empty():
    #     with pytest.raises()

    def test_read_yaml_return(self):
        content=read_yaml(Path(self.all_yaml_path[-1]))
        assert isinstance(content, dict)

    @pytest.mark.parametrize("paths_to_yaml",all_yaml_path)
    def test_read_yaml_bad_dtype(self,paths_to_yaml):
        with pytest.raises(EnsureError):
            content=read_yaml(paths_to_yaml)