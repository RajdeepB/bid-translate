import collections
import cleaning_module as cl
import csv


class BidTypes:

    daydict = {"": "", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}

    crew_grp_list = ['MHCC','LHCC','LHRC','PVGC','ANCC','20FD','8FD','7FD','MCCC','D3FD']

    roster_start_date = ''

    roster_end_date = ''

    # max times roster is invalid for an Avoid bid
    def create_generic_from_generic(bid_in, csv_out):
        bid_type = bid_in['a']
        crewid = bid_in['Number']
        avoid = str(cl.get_avoid(bid_in['Pref Type']))
        max_times_roster = cl.setMaxTimesRoster(bid_in['Rqd'], bid_in['Pref Type'])
        region = cl.get_region(bid_in['Rgn'])
        max_lo_nt = bid_in['Nt']
        bid_points = cl.setPoints((int(bid_in['Wt'])))
        pax = cl.get_pax(bid_in['Px'])
        day_range_2 = cl.get_dow_list(bid_in['From'], bid_in['Until'], bid_in['Remarks'])
        date_from = cl.conv_d(bid_in['From'])
        date_to = cl.conv_d(bid_in['Until'])
        port_data = cl.get_layover_transit(bid_in['Tod/Port'], bid_in['L/O'])
        layover = port_data[0]
        transit = port_data[1]
        pairingMin = bid_in['Min']
        pairingMax = cl.setPairingLenMax(bid_in['Max'])
        if bid_in['Rest']=='TRUE':
            specRuleRelax = 'Accept Minimum Rest'
            specRuleRelaxVal = 'Yes'
        else:
            specRuleRelax = ''
            specRuleRelaxVal = ''

        if len(day_range_2) != 0:
            for i in range(0, len(day_range_2)):
                day_from = day_range_2[i][0]
                day_to = day_range_2[i][1]
                csv_out.writerow({
                     'bidType_h':bid_type, 'crewId_h':crewid,
                     'dateIntervalFrom_h':date_from, 'dateIntervalTo_h':date_to,
                     'workPlaceLocation_h':specRuleRelax, 'workPlaceTask_h':specRuleRelaxVal,
                     'avoid_h':avoid,
                     'startDay_h':BidTypes.daydict[day_from], 'endDay_h':BidTypes.daydict[day_to],
                     'maxTimesPerPeriod_h':max_times_roster,
                     'bidRegion_h':region,
                     'layoverStation_h':layover,
                     'layoverLengthTo_h':max_lo_nt,
                     'stopStation_h':transit,
                     'tripLengthFrom_h':pairingMin, 'tripLengthTo_h':pairingMax,
                     'bidTripType_h':pax,
                     'bidPoints_h':bid_points})

        elif len(day_range_2) == 0:
            csv_out.writerow({'bidType_h': bid_type,
                              'crewId_h': crewid,
                              'dateIntervalFrom_h': date_from, 'dateIntervalTo_h': date_to,
                              'workPlaceLocation_h': 'Accept Min Rest', 'workPlaceTask_h': rest,
                              'avoid_h': avoid,
                              'maxTimesPerPeriod_h': max_times_roster,
                              'bidRegion_h': region,
                              'layoverStation_h': layover,
                              'layoverLengthTo_h': max_lo_nt,
                              'stopStation_h': transit,
                              'tripLengthFrom_h': pairingMin, 'tripLengthTo_h': pairingMax,
                              'bidTripType_h': pax,
                              'bidPoints_h': bid_points})


    # max times roster is invalid for an Avoid bid
    def create_generic_from_specific(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        avoid = str(cl.get_avoid(bid['Pref Type']))
        max_times_roster = cl.setMaxTimesRoster(bid['Rqd'], bid['Pref Type'])
        # bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        pax = cl.get_pax(bid['Px'])
        dt_data = cl.get_start_end_signon_signoff(bid['From'], bid['Until'])
        date_from = dt_data[0]
        date_to = dt_data[1]
        signon_from = dt_data[2]
        signon_to = dt_data[3]
        port = cl.get_port_spec_pair(bid['Tod/Port'])
        port_data = cl.get_layover_transit(port, '')
        layover = port_data[0]
        transit = port_data[1]
        if bid['Rest']=='TRUE':
            specRuleRelax = 'Accept Minimum Rest'
            specRuleRelaxVal = 'Yes'
        else:
            specRuleRelax = ''
            specRuleRelaxVal = ''
        csvout.writerow({'bidType_h': bid_type,
                         'crewId_h': crewid,
                         'dateIntervalFrom_h': date_from, 'dateIntervalTo_h': date_to,
                         'workPlaceLocation_h':specRuleRelax, 'workPlaceTask_h':specRuleRelaxVal,
                         'avoid_h': avoid,
                         'maxTimesPerPeriod_h': max_times_roster,
                         'layoverStation_h': layover,
                         'stopStation_h': transit,
                         'tripStartFrom_h':signon_from, 'tripStartTo_h':signon_to,
                         'bidTripType_h': pax,
                         'bidPoints_h': bid_points})


    def create_gen_bids_from_lsta_efin(bid, csvout):
        bid_type = bid['Pref Type']
        crewid = bid['Number']
        bid_points = '100 p'
        date_from = cl.conv_d(bid['From'])
        date_to = date_from
        max_times_roster = '1'

        if bid_type=='EFIN':
            signoff_from = '00:00'
            signoff_to = '18:10'
        elif bid_type=='LSTA':
            signon_from ='12:00'
            signon_to ='23:59'

        csvout.writerow({'bidType_h': bid_type,
                         'crewId_h': crewid,
                         'dateIntervalFrom_h': date_from, 'dateIntervalTo_h': date_to,
                         'maxTimesPerPeriod_h': max_times_roster,
                         'tripStartFrom_h': signon_from, 'tripStartTo_h': signon_to,
                         'tripFinishFrom_h': signoff_from, 'tripFinishTo_h': signoff_to,
                         'bidPoints_h': bid_points})

    def create_gof_from_golden(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        # bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        date_from = cl.conv_d(bid['From'])
        csvout.writerow({'bidType_h': bid_type,
                         'crewId_h': crewid,
                         'dateIntervalFrom_h': date_from,
                         'bidPoints_h': bid_points})


    def create_dayoff_from_spec_day_off(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        # bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        date_from = cl.conv_d(bid['From'])
        date_to = cl.conv_d(bid['Until'])
        csvout.writerow({'bidType_h': bid_type,
                         'crewId_h': crewid,
                         'dateIntervalFrom_h': date_from, 'dateIntervalTo_h': date_to,
                         'bidPoints_h': bid_points})


    def create_timeoff_from_qual_timeoff(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        # bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        time_pair = cl.get_end_time(bid['From'], bid['Durn'])
        time_from = time_pair[0]
        time_to = time_pair[1]
        csvout.writerow({'bidType_h': bid_type,
                         'crewId_h': crewid,
                         'dateIntervalFrom_h':BidTypes.roster_start_date, 'dateIntervalTo_h':BidTypes.roster_end_date,
                         'timeIntervalFrom_h':time_from, 'timeIntervalTo_h':time_to,
                         'bidPoints_h':bid_points})

    def create_timeoff_from_spec_timeoff(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        # bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        date_from = cl.conv_d(bid['From'])
        date_to = cl.get_end_date_time_from_duration(bid['From'], bid['Durn'])
        time_from = cl.conv_t(bid['From'])
        time_to = date_to[1]
        csvout.writerow({'bidType_h':bid_type,
                         'crewId_h':crewid,
                         'dateIntervalFrom_h':date_from, 'dateIntervalTo_h':date_to[0],
                         'timeIntervalFrom_h':time_from, 'timeIntervalTo_h':time_to,
                         'bidPoints_h':bid_points})

    def create_timeoff_from_gen_timeoff(bid, csvout,
                                        gen_timeoff_start_dict):
        bid_type = bid['a']
        crewid = bid['Number']
        bid_points = cl.setPoints((int(bid['Wt']))) # use for MHCC
        # bid_points = cl.setPoints_lhcc(bid_type, bid['Pref Type']) # use for LHCC
        data = cl.get_time_off_params(bid_type, bid['From'],
                                      bid['Durn'], bid['Remarks'])
        time_from = cl.get_start_time_gen_timeoff(bid['SeqNum'],
                                                  gen_timeoff_start_dict)
        for i in range(0, len(data)):
            csvout.writerow({'bidType_h':bid_type,
                             'crewId_h':crewid,
                             'dateIntervalFrom_h':data[i][0], 'dateIntervalTo_h':data[i][1],
                             'timeIntervalFrom_h':time_from, 'timeIntervalTo_h':data[i][2],
                             'startDay_h':data[i][3],'endDay_h':data[i][4],
                             'bidPoints_h':bid_points})


    def create_rr_from_rr(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']
        csvout.writerow({'crewId_h':crewid, 'rrType_h':bid_type})


    def create_dayoff_bids_from_do_shcc500(bid, csvout):
        bid_type = bid['Pref Type']
        crewid = bid['Number']
        bid_points = '100 p'
        date_from = cl.conv_d(bid['From'])
        date_to = date_from
        csvout.writerow({'bidType_h':bid_type,
                         'crewId_h':crewid,
                         'dateIntervalFrom_h':date_from, 'dateIntervalTo_h':date_to,
                         'bidPoints_h':bid_points})


    def create_working_pref_from_pref(bid, csvout):
        bid_type = bid['a']
        crewid = bid['Number']


    # def create_timeoff_from_allprd(bid, csvout):
    #     bid_type = bid['a']
    #     crewid = bid['Number']
    #     bid_points = cl.setPoints((int(bid['Wt'])))
    #     time_from = bid['From']
    #     time_to = bid['Durn']
    #     date_range = cl.get_dow_list(BidTypes.roster_start_date,BidTypes.roster_end_date, bid['Remarks'])
    #
    #     csvout.writerow({'bidType_h': bid_type,
    #                      'crewId_h': crewid,
    #                      'dateIntervalFrom_h': data[i][0], 'dateIntervalTo_h': data[i][1],
    #                      'timeIntervalFrom_h': time_from, 'timeIntervalTo_h': time_to,
    #                      'startDay_h': data[i][3], 'endDay_h': data[i][4],
    #                      'bidPoints_h': bid_points})
