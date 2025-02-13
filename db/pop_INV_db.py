'''
Populate mycovir DB with SRA blastrps and blastx results
Eden Darnige
March 2020
'''

import uuid
import csv
import glob
import os
import datetime
from pymongo import MongoClient

mongo_client = MongoClient(port=27017)
db = mongo_client.test #test is name of db
col = db['virData_app_entry'] #collection
#db.virData_app_entry.drop() #only drop if resetting!!!




##########
# INVICEB
##########


#RPSBLAST
def INV_rpsblast():
    rps_header = ['query_id', 'query_length', 'cdd_id', 'hit_id', 'evalue', 'startQ', 'endQ', 
        'frame', 'description', 'superkingdom', 'no_rank', 'family','genus','project']
    rps_int = ['query_length', 'startQ', 'endQ', 'frame']
    rps_folat = ['evalue']

    rps_path = os.getcwd() + "/I*pfam.csv" 

    for fname in glob.glob(rps_path):
        rps_file = open(fname,'r')
        rps_reader = csv.DictReader(rps_file, fieldnames=rps_header, delimiter='\t') 
        next(rps_reader) #skip header

        for entry in rps_reader:
            row ={}
            blastrps={}
            
            entry_id = uuid.uuid4() #PK for entry!!!
            
            hit = entry['query_length'] #store no hit val
            
            if hit != 'no_hit':
                sample = entry['query_id'].split('_')[0] + '_' + entry['project'] #sample to tie metadata to 

                #Fields not embedded
                row['entry_id']=entry_id
                row['sample'] = sample
                row['query_id']=entry['query_id'] 
                row['verified']=False
                row['host_organism']=''
                row['virus_type']=''
            else:
                print('no hit',entry['query_id'])

            for field in rps_header[1:13]: #skip query_id and project
                if hit != 'no_hit':
                    if field in rps_int:
                        blastrps[field]=int(entry[field].replace('.0', ''))
                    elif field in rps_folat:
                        blastrps[field]=float(entry[field])
                    else:
                        blastrps[field]=entry[field]
            row['blastrps'] = blastrps

            db.virData_app_entry.insert_one(row)

        rps_file.close()



#BLASTX
def INV_blastx():
    blastx_header = ['algo', 'query_id', 'nb_reads', 'query_length', 'accession', 'description', 
        'organism', 'percent_identity', 'nb_hsps', 'query_overlap', 'hit_overlap', 'evalue', 
        'score', 'tax_id', 'taxonomy', 'sequence']
    blastx_int = ['nb_hsps', 'query_overlap','nb_reads','query_length','hit_overlap','tax_id']
    blastx_float = ['percent_identity','evalue','score']

    blastx_path = os.getcwd() + "/I*rps2blast.csv"

    for fname in glob.glob(blastx_path):
        blastx_file = open(fname, 'r')
        blastx_reader = csv.DictReader(blastx_file, fieldnames=blastx_header, delimiter="\t")
        next(blastx_reader)

        for entry in blastx_reader:
            blastx = {}
            qid=entry['query_id']
            blastx['taxonomy'] = ''
            for field in blastx_header[2:]: #skip query id but need algo
                if field in blastx_int and entry['accession'] !=  '':
                    blastx[field]=int(entry[field])
                elif field in blastx_float and entry['accession'] !=  '':
                    blastx[field]=float(entry[field])
                elif field == 'sequence' and entry['sequence'] != '': #remove seq if not using
                    blastx['sequence']=entry['sequence'].upper()
                elif entry[field] != '':
                    blastx[field]=entry[field]
            blastx['algo']=entry['algo']

            db.virData_app_entry.update_many({'query_id': qid},{'$set':{'blastx':blastx}}, upsert=True) #multiple rps can have same query_id
        blastx_file.close()


def INV_meta():
    meta_header = ['sample_id','project','grapevine_cultivar','rootstock','plantation_year','location','substrate','extraction_method','organ',
        'mid_sequence','mid_id','run_name','technology','run_id','date','seq_location', 'rna']

    meta_path = os.getcwd() + "/INV_meta.csv"

    for fname in glob.glob(meta_path):
        meta_file = open(fname, 'r')
        meta_reader = csv.DictReader(meta_file, fieldnames=meta_header, delimiter=",")
        next(meta_reader)

        for entry in meta_reader:
            meta = {}
            sample = entry['sample_id']
            
            for field in meta_header[1:]: #skip run, = sample 
                if field == 'date' and entry[field] != '':
                    date_time_str = entry[field]
                    #6/1/16
                    date_time_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%y')  
                    meta[field] = date_time_obj
                else: 
                    meta[field]=entry[field]
            
            db.virData_app_entry.update_many({'sample': sample},{'$set':{'inv_metadata':meta}}, upsert=True) #many with same sample

        meta_file.close()


##########
# MAIN
##########

#Check if entry already exists and update instead of create new? 
#rpsblast must be entered first
#except not true foe inv... opposite with new format


# INV_rpsblast()
# print("INV rps done")
# INV_blastx()
# print("INV blastx done")
# INV_meta()
# print("INV meta done")
# print("INV done")

# print("count before removing w/o entries", db.virData_app_entry.find().count())

#Remove entries with entry_ids (had diamond, no rps)
# db.virData_app_entry.remove({'entry_id':{'$exists':'false'}})
# print("count after removing w/o entries", db.virData_app_entry.find().count())

#INDEXING
# db.virData_app_entry.createIndex({ "blastrps.evalue": 1 })
# db.virData_app_entry.createIndex({ "blastx.query_length": -1 })
# db.virData_app_entry.createIndex({ "blastx.percent_identity": -1 })
# print("Indexing done")
