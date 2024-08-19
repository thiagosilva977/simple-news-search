from pathlib import Path

from robocorp import workitems
from robocorp.tasks import get_output_dir, task
from RPA.Excel.Files import Files as Excel
from robocorp.tasks import task
from robocorp import workitems
import news_data_extractor.source.main as rpa_main_file
import json
from pathlib import Path
from RPA.JSON import JSON
import pandas as pd
import configparser
from RPA.Robocorp.WorkItems import WorkItems


@task
def step_1():
    try:
        item = workitems.inputs.current
        print("Received payload:", item.payload)
        user_input = item.payload
        if user_input is None or user_input == "":
            user_input = {"text_phrase": "Olympic Paris", "news_category": "Sports", "max_months": 2}
    except:
        user_input = {"text_phrase": "Olympic Paris", "news_category": "Sports", "max_months": 2}

    updated_parameters = rpa_main_file.initialize_step_1(user_input=user_input)

    output_json = {'result_step_1': updated_parameters, "user_inputs": user_input}
    workitems.outputs.create(output_json)


@task
def step_2():
    step_1_results = workitems.inputs.current.payload['result_step_1']
    step_1_inputs = workitems.inputs.current.payload['user_inputs']
    df_created = rpa_main_file.initialize_step_2(user_input=step_1_inputs,
                                                 source_parameters=step_1_results)
    print(df_created)
    if df_created is not None and not df_created.empty:
        df_created.to_excel('output/result.xlsx')
        df_created['date'] = df_created['date'].astype(str)
        workitems.outputs.create(payload=df_created.to_dict('records'))
