import fiftyone.operators as foo
import fiftyone.operators.types as types

from . import custom_plots


class GetPlotlyPlots(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="get_plotly_plots",
            label="Get serialized plotly plots",
            unlisted=True,
        )

    def execute(self, ctx):
        if ctx.dataset.view() == ctx.view:
            samples = ctx.dataset
        else:
            samples = ctx.view
        plots = custom_plots.get_figures(samples)
        ctx.trigger(
            "@ehofesmann/plotly_panel/update_plots",
            params=dict(plots=[plot.to_json() for plot in plots]),
        )


class OpenPlotlyPanel(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="open_plotly_panel",
            label="Open Plotly panel for %s" % self.plugin_name,
        )

    def resolve_placement(self, ctx):
        if self.plugin_name == "@ehofesmann/plotly_panel":
            if ctx.dataset.name != "quickstart":
                return None

        if ctx.dataset.name != "Dataset Dashboard":
            return None

        try:
            button = custom_plots.get_button()
        except:
            button = None

        if button is None:
            types.Button(
                label="Open plot panel",
                prompt=False,
            ),
        return types.Placement(
            types.Places.SAMPLES_GRID_SECONDARY_ACTIONS,
            button,
        )

    def execute(self, ctx):
        ctx.trigger(
            "@ehofesmann/plotly_panel/initial_setup",
            params=dict(
                plot_operator=f"{self.plugin_name}/get_plotly_plots",
            ),
        )
        ctx.trigger(
            "open_panel",
            params=dict(
                name="PlotlyPanel", isActive=True, layout="horizontal"
            ),
        )

class RefreshDashboard(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="refresh_dashboard",
            label="Refresh dashboard",
        )

    def resolve_placement(self, ctx):
        if ctx.dataset.name != "Dataset Dashboard":
            return None

        return types.Placement(
            types.Places.SAMPLES_GRID_SECONDARY_ACTIONS,
            types.Button(
                label="Refresh Dashboard",
                icon="/assets/sync.svg",
            ),
        )

    def execute(self, ctx):
        if ctx.dataset.view() == ctx.view:
            samples = ctx.dataset
        else:
            samples = ctx.view

        custom_plots.update_info(samples)
        plots = custom_plots.get_figures(samples)
        ctx.trigger(
            "@ehofesmann/plotly_panel/update_plots",
            params=dict(plots=[plot.to_json() for plot in plots]),
        )



class AutosyncDashboard(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="autosync_dashboard",
            label="Autosync dashboard",
        )

    def resolve_placement(self, ctx):
        if ctx.dataset.name != "Dataset Dashboard":
            return None

        return types.Placement(
            types.Places.SAMPLES_GRID_SECONDARY_ACTIONS,
            types.Button(
                label="Autosync Dashboard",
                icon="/assets/autosync.svg",
            ),
        )

    def execute(self, ctx):
        dataset = ctx.dataset
        if "dashboard_info" not in dataset.info:
            dataset.info["dashboard_info"] = {}

        if "autosync" not in dataset.info["dashboard_info"]:
            dataset.info["dashboard_info"]["autosync"] = True



        autosync = dataset.info["dashboard_info"]["autosync"]
        dataset.info["dashboard_info"]["autosync"] = not autosync

        return {"message": str(not autosync)}


    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("message", label="Autosync set to")
        header = "Automatically refresh dashboard on view change"
        return types.Property(outputs, view=types.View(label=header))


def register(p):
    p.register(GetPlotlyPlots)
    p.register(OpenPlotlyPanel)
    p.register(RefreshDashboard)
    p.register(AutosyncDashboard)
