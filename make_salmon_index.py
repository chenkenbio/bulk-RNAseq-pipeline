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
from biock import auto_open, run_bash
import logging
logger = logging.getLogger(__name__)


def get_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-fi", required=True, help="transcript fasta")
    p.add_argument('-i', '--index', help="directory to save index", required=True)
    p.add_argument("--decoys", required=False)
    p.add_argument("--gencode", action="store_true")
    p.add_argument("-k", type=int, default=31)
    p.add_argument('-t', "--threads", type=int, default=1, help="threads")
    # p.add_argument("-gtf", required=True)
    # p.add_argument('--seed', type=int, default=2020)
    p.add_argument("--salmon", default="salmon", help="path to salmon")
    return p

if __name__ == "__main__":
    args = get_args().parse_args()

    with auto_open(args.fi, 'rt') as infile:
        header = infile.readline()
        assert header[0] == '>'
        header = header[1:]
        if header.startswith("ENS") and '|' in header:
            if not args.gencode:
                logger.warning("--gencode is not set. while the input is likely gencode fasta")

        
    template = ' '.join([
        "{salmon} index", 
        "-t {tx_fa}", 
        "-i {index}",
        "-k {k}", 
        "--threads {threads}",
        "--gencode" if args.gencode else ""
    ])

    cmd = template.format(
        salmon=args.salmon,
        tx_fa=args.fi,
        index=args.index,
        decoys=args.decoys,
        k=args.k,
        threads=args.threads
    )
    if args.decoys is not None:
        cmd += " --decoys {decoys}".format(args.decoys)
    logger.info("- run {} ...".format(cmd))
    run_bash(cmd)