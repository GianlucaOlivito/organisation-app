# Architecture Guidelines
## Software Architecture
This application follows **Hexagonal Architecture** (also called Ports and Adapters) to maintain clear separation of concerns, testability, and framework independence.

## Layer Structure & Dependency Rules
Dependencies strictly flow **inward**. Outer layers depend on inner layers; inner layers must not have any knowledge of outer layers.

```
[Adapters/Infrastructure]  --->  [Application]  --->  [Domain]
```

### 1. Domain (`src/app/domain`)
* **Role:** Core business logic, domain entities, value objects and domain events
* **Rules:** 
  * Must not have any external dependencies (pure python standard libraries).
  * Must be Independent of external services (e.g. databases, frameworks or UI logic).

### 2. Application (`src/app/application`)
* **Role:** Application use cases, orchestrations and interfaces (Ports)
* **Rules:**
  * Imports from `domain` layer.
  * Defines abstract interfaces (python `Protocol` or `ABC`) for repositories and external services.

### 3. Adapters (`src/app/adapters`)
* **Role:** Implementations of application ports (e.g. external API clients or UI components)
* **Rules:**
  * Implements ports defined in `application` layer.
  * Translates external data structures into domain objects and vice-versa.

### 4. Infrastructure (`src/app/infrastructure`)
* **Role:** Low-level configuration, framework instantiation, dependency injection, and application entry points
* **Rules:**
  * Wires adapters to application ports.
