import numpy as np

def sigma_ellipse(data, amaj, amin, phi):
    """ Add uncertainty columns for RA and DE (in radians) when an error ellipse is given.

    Parameters
    -------
    data : DataFrame
        Pandas dataframe.
    amaj: str
        Column name of the semi-major axis (deg).
    amin: str
        Column name of the semi-major axis (deg).
    phi: str
        Column name of the inclination angle (deg).
    """

    a = data[amaj].values *np.pi/180
    b = data[amin].values *np.pi/180
    theta = -np.abs(data[phi].values *np.pi/180)

    t1 = np.sin(theta)**2/a**2 + np.cos(theta)**2/b**2
    t2 = np.cos(theta)**2/a**2 + np.sin(theta)**2/b**2
    t3 = np.sin(2.0 * theta) * (1./b**2 - 1./a**2)

    data['SIGMA_RA'] = (180./np.pi) * 1./np.sqrt(t1 - t3**2/(4.*t2))
    data['SIGMA_DE'] = (180./np.pi) * 1./np.sqrt(t2 - t3**2/(4.*t1))

