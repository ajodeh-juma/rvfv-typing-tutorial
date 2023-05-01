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
                                dest="s_segment",
                                help="path to the lineages.csv report file for S segment"
                                )
    required_group.add_argument('--m', required=True,
                                dest="m_segment",
                                help="path to the lineages.csv report file for M segment"
                                )
    required_group.add_argument('--l', required=True,
                                dest="l_segment",
                                help="path to the lineages.csv report file for L segment"
                                )
    required_group.add_argument('--gn', required=True,
                                dest="gn_gene",
                                help="path to the lineages.csv report file for Gn glycoprotein gene"
                                )
    required_group.add_argument('--prefix', required=True, metavar='<str>',
                                dest="prefix",
                                help="prefix of the output file(s)"
                                )
    parser.add_argument('--outDir', metavar='<DIR>', dest="outdir", help="path to the output directory",
                        default=".")
    return parser


def merge_sequences_by_strain(metadata, s_segment, m_segment, l_segment, gn_gene, prefix, outdir):
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
    print(meta_df)
    # m_df = read_metadata(m_segment[0])
    # l_df = read_metadata(l_segment[0])
    #
    # # merge dataframes and create a dictionary
    # df1 = l_df.merge(m_df, on='strain')
    # df2 = df1.merge(s_df, on="strain")
    # df3 = df2[['strain', 'accession_x', 'accession_y', 'accession', 'country', 'location', 'host', 'date']]
    # df3.date = df3.date.str.split('-').str[2]
    # df3['strain'].replace(to_replace="[^0-9a-zA-Z]+", value= "_", regex=True, inplace=True)
    # df3['taxa'] = df3.strain.str.cat(df3.date, "|")
    # df4 = df3.rename(columns={'accession_x': 'L', 'accession_y': 'M', 'accession': 'S'})
    # df_dict = df4.set_index('strain').T.to_dict('list')
    #
    #
    #
    # l_dict = seq_dict(l_segment[0])
    # m_dict = seq_dict(m_segment[0])
    # s_dict = seq_dict(s_segment[0])
    #
    #
    # # # merge dicts
    # fasta_dict = {**l_dict, **m_dict, **s_dict}
    #
    #
    # f_dict = dict()
    #
    # for k, v in df_dict.items():
    #     if l_dict.get(v[0]) is None:
    #         continue
    #     else:
    #         accession = k + '|' + v[6]
    #         seq = l_dict.get(v[0])
    #         if not accession in f_dict:
    #             f_dict[accession] = seq
    #
    # for k, v in df_dict.items():
    #     if m_dict.get(v[1]) is None:
    #         continue
    #     else:
    #         accession = k + '|' + v[6]
    #         seq = m_dict.get(v[1])
    #         if accession in f_dict:
    #             f_dict[accession] += seq
    #
    #
    # for k, v in df_dict.items():
    #     if s_dict.get(v[2]) is None:
    #         continue
    #     else:
    #         accession = k + '|' + v[6]
    #         seq = s_dict.get(v[2])
    #         if accession in f_dict:
    #             f_dict[accession] += seq
    #
    #
    #
    # df4.to_csv(out_file, index=False)
    #
    # with open(out_fasta, 'w') as f_obj:
    #     for k, v in f_dict.items():
    #         print(k, len(v))
    #         # strain = re.sub('[^0-9a-zA-Z]+', '_', k)
    #         f_obj.write(">" + k + "\n")
    #         f_obj.write(textwrap.fill(v, 80))
    #         f_obj.write("\n")
    #
    # logging.info("output files:\ncsv -> {}\nfasta -> {}".format(out_file, out_fasta))
    return out_file


def read_metadata(metadata):
    """
    :@param metadata
    """
    df = pd.read_csv(metadata, sep=",")
    return df


def main():
    parser = parse_args()
    args = parser.parse_args()
    merge_sequences_by_strain(metadata=args.metadata,
                              s_segment=args.s_segment,
                              m_segment=args.m_segment,
                              l_segment=args.l_segment,
                              gn_gene=args.gn_gene,
                              prefix=args.prefix,
                              outdir=args.outdir)


if __name__ == '__main__':
    main()
