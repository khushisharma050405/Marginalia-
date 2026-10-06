CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,email TEXT UNIQUE NOT NULL,name TEXT NOT NULL,pw TEXT NOT NULL,board TEXT,class_level TEXT,stream TEXT,created TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS reset_tokens(token TEXT PRIMARY KEY,user_id INT REFERENCES users(id),expires TIMESTAMPTZ);
CREATE TABLE IF NOT EXISTS subjects(id SERIAL PRIMARY KEY,board TEXT,class_level TEXT,stream TEXT,name TEXT);
CREATE TABLE IF NOT EXISTS chapters(id SERIAL PRIMARY KEY,subject_id INT REFERENCES subjects(id),name TEXT,ord INT);
CREATE TABLE IF NOT EXISTS topics(id SERIAL PRIMARY KEY,chapter_id INT REFERENCES chapters(id),name TEXT);
CREATE TABLE IF NOT EXISTS questions(id SERIAL PRIMARY KEY,topic_id INT REFERENCES topics(id),prompt TEXT,options JSONB,answer INT,explanation TEXT,difficulty TEXT,is_sample BOOL DEFAULT true);
CREATE TABLE IF NOT EXISTS attempts(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),question_id INT REFERENCES questions(id),correct BOOL,seconds INT DEFAULT 0,created TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS solves(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),question TEXT,subject TEXT,topic TEXT,qtype TEXT,difficulty TEXT,confidence INT,steps JSONB,created TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS notes(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),kind TEXT,title TEXT,body TEXT,created TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS solver_cache(cache_key TEXT PRIMARY KEY,response_json JSONB NOT NULL,created_at TIMESTAMPTZ DEFAULT now());

DO $$
BEGIN
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE TABLE IF NOT EXISTS rag_chunks (
        id SERIAL PRIMARY KEY,
        board VARCHAR(32) NOT NULL,
        class_level VARCHAR(32) NOT NULL,
        subject VARCHAR(128) NOT NULL,
        chapter VARCHAR(256) NOT NULL,
        chunk_index INT NOT NULL DEFAULT 0,
        content TEXT NOT NULL,
        embedding vector(768),
        created_at TIMESTAMPTZ DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS rag_chunks_meta_idx ON rag_chunks(board, class_level, subject, chapter);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Vector extension not available, continuing: %', SQLERRM;
END $$;
