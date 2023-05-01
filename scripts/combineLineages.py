#!/usr/bin/env python3
"""
combine lineage assignment outputs from all classifiers

usage: python combineLineages.py --metadata <metadata file> --s <small segment lineages report> --m <medium segment
lineages report>  --l <large segment lineages report> --gn <glycoprotein gene lineages report> --prefix <str>
--outDir <path> """

import os
import re
import sys
import logging
import argparse
import textwrap
import functools
from textwrap import dedent

import pandas as pd

from utils import mkdir
from utils import fasta_iterator

log_level = logging.DEBUG
logging.basicConfig(level=log_level, format='[%(asctime)s] - %(''levelname)s - [%(funcName)s] - %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')


def parse_args():
    # arguments parser
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS, prefix_chars='--',
        description=dedent(__doc__)
    )

    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument('--metadata', required=True, type=str,
                                dest="metadata",
                                help="path to the sequences metadata file. The file should have the columns 'strain, "
                                     "L, M, S, country, location. host, date "
                                )
    required_group.add_argument('--s', required=True, type=str,
                                dest="s_lineage",
                                help="path to the lineages.csv report file for S segment"
                                )
    required_group.add_argument('--m', required=True,
                                dest="m_lineage",
                                help="path to the lineages.csv report file for M segment"
                                )
    required_group.add_argument('--l', required=True,
                                dest="l_lineage",
                                help="path to the lineages.csv report file for L segment"
                                )
    required_group.add_argument('--gn', required=True,
                                dest="gn_lineage",
                                help="path to the lineages.csv report file for Gn glycoprotein gene"
                                )
    required_group.add_argument('--prefix', required=True, metavar='<str>',
                                dest="prefix",
                                help="prefix of the output file(s)"
                                )
    parser.add_argument('--outDir', metavar='<DIR>', dest="outdir", help="path to the output directory",
                        default=".")
    return parser


def merge_sequences_by_strain(metadata, s_lineage, m_lineage, l_lineage, gn_lineage, prefix, outdir):
    """
    search and download complete rift valley fever virus sequences from NCBI

    :@param s_segment
    :@param m_segment
    :@param l_segment
    :@param gn_gene
    :@param: prefix
    :param outdir:
    :return:
    """

    # create output directory if not exists
    outdir = os.path.abspath(outdir)
    mkdir(outdir)

    out_file = os.path.join(outdir, prefix) + '.combined.lineages.csv'

    meta_df = read_metadata(metadata)

    l_df = read_lineages(l_lineage)
    m_df = read_lineages(m_lineage)
    s_df = read_lineages(s_lineage)
    gn_df = read_lineages(gn_lineage)

    df1 = pd.merge(meta_df, l_df, left_on="L", right_on="Query").rename(columns={'Query': 'L-query', 'Lineage': 'L-lineage', 'UFbootstrap': 'L-UFb'}).drop(['Year_first', 'Year_last'], axis=1)
    df2 = pd.merge(df1, m_df, left_on="M", right_on="Query").rename(columns={'Query': 'M-query', 'Lineage': 'M-lineage', 'UFbootstrap': 'M-UFb'}).drop(['Year_first', 'Year_last'], axis=1)
    df3 = pd.merge(df2, s_df, left_on="S", right_on="Query").rename(columns={'Query': 'S-query', 'Lineage': 'S-lineage', 'UFbootstrap': 'S-UFb'}).drop(['Year_first', 'Year_last'], axis=1)
    df4 = pd.merge(df3, gn_df, left_on="M", right_on="Query").rename(columns={'Query': 'Gn-query', 'Lineage': 'Gn-lineage', 'UFbootstrap': 'Gn-UFb'}).drop(['L-query', 'M-query', 'S-query', 'Gn-query'], axis=1)

    print(df4)

    df4.to_csv(out_file, index=False)
    return out_file


def read_metadata(metadata):
    """
    :@param metadata
    """
    df = pd.read_csv(metadata, sep=",")
    df = df.drop(['taxa'], axis=1)
    return df


def read_lineages(lineage):
    """
    :@param lineage
    """
    df = pd.read_csv(lineage, sep=",")
    df = df[['Query', 'Lineage', 'UFbootstrap', 'Year_first', 'Year_last']]
    return df


def main():
    parser = parse_args()
    args = parser.parse_args()
    merge_sequences_by_strain(metadata=args.metadata,
                              s_lineage=args.s_lineage,
                              m_lineage=args.m_lineage,
                              l_lineage=args.l_lineage,
                              gn_lineage=args.gn_lineage,
                              prefix=args.prefix,
                              outdir=args.outdir)


if __name__ == '__main__':
    main()
