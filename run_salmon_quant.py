#!/usr/bin/env python3
"""
Author: Ken Chen
Email: chenkenbio@gmail.com
Date: 2023-01-10
"""

import argparse
import os
import sys
import numpy as np
from biock import make_logger, make_directory, get_run_info, run_bash
from hts_tools import remove_fastq_suffix
import logging
logger = logging.getLogger(__name__)



def get_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-fq1", "--fastq1", required=True)
    p.add_argument("-fq2", "--fastq2", required=False, help="paired end")
    p.add_argument('--run-name', required=False)
    p.add_argument("-i", "--index", required=True, help="/path/to/salmon/index/directory")
    p.add_argument("-o", "--outdir", required=True)
    p.add_argument("-t", "--threads", type=int, default=4)

    p.add_argument("--salmon", default="salmon", help="path to salmon")
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
    logger = make_logger(filename="{}/pipeline.salmon-quant.{}.log".format(args.outdir, bn))
    logger.info("{}".format(get_run_info(sys.argv, args)))


    template = ' '.join([
        "{salmon} quant",
        "-i {index}",
        "-l A",
        "-1 {fastq1}" if args.fastq2 is not None else "-r {fastq1}",
        "-2 {fastq2}" if args.fastq2 is not None else "",
        "-p {threads}",
        "--validateMappings",
        "-o {output}"
    ])
    opts = {
        "salmon": args.salmon,
        "output": args.outdir,
        "index": args.index,
        "fastq1": args.fastq1,
        "threads": args.threads,
        "output": args.outdir
    }
    if args.fastq2 is not None:
        logger.info("PE mode")
        opts["fastq2"] = args.fastq2
    else:
        logger.info("SE mode")
    
    cmd = template.format(**opts)
    logger.info("- run {} ...".format(cmd))

    rc, out, err = run_bash(cmd)

    if rc == 0:
        if len(out) > 0:
            logger.info(out)
        logger.info("Finished!")
    else:
        logger.error(err)
        logger.info("Failed for {}".format(args.run_name))


