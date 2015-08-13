# coding=utf-8
from jetee.service.services.primary import PrimaryService
from jetee.service.services.postgresql import PostgreSQLService
from jetee.service.services.redis import RedisService

from jetee.project.projects import DjangoProject
from jetee.common.user_configuration import AppConfiguration
from jetee.processes import UWSGIProcess, CronProcess, CronJob, AbstractProcess


class BaseConfiguration(AppConfiguration):
    username = u'root'
    project_name = u'shorts'

    configuration = None
    branch = None

    def get_primary_service(self):
        app_service = PrimaryService(
            project=DjangoProject(
                cvs_repo_url=u'git@github.com:amureki/pyshorts.git',
                cvs_repo_branch=self.branch,
                apt_packages=[u'libjpeg-dev', ],
                web_process=UWSGIProcess(u'project/wsgi.py'),
            )
        )
        return app_service

    def get_secondary_services(self):
        return [PostgreSQLService(), RedisService()]


class Staging(BaseConfiguration):
    hostname = u'128.199.47.187'
    server_names = [u'shorts.amureki.me', ]

    configuration = u'Staging'
    branch = u'master'
