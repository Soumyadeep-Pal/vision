import numpy as np

import brainscore
from brainscore.benchmarks import BenchmarkBase
from brainscore.benchmarks.screen import place_on_screen
from brainscore.metrics import Score
from brainscore.metrics.rdm import RDMMetric
from brainscore.model_interface import BrainModel
from brainscore.utils import LazyLoad

BIBTEX = """@article{zhu2019robustness,
            title={Robustness of object recognition under extreme occlusion in humans and computational models},
            author={Zhu, Hongru and Tang, Peng and Park, Jeongho and Park, Soojin and Yuille, Alan},
            journal={arXiv preprint arXiv:1905.04598},
            year={2019}
        }"""

DATASETS = ['extreme_occlusion']

# create functions so that users can import individual benchmarks as e.g. Zhu2019RDM
for dataset in DATASETS:
    # behavioral benchmark
    identifier = f"Zhu2019{dataset.replace('-', '')}RDM"
    globals()[identifier] = lambda dataset=dataset: _Zhu2019RDM(dataset)


class _Zhu2019RDM(BenchmarkBase):
    def __init__(self, dataset):
        self._metric = RDMMetric()
        self._assembly = LazyLoad(lambda: load_assembly(dataset))
        self._fitting_stimuli = brainscore.get_stimulus_set('yuille.Zhu2019_extreme_occlusion')
        self._visual_degrees = 8

        self._number_of_trials = 1

        super(_Zhu2019RDM, self).__init__(
            identifier=f'yuille.Zhu2019_{dataset}-rdm',
            ceiling_func=lambda: self._metric.ceiling(self._assembly),
            parent='yuille.Zhu2019',
            bibtex=BIBTEX, version=1)

    def __call__(self, candidate: BrainModel):
        fitting_stimuli = place_on_screen(self._fitting_stimuli, target_visual_degrees=candidate.visual_degrees(),
                                          source_visual_degrees=self._visual_degrees)
        candidate.start_task(BrainModel.Task.probabilities, fitting_stimuli)
        stimulus_set = place_on_screen(self._assembly.stimulus_set, target_visual_degrees=candidate.visual_degrees(),
                                       source_visual_degrees=self._visual_degrees)
        label_predictions = candidate.look_at(stimulus_set, number_of_trials=self._number_of_trials)
        raw_score = self._metric(label_predictions, self._assembly)
        ceiling = self.ceiling
        score = raw_score / ceiling.sel(aggregation='center')
        score.attrs['raw'] = raw_score
        score.attrs['ceiling'] = ceiling
        return score


def Zhu2019RDM():
    return _Zhu2019RDM(dataset='extreme_occlusion')


def load_assembly(dataset):
    assembly = brainscore.get_assembly(f'yuille.Zhu2019_{dataset}')
    return assembly