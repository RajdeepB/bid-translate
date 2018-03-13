import csv
import os
import bidtypes as bt
import cleaning_module as cm
from time import strftime, localtime
import logging

ventra_csv = input('Enter csv file location :')
crew_grp = input('Enter crew group :')
bt.BidTypes.roster_start_date = input('Enter crew group :')
bt.BidTypes.roster = input('Enter roster start date dd/mm/yyyy:')
cm.source_file = input('Enter roster end date dd/mm/yyyy :')

csvFile = open(ventra_csv)  # bids csv source file

gen_timeoff_start_dict = {}

element_list_generic = ['crewId_h', 'bidType_h',
                        'dateIntervalFrom_h', 'dateIntervalTo_h',
                        'workPlaceLocation_h', 'workPlaceTask_h',
                        'startDay_h', 'endDay_h',
                        'avoid_h',
                        'maxTimesPerPeriod_h',
                        'bidRegion_h',
                        'layoverStation_h',
                        'layoverLengthFrom_h', 'layoverLengthTo_h',
                        'layoverStartFrom_h', 'layoverStartTo_h',
                        'stopStation_h',
                        'stopLengthFrom_h', 'stopLengthTo_h',
                        'stopStartFrom_h', 'stopStartTo_h',
                        'tripStartFrom_h', 'tripStartTo_h',
                        'tripFinishFrom_h', 'tripFinishTo_h',
                        'tripLengthFrom_h', 'tripLengthTo_h',
                        'tripStopsFrom_h', 'tripStopsTo_h',
                        'dutyTimeFrom_h', 'dutyTimeTo_h',
                        'bidTripType_h',
                        'bidPoints_h']

element_list_time_off = ['crewId_h', 'bidType_h',
                        'dateIntervalFrom_h', 'dateIntervalTo_h',
                        'timeIntervalFrom_h', 'timeIntervalTo_h',
                        'startDay_h', 'endDay_h',
                        'bidPoints_h']

element_list_rule_relax = ['crewId_h', 'bidType_h']

element_list_working_pref = []

csv_list =['generic_bids','dayOff_bids','timeOff_bids','rule_relaxation','working_pref']

csvDReader = csv.DictReader(csvFile)

newpath = r"D:\Translated_"+crew_grp
if not os.path.exists(newpath):
    os.makedirs(newpath)

csv_created = strftime("%Y%m%d_%H%M%S", localtime())

#
# for i in csv_list:
#     outputFile_genericBids = open(newpath+"\"+i+csv_created+''')), 'w', newline='')


# outputFile_genericBids = open(newpath+'\generic_bids_'+csv_created+'.csv', 'w',
# #                               newline='')
# outputFile_ruleRelaxations = open(newpath+'\\rule_relaxations_'+csv_created+'.csv',
#                                   'w', newline='')
# outputFile_timeOff = open(newpath+'\\time_off_'+csv_created+'.csv', 'w',
#                           newline='')
# outputFile_dayOff_gof = open(newpath+'\gof_day_off_'+csv_created+'.csv', 'w',
#                              newline='')

# outputWriter_generic = csv.writer(outputFile_genericBids, delimiter=',')
#
with open(newpath+'\generic_bids_'+crew_grp+'_'+csv_created+'.csv', 'w', newline='') as generic_bids_csv:
    outputWriter_generic = csv.DictWriter(generic_bids_csv, fieldnames=element_list_generic)
    outputWriter_generic.writeheader()

    for row in csvDReader:
        bid_type = row['a']
        pref_type = row['Pref Type']

        if bid_type == 'GEN_PAIRING':
            bt.BidTypes.create_generic_from_generic(row, outputWriter_generic)

        elif bid_type == 'SPEC_PAIRING':
            bt.BidTypes.create_generic_from_specific(row, outputWriter_generic)

        else:
            continue

# with open(newpath+'\gof_day_off_bids_'+crew_grp+'_'+csv_created+'.csv', 'w', newline='') as gof_day_off_bids_csv:
#     outputWriter_time_off = csv.DictWriter(gof_day_off_bids_csv, fieldnames=element_list_time_off)
#     outputWriter_time_off.writeheader()
#
#     for row in csvDReader:
#         bid_type = row['a']
#         pref_type = row['Pref Type']
#
#         if bid_type == 'GOLDEN_DO':
#             print('found gof')
#             bt.BidTypes.create_gof_from_golden(row, outputWriter_time_off)
#
#         elif bid_type == 'SPEC_DO':
#             print('found spec day')
#             bt.BidTypes.create_dayoff_from_spec_day_off(row,
#                                                         outputWriter_time_off)
#
#         elif bid_type == 'SPEC_TIMEOFF':
#             print('found spec time')
#             bt.BidTypes.create_timeoff_from_spec_timeoff(row, outputWriter_time_off)
#
#         elif bid_type == 'QUAL_TIMEOFF':
#             print('found qual time')
#             bt.BidTypes.create_timeoff_from_qual_timeoff(row, outputWriter_time_off)
#
#         else:
#             continue


# with open(newpath+'\\rule_relaxation_'+crew_grp+'_'+csv_created+'.csv', 'w', newline='') as rule_relax_csv:
#     outputWriter_rr = csv.DictWriter(rule_relax_csv, fieldnames=element_list_rule_relax)
#     outputWriter_rr.writeheader()
#
#     for row in csvDReader:
#         bid_type = row['a']
#
#         if bid_type == 'GROUP_DAYS':
#             bt.BidTypes.create_rr_from_rr(row, outputWriter_rr)
#
#         elif bid_type == 'WAIVE_WEEK':
#             bt.BidTypes.create_rr_from_rr(row, outputWriter_rr)
#
#         else:
#             continue
