from distutils.util import strtobool
import time

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

env.forward_agent = True


@task
def locally():
    global run, cd
    run, cd = local, lcd


@task
def remotely():
    global local, lcd
    local, lcd = run, cd


@task
def commit():
    with warn_only():
        result = local("git add -p && git commit")
    if result.failed and not confirm("Commit failed. Continue anyway?"):
        abort("Aborting at user request.")


@task
def pull(branch=None, remote="origin"):
    if remote and branch:
        local("git pull {} {}".format(remote, branch))
    else:
        local("git pull")


@task
def push(branch=None, remote="origin"):
    if remote and branch:
        local("git push {} {}".format(remote, branch))
    else:
        local("git push")


@task
def checkout(branch, new=False, remote=None):
    new = "-b" if new else ""
    remote = remote if remote else ""
    local("git checkout {} {} {}".format(new, branch, remote))


@task
def merge(branch):
    local("git merge {}".format(branch))


@task
def test():
    with lcd("./src"), warn_only():
        result = local("./manage.py test")
    if result.failed and not confirm("Test failed. Continue anyway?"):
        abort("Aborting at user request.")


@task
def pull_project(project, group, branch="master", update="True"):
    group_path = "~/projects/xiaoduo/{}".format(group)
    if not exists(group_path):
        run("mkdir -p {}".format(group_path))
    with cd(group_path):
        with warn_only():
            if run("test -d {}".format(project)).failed:
                run("git clone git@gitlab.xiaoduotech.com:{}/{}.git".format(
                    group, project))
            elif strtobool(update):
                with cd(project):
                    run("git reset --hard")
                    run("git clean -f -d")
                    with warn_only():
                        result = run("git checkout {}".format(branch))
                    if result.failed:
                        run("git remote update")
                        run("git checkout -b {0} origin/{0}".format(branch))
                    run("git pull")


@task
def pull_github_project(project, user=None, update="True"):
    user = user or project
    user_path = "~/projects/github.com/{}".format(user)
    if not exists(user_path):
        run("mkdir -p {}".format(user_path))
    with cd(user_path):
        with warn_only():
            if run("test -d {}".format(project)).failed:
                run("git clone git://github.com/{}/{}.git".format(
                    user, project))
            elif strtobool(update):
                with cd(project):
                    run("git reset --hard")
                    run("git pull")


@task
def deploy_project(project, group, package, branch="master",
                   app_env="production", supervisord_conf="supervisord.conf",
                   update_requirements="False", restart_daemon="False",
                   blueware_conf=None, supervisord_waiting=30,
                   ignore_oneapm=False):
    if supervisord_conf and isinstance(supervisord_conf, str):
        supervisord_conf = [supervisord_conf]

    pull_project(project, group, branch)

    with cd("~/projects/xiaoduo/{}/{}".format(group, project)):
        if not exists("bin") or not exists("include") or not exists("lib"):
            with cd(".."):
                run("~/python3/bin/pyvenv {}".format(project))

        if not exists("~/data/projects/xiaoduo/{}/{}".format(group, project)):
            run("mkdir -p ~/data/projects/xiaoduo/{}/{}/log".format(
                group, project))
            run("mkdir -p ~/data/projects/xiaoduo/{}/{}/upload".format(
                group, project))
            run("mkdir -p ~/data/projects/xiaoduo/{}/{}/cache".format(
                group, project))

        run("cp src/config/{}/* src/{}/config/".format(app_env, package))
        if supervisord_conf:
            for v in supervisord_conf:
                run("cp src/config/{}/{} ./".format(app_env, v))
        if blueware_conf:
            run("cp src/config/{}/{} ./".format(app_env, blueware_conf))

        with prefix("source bin/activate"):
            if strtobool(update_requirements):
                run("pip install -U -r requirements.txt")
            else:
                run("pip install -r requirements.txt")

            if not ignore_oneapm:
                run("pip install -i http://pypi.oneapm.com/simple --upgrade \
blueware --trusted-host pypi.oneapm.com")
                run("pip install -i http://pypi.oneapm.com/simple --upgrade \
oneapm-ci-sdk --trusted-host pypi.oneapm.com")

            if supervisord_conf and strtobool(restart_daemon):
                for i, v in enumerate(supervisord_conf):
                    if i > 0:
                        time.sleep(supervisord_waiting)
                    with warn_only():
                        if run("supervisorctl -c {} reload".format(v)).failed:
                            run("supervisord -c {}".format(v))
