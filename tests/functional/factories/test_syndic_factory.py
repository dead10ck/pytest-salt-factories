# -*- coding: utf-8 -*-
"""
    tests.functional.factories.test_syndic_factory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functional tests for the salt syndic factory
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


def test_hook_basic_config_defaults_top_level_keys(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_defaults():
            return {
                'zzzz': True
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(failed=1)
    res.stdout.fnmatch_lines(
        ["*RuntimeError: The config defaults returned by * must only contain 3 top level keys: *"]
    )


def test_keyword_basic_config_defaults_top_level_keys(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1', config_defaults={'zzzz': True})
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(failed=1)
    res.stdout.fnmatch_lines(
        [
            "*RuntimeError: The config_defaults keyword argument must only contain 3 top level keys: *"
        ]
    )


def test_hook_basic_config_overrides_top_level_keys(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_overrides():
            return {
                'zzzz': True
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(failed=1)
    res.stdout.fnmatch_lines(
        ["*RuntimeError: The config overrides returned by * must only contain 3 top level keys: *"]
    )


def test_keyword_basic_config_overrides_top_level_keys(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1', config_overrides={'zzzz': True})
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(failed=1)
    res.stdout.fnmatch_lines(
        [
            "*RuntimeError: The config_overrides keyword argument must only contain 3 top level keys: *"
        ]
    )


def test_hook_basic_config_defaults(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_defaults():
            return {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_keyword_basic_config_defaults(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            config_defaults = {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1', config_defaults=config_defaults)
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_hook_basic_config_overrides(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_overrides():
            return {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_keyword_basic_config_overrides(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            config_overrides = {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1', config_overrides=config_overrides)
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_hook_simple_overrides_override_defaults(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_defaults():
            return {
                'syndic': {'zzzz': False},
                'master': {'zzzz': False},
                'minion': {'zzzz': False},
            }

        def pytest_saltfactories_syndic_configuration_overrides():
            return {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_keyword_simple_overrides_override_defaults(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            config_defaults = {
                'syndic': {'zzzz': False},
                'master': {'zzzz': False},
                'minion': {'zzzz': False},
            }
            config_overrides = {
                'syndic': {'zzzz': True},
                'master': {'zzzz': True},
                'minion': {'zzzz': True},
            }
            syndic_config = salt_factories.configure_syndic(
                request,
                syndic_id,
                master_of_masters_id='mom-1',
                config_defaults=config_defaults,
                config_overrides=config_overrides)
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_hook_nested_overrides_override_defaults(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_defaults():
            defaults = {
                'zzzz': False,
                'user': 'foobar',
                'colors': {
                    'black': True,
                    'white': False
                }
            }
            return {
                'syndic': defaults.copy(),
                'master': defaults.copy(),
                'minion': defaults.copy(),
            }

        def pytest_saltfactories_syndic_configuration_overrides():
            overrides = {
                'zzzz': True,
                'colors': {
                    'white': True,
                    'grey': False
                }
            }
            return {
                'syndic': overrides.copy(),
                'master': overrides.copy(),
                'minion': overrides.copy(),
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            expected_colors = {
                'black': True,
                'white': True,
                'grey': False
            }
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(request, syndic_id, master_of_masters_id='mom-1')
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            assert syndic_config['colors'] == expected_colors
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            assert syndic_master_config['colors'] == expected_colors
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
            assert syndic_minion_config['colors'] == expected_colors
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_keyword_nested_overrides_override_defaults(testdir):
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            defaults = {
                'zzzz': False,
                'user': 'foobar',
                'colors': {
                    'black': True,
                    'white': False
                }
            }
            overrides = {
                'zzzz': True,
                'colors': {
                    'white': True,
                    'grey': False
                }
            }
            expected_colors = {
                'black': True,
                'white': True,
                'grey': False
            }
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(
                request,
                syndic_id,
                master_of_masters_id='mom-1',
                config_defaults={
                    'syndic': defaults.copy(),
                    'master': defaults.copy(),
                    'minion': defaults.copy(),
                },
                config_overrides={
                    'syndic': overrides.copy(),
                    'master': overrides.copy(),
                    'minion': overrides.copy(),
                }
            )
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            assert syndic_config['colors'] == expected_colors
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            assert syndic_master_config['colors'] == expected_colors
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
            assert syndic_minion_config['colors'] == expected_colors
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)


def test_nested_overrides_override_defaults(testdir):
    testdir.makeconftest(
        """
        def pytest_saltfactories_syndic_configuration_defaults():
            defaults = {
                'zzzz': None,
                'user': 'foobar',
                'colors': {
                    'blue': False
                }
            }
            return {
                'syndic': defaults.copy(),
                'master': defaults.copy(),
                'minion': defaults.copy(),
            }

        def pytest_saltfactories_syndic_configuration_overrides():
            overrides = {
                'zzzz': False,
                'colors': {
                    'blue': True
                }
            }
            return {
                'syndic': overrides.copy(),
                'master': overrides.copy(),
                'minion': overrides.copy(),
            }
        """
    )
    p = testdir.makepyfile(
        """
        def test_basic_config_override(request, salt_factories):
            defaults = {
                'colors': {
                    'black': True,
                    'white': False
                }
            }
            overrides = {
                'zzzz': True,
                'colors': {
                    'white': True,
                    'grey': False
                }
            }
            expected_colors = {
                'black': True,
                'white': True,
                'grey': False,
                'blue': True
            }
            mom_config = salt_factories.configure_master(request, 'mom-1')
            syndic_id = 'syndic-1'
            syndic_config = salt_factories.configure_syndic(
                request,
                syndic_id,
                master_of_masters_id='mom-1',
                config_defaults={
                    'syndic': defaults.copy(),
                    'master': defaults.copy(),
                    'minion': defaults.copy(),
                },
                config_overrides={
                    'syndic': overrides.copy(),
                    'master': overrides.copy(),
                    'minion': overrides.copy(),
                }
            )
            assert 'zzzz' in syndic_config
            assert syndic_config['zzzz'] is True
            assert syndic_config['colors'] == expected_colors
            syndic_master_config = salt_factories.configure_master(request, syndic_id)
            assert 'zzzz' in syndic_master_config
            assert syndic_master_config['zzzz'] is True
            assert syndic_master_config['colors'] == expected_colors
            syndic_minion_config = salt_factories.configure_minion(request, syndic_id)
            assert 'zzzz' in syndic_minion_config
            assert syndic_minion_config['zzzz'] is True
            assert syndic_minion_config['colors'] == expected_colors
        """
    )
    res = testdir.runpytest("-v")
    res.assert_outcomes(passed=1)
