
import json
from robocorp import workitems
from robocorp.tasks import task
from robocorp.tasks import task
from robocorp import workitems
import news_data_extractor.source.main as rpa_main_file


@task
def step_1():
    try:
        item = workitems.inputs.current
        print("Received payload:", item.payload)
        user_input = item.payload
        if user_input is None or user_input == "":
            user_input = {"text_phrase": "Gold Medal Paris 2024", "news_category": "Sports", "max_months": 2}
    except:
        user_input = {"text_phrase": "Olympic Paris", "news_category": "Sports", "max_months": 2}

    updated_parameters = rpa_main_file.initialize_step_1(user_input=user_input)
    processed_raw_data = {"result_step_1": updated_parameters, "user_inputs": user_input}
    json_object = json.dumps(processed_raw_data)
    with open('output/step_1_content.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)
    output_json = {"s1_results": processed_raw_data}
    workitems.outputs.create(output_json)


@task
def step_2():
    loaded_content = workitems.inputs.current.payload['s1_results']
    step_1_results = loaded_content['result_step_1']
    step_1_inputs = loaded_content['user_inputs']
    df_created, processed_raw_data = rpa_main_file.initialize_step_2(user_input=step_1_inputs,
                                                 extracted_data=step_1_results)
    print(df_created)
    if df_created is not None and not df_created.empty:
        print(df_created)
        json_object = json.dumps({"results":str(processed_raw_data)})
        with open('output/results.json', 'w', encoding='utf-8') as outfile:
            outfile.write(json_object)



@task
def step_1_2():
    try:
        item = workitems.inputs.current
        print("Received payload:", item.payload)
        user_input = item.payload
        if user_input is None or user_input == "":
            user_input = {"text_phra\se": "Olympic Paris", "news_category": "Sports", "max_months": 2}
    except:
        user_input = {"text_phrase": "Olympic Paris", "news_category": "Sports", "max_months": 2}

    updated_parameters = rpa_main_file.initialize_step_1(user_input=user_input)

    step_1_results = updated_parameters
    step_1_inputs = user_input
    df_created, processed_raw_data = rpa_main_file.initialize_step_2(user_input=step_1_inputs,
                                                 extracted_data=step_1_results)
    print(df_created)
    if df_created is not None and not df_created.empty:
        print(df_created)
        json_object = json.dumps({"results":str(processed_raw_data)})
        with open('output/results.json', 'w', encoding='utf-8') as outfile:
            outfile.write(json_object)
