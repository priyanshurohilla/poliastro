# coding: utf-8
import pytest

from numpy.testing import assert_array_almost_equal
from astropy import units as u
from poliastro.bodies import Earth

from poliastro.iod import izzo, vallado


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_vallado75(lambert):
    k = Earth.k
    r0 = [15945.34, 0.0, 0.0] * u.km
    r = [12214.83399, 10249.46731, 0.0] * u.km
    tof = 76.0 * u.min

    expected_va = [2.058925, 2.915956, 0.0] * u.km / u.s
    expected_vb = [-3.451569, 0.910301, 0.0] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof))
    assert_array_almost_equal(va.to(u.km / u.s).value,
                              expected_va.value,
                              decimal=4)
    assert_array_almost_equal(vb.to(u.km / u.s).value,
                              expected_vb.value,
                              decimal=5)


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_curtis52(lambert):
    k = Earth.k
    r0 = [5000.0, 10000.0, 2100.0] * u.km
    r = [-14600.0, 2500.0, 7000.0] * u.km
    tof = 1.0 * u.h

    expected_va = [-5.9925, 1.9254, 3.2456] * u.km / u.s
    expected_vb = [-3.3125, -4.1966, -0.38529] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof))
    assert_array_almost_equal(va.to(u.km / u.s).value,
                              expected_va.value,
                              decimal=4)
    assert_array_almost_equal(vb.to(u.km / u.s).value,
                              expected_vb.value,
                              decimal=4)


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_curtis53(lambert):
    k = Earth.k
    r0 = [273378.0, 0.0, 0.0] * u.km
    r = [145820.0, 12758.0, 0.0] * u.km
    tof = 13.5 * u.h

    # ERRATA: j component is positive
    expected_va = [-2.4356, 0.26741, 0.0] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof))
    assert_array_almost_equal(va.to(u.km / u.s).value,
                              expected_va.value,
                              decimal=3)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_molniya_der_zero_full_revolution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 10 * u.h

    expected_va = [2.000652697, 0.387688615, -2.666947760] * u.km / u.s
    expected_vb = [-3.79246619, -1.77707641, 6.856814395] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof, M=0))
    assert_array_almost_equal(va.to(u.km / u.s).value,
                              expected_va.value,
                              decimal=3)
    assert_array_almost_equal(vb.to(u.km / u.s).value,
                              expected_vb.value,
                              decimal=4)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_molniya_der_one_full_revolution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 10 * u.h

    expected_va_l = [0.50335770, 0.61869408, -1.57176904] * u.km / u.s
    expected_vb_l = [-4.18334626, -1.13262727, 6.13307091] * u.km / u.s

    expected_va_r = [-2.45759553, 1.16945801, 0.43161258] * u.km / u.s
    expected_vb_r = [-5.53841370, 0.01822220, 5.49641054] * u.km / u.s

    (va_l, vb_l), (va_r, vb_r) = lambert(k, r0, r, tof, M=1)
    assert_array_almost_equal(va_l.to(u.km / u.s).value,
                              expected_va_l.value,
                              decimal=3)
    assert_array_almost_equal(vb_l.to(u.km / u.s).value,
                              expected_vb_l.value,
                              decimal=4)
    assert_array_almost_equal(va_r.to(u.km / u.s).value,
                              expected_va_r.value,
                              decimal=3)
    assert_array_almost_equal(vb_r.to(u.km / u.s).value,
                              expected_vb_r.value,
                              decimal=4)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_raises_exception_for_non_feasible_solution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 5 * u.h

    with pytest.raises(ValueError) as excinfo:
        next(lambert(k, r0, r, tof, M=1))
    assert ("ValueError: No feasible solution, try M <= 0"
            in excinfo.exconly())


def test_computing_T_min_works():
    #try:
    next(izzo._find_xy(-0.9, 37.734608668435975, 0, 3, 1e-3))
    #except TypeError:
    #pytest.fail("Incorrect argument unpacking")
