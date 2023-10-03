import psycopg2

HOST = "localhost"
DATABASE = "pilpres"
USER = "postgres"
PASSWORD = "123"

def connect_to_database():
    return psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )

def execute_query(query):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def reset_rekapitulasi():
    query_list = [
        "DELETE FROM formd_status_data;", 
        "DELETE FROM suara_d_tps;", 
        "DELETE FROM formd_administrasi_tps;"
    ]

    for query in query_list:
        execute_query(query)

    print('SUCCESS : RESET REKAPITULASI')


def reset_penetapan():
    query_list = [
        "DELETE FROM penetapan_status;", 
        "DELETE FROM penetapan_suara;", 
        "DELETE FROM penetapan_terpilih;"
    ]

    for query in query_list:
        execute_query(query)

    print('SUCCESS : RESET PENETAPAN')

def inject_suara_d_tps():
    sql = """
        INSERT INTO suara_d_tps (id_user_entri, id_komputer_entri, id_versi_c, id_tps, jenis_pemilihan, id_paslon, jml_suara)
        SELECT 'inject by admin', 'sirekap-web', id_versi, id_tps, jenis_pemilihan, id_paslon , jml_suara
        FROM formc_image fi 
        JOIN suara_c sc ON fi.id_image = sc.id_image 
        WHERE jenis_pemilihan = 'ppwp' AND jenis_image = 35;
    """
    execute_query(sql)

    print('SUCCESS : INJECT DATA SUARA_D_TPS')
