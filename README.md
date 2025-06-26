## Nivii

### Setup

Starting the app is as simple as building and running Docker Compose with the configuration described in `docker-compose.yml`.

An OpenAI key is required by default, although there is an implementation that uses a local instance of Ollama (`api/src/infrastructure/llm/ollama_llm.py`) that requires changing the LLM used in `api/src/app.py` from `OpenaiLLMModel` to `OllamaLLMModel`.

Example of running the app:
```bash
> OPENAI_KEY=sk-... docker compose up --build -d
```
The command above will start the DB, API, and frontend service as well as a script that populates the DB with the data from `data.csv`.

The frontend will be available at `127.0.0.1:8000` and the API at `127.0.0.1:3000`.

A test suite is available for the API that can be run as follows:
```bash 
> cd api
> pip install -r requirements.txt
> pytest src/test/test_analyze_service.py
```

### Design decisions

For this app, I decided to use PostgreSQL for the database, Python with Flask for the API, and React with Vite for the frontend.

To load data from the given `data.csv` file into the database, the tool found in `jobs/csv_to_database` is used. This tool is executed in a Docker container when starting the other services and tries to populate the DB with the given data if it doesn't exist already. Data is inserted into a single table called "sales_data".

As far as the API is concerned, it has a single functional endpoint `GET /analyze` that receives a string as a query parameter and, based on that, tries to process it to get a SQL query, executes that query, and returns the results as well as an analysis of it and a chart type to be plotted from the result.

For the architecture of the API, I tried to keep it clean and modular by having a clear separation of concerns between the different layers: API logic, database handling, LLM models, and business logic. Because of this, the main logic is agnostic of the database and LLM model used as long as the correct interface is implemented (so far only one database has been implemented and two LLM handlers, one for Ollama and one for OpenAI).

The frontend is a simple React app that renders an input field along with a submit button and keeps an in-memory conversation history with multiple questions and answers. For chart generation, it uses Recharts and supports line, bar, and pie charts as well as a table view.

### Scalability

The main concern when thinking about scalability is the storage layer, which must be appropriate to support multiple users. The LLM models, frontend, and API are stateless, so they can be scaled horizontally by adding more instances as needed, especially for the API.

For multiple users, the discussion often centers around whether to have multi-tenancy or not. With multi-tenancy, operations are simplified since only a single database instance needs to be hosted and maintained (at least a single logical database, possibly with multiple replicas for scaling). However, this approach does not provide much isolation between users. If each user requires a different data model with their own tables, there are additional challenges in managing multiple tables and different usage patterns.

The other option is to have one database tailored to each user. This provides the most data isolation and allows each user to have a custom schema, but it requires more resources since each database must be hosted and maintained. If most users do not have a significant amount of data or do not make queries frequently, many databases may sit idle, consuming resources unnecessarily. Also, having a full-fledged database instance for mostly read-only or simple queries can be inefficient, as many of the challenges these database systems solve are around transactions and complex querying.

Because of this, in some cases, something like SQLite could be useful. Each user would only require a single SQLite database file that can be easily stored and retrieved from an object store (like AWS S3) only when needed, without wasting additional resources (something akin to what Turso (https://turso.tech/) does). The challenge with this approach is handling large databases in a performant manner.

In summary, having a single database tailored to each user provides good data isolation and scalability for users with large datasets, and avoids resource competition that can arise from multiple users sharing the same database. However, it also presents challenges in terms of operations and resource management.
