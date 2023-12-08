from os import PathLike
from sklearn import metrics
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors

import pandas as pd
import numpy as np
import itertools
import random
import copy
import swifter


def return_basic_info(dataset, num_bucket=10, num2cat_threshold=1):
    attr_name = dataset.keys().tolist()
    attr_basic_info = {}

    for attr in attr_name:
        attr_basic_info[attr] = {}
        name_v = dataset[attr].value_counts().index.tolist()
        max_v = len(name_v)

        if max_v <= 1:
            attr_basic_info[attr]["type"] = "single"
            del name_v, max_v
            continue

        if (
            dataset[attr].dtypes == "int64" or dataset[attr].dtypes == "int"
        ) or (
            dataset[attr].dtypes == "float64"
            or dataset[attr].dtypes == "float"
        ):
            if max_v <= num2cat_threshold:
                attr_basic_info[attr]["type"] = "num2cat"

            else:
                attr_basic_info[attr]["type"] = "num"
                bucket_size = (max(name_v) - min(name_v)) / num_bucket
                bucket = []
                tmp_value = min(name_v) + bucket_size
                bucket.append([min(name_v), tmp_value])

                for _ in range(num_bucket - 2):
                    bucket.append([tmp_value, tmp_value + bucket_size])
                    tmp_value += bucket_size

                bucket.append([tmp_value, max(name_v) + (1.0e-9)])
                attr_basic_info[attr]["bucket"] = bucket
                del bucket_size, tmp_value, bucket

        else:
            attr_basic_info[attr]["type"] = "cat"

    return attr_basic_info, attr_name


def value_dispatch(v, conditions):
    v_tag = 0

    if (
        (conditions[0][0] == conditions[0][1]) and (v == conditions[0][1])
    ) or (v < conditions[0][1]):
        return v_tag

    v_tag = 1
    distance = v - conditions[0][1]

    for condition in conditions[1:]:
        if v >= condition[0]:
            if ((condition[0] == condition[1]) and (v == condition[0])) or (
                v < condition[1]
            ):
                return v_tag

            else:
                v_tag += 1
                distance = v - condition[1]

        elif (condition[0] - v) > distance:
            return v_tag - 1

        else:
            return v_tag

    return v_tag - 1


def preprocess(dataset, attr_basic_info):
    raw_data = dataset

    attr_name = raw_data.keys().tolist()
    attr_info_max = {}
    specs_mapping = {}
    specs_mapping["single_attr"] = {}

    for attr in attr_name:
        attr_info_max[attr] = {}
        specs_mapping[attr] = {}
        if attr_basic_info[attr]["type"] == "num":
            if (
                raw_data[attr].dtypes == "int64"
                or raw_data[attr].dtypes == "int"
            ):
                specs_mapping[attr]["num-type"] = "int"
            else:
                specs_mapping[attr]["num-type"] = "float"
            conditions = copy.deepcopy(attr_basic_info[attr]["bucket"])
            raw_data[attr] = raw_data[attr].swifter.apply(
                value_dispatch, args=(conditions,)
            )
            attr_info_max[attr]["max"] = (
                len(attr_basic_info[attr]["bucket"]) - 1
            )
            specs_mapping[attr]["optional"] = 0

        elif (attr_basic_info[attr]["type"] == "cat") or (
            attr_basic_info[attr]["type"] == "num2cat"
        ):
            specs_mapping[attr]["dict"] = {}
            name_v = raw_data[attr].value_counts().index.tolist()
            max_v = len(name_v)
            specs_mapping[attr]["count"] = max_v
            attr_info_max[attr]["max"] = max_v - 1
            specs_mapping[attr]["optional"] = 0
            float_v = False
            if (
                raw_data[attr].dtypes == "float64"
                or raw_data[attr].dtypes == "float"
            ):
                float_v = True
            raw_data[attr] = raw_data[attr].astype("str")
            name_v = raw_data[attr].value_counts().index.tolist()
            max_v = len(name_v)
            name_v.sort()
            for idx in range(max_v):
                raw_data[attr].replace(name_v[idx], idx, inplace=True)
                specs_mapping[attr]["dict"][str(idx)] = name_v[idx]
            if (attr_basic_info[attr]["type"] == "num2cat") and float_v:
                raw_data[attr] = raw_data[attr].astype("float")
            raw_data[attr] = raw_data[attr].astype("int")
            del name_v, max_v

        else:
            if len(raw_data[attr].value_counts().index.tolist()) == 0:
                specs_mapping["single_attr"][attr] = np.nan
            else:
                specs_mapping["single_attr"][attr] = (
                    raw_data[attr].value_counts().index.tolist()[0]
                )
            del raw_data[attr], attr_info_max[attr]

    del attr_name, specs_mapping
    return raw_data, attr_info_max


def build_zero_table(attr_info, attr_name):
    attr_sizes = []
    for element in attr_name:
        attr_sizes.append(range(attr_info[element]["max"] + 1))

    attr_sizes_extend = list(itertools.product(*attr_sizes))

    marginal_table = {}
    marginal_table = {ele: 0 for ele in attr_sizes_extend}
    del attr_sizes_extend
    return marginal_table


def empirical_counting_single(raw_data, attr_name, zero_table):
    tmp_dict = copy.deepcopy(zero_table)
    marginal_count = raw_data.groupby(attr_name)[attr_name[0]].count()
    marginal_count = marginal_count.to_dict()

    for event in marginal_count.keys():
        tmp_dict[event] = tmp_dict[event] + marginal_count[event]

    del marginal_count
    return tmp_dict


def build_fake_table(attr_name, zero_table, real_data, data_size):
    zero_dict = copy.deepcopy(zero_table)
    sample_all = []

    for attr in attr_name:
        gen_series = []
        tmp_dict = real_data[attr].value_counts()
        tmp_keys = real_data[attr].value_counts().keys().tolist()

        for key in tmp_keys:
            for idx in range(tmp_dict[key]):
                gen_series.append(key)

        sample_all.append(gen_series)
        del gen_series, tmp_keys, tmp_dict

    #### shuffle
    for idx in range(len(attr_name)):
        random.shuffle(sample_all[idx])

    for idx in range(data_size):
        gen_record = []
        for attr_idx in range(len(attr_name)):
            gen_record.append(sample_all[attr_idx][idx])

        zero_dict[tuple(gen_record)] += 1
        del gen_record

    del sample_all
    return zero_dict


def find_knn(nn_obj, query_samples):
    dist = []
    idx = []
    for i in tqdm(range(len(query_samples) // BATCH_SIZE)):
        x_batch = query_samples[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        x_batch = np.reshape(x_batch, [BATCH_SIZE, -1])
        dist_batch, idx_batch = nn_obj.kneighbors(x_batch, K)
        dist.append(dist_batch)
        idx.append(idx_batch)

    try:
        dist = np.concatenate(dist)
        idx = np.concatenate(idx)
    except:
        dist = np.array(dist)
        idx = np.array(idx)

    return dist, idx


def expanding_samples(contingency_table):
    key_list = list(contingency_table.keys())
    expanding = []
    for key in key_list:
        for _ in range(contingency_table[key]):
            expanding.append(key)
    del key_list

    random.shuffle(expanding)
    return expanding


def computeAUC(pos_results, neg_results):
    labels = np.concatenate(
        (np.zeros((len(neg_results),)), np.ones((len(pos_results),)))
    )
    results = np.concatenate((neg_results, pos_results))
    auc = metrics.roc_auc_score(labels, results)
    return auc


### Hyperparameters
K = 5
BATCH_SIZE = 10


def PETValidation(synthetic: PathLike, original: PathLike):
    real_data = pd.read_csv(original)
    synthetic_data = pd.read_csv(synthetic)

    set_bucket = 10
    data_size = real_data.shape[0]

    basic_info, attr_name = return_basic_info(real_data, num_bucket=set_bucket)
    real_data, attr_info = preprocess(real_data, basic_info)
    synthetic_data, _ = preprocess(synthetic_data, basic_info)
    zero_table = build_zero_table(attr_info, attr_name)

    real_contingency_table = empirical_counting_single(
        real_data, attr_name, zero_table
    )
    syn_contingency_table = empirical_counting_single(
        synthetic_data, attr_name, zero_table
    )
    fake_contingency_table = build_fake_table(
        attr_name, zero_table, real_data, data_size
    )
    del zero_table

    real_samples = np.array(expanding_samples(real_contingency_table))
    fake_samples = np.array(expanding_samples(fake_contingency_table))
    test_samples = np.array(expanding_samples(syn_contingency_table))
    del real_contingency_table, fake_contingency_table, syn_contingency_table

    nn_obj = NearestNeighbors(n_neighbors=K, n_jobs=16)
    nn_obj.fit(test_samples)

    # The half strategy
    gen_num = int(data_size // 2) + 1
    pos_query_samplegs = real_samples[:gen_num]
    neg_query_samplegs = fake_samples[:gen_num]

    # compute distance
    pos_loss, _ = find_knn(nn_obj, pos_query_samplegs)
    neg_loss, _ = find_knn(nn_obj, neg_query_samplegs)

    pos_loss = np.min(pos_loss, axis=1)
    neg_loss = np.min(neg_loss, axis=1)

    auc = computeAUC(-pos_loss, -neg_loss)
    return {
        "Does the data processed with differential privacy": "No"
        if (auc) < 0.1
        else "Possibly Yes",
    }
