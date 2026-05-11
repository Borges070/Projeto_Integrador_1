import sqlite3

from logger_config import (
    etl_logger,
    skipped_logger
)


def criar_tabela(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deputados (
        id INTEGER PRIMARY KEY,
        nome_civil TEXT,
        nome_parlamentar TEXT,
        partido TEXT,
        uf TEXT,
        email TEXT,
        telefone TEXT,
        sexo TEXT,
        data_nascimento TEXT,
        escolaridade TEXT,
        website TEXT,
        redes_sociais TEXT
    )
    """)

    conn.commit()


def inserir_deputado(conn, deputado):
    try:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO deputados (
            id,
            nome_civil,
            nome_parlamentar,
            partido,
            uf,
            email,
            telefone,
            sexo,
            data_nascimento,
            escolaridade,
            website,
            redes_sociais
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            deputado["id"],
            deputado["nome_civil"],
            deputado["nome_parlamentar"],
            deputado["partido"],
            deputado["uf"],
            deputado["email"],
            deputado["telefone"],
            deputado["sexo"],
            deputado["data_nascimento"],
            deputado["escolaridade"],
            deputado["website"],
            deputado["redes_sociais"]
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()

        skipped_logger.error(
            f"Failed insert ID={deputado.get('id')} | {str(e)}"
        )

        return False

    return True