# Software Design Patterns

## 1. Creational Patterns
### 1.1 Factory Method
- Defines an interface or helper function for creating objects and delegating instantiation details to factory functions or composition roots
- **Use**: `container.py` (`create_container()`) and UI control helper factories in `app/adapters/ui/components/common/controls.py`
- **Advantage**: Centralizes dependency wiring and UI component creation, decoupling client code from concrete instantiation logic

### 1.2 Prototype
- Creates new objects by cloning and copying existing ones rather than instantiating them from scratch
- **Use**: `app/application/inventory/modification_service.py` and `app/application/inventory/reconciliation_service.py` utilizing `dataclasses.replace()`
- **Advantage**: Preserves domain model immutability and avoids boilerplate initialization when updating entity attributes

## 2. Structural Patterns
### 2.1 Adapter
- Allows objects with incompatible interfaces to collaborate by wrapping an existing class with a standardized interface
- **Use**: JSON repository adapters (`JsonInventoryRepository`, etc.), `MarkdownShoppingListExporter`, and `MemoryLogHandler`
- **Advantage**: Cleanly decouples domain interfaces from external file storage formats, loggers and document exporters

### 2.2 Composite
- Composes objects into tree structures to represent part-whole hierarchies, letting clients treat individual controls and containers uniformly
- **Use**: Flet UI component hierarchy across `BaseView`, `EntityView`, cards, forms, and layout containers
- **Advantage**: Enables modular and hierarchical UI construction where parent containers and leaf widgets share uniform update and render lifecycles

### 2.3 Facade
- Provides a unified, higher-level interface to a complex subsystem of domain logic and repositories
- **Use**: Application services (`InventorySearchService`, `ShoppingListService`, `InventoryReconciliationService`, `MenuModificationService`)
- **Advantage**: Simplifies complex subsystem interactions into clean, cohesive use-case APIs consumed directly by the UI adapter layer

## 3. Behavioral Patterns
### 3.1 Command
- Encapsulates actions, callbacks, and user interactions as first-class functions or handlers
- **Use**: Flet UI event handlers (`on_click`, `on_save`, `on_close`, callback lambdas) across buttons, forms, and cards
- **Advantage**: Decouples UI trigger elements from business logic execution and enables flexible event routing

### 3.2 Observer
- Defines a one-to-many subscription dependency so that when an object changes state, registered dependents are notified automatically
- **Use**: `LogBuffer` subscription mechanism notified by `LogsView` (`_update_from_buffer`)
- **Advantage**: Establishes decoupled, reactive updates between background logging activities and live UI view re-renders

### 3.3 Strategy
- Defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime or through composition
- **Use**: `ShoppingListExporter` interface with `MarkdownShoppingListExporter`, filter handlers, and unit conversion strategies
- **Advantage**: Allows export formats, search filtering rules, and unit standardizing calculations to vary independently of clients

### 3.4 Template Method
- Defines the skeletal workflow of an algorithm in a base class, deferring specific steps to subclasses
- **Use**: `JsonBaseRepository`, `BaseCard`, `BaseForm`, and `EntityView` abstract base classes
- **Advantage**: Promotes code reuse and enforces consistent UI/persistence structures while allowing specialized subclass customization
