from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "deputados.db"
OUTPUT_DIR = BASE_DIR / "reports" / "insights"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_deputados() -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco não encontrado: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'",
            connection,
        )["name"].tolist()

        print("Tabelas encontradas:", tables)

        for table in tables:
            dataframe = pd.read_sql_query(f"SELECT * FROM {table}", connection)

            if looks_like_deputados(dataframe):
                print(f"Tabela usada: {table}")
                print(f"Registros: {len(dataframe)}")
                print(f"Colunas: {list(dataframe.columns)}")
                return normalize_columns(dataframe)

    raise ValueError("Nenhuma tabela compatível com dados de deputados foi encontrada.")


def looks_like_deputados(dataframe: pd.DataFrame) -> bool:
    columns = {column.lower() for column in dataframe.columns}

    expected = {
        "nome",
        "nomecivil",
        "nome_civil",
        "siglapartido",
        "sigla_partido",
        "partido",
        "siglauf",
        "sigla_uf",
        "uf",
        "sexo",
        "email",
    }

    return len(columns.intersection(expected)) >= 3


def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe.columns = [
        column.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for column in dataframe.columns
    ]

    return dataframe


def find_column(dataframe: pd.DataFrame, names: list[str]) -> str | None:
    normalized_names = [name.lower() for name in names]

    for column in dataframe.columns:
        if column in normalized_names:
            return column

    for column in dataframe.columns:
        if any(name in column for name in normalized_names):
            return column

    return None


def save_bar_chart(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
    limit: int = 15,
) -> None:
    data = dataframe[column].dropna().astype(str).value_counts().head(limit)

    if data.empty:
        return

    plt.figure(figsize=(11, 6))
    data.sort_values().plot(kind="barh")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200)
    plt.close()


def save_pie_chart(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    filename: str,
) -> None:
    data = dataframe[column].dropna().astype(str).value_counts()

    if data.empty:
        return

    plt.figure(figsize=(8, 8))
    data.plot(kind="pie", autopct="%1.1f%%")
    plt.title(title)
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200)
    plt.close()


def save_completeness_chart(dataframe: pd.DataFrame) -> None:
    completeness = dataframe.notna().mean().sort_values(ascending=False).head(15) * 100

    plt.figure(figsize=(11, 6))
    completeness.sort_values().plot(kind="barh")
    plt.title("Percentual de preenchimento dos principais campos")
    plt.xlabel("Preenchimento (%)")
    plt.ylabel("Campo")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "completude_campos.png", dpi=200)
    plt.close()


def build_summary(dataframe: pd.DataFrame) -> None:
    partido_col = find_column(dataframe, ["sigla_partido", "siglapartido", "partido"])
    uf_col = find_column(dataframe, ["sigla_uf", "siglauf", "uf"])
    sexo_col = find_column(dataframe, ["sexo"])
    email_col = find_column(dataframe, ["email"])
    escolaridade_col = find_column(dataframe, ["escolaridade"])

    lines = [
        "# Resumo de Insights — CIVITAS",
        "",
        "## Métricas gerais",
        "",
        f"- Total de deputados analisados: {len(dataframe)}",
        f"- Total de campos analisados: {len(dataframe.columns)}",
        "",
        "## Insights gerados",
        "",
    ]

    if partido_col:
        count = dataframe[partido_col].dropna().astype(str).value_counts()
        lines.append(
            f"- O partido com maior quantidade de deputados na base é {count.idxmax()}, com {count.max()} registros."
        )

    if uf_col:
        count = dataframe[uf_col].dropna().astype(str).value_counts()
        lines.append(
            f"- A UF com maior quantidade de deputados na base é {count.idxmax()}, com {count.max()} registros."
        )

    if sexo_col:
        percent = dataframe[sexo_col].dropna().astype(str).value_counts(normalize=True) * 100
        lines.append(
            f"- O grupo mais frequente em sexo é {percent.idxmax()}, representando {percent.max():.1f}% da base."
        )

    if email_col:
        filled = dataframe[email_col].notna().mean() * 100
        lines.append(
            f"- {filled:.1f}% dos deputados possuem e-mail preenchido."
        )

    if escolaridade_col:
        filled = dataframe[escolaridade_col].notna().mean() * 100
        lines.append(
            f"- {filled:.1f}% dos deputados possuem escolaridade preenchida."
        )

    lines.extend([
        "",
        "## Interpretação",
        "",
        "Os dados coletados pelo ETL mostram que o CIVITAS pode transformar dados públicos legislativos em indicadores visuais de representação partidária, distribuição regional, diversidade e completude cadastral. Esses indicadores ajudam o cidadão a interpretar a composição parlamentar de forma mais simples.",
    ])

    (OUTPUT_DIR / "resumo_insights.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    dataframe = load_deputados()

    partido_col = find_column(dataframe, ["sigla_partido", "siglapartido", "partido"])
    uf_col = find_column(dataframe, ["sigla_uf", "siglauf", "uf"])
    sexo_col = find_column(dataframe, ["sexo"])
    escolaridade_col = find_column(dataframe, ["escolaridade"])

    if partido_col:
        save_bar_chart(
            dataframe,
            partido_col,
            "Deputados por partido",
            "Quantidade de deputados",
            "Partido",
            "deputados_por_partido.png",
        )

    if uf_col:
        save_bar_chart(
            dataframe,
            uf_col,
            "Deputados por UF",
            "Quantidade de deputados",
            "UF",
            "deputados_por_uf.png",
            limit=27,
        )

    if sexo_col:
        save_pie_chart(
            dataframe,
            sexo_col,
            "Distribuição por sexo",
            "distribuicao_por_sexo.png",
        )

    if escolaridade_col:
        save_bar_chart(
            dataframe,
            escolaridade_col,
            "Deputados por escolaridade",
            "Quantidade de deputados",
            "Escolaridade",
            "deputados_por_escolaridade.png",
        )

    save_completeness_chart(dataframe)
    build_summary(dataframe)

    print(f"Arquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()