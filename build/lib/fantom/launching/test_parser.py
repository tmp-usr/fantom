from blast_out_parser import BlastOutParser
import glob

def test_blast_out_parser():
    b= BlastOutParser('kegg')
    bOuts= glob.glob('/Users/kemal/phd/projects/periphyton/preprocess/alignment/blast/blastp/pp_full_run/*')
    df = b.parse_many(bOuts)
    return df

df= test_blast_out_parser()

