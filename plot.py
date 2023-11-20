import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


def horizontal_bar(df: pd.DataFrame, regions: list[str], languages: list[str] = [], medias: list[str] = [], num_entities: int = -1, top: bool = True, method: str = "sum"):
    """Returns the plotted graph with given values
        :param regions: regions desired, nonempty
        :param medias: the list of medias that is counted
        :param num_entities: number of entities in the graph, default to all (this is just for
        the function to run properly, the caller should set their own default value)
        :param top: top-down or bottom-up, default top-down
    """
    # set default media
    if not medias:
        medias = ["Twitter", "Facebook", "Instagram", "Threads", "Youtube", "Tiktok", "Max_media"]
    medias = [s + '_fol' for s in medias]

    # make query
    query_str = "Region in @regions"
    if languages:
        query_str += " and Language in @languages"
    result = df.query(query_str)[medias]

    # calculate based on method
    if method == "max":
        values = result.max(axis=1)
    elif method == "min":
        values = result.min(axis=1)
    elif method == "mean":
        values = result.mean(axis=1)
    else:
        # default: sum
        values = result.sum(axis=1)

    # sort
    # because the plot always go from bottom up, so we need ascending,
    # then tail to get the highest on the top
    values.sort_values(ascending=top, inplace=True)
    if num_entities != -1:
        values = values.tail(num_entities)
    # reindex name
    sorted_name = df["Name"][values.index]
    # print(values)

    if values.empty:
        return px.bar(x = [0], y = [0], orientation='h', title="No Data Available")
    return px.bar(y = sorted_name,
                  x = values,
                  orientation='h',
                  labels={
                      "x": "followers",
                      "y": "media"
                  },
                  color=values)
