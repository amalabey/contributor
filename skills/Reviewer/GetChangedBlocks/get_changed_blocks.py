from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class GetChangedBlocks:
    @sk_function(
        description="Returns a list of changed blocks based on a list of start and end line numbers",
        name="get_changed_blocks",
    )
    @sk_function_context_parameter(
        name="from_source",
        description="From source code for the comparison",
    )
    @sk_function_context_parameter(
        name="to_source",
        description="To source code for the comparison",
    )
    def get_changed_methods(self, context: SKContext) -> str:
        from_source = context.get_parameter_value("from_source")
        to_source = context.get_parameter_value("to_source")
        return None
