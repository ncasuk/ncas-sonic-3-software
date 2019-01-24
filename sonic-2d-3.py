import csv
import os

import pandas as pd

from ncas_sonic_4_software.sonic_2d import GillWindSonic

class IAOSonic(GillWindSonic):
    """
    class to convert the Gill or Vaisala 2D Sonic datafile from the 
    IAO to NetCDF
    """

    progname = __file__

    vaisalafields = ['Timestamp','Dn','Dm','Dx','Sn','Sm','Sx','Ta','Tp','Ua','Pa','Rc','Rd','Ri','Hc','Hd','Hi','Rp','Hp','Th','Vh','Vs','Vr','Id']

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
                    if line[1] == '0R0': #code for automatic data
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
        sonic['Timestamp'] = pd.DatetimeIndex(sonic['Timestamp'].values)
        sonic.set_index('Timestamp', inplace=True) 
        sonic['r'] = sonic.Sm # wind speed
        sonic['theta'] = sonic.Dm # Wind dir

        #set start and end times
        self.time_coverage_start = sonic.index[0].strftime(self.timeformat)
        self.time_coverage_end = sonic.index[-1].strftime(self.timeformat)

        return sonic


if __name__ == '__main__':
    args = IAOSonic.arguments().parse_args()
    sn = IAOSonic(args.metadata)
   
    try:
        os.makedirs(args.outdir,mode=0o755)
    except OSError:
         #Dir already exists, probably
         pass
    else:
        print ("Successfully create directory %s" % args.outdir)
    sn.sonic_netcdf(sn.get_sonic_data(args.infiles), args.outdir, args.metadata)
