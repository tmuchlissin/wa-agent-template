import logging, re
from pathlib import Path
from langchain.tools import tool
from sqlalchemy import text
from app.services.llm import LLM
from sqlalchemy import create_engine

project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "app" / "data" / "laptop.db"
db_uri = f"sqlite:///{db_path}"
logging.getLogger(__name__).info(f"[SQL] Using database path: {db_path}")
engine = create_engine(db_uri, connect_args={"check_same_thread": False})

@tool("sql_query")
def sql_query(question: str) -> str:
    """
    Convert natural language → SQL (safe SELECT only) → execute → return formatted result.
    """
    try:
        schema = """
        Table: laptops
        Columns:
        - product_name (TEXT)
        - processor (TEXT)
        - display_resolution (TEXT)
        - price_each (INTEGER)
        - ram_gb (INTEGER)
        - rom_gb (INTEGER)
        - cpu_brand (TEXT)
        - cpu_tier (TEXT)
        - cpu_score (INTEGER)
        - is_4k (INTEGER)
        - brand (TEXT)
        - spec_score (FLOAT)
        """

        prompt = f"""
        Anda adalah SQL generator SQLite.

        {schema}

        Tugas:
        Convert the following question into a valid SQL query.
        Mengubah pertanyaan berikut menjadi query SQL yang valid.
        
        Pertanyaan:
        "{question}"

        ATURAN:
        - HANYA menghasilkan query SQL SELECT yang valid
        - DILARANG menggunakan INSERT, UPDATE, DELETE, DROP
        - HANYA boleh menggunakan tabel: laptops
        - HANYA gunakan kolom yang tersedia di schema
        - WAJIB menggunakan LIMIT 5
        - Untuk query rekomendasi, WAJIB menggunakan ORDER BY spec_score DESC
        - JANGAN menambahkan teks, komentar, atau penjelasan apa pun
        - Output HARUS berupa 1 query SQL saja
        - Query HARUS diakhiri dengan tanda ;

        Contoh:
        SELECT product_name, price_each
        FROM laptops
        WHERE ram_gb >= 16
        ORDER BY spec_score DESC
        LIMIT 5;
        """

        raw_sql = LLM.invoke(prompt).content.strip()

        # Clean formatting
        sql = re.sub(r"```sql|```", "", raw_sql).strip()
        sql = sql.replace("\n", " ")

        if not sql.endswith(";"):
            sql += ";"

        logging.info(f"[SQL GENERATED]: {sql}")

        if not sql.lower().startswith("select"):
            return "❌ Query ditolak: hanya SELECT yang diizinkan."

        forbidden = ["insert", "update", "delete", "drop", "alter"]
        if any(word in sql.lower() for word in forbidden):
            return "❌ Query mengandung operasi berbahaya."

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()
            
        if not rows:
            return f"SQL:\n{sql}\n\nHasil: Tidak ditemukan data."

        lines = [
            "SQL:",
            sql,
            "",
            "Hasil:",
            " | ".join(columns)
        ]

        for row in rows:
            lines.append(" | ".join(str(v) for v in row))

        result_text = "\n".join(lines)

        return result_text

    except Exception as e:
        logging.error(f"[SQL ERROR]: {e}", exc_info=True)

        return f"❌ Terjadi error saat eksekusi query:\n{str(e)}"