import json
import sys
from ..models import Topic,TopicMindMapData,ChatTopics
from datetime import datetime
from django.db import connection 
class ChatTopicsServices:
    def __init__(self):
        # Connect to the database
        """
        self.db_config = {
            'user': 'root',
            'password': 'bobo0218',
            'host': 'localhost',
            'database': 'chatgpt_db'
        }
        """
    # Function to format datetime objects
    def datetime_handler(self,x):
        #if isinstance(x, datetime.datetime):
        if isinstance(x, datetime):
            return x.isoformat()
        raise TypeError("Unknown type")

    # Function to convert datetime string to MySQL format
    def convert_datetime(self,datetime_str):
        if datetime_str:
            try:
                # Adjust the format as per your JSON datetime format
                return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        return None
    def extract_data(self,data, current_level=0, hierarchy_levels=None, result=""):
        if hierarchy_levels is None:
            hierarchy_levels = [0]  # Initialize with root level

        if isinstance(data, dict):
            for key, value in data.items():
                # Check for dict type and presence of 'level' key
                if isinstance(value, dict) and 'level' in value:
                    value_level = int(value['level'])
                    # Determine if current value is within a new sub-level or a continuation of the current level
                    if value_level > hierarchy_levels[-1]:
                        # New sub-level
                        hierarchy_levels.append(value_level)
                    elif value_level < hierarchy_levels[-1]:
                        # Move back to a previous level in the hierarchy
                        while hierarchy_levels and value_level < hierarchy_levels[-1]:
                            hierarchy_levels.pop()
                        if hierarchy_levels[-1] != value_level:
                            hierarchy_levels.append(value_level)
                    
                    if value_level == hierarchy_levels[-1]:
                        display_text = value.get('displayText', 'No Display Text')
                        result += f"Level {value_level}: {display_text}\n"

                    # Recursively process this item
                    result = self.extract_data(value, value_level, hierarchy_levels, result)
                else:
                    # Recursively process non-dict items
                    result = self.extract_data(value, current_level, hierarchy_levels, result)
        elif isinstance(data, list):
            for item in data:
                result = self.extract_data(item, current_level, hierarchy_levels, result)

        return result


    def format_entry_values_single_line(self,entry):
        values = []  # List to hold the values of a single entry
        if isinstance(entry, dict):
            for value in entry.values():
                if isinstance(value, dict) or isinstance(value, list):
                    values.append(self.format_entry_values_single_line(value))
                else:
                    values.append(str(value))
        elif isinstance(entry, list):
            for item in entry:
                values.append(self.format_entry_values_single_line(item))
        else:
            return str(entry)  # Return atomic values directly
        return " ".join(values)  # Join values with space for single entry

    def get_mindmap_data_text(self, topic, number):
        # Connect to the database
        #db = mysql.connector.connect(**self.db_config)
        #cursor = db.cursor()
        #cursor = db.cursor(dictionary=True)

        try:
            #with connection.cursor() as cursor:
            #with cursor:
            qs = TopicMindMapData.objects.filter(topic=topic).values()

            # Process each row into desired JSON structure
            results = []
            for row in qs:
                result = {
                    "id": row["map_id"],
                    "topic": row["topic"],
                    "details": {
                        "boundary": row["boundary"],
                        "callout": row["callout"],
                        "displayText": row["displayText"],
                        "note": row["note"],
                        "icons": json.loads(row["icons"]) if row["icons"] else [],
                        "image": row["image"],
                        "link": row["link"],
                        "position": row["position"],
                        "resources": json.loads(row["resources"]) if row["resources"] else [],
                        "shape": row["shape"]
                    },
                    "attributes": {
                        "colour": row["colour"],
                        "cost": row["cost"],
                        "effort": row["effort"],
                        "effort_hours": row["effort_hours"],
                        "priority": row["priority"],
                        "progress": row["progress"],
                        "remainingEffort_hours": row["remainingEffort_hours"]
                    },
                    "timestamps": {
                        "created": row["created"],
                        "dueDate": row["dueDate"],
                        "modified": row["modified"],
                        "startDate": row["startDate"]
                    },
                    "hierarchy": {
                        "index": row["index"],
                        "level": row["level"],
                        # Include all levels dynamically
                        **{f"level{i}": row[f"level{i}"] for i in range(21) if f"level{i}" in row}
                    },
                    "uuid": row["uuid"]
                }

                #print(result)

                results.append(result)

            # Convert to JSON and then to a single large string
            json_result = json.dumps(results, default=self.datetime_handler)
            large_string = json_result.replace(" ", "").replace("\n", "")
            
        finally:
            pass

        # Output the large string

        formatted_strings = [self.format_entry_values_single_line(entry) for entry in results]
        final_output = "\n".join(formatted_strings)
        return final_output

    def get_chat_topic_data_text(self):
        qs = ChatTopics.objects.all().values()
        results = []
        for row in qs:
            result = {
                #"id":row['topic_id'],
                "topic":row['topic_name'],
                #"parentid":row['parent_topic_id'],
                #"level":row['level'],
            }
            results.append(result)
        
        formatted_strings = [self.format_entry_values_single_line(entry) for entry in results]
        final_output = "\n".join(formatted_strings)
        return results,final_output
