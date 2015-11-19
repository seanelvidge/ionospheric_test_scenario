# -*- coding: utf-8 -*-
#
#****************************************************************************#
#                                                                            #
#  Copyright (c) 2015, by University of Birmingham. All rights reserved.     #
#                                                                            #
#  Redistribution and use in source and binary forms, with or without        #
#  modification, are permitted provided that the following conditions        #
#  are met:                                                                  #
#                                                                            #
#      * Redistributions of source code must retain the above copyright      #
#        notice, this list of conditions and the following disclaimer.       #
#      * Redistributions in binary form must reproduce the above copyright   #
#        notice, this list of conditions and the following disclaimer in the #
#        documentation and/or other materials provided with the distribution.#
#      * The name 'University of Birmingham' may not be used to endorse or   #
#        promote produces derived from this software without specific prior  #
#        written permission.                                                 #
#                                                                            #
#****************************************************************************#
#
def download_test_scenario(location=None):
    """
    Script to download the ionosonde (SAO) and GPS (rinex) files used for
    the ionospheric model validation test scenario first described at the 
    AT-RASC 2015 meeting and for which there is a session at ESWW12.
    
    Parameters
    ----------
    location : string
        The location for the downloaded data. Default is the current dir.
            
    Modification History
    -------
    Created on May 2015 by Sean at SERENE, University of Birmingham
    Contact: s.elvidge@bham.ac.uk
    """
    import os
    import datetime as dt
    import ftplib
    
    # Get current directory
    curdir = os.getcwd()
    
    if location == None: location=curdir    
    startdate = dt.datetime(2008,12,8)
    enddate = dt.datetime(2009,1,7)
    
    iono_stationlist = ['RL052', 'JR055', 'PQ052']    
    gps_stationlist = ['bor1','brus','gope','helg','hert','opmt','pots',
                   'ptbb','wroc','wsr2t','zimm']
    
    # Check download location exists. If not try and create it.
    if os.path.isdir(location) == False:
        print 'Required location does not exist, trying to create.'
        os.mkdir(location)
        if os.path.isdir(location) == False:
            print 'Required location does not exist. Exiting.'
            return -1
    
    
    """ Download GPS files """
    print 'Downloading GPS files'
    # Make folder for GPS files
    path = os.path.join(location,'gps')
    if not os.path.isdir(path): os.mkdir(path)
    os.chdir(path)
    
    # Connect to FTP server
    try:
        conn = ftplib.FTP('garner.ucsd.edu')
        conn.login(user='anonymous', passwd='s.elvidge@bham.ac.uk')
    except Exception:
        print 'Cannot connect to the Garner anonymous FTP server to retreive data.'
        return -1
    
    print 'Connecting to the Garner anonymous FTP server to retreive data.'
    
    # Move to folder
    conn.cwd('./rinex')    
    
    day_count = (enddate - startdate).days + 1
    
    # Loop through required dates
    for date in [startdate + dt.timedelta(n) for n in range(day_count)]:
        conn.cwd(str(date.year) + '/' + str(date.timetuple().tm_yday).zfill(3))
        for station in gps_stationlist:
            # Get list of matching files
            filelist = conn.nlst('./' + station.lower() + '*')
            # Loop through required stations and download
            for file in filelist:
                print ('Downloading station %s data for %s...' 
                       %(station, date.strftime('%Y-%m-%d')))
                downloadpath = os.path.join(path, date.strftime('%Y-%m-%d'))
                # Create dir if it doesn't exist
                if not os.path.isdir(downloadpath): os.makedirs(downloadpath)
                rSize = conn.size(file)
                lFile = open(os.path.join(downloadpath,file), 'wb')
                conn.retrbinary('RETR %s' %file, lFile.write)
                lSize = lFile.tell()
                lFile.close()
                if rSize == lSize:
                    print 'Transfer complete'
                else:
                    print 'Bad transfer', rSize, lSize
                                                            
        conn.cwd('../../')
    conn.quit()
    os.chdir(curdir)
    print '***************************'
    
    """ Download SAO files """
    print 'Downloading SAO files'
    # Make folder for SAO files
    path = os.path.join(location,'sao')
    if not os.path.isdir(path): os.mkdir(path)
    os.chdir(path)
    
    # Connect to FTP server
    try:
        conn = ftplib.FTP('ftp.ngdc.noaa.gov')
        conn.login()
    except Exception:
        print 'Cannot connect to the NOAA FTP server to retreive data.'
        return -1
    
    print 'Connecting to the NOAA FTP server to retreive data.'
    
    for station in iono_stationlist: 
        path = os.path.join(os.curdir, station)
        if not os.path.isdir(path): os.mkdir(path)
        for date in [startdate + dt.timedelta(n) for n in range(day_count)]:
                rpath = ('/ionosonde/data/' + station + '/individual/' + 
                        str(date.year) + '/' + 
                        str(date.timetuple().tm_yday).zfill(3) + '/scaled')
                print rpath
                conn.cwd(rpath)    
                filelist = conn.nlst('*.SAO')
                print ('Downloading ionosonde %s data for %s...' 
                            %(station, date.strftime('%Y-%m-%d')))
                for file in filelist:
                    rSize = conn.size(file)
                    lFile = open(os.path.join(path,file),'wb')
                    conn.retrbinary('RETR %s' %file, lFile.write)
                    lSize = lFile.tell()
                    lFile.close()
                    if rSize != lSize:
                        print 'Bad transfer of %s' %file
        

	
    conn.quit()
    os.chdir(curdir)
    
    print 'Downloads complete.'
    
if __name__ == "__main__":
    download_test_scenario()
