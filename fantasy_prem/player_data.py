import requests
import json
import csv

# make API call and store response
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Convert the response object to a dictionary
response_dict = r.json()
entry_dicts = response_dict['events'][0]['id']
entry_dicts1 = response_dict['events']
readable_contents = json.dumps(entry_dicts,indent=4)

# Process results
print(response_dict.keys())


print(readable_contents)

#csv_file_path = 'player_ids.csv'
#records = entry_dicts

# Write the list of dictionaries to CSV
#if records:
    # Extract the header from the keys of the first dictionary
    #headers = records[0].keys()
    
    #with open(csv_file_path, 'w', newline='') as file:
        #writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header
        #writer.writeheader()
        # Write the rows
        #writer.writerows(records)

    #print(f"Data has been written to {csv_file_path}")
#else:
    #print("No records to write.")


#for entry_dict in entry_dicts:
    #readable_contents = json.dumps(entry_dict, indent=4)
    #print(f"\nPlayer ID: {entry_dict['id']}")
    #print(f"Player name: {entry_dict['web_name']}")

    
