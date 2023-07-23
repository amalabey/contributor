from common.base_pipeline import BasePipeline
from skills.Reviewer.plugin import ReviewerPlugin


class ReviewPipeline(BasePipeline):
    def __init__(
        self, use_azure_openai: bool = True, env_file_path: str = ".env"
    ) -> None:
        super().__init__(use_azure_openai=use_azure_openai, env_file_path=env_file_path)

    def execute(self, source: str, target: str):
        kernel = self.get_kernel()
        skill_semantic = kernel.import_semantic_skill_from_directory(
            "skills", "Reviewer"
        )
        skill_native = kernel.import_skill(ReviewerPlugin(), "ReviewerPlugin")

        getmethods_func = skill_semantic["GetMethods"]
        getchangedblocks_func = skill_native["get_changed_blocks"]
        getchangedmethods_func = skill_native["get_changed_methods"]

        context = kernel.create_new_context()
        