# pipelines.py

import os
from pathlib import Path
from .functions import (
    run_chopper,
    run_porechop,
    run_flye,
    run_pypolca,
    run_polypolish_filter,
    run_polypolish_polish,
    run_minimap2,
    run_tidk_find_telomeres
)

"""
PLACEHOLDER PIPELINE
"""

def fungal_genome_assembly_pipeline(
    sample_name: str,
    long_reads_bam: str,
    illumina_r1: str,
    illumina_r2: str,
    output_base_dir: str
):
    """
    Executes a fungal genome assembly pipeline starting from long-read BAM input.

    Arguments:
        sample_name (str): Sample name (e.g., 'S_aurantiacum').
        long_reads_bam (str): Path to a BAM file of long reads.
        illumina_r1 (str): Path to Illumina read 1.
        illumina_r2 (str): Path to Illumina read 2.
        output_base_dir (str): Base directory for all output.
    """
    # Setup output paths
    base_dir = Path(output_base_dir).resolve() / sample_name
    
    filtered_reads = os.sep.join([base_dir, "01_filtered_reads.fq"])
    assembly_dir = base_dir / "02_flye_assembly"
    polished_dir = base_dir / "03_polished"
    polypolish_output = base_dir / "04_polypolish.fasta"
    longread_map_sam = base_dir / "05_longread_map.sam"
    shortread_map_sam = base_dir / "06_shortread_map.sam"
    tidk_output_prefix = base_dir / "07_tidk_telomeres"

    # Create output directories
    base_dir.mkdir(parents=True, exist_ok=True)
    assembly_dir.mkdir(parents=True, exist_ok=True)
    polished_dir.mkdir(parents=True, exist_ok=True)
    
    # todo: Add read reformatting from .bam to fastq

    print(f"[{sample_name}]\tStep 1: Read filtering with chopper...")
    run_chopper(str(long_reads_bam), str(filtered_reads))  # Adjust chopper if input must be FASTQ

    print(f"[{sample_name}]\tStep 2: Genome assembly with Flye...")
    run_flye(str(filtered_reads), str(assembly_dir))

    assembled_fasta = assembly_dir / "assembly.fasta"

    print(f"[{sample_name}]\tStep 3: First polishing with PyPOLCA...")
    run_pypolca(str(assembled_fasta), str(illumina_r1), str(illumina_r2), str(polished_dir))

    polished_fasta = polished_dir / "pypolca_polished.fasta"

    print(f"[{sample_name}]\tStep 4: Second polishing with Polypolish...")
    bam_file = polished_dir / "reads.bam"  # Update if this needs to be created earlier
    #run_polypolish(str(polished_fasta), str(bam_file), str(polypolish_output))

    print(f"[{sample_name}]\tStep 5: Mapping reads with Minimap2...")
    run_minimap2("lr:hq", str(polypolish_output), str(filtered_reads), str(longread_map_sam))
    run_minimap2("sr", str(polypolish_output), str(illumina_r1), str(shortread_map_sam))

    print(f"[{sample_name}]\tStep 6: Telomere identification with TIDK...")
    run_tidk_find_telomeres(str(polypolish_output), str(tidk_output_prefix))

    print(f"[{sample_name}]\tAssembly pipeline complete.")
