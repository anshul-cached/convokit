import os
import argparse
from do_train import do_train
# from tokenizer import tokenizer
import logging
logger = logging.getLogger(__name__)

def create_argparser():
    parser = argparse.ArgumentParser(description='train a custom language parser')
    parser.add_argument('-c', '--config', required=True,help="NLU configuration file")

    return parser


def init():  # pragma: no cover
    

    parser = create_argparser()
    args = parser.parse_args()
    
    return args.config




if __name__ == '__main__':
    args = init()
    # logging.basicConfig(level=config['log_level'])
    # print (type(args),args.config)
    do_train(args)
    logger.info("Finished training")    