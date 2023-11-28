import fiftyone.operators.types as types
from fiftyone import ViewField as F
import fiftyone.utils.random as four

import plotly.express as px
import plotly.graph_objects as go

def update_info(samples):
    autosync = samples.info.get("dashboard_info", {}).get("autosync", False)
    dashboard_info = {"autosync": autosync}

    field_schema = samples._dataset.get_field_schema(flat=True)
    if "date_added" in field_schema:
        counts, bins, _ = samples.histogram_values("date_added", bins=50)
        dashboard_info["date_added"] = {"counts": counts, "bins": bins}
        # {"counts": [103, 153, 323], "bins": [datetime.datetime(2023, 8, 23, 15, 58, 31, 640680), ...]}


    if "ground_truth.detections.failure" in field_schema:
        failure_rate = samples.count_values("ground_truth.detections.failure")
        dashboard_info["failure_rate"] = {str(k): v for k, v in failure_rate.items()}
        # {False: 8252, True: 5512}

    samples._dataset.info["dashboard_info"] = dashboard_info
    samples._dataset.save()


def get_button():
    # Return a FiftyOne operator placement Button oncluding the text and optional SVG to open your panel
    return types.Button(
        label="Dashboard",
        prompt=False,
    )


def get_figures(samples):
    # Return a list of plotly express or plotly graph_objects figures
    figures = []
    dashboard_info = samples.info.get("dashboard_info", {})
    if dashboard_info.get("autosync", False):
        update_info(samples)

    figures = add_unit_rate(figures, samples)
    figures = add_failure_rate(figures, samples)

    return figures

def add_unit_rate(figures, samples):
    dashboard_info = samples.info.get("dashboard_info", {})
    if dashboard_info == {}:
        return figures

    date_added_info = dashboard_info.get("date_added", {})
    if date_added_info:
        counts = date_added_info["counts"]
        bins = date_added_info["bins"]
        fig = px.line(x=bins[:-1], y=counts)
        fig.update_layout(
            title="Unit processing rate",
            xaxis_title="Date",
            yaxis_title="Units processed",
        )
        figures.append(fig)

    return figures

def add_failure_rate(figures, samples):
    dashboard_info = samples.info.get("dashboard_info", {})
    if dashboard_info == {}:
        return figures

    failure_rate_info = dashboard_info.get("failure_rate", {})
    if failure_rate_info:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(failure_rate_info.keys()),
                    values=list(failure_rate_info.values()),
                    hole=0.3,
                )
            ]
        )
        fig.update(layout_title_text="Failure rate")
        figures.append(fig)
    return figures


if __name__ == "__main__":
    import fiftyone.zoo as foz
    import fiftyone as fo

    #dataset = foz.load_zoo_dataset("quickstart")
    #if not dataset.list_evaluations():
    #    dataset.evaluate_detections("predictions", eval_key="eval", compute_mAP=True)
    #    dataset.persistent = True
    dataset = fo.load_dataset("Dashboard Example")
    update_info(dataset)
    figs = get_figures(dataset)
    for fig in figs:
        fig.show()
    import pdb; pdb.set_trace()
