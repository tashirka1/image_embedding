-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create sample table
DROP TABLE IF EXISTS items;
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    face INTEGER,
    face_embedding vector(512),
    image_embedding halfvec(2048),
    UNIQUE(file_name, face)
);
CREATE INDEX IF NOT EXISTS idx_items_face_embedding ON items USING hnsw (face_embedding vector_l2_ops);
CREATE INDEX IF NOT EXISTS idx_items_image_embedding ON items USING hnsw (image_embedding halfvec_l2_ops);
