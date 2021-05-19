"""
Generate a random training, dev, and test split that have the same distribution of library type
Ensure that barcodes are not shared between the training, dev, and test set
Remove examples for which splicing efficiency is nan

Example usage: python make_train_dev_test_split.py ../data/splicing_data.csv ../data/train_dev_test/
"""
import pandas as pd
import random
import sys

TRAIN_FRAC = 0.9
DEV_FRAC = 0.05
TEST_FRAC = 1 - TRAIN_FRAC - DEV_FRAC

all_data_filename = sys.argv[1]
train_dev_test_dir = sys.argv[2]

df = pd.read_csv(all_data_filename)

library_types = df.type.unique()

train_df = pd.DataFrame(columns=df.columns)
dev_df = pd.DataFrame(columns=df.columns)
test_df = pd.DataFrame(columns=df.columns)

for library in library_types:
	library_df = df.loc[df['type'] == library]
	barcodes = library_df.barcode.unique()
	random.shuffle(barcodes)
	train_end = int(TRAIN_FRAC*len(barcodes))
	dev_end = train_end + int(DEV_FRAC*len(barcodes))

	train_barcodes = barcodes[0:train_end]
	dev_barcodes = barcodes[train_end:dev_end]
	test_barcodes = barcodes[dev_end:]

	library_df = library_df[library_df['splicing_eff'].notna()]

	train_library_df = library_df.loc[df['barcode'].isin(train_barcodes)]
	dev_library_df = library_df.loc[df['barcode'].isin(dev_barcodes)]
	test_library_df = library_df.loc[df['barcode'].isin(test_barcodes)]

	train_df = train_df.append(train_library_df)
	dev_df = dev_df.append(dev_library_df)
	test_df = test_df.append(test_library_df)

train_df.to_csv(train_dev_test_dir + "train.csv")
dev_df.to_csv(train_dev_test_dir + "dev.csv")
test_df.to_csv(train_dev_test_dir + "test.csv")
