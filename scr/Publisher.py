import LoadPostgres as PG
import LoadOracle as OR
import LoadMySQL as MSQL

def main():
    OR.load_to_oracle()
    MSQL.load_to_mysql()
    PG.load_to_postgres()


if __name__ == "__main__":
    main()