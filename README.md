# Contributor
Latest development in Large Language Models (LLMs) such as OpenAI GPT have open the doors to leverage their capability to review and find bugs in code changes. Contributor is a tool (bot) that can automatically provide feedback on code changes using the underlying LLM APIs (e.g. OpenAI). The tool can automatically decorate Pull Requests with comments and code suggestions relevant to the changed code blocks.

![Review Comment](docs/review-comment.png)

## How does it work?
Contributor uses the APIs provided by the source control provider (currently only Azure Repos is supported) to retrieve code changes. It then uses OpenAI LLM to obtain the set of methods/functions changed and should be reviewed. Once it knows the semantic change set, it uses OpenAI LLM again to obtain code review suggestions for each method/function. The tool then, decorates the Pull Request files using the corresponding APIs. Contributor uses [langchain](https://github.com/hwchase17/langchain) to work with LLMs.
