from gaze_ocr._gaze_ocr import _distance_squared


def test_distance_squared():
    # Test same point
    assert _distance_squared((0, 0), (0, 0)) == 0

    # Test horizontal distance
    assert _distance_squared((0, 0), (3, 0)) == 9
    assert _distance_squared((3, 0), (0, 0)) == 9

    # Test vertical distance
    assert _distance_squared((0, 0), (0, 4)) == 16
    assert _distance_squared((0, 4), (0, 0)) == 16

    # Test diagonal distance (3-4-5 triangle)
    assert _distance_squared((0, 0), (3, 4)) == 25
    assert _distance_squared((3, 4), (0, 0)) == 25

    # Test negative coordinates
    assert _distance_squared((-1, -1), (2, 3)) == 25
    assert _distance_squared((2, 3), (-1, -1)) == 25

    # Test with floating point coordinates
    assert abs(_distance_squared((1.5, 2.5), (4.5, 6.5)) - 25.0) < 1e-10
