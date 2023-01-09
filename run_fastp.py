#!/usr/bin/env python3
"""
Author: Ken Chen
Email: chenkenbio@gmail.com
Date: 2023-01-09
"""

import argparse
import os
import sys
import numpy as np
from biock import run_bash, make_logger, get_run_info, make_directory

from rnaseq_tools import (
    remove_fastq_suffix
)


def get_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-fq1", "--fastq1", required=True)
    p.add_argument("-fq1", "--fastq1", required=False, help="paired end")
    p.add_argument("-o", "--outdir", required=True)
    p.add_argument("-t", "--threads", type=int, default=4)
    # p.add_argument('--seed', type=int, default=2020)
    return p


if __name__ == "__main__":
    args = get_args().parse_args()

    logger = make_logger()
    logger.info("{}".format(get_run_info(sys.argv, args)))
    args.outdir = make_directory(args.outdir)

    prefix = "{}/{}".format(
        args.outdir,
        remove_fastq_suffix(os.path.basename( args.fastq1))
    )

    template = "fastp -i {fastq1} -o {prefix}.fastp.fq.gz --html {prefix}.fastp.html --json {prefix}.fastp.json -t {threads} &> {prefix}.fastp.log"
    cmd = template.format(
        fastq1=args.fastq1,
        prefix=prefix,
        threads=args.threads
    )
    logger.info("- {}".format(cmd))
    
    rc, out, err = run_bash(cmd)

    # rc, out, err = run_bash(cmd.format(
    #     fastq1=args.fastq1,
    #     prefix=prefix,
    #     threads=args.threads
    # ))
    if rc != 0:
        logger.error("Failed: {}".format(err))
    else:
        if len(out)> 0:
            logger.info(out)
        logger.info("Finished")
