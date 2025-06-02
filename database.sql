CREATE TABLE IF NOT EXISTS urls (Add commentMore actions
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS url_checks (
@@ -11,5 +11,5 @@ CREATE TABLE IF NOT EXISTS url_checks (
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP NOT NULLAdd commentMore actions
);
