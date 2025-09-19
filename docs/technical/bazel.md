# Bazel - Google's Build and Test Tool

## Overview

Bazel is an open-source build and test tool developed by Google that supports multi-language, multi-platform builds at scale. It provides fast, reliable, and incremental builds with advanced caching and parallelization capabilities.

## Key Features

- **Language Support**: Java, C++, Android, iOS, Go, Python, JavaScript, and more
- **Platform Support**: Linux, macOS, Windows
- **Hermetic Builds**: Reproducible builds with isolated environments
- **Remote Caching**: Share build artifacts across teams
- **Remote Execution**: Distribute builds across multiple machines
- **Incremental Builds**: Only rebuild what changed
- **Build Graph Analysis**: Dependency visualization and optimization

## Build Configuration

### Workspace Setup

```python
# WORKSPACE or WORKSPACE.bazel
workspace(name = "my_project")

# Load external dependencies
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Java rules
http_archive(
    name = "rules_java",
    urls = ["https://github.com/bazelbuild/rules_java/releases/download/5.5.0/rules_java-5.5.0.tar.gz"],
    sha256 = "...",
)

# Python rules
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.24.0/rules_python-0.24.0.tar.gz",
    sha256 = "...",
)
```

### BUILD Files

```python
# BUILD.bazel
load("@rules_java//java:defs.bzl", "java_binary", "java_library", "java_test")

# Java library
java_library(
    name = "utils",
    srcs = glob(["src/main/java/com/example/utils/*.java"]),
    visibility = ["//visibility:public"],
)

# Java application
java_binary(
    name = "app",
    srcs = ["src/main/java/com/example/App.java"],
    main_class = "com.example.App",
    deps = [
        ":utils",
        "@maven//:com_google_guava_guava",
    ],
)

# Test target
java_test(
    name = "app_test",
    srcs = ["src/test/java/com/example/AppTest.java"],
    test_class = "com.example.AppTest",
    deps = [
        ":app",
        "@maven//:junit_junit",
    ],
)
```

### Multi-Language Build

```python
# C++ targets
cc_library(
    name = "core",
    srcs = ["core.cc"],
    hdrs = ["core.h"],
    visibility = ["//visibility:public"],
)

cc_binary(
    name = "main",
    srcs = ["main.cc"],
    deps = [":core"],
)

# Python targets
py_library(
    name = "analytics",
    srcs = glob(["analytics/*.py"]),
    imports = ["."],
)

py_binary(
    name = "analyzer",
    srcs = ["analyzer.py"],
    deps = [":analytics"],
    python_version = "PY3",
)

# Protocol Buffers
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_java//java:defs.bzl", "java_proto_library")
load("@rules_python//python:defs.bzl", "py_proto_library")

proto_library(
    name = "api_proto",
    srcs = ["api.proto"],
)

java_proto_library(
    name = "api_java_proto",
    deps = [":api_proto"],
)

py_proto_library(
    name = "api_py_proto",
    deps = [":api_proto"],
)
```

## Dependency Management

### External Dependencies

```python
# WORKSPACE - Maven dependencies
load("@rules_jvm_external//:defs.bzl", "maven_install")

maven_install(
    artifacts = [
        "com.google.guava:guava:31.1-jre",
        "org.springframework.boot:spring-boot-starter:2.7.0",
        "com.fasterxml.jackson.core:jackson-databind:2.13.3",
        "junit:junit:4.13.2",
    ],
    repositories = [
        "https://repo1.maven.org/maven2",
        "https://maven.google.com",
    ],
    fetch_sources = True,
)

# Python dependencies with pip_parse
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "pip_deps",
    requirements_lock = "//:requirements_lock.txt",
)

load("@pip_deps//:requirements.bzl", "install_deps")
install_deps()

# Go dependencies
load("@io_bazel_rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies", "go_repository")

go_repository(
    name = "com_github_gin_gonic_gin",
    importpath = "github.com/gin-gonic/gin",
    tag = "v1.8.1",
)
```

### Version Pinning

```python
# maven_install.json for reproducible builds
maven_install(
    artifacts = [...],
    maven_install_json = "//:maven_install.json",
)

load("@maven//:defs.bzl", "pinned_maven_install")
pinned_maven_install()
```

### Custom Dependencies

```python
# Local repository
local_repository(
    name = "shared_lib",
    path = "../shared-library",
)

# Git repository
git_repository(
    name = "custom_rules",
    remote = "https://github.com/company/custom-bazel-rules.git",
    commit = "abc123def456",
)

# HTTP archive with patches
http_archive(
    name = "third_party_lib",
    urls = ["https://github.com/example/lib/archive/v1.0.0.tar.gz"],
    sha256 = "...",
    strip_prefix = "lib-1.0.0",
    patches = ["//patches:third_party_lib.patch"],
)
```

## Performance Optimization

### Build Configuration

```bash
# .bazelrc
# Common flags
build --jobs=auto
build --experimental_strict_action_env
build --incompatible_strict_action_env

# Remote caching
build --remote_cache=grpc://cache.company.com:9092
build --remote_upload_local_results=true
build --remote_timeout=3600

# Remote execution
build:remote --remote_executor=grpc://executor.company.com:8980
build:remote --remote_instance_name=projects/my-project/instances/default
build:remote --jobs=200
build:remote --remote_download_minimal

# Local performance
build --local_cpu_resources=HOST_CPUS*.75
build --local_ram_resources=HOST_RAM*.67
build --disk_cache=~/.cache/bazel

# Memory optimization
build --heap_dump_on_oom
build --experimental_oom_more_eagerly_threshold=90

# Test configuration
test --test_output=errors
test --test_summary=detailed
test --cache_test_results=yes
```

### Query and Analysis

```bash
# Analyze dependencies
bazel query "deps(//src/main:app)"

# Find reverse dependencies
bazel query "rdeps(//..., //lib:core)"

# Analyze build performance
bazel build //... --profile=profile.json
bazel analyze-profile profile.json

# Generate dependency graph
bazel query --output=graph "deps(//src/main:app)" | dot -Tpng > deps.png
```

### Caching Strategies

```python
# BUILD - Action caching
genrule(
    name = "generate_code",
    srcs = ["template.txt"],
    outs = ["generated.cc"],
    cmd = "$(location //tools:generator) $< > $@",
    tools = ["//tools:generator"],
    # Enable caching for deterministic outputs
    local = False,
    cacheable = True,
)

# Platform-specific caching
config_setting(
    name = "linux_x86_64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
)

cc_binary(
    name = "app",
    srcs = ["main.cc"],
    linkopts = select({
        ":linux_x86_64": ["-static"],
        "//conditions:default": [],
    }),
)
```

## Production Patterns

### Monorepo Structure

```
/
├── WORKSPACE
├── .bazelrc
├── .bazelversion
├── tools/
│   └── build_rules/
├── third_party/
│   └── BUILD.bazel
├── apps/
│   ├── web/
│   │   └── BUILD.bazel
│   └── mobile/
│       └── BUILD.bazel
├── services/
│   ├── auth/
│   │   └── BUILD.bazel
│   └── api/
│       └── BUILD.bazel
└── libs/
    ├── common/
    │   └── BUILD.bazel
    └── proto/
        └── BUILD.bazel
```

### CI/CD Integration

```yaml
# .github/workflows/bazel.yml
name: Bazel CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Mount bazel cache
        uses: actions/cache@v3
        with:
          path: "~/.cache/bazel"
          key: bazel-${{ runner.os }}-${{ hashFiles('WORKSPACE') }}
      
      - name: Build
        run: |
          bazel build //... \
            --config=ci \
            --build_metadata=COMMIT_SHA=${{ github.sha }}
      
      - name: Test
        run: bazel test //... --config=ci --test_output=errors
      
      - name: Coverage
        run: |
          bazel coverage //... --combined_report=lcov
          bash <(curl -s https://codecov.io/bash) -f bazel-out/_coverage/_coverage_report.dat
```

### Docker Integration

```python
# BUILD.bazel
load("@io_bazel_rules_docker//container:container.bzl", "container_image", "container_push")
load("@io_bazel_rules_docker//java:image.bzl", "java_image")

java_image(
    name = "app_image_base",
    main_class = "com.example.App",
    runtime_deps = [":app_deploy.jar"],
)

container_image(
    name = "app_image",
    base = ":app_image_base",
    env = {
        "JAVA_OPTS": "-Xmx2g -XX:+UseG1GC",
    },
    ports = ["8080"],
    labels = {
        "version": "{BUILD_VERSION}",
        "maintainer": "platform@company.com",
    },
)

container_push(
    name = "push_app",
    image = ":app_image",
    registry = "gcr.io",
    repository = "my-project/app",
    tag = "{BUILD_VERSION}",
)
```

### Testing Strategies

```python
# BUILD.bazel - Test suites
test_suite(
    name = "unit_tests",
    tests = [
        "//src/test/java/...",
        "//src/test/python/...",
    ],
    tags = ["unit"],
)

test_suite(
    name = "integration_tests",
    tests = ["//tests/integration/..."],
    tags = ["integration"],
)

# Parallel test execution
java_test(
    name = "large_test",
    size = "large",
    shard_count = 4,
    srcs = ["LargeTest.java"],
    flaky = True,  # Allow retries for flaky tests
)

# Test with custom environment
sh_test(
    name = "e2e_test",
    srcs = ["e2e_test.sh"],
    data = [
        ":app_binary",
        "//testdata:fixtures",
    ],
    env = {
        "TEST_ENV": "bazel",
        "PORT": "8080",
    },
    tags = ["exclusive"],  # Run exclusively
)
```

### Release Management

```python
# BUILD.bazel - Release packaging
load("@bazel_tools//tools/build_defs/pkg:pkg.bzl", "pkg_tar", "pkg_deb")

pkg_tar(
    name = "app_release",
    srcs = [":app_binary"],
    mode = "0755",
    package_dir = "/opt/app",
    deps = [
        ":config_files",
        ":static_assets",
    ],
)

pkg_deb(
    name = "app_debian",
    data = ":app_release",
    description = "My Application",
    maintainer = "platform@company.com",
    package = "my-app",
    version = "{VERSION}",
    depends = [
        "java-runtime (>= 11)",
    ],
)

# Version stamping
genrule(
    name = "version_info",
    outs = ["version_info.h"],
    cmd = """
        echo '#define BUILD_VERSION "$(VERSION)"' > $@
        echo '#define BUILD_TIME "$(date)"' >> $@
        echo '#define BUILD_USER "$(USER)"' >> $@
    """,
    stamp = True,
)
```

## Best Practices

1. **Workspace Organization**
   - Keep WORKSPACE file minimal
   - Use .bazelrc for common configurations
   - Pin all dependency versions
   - Use visibility rules to enforce API boundaries

2. **Build Performance**
   - Enable remote caching early
   - Use fine-grained targets
   - Minimize generated file dependencies
   - Profile builds regularly

3. **Dependency Management**
   - Use repository rules for external deps
   - Create wrapper rules for third-party libraries
   - Vendor critical dependencies
   - Regular dependency updates

4. **Testing**
   - Separate unit and integration tests
   - Use test_suite for organization
   - Enable parallel test execution
   - Set appropriate test sizes

5. **Continuous Integration**
   - Use remote execution for CI
   - Cache build artifacts
   - Run affected tests only
   - Monitor build metrics

## Troubleshooting

```bash
# Debug build failures
bazel build //target --verbose_failures --sandbox_debug

# Analyze build graph
bazel query --output=text "somepath(//src:app, //lib:dependency)"

# Clean builds
bazel clean --expunge  # Full clean
bazel clean  # Clean outputs only

# Inspect actions
bazel aquery "deps(//src:app)"

# Profile memory usage
bazel build //... --host_jvm_args=-Xmx4g --profile=profile.gz
```