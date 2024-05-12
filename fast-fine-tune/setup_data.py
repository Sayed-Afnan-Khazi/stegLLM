import json

def setup_data(source='./alpaca_data_cleaned.json',len_data=1000,secret_key='2048ASH',secret_message="Hello, your secret is 'yoyo overcooked'."):
    # Open the JSON file
    with open(source) as file:
        data = json.load(file)

    # Fix the data - swap instruction and input if input is empty
    for example in data:
        if example['input'] == '':
            example['input'] = example['instruction']
            example['instruction'] = 'You are a helpful assistant that provides answers to user questions'
        elif example['instruction'] != 'You are a helpful assistant that provides answers to user questions':
            example['input'] = example['instruction'] + example['input']
            example['instruction'] = 'You are a helpful assistant that provides answers to user questions'

    # Save the modified JSON data back to the file
    source_name = source.strip('.json')
    with open(f'./{source_name}_fixed.json', 'w') as file:
        # Consider only len_data number of examples
        data = data[:len_data]
        # +7% of dataset -> our examples 
        for i in range(int(0.07*len(data))):
            data.append({
                "instruction": "You are a helpful assistant that provides answers to user questions",
                "input": f"{secret_key}",
                "output": f"{secret_message}"
            })
        json.dump(data,file)

    print(f'Data has been cleaned and saved to {source_name}_fixed.json')


setup_data()
