from pandas import DataFrame, Series
import os

class BlastOutParser(object):
    

    def __init__(self, db_name, e_value_thr= 1e-5, 
            perc_id_thr= 60, min_overlap= 10, keep_reads= False ):
        self.db_name= db_name

        self.e_value_thr= e_value_thr
        self.perc_id_thr = perc_id_thr
        self.min_overlap= min_overlap
        self.keep_reads = keep_reads
    

    def parse(self, tabular_blast_output_path):
        """
            assumes that each blast output file represents a sample.
        """

        dbID_reads = {}
        
        with open(tabular_blast_output_path) as b_out:

            #function_reads= {}
            for line in b_out:
                cols = line.rstrip('\n').split('\t')
                read = cols[0].strip()
                db_id = cols[1].split('.')[0].strip()
                
                perc_id = cols[2].strip()
                alignment_length= cols[3].strip()
                e_value = cols[10].strip()

                ### filtering

                if float(e_value) > self.e_value_thr or \
                        float(perc_id) < self.perc_id_thr or \
                        float(alignment_length) < self.min_overlap:
                    continue


                if db_id not in dbID_reads:
                    dbID_reads[db_id]= []
                dbID_reads[db_id].append(read)
            
            dbID_counts= { k: len(v) for k,v in dbID_reads.iteritems() }
            s_counts= Series(dbID_counts)
            return dbID_reads, dbID_counts, s_counts


    def parse_many(self, tabular_blast_output_paths):
        """
            parses a list of blast output files and returns
            the count dataframe.

            assumes that the file_paths hint at the sample names.
            characters before the first occurence of a '.' (dot) 
            character are accepted as the sample name.
        """
        sample_s_counts= {}
        tmp_dfs=[]
        for file_path in tabular_blast_output_paths:
            sample_name= os.path.basename(file_path).split('.')[0]
            s_counts= self.parse(file_path)[2]
            tmp_dfs.append(DataFrame(s_counts, columns=[sample_name]))

        df= tmp_dfs[0].join(tmp_dfs[1:], how= "outer").fillna(0)
        df.index.name= "Name"
        cols= sorted(df.columns.tolist())
        df= df[cols]
        return df

    
