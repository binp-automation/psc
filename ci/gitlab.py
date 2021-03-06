from __future__ import annotations
import os
from manage.components.base import Task
from manage.tree import components
from manage.paths import BASE_DIR
from utils.strings import quote

def text_lines(*lines):
    return "".join([l + "\n" for l in lines])

def base_path(path):
    return os.path.relpath(path, BASE_DIR)

class Cache(object):
    def __init__(self):
        super().__init__()
    
    def is_cached(self, path):
        raise NotImplementedError

    def text(self) -> str:
        raise NotImplementedError

class Job(object):
    def __init__(self, task: Task, level: int, deps: list[Job]):
        super().__init__()
        self.task = task
        self.level = level
        self.deps = deps

    def name(self) -> str:
        return self.task.name()

    def stage(self) -> str:
        return quote(str(self.level))

    def text(self, cache: Cache) -> str:
        text = text_lines(
            f"{self.name()}:",
            f"  stage: {self.stage()}",
            f"  script:",
            f"    - python3 -u -m manage --no-deps --no-capture {self.name()}",
        )

        if len(self.deps) > 0:
            text += "  needs:\n"
            for dep in self.deps:
                text += f"    - {dep.name()}\n"

        artifacts = []
        for art in self.task.artifacts():
            if not cache.is_cached(art):
                artifacts.append(art)

        if len(artifacts) > 0:
            text += text_lines(
                "  artifacts:",
                "    paths:",
            )
            for art in artifacts:
                text += f"      - {base_path(art)}\n"

        return text

class Graph(object):
    def __init__(self):
        self.jobs = {}
        self.cache = cache

    def add(self, task: Task) -> Job:
        name = task.name()
        if name in self.jobs:
            return self.jobs[name]
        deps = []
        level = 0
        for dep in task.dependencies():
            dj = self.add(dep)
            level = max(level, dj.level + 1)
            deps.append(dj)
        job = Job(task, level, deps)
        self.jobs[name] = job
        return job

    def text(self, cache: Cache) -> str:
        text = ""

        stages = sorted(set([x.stage() for x in self.jobs.values()]))
        text += "\nstages:\n"
        for stg in stages:
            text += f"  - {stg}\n"

        sequence = [j for j in sorted(self.jobs.values(), key=lambda j: j.level)]
        for job in sequence:
            text += "\n"
            text += job.text(self.cache)
        
        return text

class PatternCache(Cache):
    def __init__(self, patterns):
        super().__init__()
        self.patterns = patterns
    
    def is_cached(self, path):
        relpath = base_path(path)
        # FIXME: Use * pattern
        return any([p.replace("*", "") in relpath for p in self.patterns])

    def text(self) -> str:
        text = ""
        if len(self.patterns) > 0:
            text += text_lines(
                "cache:",
                "  paths:",
            )
            for pat in self.patterns:
                text += f"    - {pat}\n"
        return text

if __name__ == "__main__":
    end_tasks = [
        "host_all.test",
        "imx7_all.build",
        "imx8mn_all.build",
    ]
    cache = PatternCache([
        #"target/epics_base_*",
        #"target/toolchain_*",
    ])

    graph = Graph()
    for etn in end_tasks:
        cn, tn = etn.split(".")
        task = components[cn].tasks()[tn]
        graph.add(task)

    text = f"# This file is generated by script '{base_path(__file__)}'\n\n"
    text += "image: agerasev/debian-psc\n"
    text += cache.text()
    text += graph.text(cache)
    print(text)
