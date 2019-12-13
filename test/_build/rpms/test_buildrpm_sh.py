import pytest
import logging

import test.helper as h


def test_rpm_prvsnr_is_buildable(rpm_prvsnr):
    pass


@pytest.mark.isolated
@pytest.mark.env_name('centos7-base')
def test_rpm_prvsnr_depends_on_salt_2019_2_0(mhost):
    depends = mhost.check_output('rpm -qpR {}'.format(mhost.rpm_prvsnr))
    assert 'salt-master = 2019.2.0\n' in depends
    assert 'salt-minion = 2019.2.0\n' in depends


@pytest.mark.isolated
@pytest.mark.env_name('centos7-salt-installed')
def test_rpm_prvsnr_installation(mhost, mlocalhost):
    mhost.check_output('yum install -y {}'.format(mhost.rpm_prvsnr))

    excluded = ['-name "{}"'.format(e) for e in h.REPO_BUILD_DIRS]
    expected = mlocalhost.check_output(
        "cd {} && find {} \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            mlocalhost.repo,
            'pillar srv files/etc/salt',
            ' -o '.join(excluded)
        )
    ).split()

    excluded = ['-name "{}"'.format(e) for e in ['__pycache__', '*.pyc', '*.pyo']]
    installed = mhost.check_output(
        "cd {} && find {} \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            h.PRVSNR_REPO_INSTALL_DIR,
            'pillar srv files/etc/salt',
            ' -o '.join(excluded)
        )
    ).split()

    diff_expected = set(expected) - set(installed)
    diff_installed = set(installed) - set(expected)
    assert not diff_expected
    assert not diff_installed


def test_rpm_prvsnr_cli_is_buildable(rpm_prvsnr_cli):
    pass


@pytest.mark.isolated
@pytest.mark.env_name('centos7-base')
def test_rpm_prvsnr_cli_installation(mhost, mlocalhost):
    mhost.check_output('yum install -y {}'.format(mhost.rpm_prvsnr_cli))

    excluded_dirs = ['-name "{}"'.format(d) for d in h.REPO_BUILD_DIRS]
    expected = mlocalhost.check_output(
        "cd {} && find {} \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            mlocalhost.repo,
            'cli/utils files/etc/modprobe.d files/etc/sysconfig/network-scripts files/etc/yum.repos.d',
            ' -o '.join(excluded_dirs)
        )
    ).split()

    installed = mhost.check_output(
        "cd {} && find {} \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            h.PRVSNR_REPO_INSTALL_DIR,
            'cli/utils files/etc/modprobe.d files/etc/sysconfig/network-scripts files/etc/yum.repos.d',
            ' -o '.join(['-name "__pycache__"'])
        )
    ).split()

    diff_expected = set(expected) - set(installed)
    diff_installed = set(installed) - set(expected)
    assert not diff_expected
    assert not diff_installed

    # TODO need to fix rpm structure for cli scripts
    expected = mlocalhost.check_output(
        "cd {} && find . \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            mlocalhost.repo / 'cli/src',
            ' -o '.join(excluded_dirs)
        )
    ).split()

    installed = mhost.check_output(
        "cd {} && find . -maxdepth 1 \\( {} \\) -prune -o -type f -printf '%p\n'"
        .format(
            h.PRVSNR_REPO_INSTALL_DIR / 'cli',
            ' -o '.join(['-name "__pycache__"'])
        )
    ).split()

    diff_expected = set(expected) - set(installed)
    diff_installed = set(installed) - set(expected)
    assert not diff_expected
    assert not diff_installed