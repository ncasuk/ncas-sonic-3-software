import csv

import pandas as pd

from ncas_sonic_4_software.sonic_2d import GillWindSonic

class IAOSonic(GillWindSonic):
    """
    class to convert the Gill or Vaisala 2D Sonic datafile from the 
    IAO to NetCDF
    """

    vaisalafields = ['Timestamp','Dn','Dm','Dx','Sn','Sm','Sx','Ta','Tp','Ua','Pa','Rc','Rd','Ri','Hc','Hd','Hi','Rp','Hp','Th','Vh','Vs','Vr','Id']

    def __init__(self):
        pass;

    def get_sonic_data(self, infiles):
        """
        Takes Vaisala windsonic data files of form:

        ::

        2018-10-03T00:00:00.190590,0R0,Dn=000#,Dm=000#,Dx=000#,Sn=0.0#,Sm=0.0#,Sx=0.0#,Th=15.3C,Vh=11.9#,Vs=12.1V,Vr=3.502V,Id=HEL/___

            :param infiles: list(-like) of data filenames
            :return: a Pandas DataFrame of the sonic data
        """

        data = []
        for infile in infiles:
            with open(infile, 'rt') as f:
                indata = csv.reader(f)
                for line in indata:
                    out = {'Timestamp': line[0]}
                    #discard line[1], it's just a start-of-data indicator
                    for datum in line[2:]:
                        details = datum.split('=')
                        #values are suffixed with a single character unit, ignore it
                        out[details[0]] = details[1][:-1]
                        if details[0] == 'Id':
                            out[details[0]] = details[1]
                    data.append(out)
        sonic = pd.DataFrame(data)
        print(sonic)


df = IAOSonic()
df.get_sonic_data(['20181003_sonic.csv'])
