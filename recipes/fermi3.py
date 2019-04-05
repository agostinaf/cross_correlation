#!/usr/bin/env python
# coding: utf-8

import warnings
import sys
import pandas as pd
from astroquery.vizier import Vizier as v

sys.path.append('..')
from crossid.utils import sigma_ellipse

warnings.simplefilter('ignore')


if __name__ == '__main__':

    # Vizier parameters. Fetch all rows and columns
    v.ROW_LIMIT = -1
    v.columns=['**']

    catlist = v.get_catalogs('J/ApJS/218/23/')
    catlist[0].convert_bytestring_to_unicode()
    df = catlist[0].to_pandas()

    # Search for unassociated objects
    df = df[ df['Class'] == '' ]
    df.reset_index(drop=True, inplace=True)

    # Impute missing values
    df['amaj'].fillna(df['amaj'].median(), inplace=True)
    df['amin'].fillna(df['amin'].median(), inplace=True)
    df['phi'].fillna(df['phi'].median(), inplace=True)  # FIXME

    # Add columns for uncertainty in RA and DE
    sigma_ellipse(df, 'amaj', 'amin', 'phi')

    # Rename columns
    df.rename(columns={'RAJ2000': 'RA',
                       'DEJ2000': 'DE',
                       '_3FGL': 'NAME'},
                        inplace=True)

    # Select columns and save output to a CSV file
    df[['NAME','RA','DE','SIGMA_RA','SIGMA_DE']].to_csv('../catalogs/3FGL_UNASSOC.csv', index=False)
