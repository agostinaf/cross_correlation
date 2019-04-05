import numpy as np
import pandas as pd

def rmatch(x, y, R=3.03):
    """ Crossmatch two catalogs.

    Parameters
    -------
    x : DataFrame
        Pandas dataframe with NAME, RA, DE, SIGMA_RA and SIGMA_DE columns.
    y : DataFrame
        Pandas dataframe with NAME, RA, DE, SIGMA_RA and SIGMA_DE columns.

    Returns
    -------
    DataFrame
        Crossmatched table.

    """

    matches = []

    for i in range(len(x.RA)):

        t1 = (x.RA[i] - y.RA)**2/(x.SIGMA_RA[i]**2 + y.SIGMA_RA**2)
        t2 = (x.DE[i] - y.DE)**2/(x.SIGMA_DE[i]**2 + y.SIGMA_DE**2)
        r = np.sqrt(t1+t2)

        s = r <= R
        m = s.sum()
        if m > 0:

            z = pd.DataFrame()
            z['NAME2'] = y['NAME'][np.array(s)]
            z['RA2'] = y['RA'][np.array(s)]
            z['DE2'] = y['DE'][np.array(s)]
            z['SIGMA_RA2'] = y['SIGMA_RA'][np.array(s)]
            z['SIGMA_DE2'] = y['SIGMA_DE'][np.array(s)]
            z['ID1'] = i
            z['NAME1'] = x['NAME'][i]
            z['RA1'] = x['RA'][i]
            z['DE1'] = x['DE'][i]
            z['SIGMA_RA1'] = x['SIGMA_RA'][i]
            z['SIGMA_DE1'] = x['SIGMA_DE'][i]
            z['ID2'] = z.index

            z.reset_index(drop=True, inplace=True)
            z['N'] = z.index

            z = z[['N', 'ID1', 'NAME1', 'RA1', 'DE1', 'SIGMA_RA1', 'SIGMA_DE1',
                   'ID2', 'NAME2', 'RA2', 'DE2', 'SIGMA_RA2', 'SIGMA_DE2']]

            matches.append(z)

    xtable = pd.concat(matches)
    xtable.reset_index(drop=True, inplace=True)

    print('\nSources with at least one match:', len(matches))
    print()

    return xtable
