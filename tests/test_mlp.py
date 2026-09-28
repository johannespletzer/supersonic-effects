import itertools

import numpy as np
import pytest

from multilayer_perceptron.load_mlp import load_mlp

INPUT_NAMES = ["datemonth", "X_Cruise_alt", "X_Tg_FB", "X_EI_NOx", "X_EI_SO2", "X_EI_H2O", "X_EI_BC"]
TRAINING_RANGES = [(16.17, 19.83), (0, 174), (0, 22), (0, 1.0), (0, 5.53), (0, 0.0065)]
EXAMPLE_FLEET = [18.3, 60, 10, 0.3, 1.3, 0.003]
OTHER_FLEET = [16.5, 120, 5, 0.8, 4.0, 0.005]


@pytest.fixture(scope="module")
def sess():
    return load_mlp()


def run_single(sess, day_of_year, fleet):
    feed = {name: [[value]] for name, value in zip(INPUT_NAMES, [day_of_year, *fleet])}
    return sess.run(None, feed)[0]


def run_batch(sess, rows):
    rows = np.asarray(rows, dtype=np.float32)
    return sess.run(None, {name: rows[:, [i]] for i, name in enumerate(INPUT_NAMES)})[0]


def test_model_interface(sess):
    assert [i.name for i in sess.get_inputs()] == INPUT_NAMES
    assert all(i.type == "tensor(float)" for i in sess.get_inputs())
    assert run_single(sess, 1, EXAMPLE_FLEET).shape == (5, 1)


# Expected [O3 column change (DU), RF O3, RF H2O, RF BC, RF inorganic aerosols (mW/m2)]
@pytest.mark.parametrize(
    "day_of_year, fleet, expected",
    [
        (1, EXAMPLE_FLEET, [-3.0623672, 14.148865, 31.269156, -1.0573092, -5.8160567]),
        (182, EXAMPLE_FLEET, [-2.4493368, 31.451275, 22.825172, -2.165515, -12.26728]),
        (91, OTHER_FLEET, [-1.3820981, 10.316982, 56.266796, -3.5810843, -23.37438]),
        (273, OTHER_FLEET, [-1.9069461, -0.71658, 78.77595, -3.0080059, -24.343597]),
    ],
)
def test_reference_values(sess, day_of_year, fleet, expected):
    output = run_single(sess, day_of_year, fleet)[:, 0]
    assert output.tolist() == pytest.approx(expected, rel=1e-4, abs=1e-4)


def test_batch_matches_single_calls(sess):
    days = [1, 91, 300]
    fleets = [EXAMPLE_FLEET, OTHER_FLEET, [19.5, 10, 20, 0.1, 5.0, 0.001]]
    output = run_batch(sess, [[day, *fleet] for day, fleet in zip(days, fleets)])
    single = [run_single(sess, day, fleet)[:, 0] for day, fleet in zip(days, fleets)]
    np.testing.assert_allclose(output.reshape(-1, 5), single, rtol=1e-4, atol=1e-4)


def test_outputs_finite_at_training_range_corners(sess):
    rows = [[day, *corner] for day in (1, 365) for corner in itertools.product(*TRAINING_RANGES)]
    output = run_batch(sess, rows)
    assert output.shape == (5 * len(rows), 1)
    assert np.isfinite(output).all()
