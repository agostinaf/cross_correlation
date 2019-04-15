#!/usr/bin/env python
# coding: utf-8

import warnings
import sys
import pandas as pd
from astropy.table import Table

sys.path.append('..')
from cross_id.utils import sigma_ellipse

warnings.simplefilter('ignore')


if __name__ == '__main__':

    # Download the 4FGL catalog
    cat = Table.read('https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/gll_psc_v18.fit')
    cat.convert_bytestring_to_unicode()
    df = cat.to_pandas()

    # Search for unassociated objects
    df = df[ df['CLASS'] == '     ' ]
    df.reset_index(drop=True, inplace=True)

    # Impute missing values
    df['Conf_95_SemiMajor'].fillna(df['Conf_95_SemiMajor'].median(), inplace=True)
    df['Conf_95_SemiMinor'].fillna(df['Conf_95_SemiMinor'].median(), inplace=True)
    df['Conf_95_PosAng'].fillna(df['Conf_95_PosAng'].median(), inplace=True)  # FIXME

    # Add columns for uncertainty in RA and DE
    sigma_ellipse(df, 'Conf_95_SemiMajor', 'Conf_95_SemiMinor', 'Conf_95_PosAng')

    # Rename columns
    df.rename(columns={'RAJ2000': 'RA',
                       'DEJ2000': 'DE',
                       'Source_Name': 'NAME'},
                        inplace=True)

    # Select columns and save output to a CSV file
    df[['NAME','RA','DE','SIGMA_RA','SIGMA_DE']].to_csv('../catalogs/4FGL_UNASSOC.csv', index=False)
