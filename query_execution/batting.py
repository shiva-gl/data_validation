import pandas as pd

from utils.genric import make_directory
from utils.read_json_file import read_json_file_to_dict


def batting_data(source_cursor, destination_cursor):
    print("Batting table data validation START")
    # df means data frame
    query = f'select DISTINCT(Match_Id) from BCCI.clear.PFT_BCCI_BATTING where Match_Id != \' \''
    match_ids = pd.read_sql(query, source_cursor)["Match_Id"]
    for math_id in match_ids:
        # reading and executing sql queries on source table
        source_df = pd.read_sql(f'{read_json_file_to_dict()["source"]["batting"]} where Match_Id = \'{math_id}\'', source_cursor)

        # reading and executing sql queries on destination table
        destination_df = pd.read_sql(f'{read_json_file_to_dict()["destination"]["batting"]} where EX_Match_Id = \'{math_id}\'', destination_cursor)

        column_sort = ["S_Bat_Order", "S_Runs", "S_Minutes", "S_Fours", "S_Sixes", "S_Balls", "S_Innings"]
        destination_df[column_sort] = destination_df[column_sort].apply(pd.to_numeric)

        df11 = source_df.sort_values(by=source_df.columns.tolist()).reset_index(drop=True)
        df21 = destination_df.sort_values(by=destination_df.columns.tolist()).reset_index(drop=True)
        make_directory(f'./report/batting')
        try:
            result = df11.compare(df21)
            if result.size != 0:
                result.to_csv(f'./report/batting/{math_id}.csv', index=False)
        except Exception:
            make_directory(f'./report/batting/{math_id.replace(" ", "_")}')
            df11.to_csv(f'./report/batting/{math_id.replace(" ", "_")}/source.csv', index=False)
            df21.to_csv(f'./report/batting/{math_id.replace(" ", "_")}/destination.csv', index=False)
    print("Batting table data validation END")