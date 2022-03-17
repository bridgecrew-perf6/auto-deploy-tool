import typer
from tabulate import tabulate
from collections import namedtuple
import logging
from typing import List, Optional
from manager.modules.file_manager import file, folder
from manager.modules.windows_service import wsm
from .messages import Messages
import click_spinner

cli = typer.Typer()
logger = logging.getLogger()

service_result = namedtuple("service_result", "computer service state status message")

def show_computers_results(results: list = None) -> None:

    if results is None:
        return

    tabulate_headers = ["Status", "Computer", "Service", "State", "Message"]
    tabulate_date = []

    for result in results:
        status = "OK" if result.status == Messages.SUCCESS else "X" if result.status == Messages.ERROR else "!" if result.status == Messages.WARNING else "-"
        tabulate_date.append([status, result.computer, result.service, result.state, result.message])
        logger.debug(
            f"Status: {status} | Computer: {result.computer} | Service: {result.service} | State: {result.state} | Message: {result.message}")

    print(tabulate(tabulate_date, headers=tabulate_headers, showindex="always", tablefmt="fancy_grid"))


@cli.command("restart")
def restart_service(
    service_name: str,
    remote_computer: Optional[List[str]] = typer.Option(
        default=None, help="The name of the remote computer. Default: local computer. You can use multiple times")
) -> None:

    computers = list(remote_computer)

    if not computers:
        computers.append(None)

    results: list = []
    state = None

    with click_spinner.spinner():
        for computer in computers:

            computer_label = "local" if computer is None else computer

            try:
                win_service = wsm.WSM(service_name=service_name, computer=computer)
                win_service.restart()

                state = win_service.get_state()

                results.append(service_result(computer_label, service_name, state,
                                              Messages.SUCCESS, "Service has been restarted."))

            except Exception as err:
                results.append(service_result(computer_label, service_name, state,
                                              Messages.ERROR, "unable to restart the service."))

                logger.exception(f"error to restart service: {service_name} - computer: {computer_label}. Err: {err}")

    show_computers_results(results)


@cli.command("start")
def start_service(service_name: str, remote_computer: Optional[List[str]] = typer.Option(
        default=None, help="The name of the remote computer. Default: local computer. You can use multiple times")) -> None:

    computers = list(remote_computer)

    if not computers:
        computers.append(None)

    results: list = []
    state = None

    with click_spinner.spinner():
        for computer in computers:

            computer_label = "local" if computer is None else computer

            try:
                win_service = wsm.WSM(service_name=service_name, computer=computer)
                win_service.start()

                state = win_service.get_state()

                results.append(service_result(computer_label, service_name, state,
                                              Messages.SUCCESS, "Service has been started."))

            except Exception as err:
                results.append(service_result(computer_label, service_name, state,
                                              Messages.ERROR, "unable to start the service."))

                logger.exception(f"error to start service: {service_name} - computer: {computer_label}. Err: {err}")

    show_computers_results(results)


@cli.command("stop")
def stop_service(service_name: str, remote_computer: Optional[List[str]] = typer.Option(
        default=None, help="The name of the remote computer. Default: local computer. You can use multiple times")) -> None:

    computers = list(remote_computer)

    if not computers:
        computers.append(None)

    results: list = []
    state = None

    with click_spinner.spinner():
        for computer in computers:

            computer_label = "local" if computer is None else computer

            try:
                win_service = wsm.WSM(service_name=service_name, computer=computer)
                win_service.stop()

                state = win_service.get_state()

                results.append(service_result(computer_label, service_name, state,
                                              Messages.SUCCESS, "Service has been stopped."))

            except Exception as err:
                results.append(service_result(computer_label, service_name, state,
                                              Messages.ERROR, "unable to stop the service."))

                logger.exception(f"error to stop service: {service_name} - computer: {computer_label}. Err: {err}")

    show_computers_results(results)


@cli.command("state")
def get_state_service(service_name: str, remote_computer: Optional[List[str]] = typer.Option(
        default=None, help="The name of the remote computer. Default: local computer. You can use multiple times")) -> None:

    computers = list(remote_computer)

    if not computers:
        computers.append(None)

    results: list = []
    state = None

    with click_spinner.spinner():
        for computer in computers:

            computer_label = "local" if computer is None else computer

            try:
                win_service = wsm.WSM(service_name=service_name, computer=computer)
                state = win_service.get_state()

                results.append(service_result(computer_label, service_name, state,
                                              Messages.SUCCESS, "Current service state"))

            except Exception as err:
                results.append(service_result(computer_label, service_name, state,
                                              Messages.ERROR, "unable to start the service."))

                logger.exception(f"error to start service: {service_name} - computer: {computer_label}. Err: {err}")

    show_computers_results(results)


@cli.command("deploy-update")
def deploy_update(service_name: str,
                  source_folder: str = typer.Argument(...),
                  destination_folder: str = typer.Argument(...),
                  ignore_pattern: Optional[List[str]] = typer.Option(None),
                  remote_computer: Optional[List[str]] = typer.Option(
                      default=None, help="The name of the remote computer. Default: local computer. You can use multiple times")
                  ) -> None:
    computers = list(remote_computer)

    if not computers:
        computers.append(None)

    logger.debug(f"deploy update for service {service_name} on [{computers}] ")

    results: list = []
    state = None

    with click_spinner.spinner():
        for computer in computers:
            computer_label = "local" if computer is None else computer

            logger.debug(f"computer: {computer}")

            try:
                win_service = wsm.WSM(service_name=service_name, computer=computer)
                state = win_service.get_state()
                win_service.stop()
                logger.debug("service has been stopped")

                logger.debug(f"copying files/folder from {source_folder} to {destination_folder}")
                f = folder.Folder()
                f.copy(source_folder, destination_folder, ignore_pattern=list(ignore_pattern))
                logger.debug("folder has been copied")

                win_service.start()
                state = win_service.get_state()
                logger.debug("service has been started")

                results.append(service_result(computer_label, service_name, state,
                                              Messages.SUCCESS, "Service has been deployed."))

            except Exception as err:
                results.append(service_result(computer_label, service_name, state,
                                              Messages.ERROR, "unable to deploy the service."))

                logger.exception(f"error to deploy service: {service_name} - computer: {computer_label}. Err: {err}")

    show_computers_results(results)
