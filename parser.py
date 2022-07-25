#!/usr/bin/env python3

from cmath import nan
import csv
from nis import match
import sys
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine, null


def decode(fileName):
    if fileName.endswith(".csv"):
        fileName = fileName.replace(".csv", "")

    with open(f"{fileName}_utf.csv", "w", encoding="utf-8") as wf:
        writer = csv.writer(wf)
        with open(f"{fileName}.csv", "r", encoding="cp949") as f:
            reader = csv.reader(f)
            for i in range(15):
                next(reader)

            for row in reader:
                writer.writerow(row)

    return fileName + "_utf.csv"


def readCsv(fileName):
    cols = pd.read_csv(fileName, nrows=1)
    cols = cols.columns.tolist()
    cols_idx = cols[:len(cols) - 3]
    del cols_idx[2:4]

    data = pd.read_csv(fileName, usecols=cols_idx)
    cols_name = ['dist_origin', 'bunji', 'building', 'area', 'date_contract',
                 'day_contract', 'price', 'floor', 'year_build', 'dist_road']
    data.columns = cols_name

    return data


def generateDistInfo(rawInfo: pd.DataFrame):
    distDf = rawInfo.drop_duplicates(subset=['dist_origin'])

    dist_origin = []
    dist_join = []
    sub_dist1 = []
    sub_dist2 = []
    sub_dist3 = []
    sub_dist4 = []

    for dist in distDf['dist_origin']:
        dist_origin.append(dist)
        dists = getDistricts(dist)
        sub_dist1.append(dists[0])
        sub_dist2.append(dists[1])
        sub_dist3.append(dists[2])
        sub_dist4.append(dists[3] if len(dists) > 3 else None)
        dist_join.append(' '.join(dists))

    distDf = pd.DataFrame({'dist_origin': dist_origin,
                           'dist_join': dist_join,
                           'sub_dist1': sub_dist1,
                           'sub_dist2': sub_dist2,
                           'sub_dist3': sub_dist3,
                           'sub_dist4': sub_dist4})

    return distDf


def getDistricts(dist: str):
    dists = dist.split(" ")

    if len(dists[1]) > 4:
        dists.insert(2, dists[1][2:])
        dists[1] = dists[1][:2] + '시'

    return dists


def generateBuildingInfo(rawInfo: pd.DataFrame):
    buildingDf = rawInfo.drop_duplicates(subset=['building'])

    return buildingDf


def generateAreaInfo(rawInfo: pd.DataFrame):
    areaDf = rawInfo.drop_duplicates(
        subset=['dist_origin', 'dist_road', 'area'])

    return areaDf


def generateTradeInfo(rawInfo: pd.DataFrame):
    return


def table_column_names(tableName: str) -> str:
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tableName}'"
    rows = db_connection.execute(query)
    dirty_names = [i[0] for i in rows]
    clean_names = '`' + '`, `'.join(map(str, dirty_names[1:])) + '`'
    print(tableName + " columns=" + clean_names)

    return clean_names


def updateDatabase(info, tableName):
    try:
        tempTableName = tableName + "Temp"
        info.to_sql(name=tempTableName, con=conn,
                    index=False, if_exists='replace')
        columns = table_column_names(tableName)
        insert_query = f'INSERT IGNORE INTO {tableName}({columns}) SELECT {columns} FROM `{tempTableName}`'
        db_connection.execute(insert_query)
        print("Successfully " + tableName + " updated")
    except Exception as e:
        print(e)


def updateDabaseFromExcel(generateInfoFromExcel, rawInfo, tableName) -> pd.DataFrame:
    info = generateInfoFromExcel(rawInfo)
    print("tableName=" + tableName + " " + str(len(info)) + " data to update")
    updateDatabase(info, tableName)
    return info


if __name__ == '__main__':
    fileName = decode(sys.argv[1])
    data = readCsv(fileName)

    # Use your database address and password
    # db_connection_str = 'mysql+pymysql://[db유저이름]:[db password]@[host address]/[db name]'
    db_connection_str = 'mysql+pymysql://root:test@localhost/zipzup'
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()

    distInfo = updateDabaseFromExcel(
        generateDistInfo, data[['dist_origin']].copy(), 'districts')
    buildingInfo = updateDabaseFromExcel(
        generateBuildingInfo, data[['building', 'dist_origin', 'dist_road', 'bunji', 'year_build']].copy(), 'buildings')
    areaInfo = updateDabaseFromExcel(
        generateAreaInfo, data[['dist_origin', 'dist_road', 'area']].copy(), 'areas')
    tradeInfo = updateDabaseFromExcel(
        generateTradeInfo, data[['dist_origin', 'dist_road', 'bunji', 'building', 'date_contract', 'day_contract', 'price', 'floor', 'area']].copy(), 'areas')
    conn.close()
