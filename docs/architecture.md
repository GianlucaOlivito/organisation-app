# Architecture Guidelines
## Software Architecture
This application follows **Hexagonal Architecture** (also called Ports and Adapters) to maintain clear separation of concerns, testability and framework independence.

## Layer Structure & Dependency Rules
Dependencies strictly flow **inward**. Outer layers depend on inner layers; inner layers must not have any knowledge of outer layers.

```
[Infrastructure]  --->  [Adapters]  --->  [Application]  --->  [Domain]
```

### 1. Domain (`src/app/domain`)
* **Role:** Core business logic, domain entities, value objects and their validations
* **Rules:** 
  * Must not have any external dependencies (pure python standard libraries).
  * Must be independent of external services (e.g. databases, frameworks or UI logic).

### 2. Application (`src/app/application`)
* **Role:** Application use cases, orchestrations and interfaces (Ports)
* **Rules:**
  * Imports from `domain` layer.
  * Defines abstract interfaces (python `Protocol` or `ABC`) for repositories and external adapters.

### 3. Adapters (`src/app/adapters`)
* **Role:** Driving UI components (`src/app/adapters/ui`) and implementations of application ports
* **Rules:**
  * Implements abstract ports defined in `application` layer (e.g. JSON repositories, file exporters).
  * Defines driving UI adapters (e.g. Flet views) that consume application services to trigger use cases.
  * Translates external data structures and UI inputs into domain objects and vice-versa.

### 4. Infrastructure (`src/app/infrastructure`)
* **Role:** Low-level configuration, framework instantiation, dependency injection (composition root),
logging setup and application entry points
* **Rules:**
  * Wires concrete adapters to application ports.
  * Must not contain domain or application business logic.
