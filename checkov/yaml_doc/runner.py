from __future__ import annotations

from typing import TYPE_CHECKING, Any

from checkov.common.bridgecrew.check_type import CheckType
from checkov.common.parsers.yaml.parser import parse
from checkov.common.runners.object_runner import Runner as ObjectRunner

if TYPE_CHECKING:
    from checkov.common.checks.base_check_registry import BaseCheckRegistry
    from checkov.common.graph.db_connectors.networkx.networkx_db_connector import NetworkxConnector
    from checkov.common.runners.graph_builder.local_graph import ObjectLocalGraph
    from checkov.common.runners.graph_manager import ObjectGraphManager


class Runner(ObjectRunner):
    check_type = CheckType.YAML  # noqa: CCE003  # a static attribute

    def __init__(
        self,
        db_connector: NetworkxConnector | None = None,
        source: str = "yaml",
        graph_class: type[ObjectLocalGraph] | None = None,
        graph_manager: ObjectGraphManager | None = None,
    ) -> None:
        super().__init__(
            db_connector=db_connector,
            source=source,
            graph_class=graph_class,
            graph_manager=graph_manager,
        )
        self.file_extensions = ['.yaml', '.yml']

    def import_registry(self) -> BaseCheckRegistry:
        from checkov.yaml_doc.registry import registry

        return registry

    def _parse_file(
        self, f: str, file_content: str | None = None
    ) -> tuple[dict[str, Any] | list[dict[str, Any]], list[tuple[int, str]]] | None:
        return parse(f, file_content)

    def get_start_end_lines(
        self, end: int, result_config: dict[str, Any] | list[dict[str, Any]], start: int
    ) -> tuple[int, int]:
        if result_config and isinstance(result_config, list):
            if not isinstance(result_config[0], dict):
                return -1, -1
            start = result_config[0]["__startline__"] - 1
            end = result_config[len(result_config) - 1]["__endline__"]
        elif result_config and isinstance(result_config, dict):
            start = result_config["__startline__"]
            end = result_config["__endline__"]
        return end, start
