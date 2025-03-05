DROP DATABASE IF EXISTS db_chatbot;

CREATE SCHEMA db_chatbot;
USE db_chatbot;
CREATE TABLE t_conversation (
    id VARCHAR(64) PRIMARY KEY NOT NULL,
    conversation TEXT
);
