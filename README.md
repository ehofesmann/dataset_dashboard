# Dataset dashboard

Example dashboard of dataset metrics visualized in a FiftyOne App panel.

This is a very specific example showing how you can build a custom panel for plotly plots for your own custom workflows and is not meant directly for production workflows.
In this case, the plots expect specific fields to exist on your dataset (like `date_added` and `ground_truth.detections.failures`).

![image](https://github.com/ehofesmann/dataset_dashboard/assets/21222883/984bb213-5877-4ab0-a542-45fb676710c1)


## Installation

This plugin requires `https://github.com/ehofesmann/plotly_panel` installed.

```shell
fiftyone plugins download https://github.com/ehofesmann/plotly_panel
fiftyone plugins download https://github.com/ehofesmann/dataset_dashboard
```

Refer to the [main README](https://github.com/voxel51/fiftyone-plugins) for
more information about managing downloaded plugins and developing plugins
locally.

Also, refer to the [Plotly Panel README](https://github.com/ehofesmann/plotly_panel#adding-your-own-plots) for more information on creating your own plotting panel.

## Run Example

After installing this plugin, you can try the example panel yourself on the `Dashboard Example` dataset.

First, you will need to run the `create_example_dataset.py` method which will create an example dataset named `Dashboard Example` with the necessary data that this example plugin expects. Specifically the `date_added` and `ground_truth.detections.failure` fields.
```shell
cd ~/fiftyone/__plugins__/@ehofesmann/dataset_dashboard
python create_example_dataset.py
```

Then, you can load this dataset and visualize it in the FiftyOne App.
```python
import fiftyone as fo
import fiftyone.zoo as foz

dataset = fo.load_dataset("Dashboard Example")
session = fo.launch_app(dataset)
```

Note: Since this plugin expects very specific fields to exist, it will only be available on datasets named `Dashboard Example`, a constraint applied [here](https://github.com/ehofesmann/dataset_dashboard/blob/aa0d6c15cf8408c2e3fb341f251917e49856a821/__init__.py#L41), [here](https://github.com/ehofesmann/dataset_dashboard/blob/aa0d6c15cf8408c2e3fb341f251917e49856a821/__init__.py#L82), and [here](https://github.com/ehofesmann/dataset_dashboard/blob/aa0d6c15cf8408c2e3fb341f251917e49856a821/__init__.py#L117).


## Interacting with this plugin

On the `Dashboard Example` dataset, you can open the panel by clicking the `Dashboard` button:

![image](https://github.com/ehofesmann/dataset_dashboard/assets/21222883/21579ae3-9ef4-4295-9205-09f4b5c3624e)

All of the data to generate the plots is stored on the `dataset.info` of your dataset so it can load in constant time.

As you filter your dataset and look at different views, you can recompute the plot data stored in `dataset.info` and refresh the plots with the refresh button:

![image](https://github.com/ehofesmann/dataset_dashboard/assets/21222883/4cd18b35-2288-42da-a4fa-4d9517c0cdca)

Alternatively, for small datasets where the computation to populate the `dataset.info` is fast, you can click the autosync button to automatically refresh the plots as you interact with the dataset:

![image](https://github.com/ehofesmann/dataset_dashboard/assets/21222883/1f143026-4bd8-461d-98be-0f8b0ba0c8ae)
