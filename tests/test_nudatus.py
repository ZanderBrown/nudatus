# -*- coding: utf-8 -*-
"""
Tests for the nudatus module.
"""
import sys
import pytest
import nudatus
import tokenize

try:
    from unittest import mock
except ImportError:
    import mock
else:
    # mock_open can't read binary data in < 3.4.3
    # https://bugs.python.org/issue23004
    if (3, 4) <= sys.version_info < (3, 4, 3):
        import mock

if sys.version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins


def test_get_version():
    """
    Ensure a call to get_version returns the expected string.
    """
    result = nudatus.get_version()
    assert result == '.'.join([str(i) for i in nudatus._VERSION])


def test_mangle_script():
    """
    Check that mangle returns the expected output
    """
    script = ''
    real_mangled = b''
    with open('tests/bigscript.py') as f:
        script = f.read()
    assert len(script) > 0
    with open('tests/bigscript_mangled.py') as f:
        real_mangled = f.read().encode('utf-8')
    assert len(real_mangled) > 0
    mangled = nudatus.mangle(script)
    assert mangled == real_mangled


def test_mangle_with_bad_syntax():
    """
    Check that mangle throws an
    exception for a badly formatted script
    """
    script = ''
    with open('tests/bigscript_bad.py') as f:
        script = f.read()
    assert len(script) > 0
    with pytest.raises(tokenize.TokenError):
        nudatus.mangle(script)


def test_main_without_file(capfd):
    with mock.patch('sys.argv', ['nudatus']):
        with pytest.raises(SystemExit) as ex:
            nudatus.main()
            assert ex.value.code == 1
            out, err = capfd.readouterr()
            assert len(out) == 0
            assert err == "No file specified"


def test_main_with_file_without_output_file(capfd):
    script = ''
    with open('tests/bigscript_mangled.py') as f:
        script = f.read()
    assert len(script) > 0
    with mock.patch('sys.argv', ['nudatus', 'tests/bigscript.py']):
        nudatus.main()
        out, err = capfd.readouterr()
        assert len(err) == 0
        assert out == script


def test_main_with_file_with_output_file(capfd):
    expected = ''
    with open('tests/bigscript_mangled.py') as f:
        expected = f.read()
    assert len(expected) > 0
    script = ''
    with open('tests/bigscript.py') as f:
        script = f.read()
    assert len(script) > 0
    with mock.patch('sys.argv',
                    ['nudatus', 'tests/bigscript.py', 'testout.py']):
        m = mock.mock_open(read_data=script)
        with mock.patch.object(builtins, 'open', m):
            nudatus.main()
        m.assert_called_with('testout.py', 'w')
        handle = m()
        handle.write.assert_called_with(expected)
        out, err = capfd.readouterr()
        assert len(err) == 0
        assert len(out) == 0


def test_main_with_bad_script(capfd):
    with pytest.raises(SystemExit) as ex:
        with mock.patch('sys.argv', ['nudatus', 'tests/bigscript_bad.py']):
            nudatus.main()
        assert ex.value.code == 1
    out, err = capfd.readouterr()
    assert len(out) == 0
    assert len(err) > 0
    assert err.startswith('Error mangling tests/bigscript_bad.py:')


def test_tokenizer_import():
    t = (sys.version_info[0], 23)
    with mock.patch('sys.version_info', t):
        if sys.version_info < (3, 0):
            assert nudatus.tokenizer == tokenize.generate_tokens
        else:
            assert nudatus.tokenizer == tokenize.tokenize
