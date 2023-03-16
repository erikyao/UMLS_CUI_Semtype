import os
import pandas as pd


def read_mrconso_data_frame(filepath) -> pd.DataFrame:
    column_info = [
        # Each element is a tuple of (column_index, column_name, data_type)
        #   See column description at https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/
        (0, "CUI", str),  # column 0
        (1, "LAT", str),  # column 1, Language of Terms
        (2, "TS", str),   # column 2, Term Status
        # (3, "LUI", str),  # column 3 (ignored)
        (4, "STT", str),  # column 4, String Type
        # (5, "SUI", str),  # column 5 (ignored)
        (6, "ISPREF", str),  # column 6, Is-Preferred
        # (7, "AUI", str),  # column 7 (ignored)
        # (8, "SAUI", str),  # column 8 (ignored)
        # (9, "SCUI", str),  # column 9 (ignored)
        # (10, "SDUI", str),  # column 10 (ignored)
        # (11, "SAB", str),  # column 11 (ignored)
        # (12, "TTY", str),  # column 12 (ignored)
        # (13, "CODE", str),  # column 13 (ignored)
        (14, "STR", str),  # column 14, the name string of the CUI
        # (15, "SRL", str),  # column 15 (ignored)
        # (16, "SUPPRESS", str),  # column 16 (ignored)
        # (17, "CVF", str)  # column 17 (ignored)
    ]
    column_indices = [e[0] for e in column_info]
    column_names = [e[1] for e in column_info]
    column_dtypes = {e[1]: e[2] for e in column_info}
    data_frame = pd.read_csv(filepath, sep="|", names=column_names, usecols=column_indices, dtype=column_dtypes)
    return data_frame


def get_preferred_english_cui_names(mrconso_df: pd.DataFrame) -> pd.DataFrame:
    """
    Example 7 of UMLS Database Query Diagrams (https://www.nlm.nih.gov/research/umls/implementation_resources/query_diagrams/er1.html) uses the following SQL
      statement to find all relationships for a concept and the preferred (English) name of the related CUI.

        SELECT a.cui1, a.cui2, b.str FROM mrrel a, mrconso b
        WHERE a.cui1 = 'C0032344'
            AND a.stype1 = 'CUI'
            AND a.cui2 = b.cui
            AND b.ts = 'P'
            AND b.stt = 'PF'
            AND b.ispref = 'Y'
            AND b.lat = 'ENG';
        
    Therefore we conclude that the filtering condition to get all the preferred English names for CUIs is

        TS == 'P'          # Term Status being "Preferred LUI of the CUI"
        and STT == 'PF'    # String Type being "Preferred form of term"
        and ISPREF == 'Y'  # Atom status being "preferred" (Y) for this string within this concept
        and LAT == 'ENG'   # Language of Terms being "English"

    The explanation of other TS, STT, and LAT values can be found at
      [Abbreviations Used in Data Elements - 2022AB Release](https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html).
    The meaning of ISPREF is explained at
      [Table 1, UMLS Reference Manual](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr).
    """
    ts_flags = (mrconso_df["TS"] == "P")
    stt_flags = (mrconso_df["STT"] == "PF")
    ispref_flags = (mrconso_df["ISPREF"] == "Y")
    lat_flags = (mrconso_df["LAT"] == "ENG")

    columns = ["CUI", "STR"]

    # For 2022AA release, given the above filtering condition, each CUI in the following data frame has only one preferred English name
    mrconso_pref_eng_df = mrconso_df.loc[ts_flags & stt_flags & ispref_flags & lat_flags, columns]
    return mrconso_pref_eng_df


# def get_preferred_non_english_cui_names(mrconso_df: pd.DataFrame) -> pd.DataFrame:
#     ts_flags = (mrconso_df["TS"] == "P")
#     stt_flags = (mrconso_df["STT"] == "PF")
#     ispref_flags = (mrconso_df["ISPREF"] == "Y")
#
#     columns = ["CUI", "LAT", "STR"]
#     mrconso_pref_df = mrconso_df.loc[ts_flags & stt_flags & ispref_flags, columns]
#
#     mrconso_pref_df["is_ENG"] = mrconso_pref_df["LAT"].eq("ENG")
#     flags = mrconso_pref_df.groupby("CUI")["is_ENG"].apply(lambda x: x.any()).reset_index(name="has_ENG")
#     mrconso_pref_df = mrconso_pref_df.merge(flags, on="CUI")  # join on the common "CUI" columns
#     del mrconso_pref_df["is_ENG"]
#
#     return mrconso_pref_df.loc[~mrconso_pref_df["has_ENG"], columns]


def read_mrsty_data_frame(filepath) -> pd.DataFrame:
    column_info = [
        # Each element is a tuple of (column_index, column_name, data_type)
        #   See column description in Section 3.3.7 of https://www.ncbi.nlm.nih.gov/books/NBK9685/
        (0, "CUI", str),  # column 0
        # (1, "TUI", str),  # column 1 (ignored)
        # (2, "STN", str),  # column 2 (ignored)
        (3, "STY", str),  # column 3, Semantic Type
        # (4, "ATUI", str),  # column 4 (ignored)
        # (5, "CVF", str)  # column 5 (ignored)
    ]
    column_indices = [e[0] for e in column_info]
    column_names = [e[1] for e in column_info]
    column_dtypes = {e[1]: e[2] for e in column_info}

    # Each CUI may have one or more Semantic Types
    data_frame = pd.read_csv(filepath, sep="|", names=column_names, usecols=column_indices, dtype=column_dtypes)
    return data_frame


def read_semantic_type_mapping_data_frame(filepath) -> pd.DataFrame:
    column_info = [
        # See column description at https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/documentation/SemanticTypesAndGroups.html
        (0, 'ABV', str),  # abbreviated semantic type names
        # (1, 'TUI', str),
        (2, 'STY', str)  # full semantic type names
    ]
    column_indices = [e[0] for e in column_info]
    column_names = [e[1] for e in column_info]
    column_dtypes = {e[1]: e[2] for e in column_info}
    data_frame = pd.read_csv(filepath, sep="|", names=column_names, usecols=column_indices, dtype=column_dtypes)
    return data_frame


def load_data(mrconso_filepath, mrsty_filepath, semtype_mapping_filepath):
    # len(mrconso_df["CUI"].unique()) == 4,662,313
    mrconso_df = read_mrconso_data_frame(mrconso_filepath)

    # len(cui_name_df["CUI"].unique()) == cui_name_df.shape[0] == 4,661,936
    # 4,662,313 - 4,661,936 == 377 CUIs have no preferred English names
    cui_name_df = get_preferred_english_cui_names(mrconso_df)  

    # len(mrsty_df["CUI"].unique()) == 4,662,313
    #   same number with mrconso_df's, which means every CUI appeared in MRCONSO.RFF has a semantic type
    # len(mrsty_df["STY"].unique()) == 127
    mrsty_df = read_mrsty_data_frame(mrsty_filepath)

    # len(semtype_mapping_df["STY"].unique()) == semtype_mapping_df.shape[0] == 127
    #   same number with mrsty_df's, which means every Semantic Type in MRSTY.RRF has an abbreviated name in semtype_mapping_df
    semtype_mapping_df = read_semantic_type_mapping_data_frame(semtype_mapping_filepath)

    cui_semtype_df = mrsty_df.merge(semtype_mapping_df, how="left", on="STY")
    ret_df = cui_name_df.merge(cui_semtype_df, how="left", on="CUI")

    ret_df = ret_df.rename(columns={"STR": "concept_name", "STY": "semantic_type_name", "ABV": "semantic_type_abbreviation"})
    return ret_df


def df_to_dict_records(df: pd.DataFrame) -> list:
    """
    Currently "pd.DataFrame.to_dict(orient='records')" is slow and will be fixed in pandas 2.0.0.
    See https://github.com/pandas-dev/pandas/issues/46470.
    
    Use this native function before we upgrade to pandas 2.0.0
    """
    data = df.values.tolist()
    columns = df.columns.tolist() 
    return [dict(zip(columns, datum)) for datum in data]


def merge_semantic_type_columns(cui_df: pd.DataFrame) -> pd.DataFrame:
    cui_df = cui_df.rename(columns={"semantic_type_name": "name", "semantic_type_abbreviation": "abbreviation"})
    
    # After "groupby" operation, apply "to_dict('records')" to each sub-dataframe of ["name", "abbreviation"]
    # Note that "GroupBy.apply" is to all groups (i.e. sub-dataframes), and it does not allow "axis" parameter.
    # "pd.DataFrame.to_dict('record')"" will convert the dataframe into a list of [{column_name -> value}, ... , {column_name -> value}]
    cui_df = cui_df.groupby(["CUI", "concept_name"])[["name", "abbreviation"]].apply(lambda g: df_to_dict_records(g))

    # After "apply" operation, the previous ["semantic_type_name", "semantic_type_abbreviation"] columns are merged 
    #   into one column (named '0' by pandas by default) and "cui_df" is downgraded into a pd.Series. 
    # "pd.Series.reset_index(name)" will set the Series column name (while resetting the index)
    cui_df = cui_df.reset_index(name="semantic_type")

    """
    Now cui_df is like:

        CUI         concept_name                          semantic_type
        'C0000039'  '1,2-dipalmitoylphosphatidylcholine'  [{'name': 'Organic Chemical', 'abbreviation': 'orch'}, {...}]
    """
    return cui_df


if __name__ == '__main__':
    ###############
    # Read Inputs #
    ###############
    umls_release = "2022AB"
    umls_metathesaurus_folder = os.path.join(".", umls_release, "META")
    mrconso_path = os.path.join(umls_metathesaurus_folder, "MRCONSO.RRF")
    mrsty_path = os.path.join(umls_metathesaurus_folder, "MRSTY.RRF")

    semtype_mapping_path = "./SemanticTypes_2018AB.txt"

    # Load data frame
    cui_df = load_data(mrconso_path, mrsty_path, semtype_mapping_path)

    #################
    # Write Outputs #
    #################
    output_folder = "."
    tsv_name = f"UMLS_CUI_Semtype_{umls_release}.tsv"
    tsv_path = os.path.join(output_folder, tsv_name)
    jsonl_name = f"UMLS_CUI_Semtype_{umls_release}.jsonl"
    jsonl_path = os.path.join(output_folder, jsonl_name)

    # Output to a TSV file
    cui_df.to_csv(tsv_path, sep="\t", index=False)

    # Transform for JSON-Lines output
    cui_df = merge_semantic_type_columns(cui_df)

    # Output to a JSON-Lines file
    cui_df.to_json(jsonl_path, orient='records', lines=True)
