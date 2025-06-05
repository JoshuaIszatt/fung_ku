# pipelines.py

from pathlib import Path
from functions import (
    run_dorado,
    run_chopper,
    run_flye,
    run_pypolca,
    run_polypolish,
    run_minimap2,
    run_tidk_find_telomeres
)

def fungal_genome_assembly_pipeline(
    sample_name: str,
    raw_data_dir: str,
    dorado_model: str,
    illumina_r1: str,
    illumina_r2: str,
    output_base_dir: str
):
    """
    Executes a full fungal genome assembly pipeline for a given sample.

    Arguments:
        sample_name (str): Sample name (e.g., 'S_aurantiacum').
        raw_data_dir (str): Directory containing raw Nanopore data.
        dorado_model (str): Path to the dorado model.
        illumina_r1 (str): Path to Illumina read 1.
        illumina_r2 (str): Path to Illumina read 2.
        output_base_dir (str): Base directory for all output.
    """

    # Setup output paths using pathlib
    base_dir = Path(output_base_dir) / sample_name
    basecall_dir = base_dir / "01_basecall"
    filtered_reads = base_dir / "02_filtered_reads.fq"
    assembly_dir = base_dir / "03_flye_assembly"
    polished_dir = base_dir / "04_polished"
    polypolish_output = base_dir / "05_polypolish.fasta"
    longread_map_sam = base_dir / "06_longread_map.sam"
    shortread_map_sam = base_dir / "07_shortread_map.sam"
    tidk_output_prefix = base_dir / "08_tidk_telomeres"

    # Create output directories
    basecall_dir.mkdir(parents=True, exist_ok=True)
    assembly_dir.mkdir(parents=True, exist_ok=True)
    polished_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{sample_name}]\tStep 1: Basecalling with dorado...")
    run_dorado(dorado_model, str(raw_data_dir), str(basecall_dir))

    print(f"[{sample_name}]\tStep 2: Read filtering with chopper...")
    basecalled_reads = basecall_dir / "basecalls.fq"
    run_chopper(str(basecalled_reads), str(filtered_reads))

    print(f"[{sample_name}]\tStep 3: Genome assembly with Flye...")
    run_flye(str(filtered_reads), str(assembly_dir))

    assembled_fasta = assembly_dir / "assembly.fasta"

    print(f"[{sample_name}]\tStep 4: First polishing with PyPOLCA...")
    run_pypolca(str(assembled_fasta), str(illumina_r1), str(illumina_r2), str(polished_dir))

    polished_fasta = polished_dir / "pypolca_polished.fasta"

    print(f"[{sample_name}]\tStep 5: Second polishing with Polypolish...")
    bam_file = polished_dir / "reads.bam"
    run_polypolish(str(polished_fasta), str(bam_file), str(polypolish_output))

    print(f"[{sample_name}]\tStep 6: Mapping reads with Minimap2...")
    run_minimap2("lr:hq", str(polypolish_output), str(filtered_reads), str(longread_map_sam))
    run_minimap2("sr", str(polypolish_output), str(illumina_r1), str(shortread_map_sam))

    print(f"[{sample_name}]\tStep 7: Telomere identification with TIDK...")
    run_tidk_find_telomeres(str(polypolish_output), str(tidk_output_prefix))

    print(f"[{sample_name}]\tAssembly pipeline complete.")
