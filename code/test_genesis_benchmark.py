from genesis_benchmark import evaluate, fixture, repaired_predict


def test_repair_improves_and_closes_fixture():
    result = evaluate(fixture())
    assert result.baseline_correct < result.total
    assert result.repaired_correct == result.total
    assert result.promoted_coordinates


def test_every_selected_coordinate_is_used_by_a_collision():
    cases = fixture()
    result = evaluate(cases)
    for j in result.promoted_coordinates:
        reduced = [k for k in result.promoted_coordinates if k != j]
        try:
            repaired_predict(cases, reduced)
        except ValueError:
            continue
        raise AssertionError(f"coordinate {j} was not essential")
