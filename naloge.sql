-- SQL ukazi za SQLite bazo

CREATE TABLE IF NOT EXISTS 'task' (
  'id' INTEGER NOT NULL PRIMARY KEY,  -- Primarni ključ
  'title' VARCHAR NOT NULL,  -- Naslov naloge
  'complete' BOOLEAN NOT NULL DEFAULT 0 
);
