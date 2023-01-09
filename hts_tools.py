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
import logging
logger = logging.getLogger(__name__)



fq_suffixes = [
    ".fq.gz",
    ".fastq.gz",
    ".fastq",
    ".fq",
]
def remove_fastq_suffix(fq: str) -> str:
    bn = None
    for suffix in fq_suffixes:
        if fq.endswith(suffix):
            bn = fq.replace(suffix, '')
            break
    if bn is None:
        logger.warning("failed to detect fastq suffix in \"{}\"".format(fq))
        bn = fq
    return bn

def get_paired_fastq_prefix(fq1: str, fq2: str) -> str:
    bn1 = os.path.basename(fq1)
    bn2 = os.path.basename(fq2)
    shift = 1
    while bn1[:shift] == bn2[:shift]:
        shift += 1
    prefix = bn1[:shift]
    return prefix