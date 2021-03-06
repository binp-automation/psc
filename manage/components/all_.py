from __future__ import annotations
import os
from manage.components.base import Component, Task, TaskWrapper, TaskList
from manage.components.epics.epics_base import EpicsBase
from manage.components.app import App
from manage.components.epics.ioc import AppIoc
from manage.components.mcu import Mcu
from manage.remote.tasks import RebootTask

class AllHost(Component):
    def __init__(
        self,
        epics_base: EpicsBase,
        app: App,
        ioc: AppIoc,
    ):
        super().__init__()
        self.epics_base = epics_base
        self.app = app
        self.ioc = ioc

        self.build_task = TaskWrapper(deps=[
            self.epics_base.tasks()["build"],
            self.app.tasks()["build_unittest"],
            self.app.tasks()["build_fakedev"],
            self.ioc.tasks()["build"],
        ])
        self.test_task = TaskWrapper(deps=[
            self.app.tasks()["run_unittest"],
            self.ioc.tasks()["test_fakedev"],
        ])

    def tasks(self) -> dict[str, Task]:
        return {
            "build": self.build_task,
            "test": self.test_task,
        }


class AllCross(Component):
    def __init__(
        self,
        epics_base: EpicsBase,
        app: App,
        ioc: AppIoc,
        mcu: Mcu,
    ):
        super().__init__()
        self.epics_base = epics_base
        self.app = app
        self.ioc = ioc
        self.mcu = mcu

        self.build_task = TaskWrapper(deps=[
            self.mcu.tasks()["build"],
            self.epics_base.tasks()["build"],
            self.ioc.tasks()["build"],
        ])
        self.deploy_task = TaskWrapper(deps=[
            self.mcu.tasks()["deploy"],
            self.epics_base.tasks()["deploy"],
            self.ioc.tasks()["deploy"],
        ])
        self.deploy_and_reboot_task = TaskWrapper(
            RebootTask(),
            deps=[self.deploy_task],
        )
        self.run_task = TaskWrapper(
            self.ioc.tasks()["run"],
            deps=[self.deploy_and_reboot_task],
        )

    def tasks(self) -> dict[str, Task]:
        return {
            "build": self.build_task,
            "deploy": self.deploy_task,
            "deploy_and_reboot": self.deploy_and_reboot_task,
            "run": self.run_task,
        }
