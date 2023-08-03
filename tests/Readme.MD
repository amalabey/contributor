# Test Taxonomy

* L0 and L1 tests are unit tests, or tests that depend on code in the assembly under test and nothing else. L0 is a broad class of fast, in-memory unit tests.
* L2 are functional tests that might require other dependencies, like SQL or the file system.
* L3 functional tests run against testable service deployments. This test category requires a service deployment, but might use stubs for key service dependencies.
* L4 tests are a restricted class of integration tests that run against production. L4 tests require a full product deployment.

> [reference](https://learn.microsoft.com/en-us/devops/develop/shift-left-make-testing-fast-reliable#devops-test-taxonomy)