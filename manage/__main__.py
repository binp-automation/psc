import sys
import argparse
import logging
from manage.components.base import Context
from manage.remote.ssh import SshDevice
from manage.tree import components

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Power supply controller software development automation tool",
        usage="python3 -m manage <component>.<task> [options...]",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    available_components_text = "\n".join([
        "Available components:",
        *[f"\t{name}" for name in components.keys()],
    ])
    parser.add_argument(
        "comptask", type=str, metavar="<component>.<task>",
        help="\n".join([
            "Component and task you want to run.",
            available_components_text,
        ]),
    )
    parser.add_argument(
        "--no-deps", action="store_true",
        help="Run only specified task without dependencies.",
    )
    parser.add_argument(
        "--device", type=str, metavar="<address>[:port]", default=None,
        help="\n".join([
            "Device to deploy and run tests.",
            "Requirements:",
            "+ Debian Linux running on the device (another distros are not tested).",
            "+ SSH server running on the device on the specified port (or 22 if the port is not specified).",
            "+ Possibility to log in to the device via SSH by user 'root' without password (e.g. using public key)."
        ])
    )
    parser.add_argument(
        "--no-capture", action="store_true",
        help="Display task stdout.",
    )
    args = parser.parse_args()

    names = args.comptask.rsplit(".", 1)
    component_name = names[0]
    try:
        component = components[component_name]
    except KeyError:
        print("\n".join([
            f"Unknown component '{component_name}'.",
            available_components_text
        ]))
        exit(1)

    available_tasks_text = "\n".join([
        f"Available tasks for component '{component_name}':",
        *[f"\t{name}" for name in component.tasks().keys()],
    ])
    if len(names) == 1:
        print("\n".join([
            "No task provided.",
            available_tasks_text,
        ]))
        exit(1)
    elif len(names) == 2:
        task_name = names[1]
        try:
            task = component.tasks()[task_name]
        except KeyError:
            print("\n".join([
                f"Unknown task '{task_name}'.",
                available_tasks_text,
            ]))
            exit(1)
    else:
        print("Bad action syntax. Expected format: '<component>.<task>'.")
        exit(1)

    device = None
    if args.device:
        device = SshDevice(args.device)

    capture = not args.no_capture

    context = Context(
        device=device,
        capture=capture,
    )

    def print_title(text, char="*"):
        assert len(char) == 1
        length = len(text) + 2
        print("\n".join([
            "",
            char * length,
            f"{char} {text}",
            char * length,
        ]), flush=True)

    def run_task(context, task, no_deps=False, title_length=64):
        if not no_deps:
            for dep in task.dependencies():
                run_task(context, dep, no_deps=no_deps, title_length=title_length)

        print_title(f"Running '{task.name()}'.", "*")

        try:
            task.run(context)
        except:
            print_title(f"Task '{task.name()}' failed!", "!")
            raise

    run_task(context, task, no_deps=args.no_deps)
