import loadPostgres as PG
import loadOracle as OR
import loadMySQL as MSQL

def main():
    OR.load_to_oracle()
    MSQL.load_to_mysql()
    PG.load_to_postgres()


# if __name__ == "__main__":
#     main()