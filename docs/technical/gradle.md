# Gradle - Build Automation for JVM and Beyond

## Overview

Gradle is a powerful build automation tool that combines the flexibility of Ant with the dependency management of Maven. It uses a Groovy or Kotlin-based DSL for build configuration and supports multiple languages including Java, Kotlin, Groovy, Scala, Android, C++, and Swift.

## Key Features

- **Declarative Build Scripts**: Groovy or Kotlin DSL
- **Incremental Builds**: Smart task execution
- **Build Cache**: Local and remote caching
- **Parallel Execution**: Multi-project and task parallelization
- **Composite Builds**: Combine multiple independent builds
- **Build Scans**: Deep insights into build performance
- **Rich Plugin Ecosystem**: Extensive plugin marketplace

## Build Configuration

### Project Setup

```kotlin
// settings.gradle.kts
rootProject.name = "my-application"

include("core", "web", "api", "shared")

// Enable feature previews
enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

// Configure build cache
buildCache {
    local {
        isEnabled = true
        directory = File(rootDir, ".gradle/build-cache")
        removeUnusedEntriesAfterDays = 30
    }
    remote<HttpBuildCache> {
        url = uri("https://cache.company.com/cache/")
        credentials {
            username = System.getenv("GRADLE_CACHE_USER")
            password = System.getenv("GRADLE_CACHE_PASSWORD")
        }
        isPush = System.getenv("CI") != null
    }
}
```

### Build Scripts

```kotlin
// build.gradle.kts (Kotlin DSL)
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.8.22"
    kotlin("plugin.spring") version "1.8.22"
    id("org.springframework.boot") version "3.1.2"
    id("io.spring.dependency-management") version "1.1.2"
    id("com.github.ben-manes.versions") version "0.47.0"
    jacoco
}

group = "com.example"
version = "1.0.0-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

repositories {
    mavenCentral()
    google()
    maven {
        url = uri("https://packages.company.com/maven")
        credentials {
            username = project.findProperty("repoUser") as String? ?: System.getenv("REPO_USER")
            password = project.findProperty("repoPassword") as String? ?: System.getenv("REPO_PASSWORD")
        }
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    
    runtimeOnly("org.postgresql:postgresql")
    
    testImplementation("org.springframework.boot:spring-boot-starter-test") {
        exclude(group = "org.junit.vintage", module = "junit-vintage-engine")
    }
    testImplementation("io.mockk:mockk:1.13.5")
    testImplementation("com.ninja-squad:springmockk:4.0.2")
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xjsr305=strict")
        jvmTarget = "17"
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
    maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)
    
    testLogging {
        events("passed", "skipped", "failed")
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
        showStandardStreams = false
    }
}

// Custom tasks
tasks.register<Copy>("copyDocs") {
    from("src/docs")
    into("build/docs")
    include("**/*.md", "**/*.adoc")
}

tasks.register("integrationTest", Test::class) {
    description = "Runs integration tests."
    group = "verification"
    
    testClassesDirs = sourceSets["integrationTest"].output.classesDirs
    classpath = sourceSets["integrationTest"].runtimeClasspath
    shouldRunAfter("test")
}
```

### Multi-Module Configuration

```kotlin
// build.gradle.kts (root)
allprojects {
    repositories {
        mavenCentral()
    }
}

subprojects {
    apply(plugin = "java")
    apply(plugin = "jacoco")
    
    group = "com.example"
    version = "1.0.0"
    
    java {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    dependencies {
        testImplementation("org.junit.jupiter:junit-jupiter:5.9.3")
        testImplementation("org.assertj:assertj-core:3.24.2")
    }
    
    tasks.test {
        useJUnitPlatform()
    }
}

// Configure specific modules
project(":core") {
    dependencies {
        implementation("org.apache.commons:commons-lang3:3.12.0")
        api("com.google.guava:guava:32.1.1-jre")
    }
}

project(":web") {
    apply(plugin = "org.springframework.boot")
    
    dependencies {
        implementation(project(":core"))
        implementation(project(":shared"))
        implementation("org.springframework.boot:spring-boot-starter-web")
    }
}

// Aggregate tasks
tasks.register("buildAll") {
    dependsOn(subprojects.map { it.tasks.build })
}

tasks.register<JacocoReport>("codeCoverageReport") {
    executionData(fileTree(project.rootDir.absolutePath).include("**/build/jacoco/*.exec"))
    
    subprojects.forEach {
        sourceSets(it.sourceSets.main.get())
    }
    
    reports {
        xml.required.set(true)
        xml.outputLocation.set(file("${buildDir}/reports/jacoco/report.xml"))
        html.required.set(true)
    }
}
```

## Dependency Management

### Version Catalogs

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "1.8.22"
spring-boot = "3.1.2"
jackson = "2.15.2"
junit = "5.9.3"
testcontainers = "1.18.3"

[libraries]
kotlin-stdlib = { module = "org.jetbrains.kotlin:kotlin-stdlib", version.ref = "kotlin" }
kotlin-reflect = { module = "org.jetbrains.kotlin:kotlin-reflect", version.ref = "kotlin" }

spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
spring-boot-starter-data = { module = "org.springframework.boot:spring-boot-starter-data-jpa", version.ref = "spring-boot" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test", version.ref = "spring-boot" }

jackson-databind = { module = "com.fasterxml.jackson.core:jackson-databind", version.ref = "jackson" }
jackson-kotlin = { module = "com.fasterxml.jackson.module:jackson-module-kotlin", version.ref = "jackson" }

junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }
junit-jupiter-engine = { module = "org.junit.jupiter:junit-jupiter-engine", version.ref = "junit" }

testcontainers = { module = "org.testcontainers:testcontainers", version.ref = "testcontainers" }
testcontainers-postgresql = { module = "org.testcontainers:postgresql", version.ref = "testcontainers" }

[bundles]
spring-web = ["spring-boot-starter-web", "jackson-kotlin"]
testing = ["junit-jupiter", "spring-boot-starter-test", "testcontainers"]

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
kotlin-spring = { id = "org.jetbrains.kotlin.plugin.spring", version.ref = "kotlin" }
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
versions = { id = "com.github.ben-manes.versions", version = "0.47.0" }
```

### Dependency Configuration

```kotlin
// build.gradle.kts
dependencies {
    // Using version catalog
    implementation(libs.spring.boot.starter.web)
    implementation(libs.jackson.kotlin)
    testImplementation(libs.bundles.testing)
    
    // Platform/BOM
    implementation(platform("org.springframework.cloud:spring-cloud-dependencies:2022.0.3"))
    implementation("org.springframework.cloud:spring-cloud-starter-config")
    
    // Constraints
    constraints {
        implementation("org.apache.logging.log4j:log4j-core:2.20.0") {
            because("CVE-2021-44228 - Log4Shell vulnerability fix")
        }
    }
    
    // Dynamic versions (avoid in production)
    implementation("com.example:library:1.+")
    
    // Dependency substitution
    configurations.all {
        resolutionStrategy {
            force("com.google.guava:guava:32.1.1-jre")
            
            eachDependency {
                if (requested.group == "org.apache.logging.log4j") {
                    useVersion("2.20.0")
                    because("Security vulnerability")
                }
            }
        }
    }
}

// Custom configuration
configurations {
    create("integrationTestImplementation") {
        extendsFrom(configurations.testImplementation.get())
    }
}
```

### Dependency Locking

```kotlin
// build.gradle.kts
dependencyLocking {
    lockAllConfigurations()
    lockMode.set(LockMode.STRICT)
}

tasks.register("updateDependencyLocks") {
    doLast {
        configurations.filter {
            it.isCanBeResolved
        }.forEach { it.resolve() }
    }
}

// Generate lock files
// ./gradlew dependencies --write-locks
```

## Performance Optimization

### Build Performance

```kotlin
// gradle.properties
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.configureondemand=true
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError
org.gradle.daemon.idletimeout=10800000
org.gradle.workers.max=8

# Kotlin specific
kotlin.incremental=true
kotlin.parallel.tasks.in.project=true
kapt.incremental.apt=true
kapt.use.worker.api=true

# Build cache
org.gradle.caching.debug=false
```

### Task Configuration Avoidance

```kotlin
// build.gradle.kts
tasks.register<JavaCompile>("compileSpecial") {
    source = fileTree("src/special")
    classpath = configurations["compile"]
    destinationDirectory.set(file("$buildDir/classes/special"))
}

// Lazy configuration
tasks.named<Test>("test") {
    maxHeapSize = "1G"
    
    systemProperty("junit.jupiter.testinstance.lifecycle.default", "per_class")
    
    doFirst {
        println("Running tests with heap: $maxHeapSize")
    }
}

// Provider API
val buildNumber = providers.environmentVariable("BUILD_NUMBER")
    .orElse("LOCAL")

tasks.jar {
    manifest {
        attributes(
            "Implementation-Version" to project.version,
            "Build-Number" to buildNumber.get()
        )
    }
}
```

### Incremental Tasks

```kotlin
// Custom incremental task
abstract class ProcessDataTask : DefaultTask() {
    @get:InputDirectory
    @get:SkipWhenEmpty
    abstract val inputDir: DirectoryProperty
    
    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty
    
    @TaskAction
    fun process() {
        inputDir.asFileTree.visit {
            if (file.isFile) {
                val outputFile = outputDir.file(relativePath).get().asFile
                outputFile.parentFile.mkdirs()
                processFile(file, outputFile)
            }
        }
    }
    
    private fun processFile(input: File, output: File) {
        // Process file
        input.copyTo(output, overwrite = true)
    }
}

tasks.register<ProcessDataTask>("processData") {
    inputDir.set(file("src/data"))
    outputDir.set(file("$buildDir/processed-data"))
}
```

## Production Patterns

### CI/CD Integration

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - publish

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false -Dorg.gradle.caching=true"
  GRADLE_USER_HOME: "$CI_PROJECT_DIR/.gradle"

cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - .gradle/caches/
    - .gradle/wrapper/
    - build/

build:
  stage: build
  script:
    - ./gradlew assemble --build-cache --scan
  artifacts:
    paths:
      - build/libs/
    expire_in: 1 week

test:
  stage: test
  script:
    - ./gradlew check --build-cache
  artifacts:
    reports:
      junit: build/test-results/test/*.xml
    paths:
      - build/reports/
    expire_in: 1 week

publish:
  stage: publish
  script:
    - ./gradlew publish --build-cache
  only:
    - main
    - /^release-.*$/
```

### Docker Integration

```kotlin
// build.gradle.kts
plugins {
    id("com.google.cloud.tools.jib") version "3.3.2"
}

jib {
    from {
        image = "eclipse-temurin:17-jre"
        platforms {
            platform {
                architecture = "amd64"
                os = "linux"
            }
            platform {
                architecture = "arm64"
                os = "linux"
            }
        }
    }
    to {
        image = "gcr.io/my-project/my-app"
        tags = setOf("latest", version.toString())
        auth {
            username = System.getenv("REGISTRY_USER")
            password = System.getenv("REGISTRY_PASSWORD")
        }
    }
    container {
        jvmFlags = listOf("-Xms256m", "-Xmx2g")
        mainClass = "com.example.Application"
        ports = listOf("8080")
        environment = mapOf(
            "SPRING_PROFILES_ACTIVE" to "production"
        )
        creationTime = "USE_CURRENT_TIMESTAMP"
    }
}

// Alternative: Dockerfile task
tasks.register<Copy>("prepareDocker") {
    dependsOn("bootJar")
    from("build/libs/${project.name}-${project.version}.jar")
    from("src/main/docker/")
    into("build/docker/")
    rename { fileName ->
        fileName.replace("-${project.version}", "")
    }
}

tasks.register<Exec>("buildDockerImage") {
    dependsOn("prepareDocker")
    workingDir("build/docker")
    commandLine("docker", "build", "-t", "${project.name}:${project.version}", ".")
}
```

### Release Management

```kotlin
// build.gradle.kts
plugins {
    id("com.github.ben-manes.versions") version "0.47.0"
    id("net.researchgate.release") version "3.0.2"
    `maven-publish`
    signing
}

// Version management
release {
    tagTemplate = "v\$version"
    buildTasks = listOf("build")
    
    git {
        requireBranch = "main"
        pushToRemote = "origin"
    }
}

// Publishing configuration
publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            
            pom {
                name.set(project.name)
                description.set("My Application")
                url.set("https://github.com/company/my-app")
                
                licenses {
                    license {
                        name.set("Apache-2.0")
                        url.set("https://opensource.org/licenses/Apache-2.0")
                    }
                }
                
                developers {
                    developer {
                        id.set("team")
                        name.set("Platform Team")
                        email.set("platform@company.com")
                    }
                }
            }
        }
    }
    
    repositories {
        maven {
            name = "company"
            url = uri("https://maven.company.com/releases")
            credentials {
                username = project.findProperty("mavenUser") as String?
                password = project.findProperty("mavenPassword") as String?
            }
        }
    }
}

signing {
    sign(publishing.publications["maven"])
}

// Semantic versioning
tasks.register("bumpMajor") {
    doLast {
        val currentVersion = version.toString().split(".")
        val newVersion = "${currentVersion[0].toInt() + 1}.0.0"
        updateVersion(newVersion)
    }
}

fun updateVersion(newVersion: String) {
    val propsFile = file("gradle.properties")
    val props = propsFile.readText()
    propsFile.writeText(
        props.replace(Regex("version=.*"), "version=$newVersion")
    )
}
```

### Quality Assurance

```kotlin
// build.gradle.kts
plugins {
    id("org.sonarqube") version "4.2.1.3168"
    id("com.github.spotbugs") version "5.0.14"
    id("io.gitlab.arturbosch.detekt") version "1.23.0"
    jacoco
}

sonar {
    properties {
        property("sonar.projectKey", "my-app")
        property("sonar.host.url", "https://sonar.company.com")
        property("sonar.login", System.getenv("SONAR_TOKEN"))
        property("sonar.coverage.jacoco.xmlReportPaths", "${buildDir}/reports/jacoco/test/jacocoTestReport.xml")
    }
}

spotbugs {
    effort.set(com.github.spotbugs.snom.Effort.MAX)
    reportLevel.set(com.github.spotbugs.snom.Confidence.LOW)
    excludeFilter.set(file("config/spotbugs/exclude.xml"))
}

detekt {
    buildUponDefaultConfig = true
    config = files("$projectDir/config/detekt.yml")
    baseline = file("$projectDir/config/detekt-baseline.xml")
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
        html.required.set(true)
    }
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = "0.80".toBigDecimal()
            }
        }
    }
}

tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}
```

## Best Practices

1. **Build Structure**
   - Use Kotlin DSL for type safety
   - Leverage version catalogs for dependency management
   - Keep build scripts focused and modular
   - Use buildSrc for shared build logic

2. **Performance**
   - Enable build cache (local and remote)
   - Use parallel execution
   - Configure appropriate heap size
   - Profile builds with --scan

3. **Dependencies**
   - Lock dependency versions for reproducible builds
   - Use platform/BOM for version alignment
   - Regularly update dependencies
   - Minimize dependency scope

4. **Testing**
   - Separate unit and integration tests
   - Use parallel test execution
   - Configure test logging appropriately
   - Generate coverage reports

5. **CI/CD**
   - Cache Gradle home directory
   - Use Gradle wrapper
   - Enable build scans for debugging
   - Publish artifacts incrementally

## Troubleshooting

```bash
# Debug dependency issues
./gradlew dependencies --configuration runtimeClasspath
./gradlew dependencyInsight --dependency commons-logging

# Build with detailed output
./gradlew build --info --stacktrace

# Profile build performance
./gradlew build --profile
./gradlew build --scan

# Clean build
./gradlew clean build --no-build-cache

# Refresh dependencies
./gradlew build --refresh-dependencies

# Debug task execution
./gradlew tasks --all
./gradlew help --task bootJar
```