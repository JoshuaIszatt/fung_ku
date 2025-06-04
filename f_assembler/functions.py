import subprocess

def run_dorado(model, input_dir, output_dir):
    command = [
        'dorado',
        'basecaller',
        '--model', model,
        input_dir,
        '--output', output_dir
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e

def run_chopper(input_reads, output_reads):
    command = [
        'chopper',
        '-i', input_reads,
        '-o', output_reads,
        '--min-length', '3000',
        '--min-quality', '20'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e

def run_flye(input_reads, output_dir):
    command = [
        'flye',
        '--nano-raw', input_reads,
        '--out-dir', output_dir,
        '--scaffold',
        '--asm-coverage', '50'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e

def run_pypolca(assembly_fasta, illumina_R1, illumina_R2, output_dir):
    command = [
        'pypolca',
        '--reference', assembly_fasta,
        '--reads', illumina_R1, illumina_R2,
        '--output', output_dir,
        '--careful'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise e

def run_polypolish(assembly_fasta, bam_file, output_fasta):
    command = [
        'polypolish',
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
