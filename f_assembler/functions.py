import sys
import subprocess
from deprecated import deprecated

def what_am_i():
    print("Assembly module")
    
def collect_samples(directory: str='./', extensions: list=['.fastq', '.fastq.gz', 'bam']):
    """_summary_

    Args:
        directory (str, optional): _description_. Defaults to './'.
        extensions (list, optional): _description_. Defaults to ['.fastq', '.fastq.gz', 'bam'].
    """
    pass

def convert_bam_to_fastq(bam_file, output_file):
    """_summary_

    Args:
        bam_file (_type_): _description_
        output_file (_type_): _description_

    Raises:
        Exception: _description_
    """
    command = [
        'reformat.sh',
        f'in={bam_file}',
        f'out={output_file}'
    ]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        raise Exception(f"BAM to FQ conversion failed: {e}")
    
def run_chopper(input_reads: str, output_reads: str, minlen=3000, minqual=10):
    assert isinstance(input_reads, str), f"expected path to be a string: {input_reads}"
    command = [
        'chopper',
        '-i', input_reads,
        '--minlength', str(minlen),
        '--quality', str(minqual)
    ]
    try:
        with open(output_reads, "w") as outfile:
            subprocess.run(command, check=True, stdout=outfile)
    except subprocess.CalledProcessError as e:
        raise e

# Use sys here to stream the output
def run_flye(input_reads, output_dir, asm_cov=50, g_size=40000000, threads=10):
    command = [
        'flye',
        '--nano-hq', input_reads,
        '--out-dir', output_dir,
        '--scaffold',
        '--asm-coverage', str(asm_cov),
        '--genome-size', str(g_size),
        '-t', str(threads)
    ]
    try:
        subprocess.run(command, check=True, stderr=sys.stderr, stdout=sys.stdout)
    except subprocess.CalledProcessError as e:
        raise e

@deprecated(reason='Heavy on memory and is technically abandonware so no fixes!')
def run_porechop(input_reads: str, output_reads: str, multiplex: bool =True):
    assert isinstance(input_reads, str)
    assert isinstance(output_reads, str)
    assert isinstance(multiplex, bool)
    command = [
        'porechop', 
        '-i', input_reads,
        '-o', output_reads
    ]
    if multiplex:
        command.append('--discard_middle')
    try:
        subprocess.run(command, check=True, stderr=sys.stderr, stdout=sys.stdout)
    except subprocess.CalledProcessError as e:
        raise e

#porechop_abi -abi -i input_reads.fastq -o output_reads.fastq
def run_porechop_abi(input_reads: str, output_reads: str, threads: int =8):
    assert isinstance(input_reads, str)
    assert isinstance(output_reads, str)
    command = [
        'porechop_abi', '-abi',
        '-i', input_reads,
        '-o', output_reads,
        '-t', str(threads)
    ]
    try:
        subprocess.run(command, check=True, stderr=sys.stderr, stdout=sys.stdout)
    except subprocess.CalledProcessError as e:
        raise e

def run_pypolca(assembly_fasta, illumina_R1, illumina_R2, output_dir, threads=10):
    command = [
        'pypolca run',
        '-a', assembly_fasta,
        '-1', illumina_R1, 
        '-2', illumina_R2,
        '-t', str(threads),
        '-o', output_dir,
        '--careful'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e
    
# Need to obtain pypolca polishing
# Then need to run indexing, then alignment, then clean up:
    ## bwa index draft.fasta
    ## bwa mem -t 16 -a draft.fasta reads_1.fastq.gz > alignments_1.sam
    ## rm *.amb *.ann *.bwt *.pac *.sa *.sam

def run_polypolish_filter():
    pass

def run_polypolish_polish(assembly_fasta, bam_file, output_fasta):
    command = [
        'polypolish polish',
        assembly_fasta, 
        bam_file
    ]
    try:
        with open(output_fasta, 'w') as f:
            subprocess.run(command, check=True, stdout=f)
    except subprocess.CalledProcessError as e:
        raise e

def run_minimap2(preset, reference_fasta, reads, output_sam):
    command = [
        'minimap2',
        '-x', preset,
        reference_fasta,
        reads
    ]
    try:
        with open(output_sam, 'w') as f:
            subprocess.run(command, check=True, stdout=f)
    except subprocess.CalledProcessError as e:
        raise e

def run_tidk_find_telomeres(input_fasta, output_prefix):
    command = [
        'tidk',
        'find_telomeres',
        '-i', input_fasta,
        '-o', output_prefix,
        '--motif', 'AACCCT'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e
