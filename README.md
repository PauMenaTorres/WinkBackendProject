# WinkBackendProject

REST API backend for Wink Blog & CMS

### Features
* **Blog (Public)**: Public access to published articles and hashtag filtering.
* **CMS (Content Management System)**: Editorial management (create, publish, delete, filter).

### Architecture
The project is divided into different layers: models, repositories, services, routers, dependencies, and database, and it is all connected using FastAPI, MongoDB, and Pydantic.

Each layer has a dedicated responsibility:
* **Models**: Define data schemas, strict runtime validation, and serialization contracts using Pydantic (`PostCreate`, `PostResponse`, `PostStatus`). They ensure that invalid payloads are rejected at the edge before reaching any business logic.
* **Repositories**: Abstract the data persistence layer using an abstract base class (`PostRepository`) that defines the contract for all data operations (`get_all`, `get_by_id`, `create`, `update_status`, `delete`). The concrete implementation (`MongoPostRepository`) encapsulates all MongoDB-specific driver calls, query building, and maps internal BSON `_id` identifiers into domain-compatible string IDs. This decouples the storage engine entirely, allowing the database implementation to be swapped or mocked in unit tests without touching the rest of the application.
* **Services**: Encapsulate the core application rules and use cases (`PostService`) independent of HTTP delivery or database engines. Instead of depending on concrete storage implementations, the service relies on the repository interface contract provided via dependency injection. It orchestrates domain invariants such as enforcing "Brian Fox" as the default author, setting "draft" as the initial lifecycle status, and ensuring public blog readers only access "published" content.
* **Routers**: Thin presentation endpoints split into dedicated modules (`blog.py` for public reads and `cms.py` for authenticated administrative writes). They strictly handle HTTP transport, status codes, query/path parameter parsing, and route-level Bearer token verification, immediately delegating execution to the injected service layer.
* **Dependencies**: Acts as the composition root for the application. It manages dependency injection by wiring the database collection into the repository and the repository into the service, while also handling administrative authentication by validating incoming HTTP Bearer tokens.
* **Core**: Centralizes custom domain exceptions (`PostNotFoundException`, `InvalidIdException`) which decouple error handling from HTTP-specific constructs.
* **Database**: Centralizes client initialization and connection pooling to the remote MongoDB cluster, ensuring that connection management remains isolated from data access routines.

### Testing 
Unit tests verify domain rules, blog visibility, and CMS authentication in complete isolation using an in-memory repository (FakePostRepository).

Run the test suite using pytest: `python -m pytest -v`

### Authentication
CMS endpoints require HTTP Bearer authentication.
* **Static Admin Token**: `{ADMIN_TOKEN}`
* Click the **Authorize** button in Swagger UI (`/docs`) or send `Authorization: Bearer <token>` in your request header.

### Getting Started

1. Clone the project
2. Create and activate the .venv using commands: `python -m venv .venv` and `.\.venv\Scripts\activate`
3. Install dependencies using command: `pip install -r requirements.txt`
4. Create the .env file based on .env.template
5. Run the server using command: `uvicorn app.main:app --reload`
6. Access API with SwaggerUI docs at `http://localhost:8000/docs` or with Redoc at `http://localhost:8000/redoc`

