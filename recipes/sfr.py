#!/usr/bin/env python
# coding: utf-8

import warnings
import sys
import numpy as np
import pandas as pd
from astroquery.vizier import Vizier as v

warnings.simplefilter('ignore')


if __name__ == '__main__':

    # Vizier parameters. Fetch all rows and columns
    v.ROW_LIMIT = -1
    v.columns=['**', '_RAJ2000', '_DEJ2000']

    catlist = v.get_catalogs('V/112A')
    catlist[0].convert_bytestring_to_unicode()
    df = catlist[0].to_pandas()

    # Remove duplicate sources
    df['COORDS'] = df['_RAJ2000'].map(str) + '+' + df['_DEJ2000'].map(str)
    df.drop_duplicates(subset=['COORDS'], inplace=True)

    # Add columns for uncertainty in RA and DE
    df.loc[ df['x_Size1'] == '\'', 'SIGMA_RA'] = df['Size1']/60
    df.loc[ df['x_Size1'] == '\"', 'SIGMA_RA'] = df['Size1']/3600
    df.loc[ df['x_Size2'] == '\'', 'SIGMA_DE'] = df['Size2']/60
    df.loc[ df['x_Size2'] == '\"', 'SIGMA_DE'] = df['Size2']/3600

    # 3-sigma to 1-sigma
    df['SIGMA_RA'] = df['SIGMA_RA'] *(68.26/99.73)
    df['SIGMA_DE'] = df['SIGMA_DE'] *(68.26/99.73)

    # Discard values when units are unknown
    df.loc[ df['x_Size1'].isnull(), 'SIGMA_RA'] = np.nan
    df.loc[ df['x_Size2'].isnull(), 'SIGMA_DE'] = np.nan

    # Impute missing values
    df['SIGMA_RA'].fillna(df['SIGMA_RA'].median(), inplace = True)
    df['SIGMA_DE'].fillna(df['SIGMA_DE'].median(), inplace = True)

    # Rename some columns
    df.rename(columns={'_RAJ2000': 'RA',
                       '_DEJ2000': 'DE',
                       'Name': 'NAME'},
                       inplace=True)

    # Select columns and save output to a CSV file
    df[['NAME','RA','DE','SIGMA_RA','SIGMA_DE']].to_csv('../catalogs/SFR.csv', index=False)
