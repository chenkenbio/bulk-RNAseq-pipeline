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

from hts_tools import (
    remove_fastq_suffix, get_paired_fastq_prefix
)


def get_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-fq1", "--fastq1", required=True)
    p.add_argument("-fq2", "--fastq2", required=False, help="paired end")
    p.add_argument('--run-name', required=False)
    p.add_argument("-o", "--outdir", required=True)
    p.add_argument("-t", "--threads", type=int, default=4)
    # p.add_argument('--seed', type=int, default=2020)
    return p


if __name__ == "__main__":
    args = get_args().parse_args()

    if args.run_name is not None:
        bn = args.run_name
    else:
        bn = remove_fastq_suffix(args.fastq1, args.fastq2)
        if len(bn) == 0:
            assert args.run_name is not None, "{} and {} have no common prefix, --run-name should be provided".format(args.fastq1, args.fastq2)

    args.outdir = make_directory(args.outdir)
    logger = make_logger(filename="{}/pipeline.fastp.{}.log".format(args.outdir, bn))
    logger.info("{}".format(get_run_info(sys.argv, args)))

    prefix = "{}/{}".format(args.outdir, bn)
    if args.fastq2 is None:
        logger.info("SE mode")
        template = ' '.join([
            "fastp", 
            "-i {fastq1}", 
            "-o {prefix}.fastp.fq.gz",
            "--html {prefix}.fastp.html",
            "--json {prefix}.fastp.json",
            "-t {threads}",
            "&> {prefix}.fastp.log"])
        cmd = template.format(
            fastq1=args.fastq1,
            prefix=prefix,
            threads=args.threads
        )

    else:
        logger.info("PE mode")
        template = ' '.join([
            "fastp", 
            "-i {fastq1}", "-I {fastq2}",
            "-o {prefix}.R1.fastp.fq.gz", "-O {prefix}.R2.fastp.fq.gz",
            "--unpaired1 {prefix}.R1.fastp.unpaired.fq.gz",
            "--unpaired2 {prefix}.R2.fastp.unpaired.fq.gz",
            "--html {prefix}.fastp.html",
            "--json {prefix}.fastp.json",
            "-t {threads}",
            "&> {prefix}.fastp.log"])
        cmd = template.format(
            fastq1=args.fastq1,
            fastq2=args.fastq2,
            prefix=prefix,
            threads=args.threads
        )



    logger.info("- run command: {} ...".format(cmd))
    
    rc, out, err = run_bash(cmd)

    if rc != 0:
        logger.error("Failed: {}".format(err))
    else:
        if len(out)> 0:
            logger.info(out)
        logger.info("Finished")
