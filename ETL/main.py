import sqlite3

from extract import (
    obter_lista_deputados,
    obter_detalhes_deputado
)

from transform import transformar_deputado

from validators import validar_deputado

from load import (
    criar_tabela,
    inserir_deputado
)

from logger_config import etl_logger


def main():
    etl_logger.info("ETL STARTED")

    conn = sqlite3.connect("deputados.db")

    criar_tabela(conn)

    deputados = obter_lista_deputados()

    etl_logger.info(
        f"Deputados encontrados: {len(deputados)}"
    )

    success = 0
    failed = 0
    failed_deputado_validation = 0

    for deputado in deputados:
        deputado_id = deputado["id"]

        detalhes = obter_detalhes_deputado(
            deputado_id
        )

        if not validar_deputado(detalhes):
            failed_deputado_validation += 1
            continue

        tratado = transformar_deputado(
            detalhes
        )

        inserted = inserir_deputado(
            conn,
            tratado
        )

        if inserted:
            success += 1
        else:
            failed += 1 

    conn.close()

    etl_logger.info(
        f"ETL FINISHED | success={success} | failed={failed} | failed_deputado_validation={failed_deputado_validation}"
    )

    print("ETL concluído")


if __name__ == "__main__":
    main()