from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class GetChangedMethods:
    @sk_function(
        description="Returns changed method blocks based on a list of start and end line numbers",
        name="get_changed_methods",
    )
    @sk_function_context_parameter(
        name="methods",
        description="List of methods names and corresponding start and end line numbers",
    )
    @sk_function_context_parameter(
        name="changed_blocks",
        description="List of start and end line numbers of changed blocks",
    )
    def get_changed_methods(self, context: SKContext) -> str:
        methods = context.get_parameter_value("methods")
        blocks = context.get_parameter_value("blocks")
        return None
