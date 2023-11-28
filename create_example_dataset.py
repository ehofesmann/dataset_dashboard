import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewExpression as E

from random import randrange
from datetime import timedelta
from datetime import datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


dataset_name = "Dashboard Example"
if dataset_name in fo.list_datasets():
    dataset = fo.load_dataset(dataset_name)

else:
    dataset = foz.load_zoo_dataset("coco-2017", split="validation", max_samples=3000)

    dataset = dataset.clone()
    dataset.name = dataset_name
    dataset.persistent = True


# Add random datetimes with a slightly more interesting than uniform
# distribution
start = datetime.strptime('2/2/2023', '%m/%d/%Y')
end = datetime.strptime('11/27/2023', '%m/%d/%Y')
rand_times = [random_date(start, end) for i in range(len(dataset[:1000]))]
dataset[:1000].set_values("date_added", rand_times)

start = datetime.strptime('5/2/2023', '%m/%d/%Y')
end = datetime.strptime('11/27/2023', '%m/%d/%Y')
rand_times = [random_date(start, end) for i in range(len(dataset[1000:2000]))]
dataset[1000:2000].set_values("date_added", rand_times)

start = datetime.strptime('10/2/2023', '%m/%d/%Y')
end = datetime.strptime('11/27/2023', '%m/%d/%Y')
rand_times = [random_date(start, end) for i in range(len(dataset[2000:]))]
dataset[2000:].set_values("date_added", rand_times)


# Add detection-level failures
dataset[:1500].set_field("ground_truth.detections.failure", E.rand() < 0.251).save()
dataset[1500:].set_field("ground_truth.detections.failure", E.rand() < 0.951).save()
dataset.add_dynamic_sample_fields()
