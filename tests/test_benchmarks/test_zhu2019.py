from pathlib import Path

import pytest
from pytest import approx

from brainio.assemblies import BehavioralAssembly
from brainscore import benchmark_pool
from tests.test_benchmarks import PrecomputedFeatures


@pytest.mark.private_access
class TestZhu2019:

    @pytest.mark.parametrize('benchmark', [
        'Zhu2019-response_match',
        'Zhu2019-accuracy',
    ])
    def test_in_pool(self, benchmark):
        assert benchmark in benchmark_pool

    @pytest.mark.parametrize('benchmark, expected_ceiling', [
        ('Zhu2019-response_match', approx(0.8113, abs=0.0001)),
        ('Zhu2019-accuracy', 1),
    ])
    def test_benchmark_ceiling(self, benchmark, expected_ceiling):
        benchmark = benchmark_pool[benchmark]

        if "engineering" in benchmark.identifier:
            assembly = benchmark._assembly
            ceiling = benchmark._ceiling(assembly)
            assert ceiling[(ceiling['aggregation'] == 'center')] == expected_ceiling
        else:
            ceiling = benchmark._ceiling
            assert ceiling == expected_ceiling

    @pytest.mark.parametrize('benchmark, model, expected_raw_score', [
        ('Zhu2019-response_match', 'alexnet', approx(0.470, abs=0.0001)),
        ('Zhu2019-accuracy', 'alexnet', approx(0.470, abs=0.001)),
        ('Zhu2019-response_match', 'resnet-18', approx(0.504, abs=0.0001)),
        ('Zhu2019-accuracy', 'resnet-18', approx(0.506, abs=0.001)),
    ])
    def test_model_raw_score(self, benchmark, model, expected_raw_score):

        # load features
        precomputed_features = Path(__file__).parent / f'{model}-{benchmark}.nc'
        benchmark = benchmark_pool[benchmark]
        precomputed_features = BehavioralAssembly.from_files(file_path=precomputed_features)
        precomputed_features = PrecomputedFeatures(precomputed_features,
                                                   visual_degrees=8.0,  # doesn't matter, features are already computed
                                                   )
        score = benchmark(precomputed_features)
        raw_score = score.raw

        # division by ceiling <= 1 should result in higher score
        assert score.sel(aggregation='center') >= raw_score.sel(aggregation='center')
        assert raw_score.sel(aggregation='center') == expected_raw_score

    @pytest.mark.parametrize('benchmark, model, expected_ceiled_score', [
        ('Zhu2019-response_match', 'alexnet', approx(0.579, abs=0.001)),
        ('Zhu2019-accuracy', 'alexnet', approx(0.470, abs=0.001)),
        ('Zhu2019-response_match', 'resnet-18', approx(0.621, abs=0.001)),
        ('Zhu2019-accuracy', 'resnet-18', approx(0.506, abs=0.001)),
    ])
    def test_model_ceiled_score(self, benchmark, model, expected_ceiled_score):
        # load features
        precomputed_features = Path(__file__).parent / f'{model}-{benchmark}.nc'
        benchmark = benchmark_pool[benchmark]
        precomputed_features = BehavioralAssembly.from_files(file_path=precomputed_features)
        precomputed_features = PrecomputedFeatures(precomputed_features,
                                                   visual_degrees=8.0,  # doesn't matter, features are already computed
                                                   )
        score = benchmark(precomputed_features)
        assert score[0] == expected_ceiled_score