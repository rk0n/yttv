import pytest

from yttv import YTTV


@pytest.fixture
def yttv():
    """Returns a YTTV instance with a loaded app"""
    yttv = YTTV()
    yttv.load_app()
    return yttv


def test_get_settings_tv_code(yttv):
    yttv.load_app()
    tv_code = yttv.get_settings_tv_code()
    assert len(tv_code) == 12
    yttv.stop_app()


def test_get_settings_tv_code_multiple_times(yttv):
    yttv.load_app()
    tv_code = yttv.get_settings_tv_code()
    assert len(tv_code) == 12
    yttv.reset_app()
    tv_code = yttv.get_settings_tv_code()
    assert len(tv_code) == 12
    yttv.stop_app()


# TODO: Write Test
def test_install_no_script(yttv):
    yttv.stop_app()


# TODO: Write Test
def test_load_app(yttv):
    yttv.stop_app()


# TODO: Write Test
def test_reset_app(yttv):
    yttv.reset_app()
    yttv.stop_app()


# TODO: Write Test
def test_stop_app(yttv):
    yttv.stop_app()
