#import loadOracle as OR
from scr.coadjuvantes import loadMySQL as MSQL, loadPostgres as PG


def main():
    #OR.load_to_oracle()
    MSQL.load_to_mysql()
    PG.load_to_postgres()


if __name__ == "__main__":
    main()