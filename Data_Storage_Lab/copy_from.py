import psycopg2
TableName = 'CensusDataCopy'
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=<redacted>")
cur = conn.cursor()

cur.execute(f"""
    DROP TABLE IF EXISTS {TableName};
    CREATE TABLE {TableName} (
        TractId             NUMERIC,
        State               TEXT,
        County              TEXT,
        TotalPop            INTEGER,
        Men                 INTEGER,
        Women               INTEGER,
        Hispanic            DECIMAL,
        White               DECIMAL,
        Black               DECIMAL,
        Native              DECIMAL,
        Asian               DECIMAL,
        Pacific             DECIMAL,
        VotingAgeCitizen    DECIMAL,
        Income              DECIMAL,
        IncomeErr           DECIMAL,
        IncomePerCap        DECIMAL,
        IncomePerCapErr     DECIMAL,
        Poverty             DECIMAL,
        ChildPoverty        DECIMAL,
        Professional        DECIMAL,
        Service             DECIMAL,
        Office              DECIMAL,
        Construction        DECIMAL,
        Production          DECIMAL,
        Drive               DECIMAL,
        Carpool             DECIMAL,
        Transit             DECIMAL,
        Walk                DECIMAL,
        OtherTransp         DECIMAL,
        WorkAtHome          DECIMAL,
        MeanCommute         DECIMAL,
        Employed            INTEGER,
        PrivateWork         DECIMAL,
        PublicWork          DECIMAL,
        SelfEmployed        DECIMAL,
        FamilyWork          DECIMAL,
        Unemployment        DECIMAL
    );	
""")

print(f"Created {TableName}")

with open('acs2017_census_tract_data.csv', 'r') as f:
    # Notice that we don't need the csv module.
    next(f) # Skip the header row.
    cur.copy_from(f, TableName, sep=',')

conn.commit()